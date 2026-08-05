# antcrew — Service Level Agreement and Data Processing Terms

*Version 1.1 — August 2026*

This document governs the relationship between **antcrew** ("antcrew", "we", "Processor") and
the organisation using antcrew-platform ("Customer", "Controller") with respect to service
levels, operational responsibilities, business continuity, and the processing of personal data
under GDPR / LOPDGDD.

---

## 1. Scope

This document applies to all commercially contracted use of **antcrew-platform** (the managed
web application) and, where deployed, **antcrew-proxy** (the customer-operated LLM relay).

Free-tier and trial workspaces receive best-effort service only. No SLA applies until a paid
plan is in effect.

---

## 2. Definitions

| Term | Meaning |
|---|---|
| **Platform** | The managed antcrew-platform service, hosted by antcrew on Hetzner infrastructure |
| **Proxy** | The antcrew-proxy binary deployed and operated by the Customer on their own infrastructure |
| **Run / Request** | A single pipeline execution triggered via the Platform UI or API |
| **Incident** | A degradation or outage affecting the Platform's availability or data integrity |
| **Business hours** | Monday–Friday 09:00–18:00 CET/CEST, excluding Spanish public holidays |
| **RTO** | Recovery Time Objective — target time to restore service after an incident |
| **RPO** | Recovery Point Objective — maximum acceptable data loss in a failure scenario |
| **Controller** | The Customer, as defined under GDPR Art. 4(7) |
| **Processor** | antcrew, acting on the Customer's instructions |
| **Sub-processor** | Third-party processors engaged by antcrew to deliver the service |

---

## 3. Platform service levels

### 3.1 Availability

| Tier | Monthly uptime target | Max planned downtime per event |
|---|---|---|
| Commercial | 99.0% (~7.3 h/month) | 2 hours (24 h advance notice) |
| Enterprise (future) | 99.5% (~3.6 h/month) | 1 hour (48 h advance notice) |

Availability is measured as HTTP 2xx responses to the `/health` endpoint from two independent
probe locations. Periods of planned maintenance announced with adequate notice are excluded from
availability calculations.

The **Proxy** is customer-operated and is **not included** in any antcrew uptime commitment.
Customer is responsible for proxy availability (see Section 4).

### 3.2 Performance

- API median response time target: **< 500 ms** (excluding time to first token from LLM providers)
- WebSocket event delivery target: **< 2 s** end-to-end from engine event to browser

### 3.3 Exclusions

antcrew is not responsible for:

- LLM provider outages (Anthropic, OpenAI, Groq, etc.)
- Network latency or packet loss between the Customer's infrastructure and the Platform
- Service degradation caused by Customer's own API key exhaustion or rate-limit policies
- Force majeure events

---

## 4. Proxy operational responsibilities

The Proxy runs on Customer infrastructure. The following responsibilities belong exclusively to
the Customer.

| Responsibility | Customer | antcrew |
|---|:---:|:---:|
| Uptime of the proxy process and host | ✅ | |
| TLS termination on the proxy endpoint | ✅ | |
| Keeping `PROXY_TOKEN` confidential | ✅ | |
| Storing LLM API keys securely | ✅ | |
| Firewall: restrict inbound to platform egress IPs | ✅ (recommended) | |
| Software updates to the proxy image | ✅ | |
| Monitoring proxy logs for anomalies | ✅ | |
| Issuing and revoking `PROXY_TOKEN` | ✅ (via Platform UI) | |
| Proxy image distribution and CVE patching | | ✅ |
| Structured audit logging in proxy image | | ✅ |

When the Proxy is unreachable, the Platform returns `503` to callers. This counts as an
LLM-provider failure, not a Platform outage.

### 4.1 Recommended proxy configuration

```yaml
restart: unless-stopped          # Docker Compose
healthcheck: GET /health         # supervisor should restart on 3 consecutive failures
```

Contact support for the current list of Platform egress IPs to use in firewall rules.

---

## 5. Support

### 5.1 Severity levels

| Priority | Definition | Examples |
|---|---|---|
| **P1 — Critical** | Platform unavailable; data breach suspected | Platform returns 5xx for all users; unauthorized access to run data |
| **P2 — High** | Major feature broken; data inconsistency | All runs fail; HITL queue unresponsive; billing grossly incorrect |
| **P3 — Normal** | Feature degraded; non-blocking issue | Single endpoint slow; UI rendering issue; documentation gap |

### 5.2 Response targets (business hours unless noted)

| Priority | Initial response | Status updates | Resolution target |
|---|---|---|---|
| P1 | 4 business hours; security breaches: 2 hours any day | Every 4 hours | Best effort — RTO 8 business hours |
| P2 | 1 business day | Daily | 5 business days |
| P3 | 3 business days | Weekly | Next maintenance release |

### 5.3 Emergency contact

Security incidents and suspected data breaches must be reported to
**security@antcrew.org** and will be escalated immediately regardless of time of day.

For all other incidents, file a ticket via the Platform's in-app support widget or email
**support@antcrew.org**.

---

## 6. Business continuity and data portability

### 6.1 Recovery objectives

