from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, List
from .database import get_db
from .models import Base, User, Tier, Feature, TierFeature
from .database import engine
from .feature_gate import FeatureGate, FeatureEntitlementService
from pydantic import BaseModel

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Fayzy Feature Entitlement System")


# Pydantic models for API
class FeatureCheckResponse(BaseModel):
    user_id: int
    feature_slug: str
    has_access: bool


class UserFeaturesResponse(BaseModel):
    user_id: int
    features: List[str]


# Example routes demonstrating usage
@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Fayzy Feature Entitlement System"}


@app.get("/users/{user_id}/features", response_model=UserFeaturesResponse)
async def get_user_features(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get all features available to a user."""
    service = FeatureEntitlementService(db)
    features = service.get_user_features(user_id)
    return UserFeaturesResponse(user_id=user_id, features=list(features))


@app.get("/users/{user_id}/features/{feature_slug}", response_model=FeatureCheckResponse)
async def check_user_feature(
    user_id: int,
    feature_slug: str,
    db: Session = Depends(get_db)
):
    """Check if a user has access to a specific feature."""
    service = FeatureEntitlementService(db)
    has_access = service.has_feature(user_id, feature_slug)
    return FeatureCheckResponse(
        user_id=user_id,
        feature_slug=feature_slug,
        has_access=has_access
    )


@app.get("/protected/advanced-integrations")
async def advanced_integrations_endpoint(
    user_id: int,
    features: set = Depends(FeatureGate(["can_access_advanced_integrations"]))
):
    """
    Example protected endpoint that requires specific feature.
    Only users with 'can_access_advanced_integrations' feature can access.
    """
    return {
        "message": "Access granted to advanced integrations",
        "user_id": user_id,
        "available_features": list(features)
    }


@app.get("/protected/unlimited-associates")
async def unlimited_associates_endpoint(
    user_id: int,
    features: set = Depends(FeatureGate(["unlimited_associates"]))
):
    """
    Example protected endpoint that requires unlimited_associates feature.
    Only users with this feature (e.g., Pro tier) can access.
    """
    return {
        "message": "Access granted to unlimited associates",
        "user_id": user_id,
        "available_features": list(features)
    }


# Admin/Setup endpoints (in production, these should be protected)
@app.post("/admin/setup-demo-data")
async def setup_demo_data(db: Session = Depends(get_db)):
    """Setup demo data for testing."""
    # Create tiers
    free_tier = Tier(id=1, name="Free", description="Free tier")
    teams_tier = Tier(id=2, name="Teams", description="Teams tier")
    pro_tier = Tier(id=3, name="Pro", description="Pro tier")
    
    db.add_all([free_tier, teams_tier, pro_tier])
    db.commit()
    
    # Create features
    features = [
        Feature(slug="unlimited_associates", name="Unlimited Associates", description="Allow unlimited associates"),
        Feature(slug="can_access_advanced_integrations", name="Advanced Integrations", description="Access to advanced integrations"),
        Feature(slug="priority_support", name="Priority Support", description="Priority customer support"),
        Feature(slug="custom_branding", name="Custom Branding", description="Custom branding options"),
    ]
    
    for feature in features:
        db.add(feature)
    db.commit()
    
    # Map features to tiers
    # Free tier: no special features
    
    # Teams tier: advanced integrations and priority support
    db.add(TierFeature(tier_id=2, feature_slug="can_access_advanced_integrations", enabled=True))
    db.add(TierFeature(tier_id=2, feature_slug="priority_support", enabled=True))
    
    # Pro tier: all features
    db.add(TierFeature(tier_id=3, feature_slug="unlimited_associates", enabled=True))
    db.add(TierFeature(tier_id=3, feature_slug="can_access_advanced_integrations", enabled=True))
    db.add(TierFeature(tier_id=3, feature_slug="priority_support", enabled=True))
    db.add(TierFeature(tier_id=3, feature_slug="custom_branding", enabled=True))
    
    db.commit()
    
    # Create test users
    from datetime import datetime, timedelta, timezone
    
    user_free = User(id=1, email="free@example.com", tier_id=1, subscription_expires_at=None)
    user_teams = User(id=2, email="teams@example.com", tier_id=2, subscription_expires_at=datetime.now(timezone.utc) + timedelta(days=30))
    user_pro = User(id=3, email="pro@example.com", tier_id=3, subscription_expires_at=datetime.now(timezone.utc) + timedelta(days=30))
    user_expired = User(id=4, email="expired@example.com", tier_id=3, subscription_expires_at=datetime.now(timezone.utc) - timedelta(days=10), grace_period_days=7)
    user_grace = User(id=5, email="grace@example.com", tier_id=3, subscription_expires_at=datetime.now(timezone.utc) - timedelta(days=3), grace_period_days=7)
    
    db.add_all([user_free, user_teams, user_pro, user_expired, user_grace])
    db.commit()
    
    return {"message": "Demo data created successfully"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
