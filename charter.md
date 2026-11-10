# Agent Auth (AAuth) Working Group Charter

## Charter

### (i) Working Group name

Agent Auth (AAuth) Working Group

### (ii) Purpose

The purpose of this working group is to develop specifications for agents
that act on behalf of people and organizations: how an agent proves who it
is and who it acts for, and how it obtains and uses authorization across
trust domains.

Agents discover resources at runtime, act across organizational
boundaries, and need decisions from the people they act for while a task
is underway. This working group will develop a protocol for that model.

### (iii) Scope

The scope of the working group includes:

- Agent identity. Identifying agents and the providers that issue their
  identity, with proof of possession on every request and no
  pre-registration or shared secrets.
- Person identity. Asserting to a resource which person or organization an
  agent acts for, building on OpenID Connect and other OpenID Foundation
  specifications.
- Authorization. Requesting, granting, and presenting access to resources,
  from decisions on identity alone to policy decisions by a resource's
  access server across trust domains.
- Agent governance. Missions, and the person's consent to and oversight of
  what an agent does.
- Delegation. Agents acting through other agents and through resources that
  act as agents.
- Discovery and trust. Metadata, key discovery, and binding keys and
  metadata to entities.
- Events and lifecycle. Asynchronous delivery to agents, and token expiry
  and revocation.
- Conformance and compliance testing for each role.
- Security and privacy considerations for all of the above.

Out of scope:

- How a person server or supervisor decides whether to approve a request.
- How a person server authenticates or identity-proofs the person.
- Agent runtime and model behavior.
- Payment protocols.
- Changes to OAuth 2.0, OpenID Connect, or HTTP Message Signatures
  (RFC 9421).

### (iv) Proposed specifications

| Working title | Implementers Draft | Final |
|---|---|---|
| AAuth Protocol 1.0 | Q2 2027 | Q1 2028 |
| AAuth Supervision 1.0 | Q3 2027 | Q2 2028 |
| HTTP Signature Keys 1.0 | Q1 2027 | Q4 2027 |
| AAuth Events 1.0 | Q4 2027 | Q2 2028 |
| AAuth Rich Resource Requests (R3) 1.0 | Q4 2027 | Q3 2028 |
| AAuth Budgets 1.0 | Q1 2028 | Q3 2028 |

Other deliverables:

- Conformance test suites for each role (agent, agent provider, resource,
  person server, access server), developed with the OpenID Foundation
  certification team for use in OpenID Certification, projected alongside
  each Implementers Draft.
- Compliance test suites that deployers can run against their own agents
  and servers.

The WG may also produce further profiles within scope.

### (v) Anticipated audience or users

- Developers of agents and agent platforms, who operate agent providers.
- Resource providers, including API providers and MCP servers.
- Operators of person servers: identity providers, enterprises, and
  consumer services.
- Operators of access servers and policy engines.
- Vendors of SDKs, API gateways, and proxies that add AAuth to existing
  resources.
- Enterprises that deploy and govern agents.

### (vi) Language

English.

### (vii) Method of work

Mailing list, a GitHub repository under the OpenID Foundation
organization, and regular conference calls. Face-to-face meetings where
useful, including alongside IIW, IETF meetings, and OpenID Foundation
workshops. Interoperability events once an Implementers Draft is approved.

### (viii) Basis for determining when the work is completed

The work is complete when the specifications in (iv) are approved as Final
Specifications through the OpenID Foundation process, including vote by
the membership, and independent implementations of each role have
demonstrated interoperability.

## Background Information

### (i) Related work and liaisons

The WG will coordinate with the following groups.

OpenID Foundation:

- AB/Connect (OpenID Connect, Enterprise Extensions, Federation)
- AuthZEN
- eKYC & IDA, including the OpenID Authority draft
- Digital Credentials Protocols (DCP)
- Digital Credentials Harmonized Presentation (DCHP)
- IPSIE
- Shared Signals
- Artificial Intelligence Identity Management Community Group

IETF:

- OAuth WG
- HTTP WG (httpbis)
- WIMSE
- Web Bot Auth (webbotauth)

Other:

- FIDO Alliance
- W3C
- Linux Foundation: Model Context Protocol (MCP) and Agent2Agent (A2A)
  projects

### (ii) Proposers

- Dick Hardt, dick.hardt@gmail.com, Individual
- Wayne Chang, wayne@spruceid.com, SpruceID
- Jared Hanson, jared@keycard.ai, Keycard
- Karl McGuinness, me@karlmcguinness.com, Individual
- Christian Posta, christian.posta@gmail.com, Individual

Proposed editor: Dick Hardt

### (iii) Anticipated contributions

- draft-hardt-oauth-aauth-protocol-11, AAuth Protocol
  <https://datatracker.ietf.org/doc/draft-hardt-oauth-aauth-protocol/>
- draft-hardt-aauth-supervision, AAuth Supervision
  <https://dickhardt.github.io/AAuth/draft-hardt-aauth-supervision.html>
- draft-hardt-aauth-bootstrap, AAuth Bootstrap Guidance
  <https://datatracker.ietf.org/doc/draft-hardt-aauth-bootstrap>
- draft-hardt-aauth-events, AAuth Events
  <https://github.com/dickhardt/AAuth/blob/main/draft-hardt-aauth-events.md>
- draft-hardt-aauth-r3, AAuth Rich Resource Requests
  <https://github.com/dickhardt/AAuth/blob/main/draft-hardt-aauth-r3.md>
- draft-hardt-aauth-budgets, AAuth Budgets
  <https://github.com/dickhardt/AAuth/blob/main/draft-hardt-aauth-budgets.md>
