"""Smoke tests for antcrew-proxy.

Run with:  PROXY_TOKEN=test pytest tests/
"""
import os

import pytest
from fastapi.testclient import TestClient

os.environ.setdefault("PROXY_TOKEN", "smoke-test-token")

import main  # noqa: E402 — import after env is set

# Use the token that main actually loaded (may differ from the default if env was pre-set).
_TOKEN = main.PROXY_TOKEN


@pytest.fixture()
def client() -> TestClient:
    return TestClient(main.app, raise_server_exceptions=False)


def test_health_ok(client: TestClient) -> None:
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["ok"] is True


def test_missing_token_is_rejected(client: TestClient) -> None:
    resp = client.post("/openai/v1/chat/completions", json={"model": "gpt-4o"})
    assert resp.status_code == 401


def test_unknown_provider_returns_404(client: TestClient) -> None:
    resp = client.post(
        "/nonexistent-provider/v1/chat/completions",
        json={"model": "x"},
        headers={"x-api-key": _TOKEN},
    )
    assert resp.status_code == 404
