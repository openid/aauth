# Resources

## Contributed drafts

These drafts are the anticipated contributions listed in the
[charter](charter.md). They are currently maintained as individual
Internet-Drafts at [dickhardt/AAuth](https://github.com/dickhardt/AAuth).

| Draft | Scope | Editor's copy |
|---|---|---|
| [AAuth Protocol](https://datatracker.ietf.org/doc/draft-hardt-oauth-aauth-protocol/) | Agent, person, resource, and auth tokens; access modes; missions; PS–AS federation | [html](https://dickhardt.github.io/AAuth/draft-hardt-oauth-aauth-protocol.html) |
| [HTTP Signature Keys](https://datatracker.ietf.org/doc/draft-hardt-httpbis-signature-key/) | The `Signature-Key` header and key discovery that AAuth signs with | [html](https://dickhardt.github.io/signature-key/draft-hardt-httpbis-signature-key.html) |
| AAuth Supervision | The PS–SS interface where a supervision server decides on the person's behalf | [html](https://dickhardt.github.io/AAuth/draft-hardt-aauth-supervision.html) |
| [AAuth Events](https://datatracker.ietf.org/doc/draft-hardt-aauth-events/) | Event delivery to agents through their agent provider | [html](https://dickhardt.github.io/AAuth/draft-hardt-aauth-events.html) |
| [AAuth R3](https://datatracker.ietf.org/doc/draft-hardt-aauth-r3/) | Rich Resource Requests: authorization in MCP, OpenAPI, gRPC, and GraphQL vocabularies | [html](https://dickhardt.github.io/AAuth/draft-hardt-aauth-r3.html) |
| [AAuth Budgets](https://datatracker.ietf.org/doc/draft-hardt-aauth-budgets/) | Spending ceilings for metered resources | [html](https://dickhardt.github.io/AAuth/draft-hardt-aauth-budgets.html) |
| [AAuth Bootstrap](https://datatracker.ietf.org/doc/draft-hardt-aauth-bootstrap/) | Informational: how an agent provider enrolls agents and issues agent tokens | [html](https://dickhardt.github.io/AAuth/draft-hardt-aauth-bootstrap.html) |

- [Updating from -10 to -11](https://github.com/dickhardt/AAuth/tree/main/upgrade-10-to-11)
- [Interoperability Demo Profile](https://github.com/dickhardt/AAuth/blob/main/interop-demo-profile.md):
  the minimum live pieces needed to show interoperability

## Implementations

| Project | Kind |
|---|---|
| [packages-js](https://github.com/aauth-dev/packages-js) | TypeScript SDK for agents and MCP servers |
| [dotnet-samples](https://github.com/aauth-dev/dotnet-samples) | .NET SDK and samples |
| [aauth-python-library](https://github.com/christian-posta/aauth-python-library) | Python request signing and verification |
| [aauth-go-library](https://github.com/christian-posta/aauth-go-library) | Go request signing and verification |
| [regent-httpsig](https://github.com/regent-protocol/regent-httpsig) | Python resource-side verification and budgets metering |
| [keycloak-aauth-extension](https://github.com/christian-posta/keycloak-aauth-extension) | Keycloak SPI |
| [aauth-person-server](https://github.com/christian-posta/aauth-person-server) | Person server with missions |
| [extauth-aauth-resource](https://github.com/christian-posta/extauth-aauth-resource) | Envoy / agentgateway ext-authz that makes an HTTP, MCP, or A2A service an AAuth resource |
| [whoami](https://github.com/aauth-dev/whoami) | Identity claims resource |
| [proxy](https://github.com/aauth-dev/proxy) | The user's AAuth agent as an MCP server |
| [AAuth Web Agent](https://web-agent.aauth.dev) | Protocol playground |
| [AAuth Explorer](https://explorer.aauth.dev) | Walkthrough of the protocol flows |
| [aauth-full-demo](https://github.com/christian-posta/aauth-full-demo) | A2A multi-agent flow with Keycloak and user consent |

To add an implementation, open a pull request against this file.

## Community

- [aauth.dev](https://www.aauth.dev): explainers, diagrams, and the AAuth Explorer
- [AAuth community Slack](https://www.aauth.dev/slack): implementation discussion

## Related work

The charter lists these groups for coordination.

OpenID Foundation:

- [AB/Connect](https://openid.net/wg/connect/) (OpenID Connect, Enterprise Extensions, Federation)
- [AuthZEN](https://openid.net/wg/authzen/)
- [eKYC & IDA](https://openid.net/wg/ekyc-ida/), including the
  [OpenID Authority draft](https://github.com/openid/eKYC-IDA-Authority)
- [Digital Credentials Protocols (DCP)](https://openid.net/wg/digital-credentials-protocols/)
- [Digital Credentials Harmonized Presentation (DCHP)](https://openid.net/wg/digital-credentials-harmonized-presentation-working-group/)
- [IPSIE](https://openid.net/wg/ipsie/)
- [Shared Signals](https://openid.net/wg/sharedsignals/)
- [Artificial Intelligence Identity Management Community Group](https://openid.net/cg/artificial-intelligence-identity-management-community-group/)

IETF:

- [OAuth WG](https://datatracker.ietf.org/wg/oauth/about/)
- [HTTP WG (httpbis)](https://datatracker.ietf.org/wg/httpbis/about/)
- [WIMSE](https://datatracker.ietf.org/wg/wimse/about/)
- [Web Bot Auth (webbotauth)](https://datatracker.ietf.org/wg/webbotauth/about/)

Other:

- [FIDO Alliance](https://fidoalliance.org/)
- [W3C](https://www.w3.org/)
- Linux Foundation: [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
  and [Agent2Agent (A2A)](https://a2a-protocol.org/)

## OpenID Foundation policies

- [IPR Contribution Agreement](https://openid.net/intellectual-property/)
- [IPR Policy](https://openid.net/wp-content/uploads/2024/10/OIDF-Policy_IPR-Policy_Final_2024-10-19.pdf)
- [Process Document](https://openid.net/wp-content/uploads/2024/10/OIDF_Process-Document_Final_2024-10-19.pdf)
- [Antitrust Policy](https://openid.net/wp-content/uploads/2024/09/OIDF-Antitrust-Policy_Final_2024-09-12.pdf)
- [Code of Conduct](CODE_OF_CONDUCT.md)
- [All OpenID Foundation policies](https://openid.net/policies/)
