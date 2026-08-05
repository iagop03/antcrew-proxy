# antcrew-proxy Changelog

## 1.1.0 (2026-08-06)

### Added
- Per-request structured log line (`proxy.request`) with `provider`, `path`, `status`,
  `duration_ms`, and optional `request_id` (extracted from `x-request-id` / `request-id` /
  `cf-ray` response headers). Errors and 5xx responses log at ERROR level; 4xx at WARNING;
  success at INFO. No request or response body content is ever logged.
- `_REQUEST_ID_HEADERS` constant listing the response headers checked for upstream
  correlation IDs (useful when filing support tickets with the LLM provider).

### Unreleased
_Nothing yet._

---

## 1.0.0 (2026-07-31)

### Added
- `__version__ = "1.0.0"` exported from `main.py`
- Pinned dependency versions in `requirements.txt` for reproducible builds
- `Dockerfile` now installs from `requirements.txt` instead of ad-hoc pip args
- Smoke tests in `tests/test_smoke.py` covering health, auth rejection, and unknown provider
- Support for DeepSeek, Mistral, xAI (Grok), Together, Fireworks, Cerebras, LM Studio, vLLM providers

### Changed
- `Dockerfile`: switched from `RUN pip install --no-cache-dir fastapi uvicorn httpx` to `COPY requirements.txt` + `RUN pip install -r requirements.txt`

### Unreleased
_Nothing yet._
