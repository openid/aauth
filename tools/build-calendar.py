#!/usr/bin/env python3
"""Build the AAuth WG meeting calendar from the OpenID Foundation calendar.

The OpenID Foundation calendar is the source of record. This script fetches
its public feed, keeps the AAuth WG events, and writes:

  <out>/aauth-wg.ics   the AAuth WG feed that people subscribe to
  <out>/index.html     a page with subscribe links and the next meeting

With --readme, it also rewrites the block between the next-meeting markers
in README.md.

It exits non-zero, without writing anything, if the OIDF feed can't be
fetched or has no AAuth events, so a failed run never publishes an empty
feed that would clear subscribers' calendars.

    python tools/build-calendar.py --out _site --readme README.md
    python tools/build-calendar.py --source saved.ics --out _site   # offline
"""

import argparse
import datetime as dt
import html
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path
from zoneinfo import ZoneInfo

import icalendar
import recurring_ical_events

OIDF_CALENDAR_ID = "o6vc2o4nrv8ihi1dng0l2rhfhs@group.calendar.google.com"
OIDF_FEED = (
    "https://calendar.google.com/calendar/ical/"
    + urllib.parse.quote(OIDF_CALENDAR_ID)
    + "/public/basic.ics"
)
OIDF_CALENDAR_PAGE = "https://openid.net/calendar/"

# An event belongs to the AAuth WG if its title contains "AAuth". Every
# instance of a matching event's UID is kept, so changed or cancelled single
# meetings come along with the series.
MATCH = re.compile(r"\bAAuth\b", re.IGNORECASE)

CALENDAR_NAME = "OpenID Foundation AAuth WG"
SITE_URL = "https://openid.github.io/aauth/"
FEED_URL = SITE_URL + "aauth-wg.ics"
WEBCAL_URL = "webcal://" + FEED_URL.removeprefix("https://")
REPO_URL = "https://github.com/openid/aauth"
MAILING_LIST = "https://lists.openid.net/mailman/listinfo/openid-specs-aauth"

# The first zone sets the date shown; the others are listed alongside it.
ZONES = ["America/Los_Angeles", "America/New_York", "UTC", "Europe/Paris"]
HORIZON = dt.timedelta(days=120)  # how far ahead to look for the next meeting
SKIP_WINDOW = dt.timedelta(days=60)  # how far ahead to list skipped meetings

README_START = "<!-- next-meeting:start -->"
README_END = "<!-- next-meeting:end -->"

SUBSCRIBE = {
    "Google Calendar": "https://calendar.google.com/calendar/r?cid="
    + urllib.parse.quote(WEBCAL_URL, safe=""),
    "Outlook.com": "https://outlook.live.com/calendar/0/addfromweb?"
    + urllib.parse.urlencode({"url": FEED_URL, "name": CALENDAR_NAME}),
    "Microsoft 365": "https://outlook.office.com/calendar/0/addfromweb?"
    + urllib.parse.urlencode({"url": FEED_URL, "name": CALENDAR_NAME}),
    "Apple Calendar": WEBCAL_URL,
}


def fetch(source):
    if re.match(r"https?://", source):
        req = urllib.request.Request(source, headers={"User-Agent": "aauth-calendar"})
        with urllib.request.urlopen(req, timeout=60) as resp:
            return resp.read()
    return Path(source).read_bytes()


def filter_calendar(src):
    """Return a calendar holding only the AAuth events and their time zones."""
    events = list(src.walk("VEVENT"))
    uids = {str(e.get("UID")) for e in events if MATCH.search(str(e.get("SUMMARY", "")))}
    keep = [e for e in events if str(e.get("UID")) in uids]
    if not keep:
        sys.exit("error: no AAuth events in the OIDF calendar")

    tzids = set()
    for e in keep:
        tzids.update(re.findall(r";TZID=([^;:]+)", e.to_ical().decode()))

    out = icalendar.Calendar()
    out.add("PRODID", "-//OpenID Foundation//AAuth WG calendar//EN")
    out.add("VERSION", "2.0")
    out.add("CALSCALE", "GREGORIAN")
    out.add("METHOD", "PUBLISH")
    out.add("X-WR-CALNAME", CALENDAR_NAME)
    out.add("X-WR-CALDESC", f"AAuth WG meetings, from the OpenID Foundation calendar. {SITE_URL}")
    # Refresh hints (RFC 7986 and the Microsoft equivalent). Google ignores them.
    out.add("REFRESH-INTERVAL", dt.timedelta(hours=1), parameters={"VALUE": "DURATION"})
    out.add("X-PUBLISHED-TTL", "PT1H")
    for tz in src.walk("VTIMEZONE"):
        if str(tz.get("TZID")) in tzids:
            out.add_component(tz)
    for e in keep:
        out.add_component(e)
    return out


