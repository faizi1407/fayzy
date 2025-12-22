import pytest
from fastapi import status


def test_get_user_features_api(client, setup_demo_data):
    """Test the API endpoint for getting user features."""
    pro_user_id = setup_demo_data["users"]["pro"].id
    
    response = client.get(f"/users/{pro_user_id}/features")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert data["user_id"] == pro_user_id
    assert "unlimited_associates" in data["features"]
    assert "can_access_advanced_integrations" in data["features"]


def test_check_specific_feature_api(client, setup_demo_data):
    """Test the API endpoint for checking a specific feature."""
    pro_user_id = setup_demo_data["users"]["pro"].id
    
    response = client.get(f"/users/{pro_user_id}/features/unlimited_associates")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert data["user_id"] == pro_user_id
    assert data["feature_slug"] == "unlimited_associates"
    assert data["has_access"] is True


def test_teams_user_lacks_feature_api(client, setup_demo_data):
    """Test Teams user doesn't have Pro-only feature via API."""
    teams_user_id = setup_demo_data["users"]["teams"].id
    
    response = client.get(f"/users/{teams_user_id}/features/unlimited_associates")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert data["has_access"] is False


def test_protected_endpoint_with_feature(client, setup_demo_data):
    """Test accessing protected endpoint with required feature."""
    pro_user_id = setup_demo_data["users"]["pro"].id
    
    response = client.get(f"/protected/unlimited-associates?user_id={pro_user_id}")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert "Access granted" in data["message"]


def test_protected_endpoint_without_feature(client, setup_demo_data):
    """Test accessing protected endpoint without required feature."""
    teams_user_id = setup_demo_data["users"]["teams"].id
    
    response = client.get(f"/protected/unlimited-associates?user_id={teams_user_id}")
    assert response.status_code == status.HTTP_403_FORBIDDEN
    
    data = response.json()
    assert "Missing required features" in data["detail"]


def test_advanced_integrations_endpoint_with_feature(client, setup_demo_data):
    """Test Teams user can access advanced integrations endpoint."""
    teams_user_id = setup_demo_data["users"]["teams"].id
    
    response = client.get(f"/protected/advanced-integrations?user_id={teams_user_id}")
    assert response.status_code == status.HTTP_200_OK


def test_advanced_integrations_endpoint_without_feature(client, setup_demo_data):
    """Test Free user cannot access advanced integrations endpoint."""
    free_user_id = setup_demo_data["users"]["free"].id
    
    response = client.get(f"/protected/advanced-integrations?user_id={free_user_id}")
    assert response.status_code == status.HTTP_403_FORBIDDEN