| Scenario | RTO | RPO |
|---|---|---|
| Single-host failure (Hetzner) | 4 hours | 24 hours (daily backup cadence) |
| Database failure (Neon) | 2 hours | 15 minutes (Neon continuous WAL) |
| Full region failure | 24 hours | 24 hours |

### 6.2 Data portability

On written request or at contract termination, antcrew will provide, within 30 days:

- All `run` records (run_id, team, request, status, cost, timestamps) as CSV
- All `ticket` and `event` records associated with Customer runs, as JSON
- API key list (names only — the actual keys are stored hashed)

We will provide a PostgreSQL dump on request for Enterprise customers.

### 6.3 Continuity if antcrew ceases to operate

If antcrew discontinues the Platform service:

1. Customers will receive **90 days' written notice** (30 days in case of insolvency proceedings).
2. During the notice period, full data export will be available via the standard export endpoint.
3. The **antcrew-proxy** image and the **antcrew-engine** SDK are MIT-licensed and will remain
   functional independently — customers can route directly to LLM providers without the Platform.
4. The **antcrew** framework (Layer 1) is MIT-licensed — team pipelines continue to run without
   any antcrew service dependency.

The Platform itself is not open-sourced, but its transport protocol (REST + WebSocket + webhook)
is documented in the public API reference so that customers can migrate to an alternative
orchestration platform.

---

## 7. Data processing agreement (GDPR Art. 28)

### 7.1 Roles

The **Customer** is the **Controller** (responsable del tratamiento) of personal data
included in run requests, ticket content, and user account information.

**antcrew** is the **Processor** (encargado del tratamiento), acting solely on the
documented instructions of the Controller.

Where the Customer deploys and operates the Proxy, the Customer also acts as Processor
for data flowing through the Proxy to LLM providers.

### 7.2 Subject matter and duration

antcrew processes personal data as necessary to provide the Platform, for the duration of the
Customer's active subscription, plus any statutory retention period thereafter.

### 7.3 Nature and purpose of processing

| Purpose | Legal basis (Controller) | Legitimate interest / contract |
|---|---|---|
| Executing pipeline runs on behalf of the Customer | Art. 6(1)(b) — contract performance | Customer's instruction |
| Storing run history and tickets for audit / replay | Art. 6(1)(b) or (f) | Business continuity, debugging |
| Authentication and access control | Art. 6(1)(b) | Secure service delivery |
| Billing and usage metering | Art. 6(1)(b) | Contract performance |

### 7.4 Categories of personal data processed

The Platform may process the following categories, depending on what the Customer includes
in run requests:

| Category | Examples | Stored in |
|---|---|---|
| Identifiers | Names, emails, employee IDs | `run.request` (if included by caller), `user` table |
| Contact data | Email addresses | `user` table |
| Free-form text | Any text submitted as a run request | `run.request` (indefinite retention — **see Section 7.7**) |
| Technical identifiers | IP addresses (in access logs), API key labels | nginx/platform access logs (30 days), `api_key` table |

### 7.5 Categories of data subjects

- Employees of the Customer who use the Platform
- End users whose data is referenced in run requests (if applicable)
- Members of the Customer's development team who trigger runs programmatically

### 7.6 Obligations of antcrew as Processor (Art. 28(3))

antcrew commits to:

a. **Process only on instructions.** Process personal data only according to the
   Customer's documented instructions, including as set out in this document. We will
   inform the Customer if we consider an instruction to infringe applicable law.

b. **Confidentiality.** Ensure that persons authorised to process personal data are
   bound by confidentiality obligations.

c. **Security.** Implement appropriate technical and organisational measures (see
   Section 9).

d. **Sub-processors.** Not engage a new sub-processor without (i) informing the
   Customer, and (ii) allowing a 30-day objection window. Where the Customer objects
   and a solution cannot be found, either party may terminate the agreement. See
   current sub-processor list in Section 8.

e. **Data subject rights.** Assist the Customer in responding to data subject requests
   (access, rectification, erasure, portability, restriction) within the time required
   under applicable law. We do not currently provide an automated erasure workflow;
   deletion requests must be handled by the Customer's administrator via the admin API
   or direct database query (documented in [data-retention.md](../platform/data-retention.md)).

f. **Security assistance.** Assist the Customer in fulfilling obligations under Art.
   32–36 (security, breach notification, DPIA).

g. **Deletion / return.** At the end of the service relationship, delete or return all
   personal data and delete existing copies, unless Union or Member State law requires
   storage of the personal data.

h. **Audit.** Provide all information necessary to demonstrate compliance with Art. 28,
   and allow for and contribute to audits and inspections conducted by the Customer or
   an auditor mandated by the Customer (with reasonable advance notice).

### 7.7 Retention — Controller obligations

`run.request` is retained indefinitely by default. This column may contain personal data
submitted by the Customer. **The Customer (as Controller) is responsible for ensuring
that this retention is compatible with the legal basis under which the data was collected.**

If a data subject exercises the right to erasure (GDPR Art. 17), the Customer's
administrator must delete the relevant rows via the API. See
[data-retention.md](../platform/data-retention.md) for deletion SQL.

