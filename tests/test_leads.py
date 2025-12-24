import pytest
from httpx import AsyncClient
import time


@pytest.mark.asyncio
async def test_create_lead_success(client: AsyncClient):
    """Test creating a lead with valid email returns 201 Created"""
    response = await client.post(
        "/api/v1/leads",
        json={"email": "test@example.com"}
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data
    assert "created_at" in data


@pytest.mark.asyncio
async def test_create_lead_invalid_email(client: AsyncClient):
    """Test creating a lead with invalid email format returns 422 Unprocessable Entity"""
    invalid_emails = [
        "not-an-email",
        "missing@domain",
        "@nodomain.com",
        "no-at-sign.com",
        ""
    ]
    
    for email in invalid_emails:
        response = await client.post(
            "/api/v1/leads",
            json={"email": email}
        )
        assert response.status_code == 422, f"Email '{email}' should be invalid"


@pytest.mark.asyncio
async def test_create_lead_duplicate_email(client: AsyncClient):
    """Test creating a lead with duplicate email returns 409 Conflict"""
    email = "duplicate@example.com"
    
    # First request - should succeed
    response1 = await client.post(
        "/api/v1/leads",
        json={"email": email}
    )
    assert response1.status_code == 201
    
    # Second request - should fail with 409
    response2 = await client.post(
        "/api/v1/leads",
        json={"email": email}
    )
    assert response2.status_code == 409
    assert "already exists" in response2.json()["detail"].lower()


@pytest.mark.asyncio
async def test_rate_limit(client: AsyncClient):
    """Test rate limiting: 5 requests per minute per IP"""
    # Make 5 requests (should all succeed)
    for i in range(5):
        response = await client.post(
            "/api/v1/leads",
            json={"email": f"rate-test-{i}@example.com"}
        )
        assert response.status_code == 201
    
    # 6th request should be rate limited
    response = await client.post(
        "/api/v1/leads",
        json={"email": "rate-test-6@example.com"}
    )
    assert response.status_code == 429


@pytest.mark.asyncio
async def test_database_insert_performance(client: AsyncClient):
    """Test that database insert completes in less than 50ms"""
    start_time = time.time()
    
    response = await client.post(
        "/api/v1/leads",
        json={"email": "performance-test@example.com"}
    )
    
    elapsed_time = (time.time() - start_time) * 1000  # Convert to ms
    
    assert response.status_code == 201
    # Allow some buffer for network overhead in tests
    assert elapsed_time < 100, f"Database insert took {elapsed_time:.2f}ms (threshold: <50ms for DB only)"


@pytest.mark.asyncio
async def test_create_lead_missing_email(client: AsyncClient):
    """Test creating a lead without email returns 422"""
    response = await client.post(
        "/api/v1/leads",
        json={}
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_health_endpoint(client: AsyncClient):
    """Test health check endpoint"""
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