def as_utc(value):
    if isinstance(value, dt.datetime):
        return value.astimezone(dt.timezone.utc) if value.tzinfo else value.replace(tzinfo=dt.timezone.utc)
    return dt.datetime.combine(value, dt.time(), dt.timezone.utc)


def cancelled(e):
    return str(e.get("STATUS", "")).upper() == "CANCELLED"


def next_meeting(cal, now):
    """The first meeting that hasn't ended yet, or None."""
    upcoming = [
        e
        for e in recurring_ical_events.of(cal).between(now, now + HORIZON)
        if not cancelled(e) and as_utc(e["DTEND"].dt) > now
    ]
    return min(upcoming, key=lambda e: as_utc(e["DTSTART"].dt), default=None)


def skipped_meetings(cal, now):
    """Start times of upcoming meetings removed from the series."""
    skipped = set()
    for e in cal.walk("VEVENT"):
        exdate = e.get("EXDATE")
        for group in exdate if isinstance(exdate, list) else [exdate] if exdate else []:
            skipped.update(as_utc(d.dt) for d in group.dts)
        if cancelled(e) and e.get("RECURRENCE-ID"):
            skipped.add(as_utc(e["RECURRENCE-ID"].dt))
    return sorted(t for t in skipped if now < t <= now + SKIP_WINDOW)


def day(t):
    local = t.astimezone(ZoneInfo(ZONES[0]))
    return f"{local:%A, %B} {local.day}, {local.year}"


def times(start, end):
    zones = [ZoneInfo(z) for z in ZONES]
    first_start, first_end = start.astimezone(zones[0]), end.astimezone(zones[0])
    first = f"{first_start:%H:%M}–{first_end:%H:%M} {first_start.tzname()}"
    others = " · ".join(f"{start.astimezone(z):%H:%M} {start.astimezone(z).tzname()}" for z in zones[1:])
    return f"{first} ({others})"


def join_or(items):
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " or " + items[-1]


def summary(cal, now):
    """(next meeting line, skipped meetings line) as plain text."""
    meeting = next_meeting(cal, now)
    if meeting:
        start, end = as_utc(meeting["DTSTART"].dt), as_utc(meeting["DTEND"].dt)
        when = f"{day(start)}, {times(start, end)}"
    else:
        when = None
    skipped = skipped_meetings(cal, now)
    skips = f"No meeting on {join_or([day(t) for t in skipped])}." if skipped else None
    return when, skips


def readme_block(when, skips):
    lines = [README_START]
    if when:
        lines.append(f"**Next meeting:** {when}")
    else:
        lines.append(f"**Next meeting:** none scheduled. See the [OpenID Foundation calendar]({OIDF_CALENDAR_PAGE}).")
    if skips:
        lines += ["", skips]
    lines.append(README_END)
    return "\n".join(lines)


def updated_readme(path, block):
    text = path.read_text()
    pattern = re.compile(re.escape(README_START) + ".*?" + re.escape(README_END), re.DOTALL)
    if not pattern.search(text):
        sys.exit(f"error: {path} has no {README_START} ... {README_END} block")
    return pattern.sub(lambda _: block, text, count=1)


