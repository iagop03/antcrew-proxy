# antcrew-proxy Changelog

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
