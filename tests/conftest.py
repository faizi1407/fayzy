import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime, timedelta, timezone
from app.models import Base, User, Tier, Feature, TierFeature
from app.database import get_db
from app.main import app
from fastapi.testclient import TestClient

# Test database
TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database for each test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with overridden database dependency."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def setup_demo_data(db_session: Session):
    """Setup demo data for tests."""
    # Create tiers
    free_tier = Tier(id=1, name="Free", description="Free tier")
    teams_tier = Tier(id=2, name="Teams", description="Teams tier")
    pro_tier = Tier(id=3, name="Pro", description="Pro tier")
    
    db_session.add_all([free_tier, teams_tier, pro_tier])
    db_session.commit()
    
    # Create features
    features = [
        Feature(slug="unlimited_associates", name="Unlimited Associates"),
        Feature(slug="can_access_advanced_integrations", name="Advanced Integrations"),
        Feature(slug="priority_support", name="Priority Support"),
    ]
    
    for feature in features:
        db_session.add(feature)
    db_session.commit()
    
    # Map features to tiers
    # Teams tier: advanced integrations only
    db_session.add(TierFeature(tier_id=2, feature_slug="can_access_advanced_integrations", enabled=True))
    db_session.add(TierFeature(tier_id=2, feature_slug="priority_support", enabled=True))
    
    # Pro tier: all features
    db_session.add(TierFeature(tier_id=3, feature_slug="unlimited_associates", enabled=True))
    db_session.add(TierFeature(tier_id=3, feature_slug="can_access_advanced_integrations", enabled=True))
    db_session.add(TierFeature(tier_id=3, feature_slug="priority_support", enabled=True))
    
    db_session.commit()
    
    # Create test users
    user_free = User(id=1, email="free@example.com", tier_id=1, subscription_expires_at=None)
    user_teams = User(id=2, email="teams@example.com", tier_id=2, subscription_expires_at=datetime.now(timezone.utc) + timedelta(days=30))
    user_pro = User(id=3, email="pro@example.com", tier_id=3, subscription_expires_at=datetime.now(timezone.utc) + timedelta(days=30))
    user_expired = User(id=4, email="expired@example.com", tier_id=3, subscription_expires_at=datetime.now(timezone.utc) - timedelta(days=10), grace_period_days=7)
    user_grace = User(id=5, email="grace@example.com", tier_id=3, subscription_expires_at=datetime.now(timezone.utc) - timedelta(days=3), grace_period_days=7)
    
    db_session.add_all([user_free, user_teams, user_pro, user_expired, user_grace])
    db_session.commit()
    
    return {
        "tiers": {"free": free_tier, "teams": teams_tier, "pro": pro_tier},
        "users": {
            "free": user_free,
            "teams": user_teams,
            "pro": user_pro,
            "expired": user_expired,
            "grace": user_grace,
        }
    }