def page(when, skips):
    e = html.escape
    buttons = "\n".join(
        f'      <a class="button" href="{e(url)}">{e(label)}</a>' for label, url in SUBSCRIBE.items()
    )
    next_html = (
        f"<p class=\"next\"><strong>Next meeting:</strong> {e(when)}</p>"
        if when
        else f'<p class="next"><strong>Next meeting:</strong> none scheduled. See the '
        f'<a href="{OIDF_CALENDAR_PAGE}">OpenID Foundation calendar</a>.</p>'
    )
    skips_html = f"<p>{e(skips)}</p>" if skips else ""
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AAuth WG Meetings</title>
  <style>
    :root {{ --bg: #ffffff; --fg: #1f2328; --muted: #59636e; --line: #d1d9e0; --accent: #0969da; }}
    @media (prefers-color-scheme: dark) {{
      :root {{ --bg: #0d1117; --fg: #e6edf3; --muted: #9198a1; --line: #3d444d; --accent: #4493f8; }}
    }}
    body {{ margin: 0; background: var(--bg); color: var(--fg);
           font: 16px/1.5 -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; }}
    main {{ max-width: 40rem; margin: 0 auto; padding: 2rem 1rem; }}
    h1 {{ font-size: 1.6rem; margin: 0 0 0.25rem; }}
    a {{ color: var(--accent); }}
    .muted {{ color: var(--muted); }}
    .next {{ font-size: 1.1rem; }}
    .buttons {{ display: flex; flex-wrap: wrap; gap: 0.5rem; margin: 1rem 0; }}
    .button {{ border: 1px solid var(--line); border-radius: 6px; padding: 0.45rem 0.9rem;
              text-decoration: none; background: none; color: var(--accent);
              font: inherit; font-weight: 600; cursor: pointer; }}
    .feed {{ display: flex; flex-wrap: wrap; align-items: center; gap: 0.5rem; }}
    code {{ word-break: break-all; }}
  </style>
</head>
<body>
  <main>
    <h1>AAuth WG Meetings</h1>
    <p class="muted">OpenID Foundation Agent Auth (AAuth) Working Group</p>
    {next_html}
    {skips_html}
    <h2>Add the meetings to your calendar</h2>
    <p>These links subscribe you to the AAuth WG calendar, so cancellations and changes reach your calendar.</p>
    <div class="buttons">
{buttons}
    </div>
    <p>Other calendar apps: copy this address into the app's option to subscribe to a calendar by URL.
      Downloading the file instead imports a copy that won't get cancellations or changes.</p>
    <p class="feed"><code>{e(FEED_URL)}</code>
      <button type="button" class="button" id="copy">Copy</button></p>
    <p class="muted">Calendar apps refresh subscriptions on their own schedule. Google can take up to a day,
      so short-notice cancellations are also announced on the <a href="{MAILING_LIST}">mailing list</a>.
      The feed is generated hourly from the <a href="{OIDF_CALENDAR_PAGE}">OpenID Foundation calendar</a>,
      which is the source of record.</p>
    <p><a href="{REPO_URL}">Working group repository</a></p>
  </main>
  <script>
    document.getElementById("copy").addEventListener("click", async (event) => {{
      const button = event.currentTarget;
      try {{
        await navigator.clipboard.writeText({FEED_URL!r});
        button.textContent = "Copied";
      }} catch {{
        // Clipboard unavailable: select the address so it can be copied by hand.
        getSelection().selectAllChildren(button.previousElementSibling);
        button.textContent = "Press Ctrl+C / ⌘C";
      }}
      setTimeout(() => {{ button.textContent = "Copy"; }}, 2000);
    }});
  </script>
</body>
</html>
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--source", default=OIDF_FEED, help="OIDF feed URL or a saved .ics file")
    ap.add_argument("--out", required=True, type=Path, help="directory for aauth-wg.ics and index.html")
    ap.add_argument("--readme", type=Path, help="README.md whose next-meeting block to rewrite")
    ap.add_argument("--now", help="ISO 8601 time to treat as now (for testing)")
    args = ap.parse_args()

    now = dt.datetime.fromisoformat(args.now) if args.now else dt.datetime.now(dt.timezone.utc)
    now = as_utc(now)

    src = icalendar.Calendar.from_ical(fetch(args.source))
    cal = filter_calendar(src)
    when, skips = summary(cal, now)
    readme = updated_readme(args.readme, readme_block(when, skips)) if args.readme else None

    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "aauth-wg.ics").write_bytes(cal.to_ical())
    (args.out / "index.html").write_text(page(when, skips))
    if readme is not None:
        args.readme.write_text(readme)

    print(f"next meeting: {when or 'none scheduled'}")
    if skips:
        print(skips)


if __name__ == "__main__":
    main()
