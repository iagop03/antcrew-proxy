# antcrew-proxy — Responsibility Boundaries

## What the proxy is

antcrew-proxy is a **customer-deployed, single-binary HTTP relay** that sits between antcrew-platform and your LLM provider. The platform sends requests authenticated with a `PROXY_TOKEN`; the proxy validates the token and forwards the request to the real provider using your actual API keys.

The platform never stores your provider API keys. The proxy holds them.

---

## Who is responsible for what

| Responsibility | Platform (Anthropic) | Customer (proxy operator) |
|---|:---:|:---:|
| Generating and rotating `PROXY_TOKEN` | ✅ | |
| Keeping `PROXY_TOKEN` secret | | ✅ |
| Storing provider API keys securely | | ✅ |
| TLS termination on the public proxy endpoint | | ✅ |
| Uptime of the proxy process / container | | ✅ |
| Firewall: restrict inbound to platform IPs | | ✅ (recommended) |
| Detecting and rotating a compromised `PROXY_TOKEN` | ✅ (via platform UI) | notify platform |
| Detecting and rotating a compromised provider key | | ✅ |
| Software updates to this proxy image | | ✅ |

---

## Availability

The proxy is **not** a managed service. If the proxy goes down, runs that reach out to LLM providers will fail. The platform returns `503` to callers when the proxy is unreachable.

Recommended: run the proxy behind a process supervisor (Docker `--restart=always`, systemd, or Kubernetes Deployment with `replicas: 1`).

---

## Network requirements

The proxy must be **reachable from the platform** at the URL you configured. It does **not** need to be reachable from the end user's browser — only from the platform backend.

Minimum outbound: HTTPS to your provider's API (e.g. `api.anthropic.com:443`).  
Minimum inbound: HTTP/HTTPS on port 8080 (or whichever port you expose) from the platform.

---

## Security recommendations

1. **Never expose the proxy to the public internet without TLS.** Put it behind nginx/Caddy or use a cloud load balancer with HTTPS.
2. **Firewall inbound** to the platform's egress IPs only (contact support for the current IP list).
3. **Rotate `PROXY_TOKEN`** whenever platform operator access changes (use the platform's `/workspaces/{id}/proxy/generate` endpoint).
4. **Do not log request bodies** — they contain prompt content and may contain sensitive user data.
5. **Mount secrets from environment variables or a secrets manager**, not baked into the Docker image.

---

## Incident response

If you suspect the proxy or a provider key has been compromised:

1. Rotate the provider API key with your LLM provider immediately.
2. Revoke the `PROXY_TOKEN` via the platform UI (`Settings → Proxy → Revoke`).
3. Generate a new `PROXY_TOKEN`, update the proxy environment, and restart.
4. Review proxy access logs for unusual traffic patterns.
