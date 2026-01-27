"""Tests for health check endpoint."""


class TestHealthCheck:
    """Tests for health check endpoint."""

    def test_health_check(self, client):
        """Test health check endpoint returns healthy status."""
        response = client.get("/api/health")

        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}
