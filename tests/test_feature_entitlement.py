import pytest
import time
from app.feature_gate import FeatureEntitlementService
from datetime import datetime, timedelta


def test_pro_user_has_unlimited_associates(db_session, setup_demo_data):
    """
    Acceptance Criteria 1:
    GIVEN a user on the Pro tier,
    WHEN checking for 'unlimited_associates',
    THEN the service returns True based on DB config.
    """
    service = FeatureEntitlementService(db_session)
    pro_user_id = setup_demo_data["users"]["pro"].id
    
    # Check that Pro user has unlimited_associates
    has_feature = service.has_feature(pro_user_id, "unlimited_associates")
    assert has_feature is True, "Pro user should have unlimited_associates feature"
    
    # Verify via get_user_features
    features = service.get_user_features(pro_user_id)
    assert "unlimited_associates" in features, "unlimited_associates should be in Pro user's features"


def test_teams_user_lacks_unlimited_associates(db_session, setup_demo_data):
    """
    Acceptance Criteria 2:
    GIVEN a user on the Teams tier,
    WHEN checking for 'unlimited_associates',
    THEN the service returns False.
    """
    service = FeatureEntitlementService(db_session)
    teams_user_id = setup_demo_data["users"]["teams"].id
    
    # Check that Teams user does NOT have unlimited_associates
    has_feature = service.has_feature(teams_user_id, "unlimited_associates")
    assert has_feature is False, "Teams user should NOT have unlimited_associates feature"
    
    # Verify via get_user_features
    features = service.get_user_features(teams_user_id)
    assert "unlimited_associates" not in features, "unlimited_associates should NOT be in Teams user's features"


def test_entitlement_check_performance(db_session, setup_demo_data):
    """
    Acceptance Criteria 3:
    Entitlement checks must add < 10ms of overhead to API requests.
    """
    service = FeatureEntitlementService(db_session)
    pro_user_id = setup_demo_data["users"]["pro"].id
    
    # Warm up the cache
    service.get_user_features(pro_user_id)
    
    # Measure cached performance (should be very fast)
    start_time = time.perf_counter()
    for _ in range(100):
        service.has_feature(pro_user_id, "unlimited_associates")
    end_time = time.perf_counter()
    
    avg_time_ms = ((end_time - start_time) / 100) * 1000
    assert avg_time_ms < 10, f"Average entitlement check took {avg_time_ms:.2f}ms, should be < 10ms"


def test_grace_period_active_subscription(db_session, setup_demo_data):
    """
    Acceptance Criteria 4:
    The system must support 'grace periods' where features remain active after subscription expiration.
    Test user within grace period.
    """
    service = FeatureEntitlementService(db_session)
    grace_user_id = setup_demo_data["users"]["grace"].id
    
    # User expired 3 days ago but has 7-day grace period, should still have features
    has_feature = service.has_feature(grace_user_id, "unlimited_associates")
    assert has_feature is True, "User within grace period should still have features"
    
    features = service.get_user_features(grace_user_id)
    assert len(features) > 0, "User within grace period should have features"


def test_grace_period_expired_subscription(db_session, setup_demo_data):
    """
    Acceptance Criteria 4:
    Test user beyond grace period loses access.
    """
    service = FeatureEntitlementService(db_session)
    expired_user_id = setup_demo_data["users"]["expired"].id
    
    # User expired 10 days ago with 7-day grace period, should have NO features
    has_feature = service.has_feature(expired_user_id, "unlimited_associates")
    assert has_feature is False, "User beyond grace period should NOT have features"
    
    features = service.get_user_features(expired_user_id)
    assert len(features) == 0, "User beyond grace period should have no features"


def test_cache_is_used(db_session, setup_demo_data):
    """
    Acceptance Criteria 5:
    All entitlement checks are cached in Redis to minimize DB load.
    """
    service = FeatureEntitlementService(db_session)
    pro_user_id = setup_demo_data["users"]["pro"].id
    
    # First call should query DB and cache
    features1 = service.get_user_features(pro_user_id)
    
    # Second call should use cache (we can verify this by checking it's faster)
    start_time = time.perf_counter()
    features2 = service.get_user_features(pro_user_id)
    end_time = time.perf_counter()
    
    assert features1 == features2, "Cached features should match original features"
    
    # Cached call should be very fast
    cache_time_ms = (end_time - start_time) * 1000
    assert cache_time_ms < 5, f"Cached call took {cache_time_ms:.2f}ms, should be < 5ms"


def test_free_user_has_no_special_features(db_session, setup_demo_data):
    """Test that Free tier users have no premium features."""
    service = FeatureEntitlementService(db_session)
    free_user_id = setup_demo_data["users"]["free"].id
    
    features = service.get_user_features(free_user_id)
    assert len(features) == 0, "Free user should have no premium features"
    
    assert not service.has_feature(free_user_id, "unlimited_associates")
    assert not service.has_feature(free_user_id, "can_access_advanced_integrations")


def test_teams_user_has_correct_features(db_session, setup_demo_data):
    """Test that Teams tier users have the right features."""
    service = FeatureEntitlementService(db_session)
    teams_user_id = setup_demo_data["users"]["teams"].id
    
    features = service.get_user_features(teams_user_id)
    
    # Teams should have these features
    assert "can_access_advanced_integrations" in features
    assert "priority_support" in features
    
    # But not these
    assert "unlimited_associates" not in features


def test_pro_user_has_all_features(db_session, setup_demo_data):
    """Test that Pro tier users have all features."""
    service = FeatureEntitlementService(db_session)
    pro_user_id = setup_demo_data["users"]["pro"].id
    
    features = service.get_user_features(pro_user_id)
    
    # Pro should have all features
    assert "unlimited_associates" in features
    assert "can_access_advanced_integrations" in features
    assert "priority_support" in features


def test_nonexistent_user_has_no_features(db_session, setup_demo_data):
    """Test that a nonexistent user has no features."""
    service = FeatureEntitlementService(db_session)
    
    features = service.get_user_features(999)
    assert len(features) == 0, "Nonexistent user should have no features"
