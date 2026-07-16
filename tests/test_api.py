"""
tests/test_api.py
Integration tests for the Flask API endpoints in app.py
"""

import pytest

from app import app


@pytest.fixture
def client():
    """Configure Flask test client."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# ---------------------------------------------------------------------------
# GET /health
# ---------------------------------------------------------------------------


class TestHealth:
    def test_health_returns_200(self, client):
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_body(self, client):
        data = client.get("/health").get_json()
        assert data == {"status": "ok"}


# ---------------------------------------------------------------------------
# GET /operations
# ---------------------------------------------------------------------------


class TestListOperations:
    def test_operations_returns_200(self, client):
        response = client.get("/operations")
        assert response.status_code == 200

    def test_operations_contains_expected_keys(self, client):
        data = client.get("/operations").get_json()
        assert "operations" in data
        expected = {"add", "subtract", "multiply", "divide", "power", "modulo"}
        assert expected == set(data["operations"])


# ---------------------------------------------------------------------------
# POST /calculate – happy-path cases
# ---------------------------------------------------------------------------


class TestCalculateSuccess:
    def _post(self, client, payload):
        return client.post("/calculate", json=payload)

    def test_add(self, client):
        res = self._post(client, {"operation": "add", "a": 3, "b": 4})
        assert res.status_code == 200
        assert res.get_json()["result"] == 7

    def test_subtract(self, client):
        res = self._post(client, {"operation": "subtract", "a": 10, "b": 3})
        assert res.get_json()["result"] == 7

    def test_multiply(self, client):
        res = self._post(client, {"operation": "multiply", "a": 6, "b": 7})
        assert res.get_json()["result"] == 42

    def test_divide(self, client):
        res = self._post(client, {"operation": "divide", "a": 10, "b": 4})
        assert res.get_json()["result"] == pytest.approx(2.5)

    def test_power(self, client):
        res = self._post(client, {"operation": "power", "a": 2, "b": 8})
        assert res.get_json()["result"] == 256

    def test_modulo(self, client):
        res = self._post(client, {"operation": "modulo", "a": 10, "b": 3})
        assert res.get_json()["result"] == 1

    def test_response_echoes_inputs(self, client):
        payload = {"operation": "add", "a": 1, "b": 2}
        data = self._post(client, payload).get_json()
        assert data["operation"] == "add"
        assert data["a"] == 1
        assert data["b"] == 2
        assert data["result"] == 3

    def test_float_operands(self, client):
        res = self._post(client, {"operation": "add", "a": 1.5, "b": 2.5})
        assert res.get_json()["result"] == pytest.approx(4.0)


# ---------------------------------------------------------------------------
# POST /calculate – error cases
# ---------------------------------------------------------------------------


class TestCalculateErrors:
    def _post(self, client, payload):
        return client.post("/calculate", json=payload)

    def test_missing_body_returns_400(self, client):
        res = client.post("/calculate", data="not json", content_type="text/plain")
        assert res.status_code == 400

    def test_missing_operation_field(self, client):
        res = self._post(client, {"a": 1, "b": 2})
        assert res.status_code == 400
        assert "error" in res.get_json()

    def test_missing_a_field(self, client):
        res = self._post(client, {"operation": "add", "b": 2})
        assert res.status_code == 400

    def test_missing_b_field(self, client):
        res = self._post(client, {"operation": "add", "a": 1})
        assert res.status_code == 400

    def test_non_numeric_a_returns_400(self, client):
        res = self._post(client, {"operation": "add", "a": "ten", "b": 2})
        assert res.status_code == 400

    def test_non_numeric_b_returns_400(self, client):
        res = self._post(client, {"operation": "add", "a": 1, "b": "two"})
        assert res.status_code == 400

    def test_divide_by_zero_returns_400(self, client):
        res = self._post(client, {"operation": "divide", "a": 5, "b": 0})
        assert res.status_code == 400
        assert "error" in res.get_json()

    def test_modulo_by_zero_returns_400(self, client):
        res = self._post(client, {"operation": "modulo", "a": 5, "b": 0})
        assert res.status_code == 400

    def test_unknown_operation_returns_400(self, client):
        res = self._post(client, {"operation": "sqrt", "a": 9, "b": 0})
        assert res.status_code == 400
        assert "error" in res.get_json()