antcrew recommends that Customers with strict retention obligations consider implementing
a periodic deletion routine.

### 7.8 International transfers

antcrew hosts the Platform in the EU (Hetzner, Frankfurt/Helsinki). The Neon PostgreSQL
service is hosted within the EU region selected by the Customer at workspace creation.

However, LLM providers — Anthropic (US), OpenAI (US), Groq (US) — are established in
third countries. Run content (prompts and responses) is transferred to these providers
when executing LLM-backed pipelines.

**Controller's responsibility:** The Customer must ensure an appropriate transfer
mechanism is in place for transfers to each LLM provider, e.g.:

- Anthropic: execute Anthropic's Data Processing Addendum (available at
  anthropic.com/privacy) and rely on Standard Contractual Clauses (SCC).
- OpenAI: execute OpenAI's API Data Processing Addendum and SCC.
- Groq: review Groq's DPA and SCC documentation.

**Proxy mode:** Customers who deploy the Proxy and use BYOK or proxy mode are solely
responsible for transfers to LLM providers through their own proxy infrastructure.

---

## 8. Sub-processors

| Sub-processor | Country | Purpose | Transfer mechanism |
|---|---|---|---|
| Hetzner Online GmbH | Germany (EU) | Infrastructure / compute | Within EEA — no transfer |
| Neon, Inc. | Germany (EU region) | PostgreSQL database | Within EEA — no transfer |
| Resend | EU data residency | Transactional email | SCC / EU hosting |
| Anthropic PBC | USA | LLM inference (managed mode) | SCC via Anthropic DPA |
| OpenAI, LLC | USA | LLM inference (managed mode, optional) | SCC via OpenAI DPA |
| Groq, Inc. | USA | LLM inference (managed mode, optional) | SCC via Groq DPA |

LLM sub-processors are engaged only when the Customer's workspace is configured for
**managed** LLM mode. Customers in **BYOK** or **proxy** mode route LLM calls
directly to their own provider credentials; antcrew's servers do not transmit run
content to LLM providers in those modes.

antcrew will publish updates to this list with 30 days' notice.

---

## 9. Technical and organisational measures (Art. 32)

| Domain | Measure |
|---|---|
| **Encryption at rest** | Database encrypted at rest via Neon's server-side encryption |
| **Encryption in transit** | TLS 1.2+ enforced on all platform endpoints; HSTS enabled |
| **Authentication** | API keys stored as bcrypt hashes; passwords not stored in plaintext |
| **Secrets** | Provider API keys (managed mode) encrypted with Fernet before database storage; `BYOK_ENCRYPTION_KEY` held in environment, not in source code |
| **Access control** | Workspace isolation at the database level; row-level filtering on every query |
| **Audit logging** | Platform access and HITL review decisions written to append-only log |
| **Proxy logging** | Proxy emits structured per-request logs (provider, status, duration, request_id) with no prompt/response content |
| **Vulnerability management** | Dependencies pinned; Dependabot PRs reviewed weekly; Docker images rebuilt on base image updates |
| **Incident response** | Documented runbook; security@antcrew.org monitored 24/7 |
| **Backup** | Daily backup of application state; Neon continuous WAL for < 15-min RPO |
| **Personnel** | Persons with access to production data bound by confidentiality; access principle of least privilege |

---

## 10. Incident response

### 10.1 Data breach procedure

1. **Detection.** Continuous monitoring via structured logs and alerting.
2. **Containment.** Isolate affected components within 2 hours of confirmed breach.
3. **Assessment.** Determine scope and categories of personal data affected.
4. **Notification.** Notify the Customer within **48 hours** of confirmed breach,
   providing: nature of the incident, categories and approximate number of data subjects
   affected, likely consequences, proposed containment and remediation measures.
5. **Regulator.** The Customer (as Controller) is responsible for notifying the relevant
   supervisory authority (AEPD in Spain) within 72 hours per Art. 33.

### 10.2 Security incident contact

`security@antcrew.org` — monitored 24 hours/day, 7 days/week.

---

## 11. Responsibility matrix (consolidated)

| Area | antcrew | Customer |
|---|:---:|:---:|
| Platform availability (excluding LLM providers) | ✅ | |
| Proxy uptime | | ✅ |
| LLM provider uptime | | (Provider's responsibility) |
| `PROXY_TOKEN` confidentiality | ✅ (generation) | ✅ (storage and rotation) |
| LLM API key storage and rotation | | ✅ |
| TLS on proxy endpoint | | ✅ |
| Encryption of data at rest (Platform) | ✅ | |
| Deletion of personal data on request | ✅ (tooling) | ✅ (initiation, decision) |
| Transfer mechanism for US LLM providers | | ✅ |
| Breach notification to AEPD | | ✅ (Controller duty) |
| Art. 32 TOMs for the Platform | ✅ | |
| Art. 32 TOMs for the Proxy | | ✅ |
| Data subject rights response | ✅ (assistance) | ✅ (response and decision) |

---

*Questions and DPA execution requests: legal@antcrew.org*
*Security incidents: security@antcrew.org*
*Support: support@antcrew.org or in-app widget*
