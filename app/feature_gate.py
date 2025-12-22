from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Set, Optional
from .database import get_db
from .models import User, TierFeature
from .cache import CacheService


class FeatureEntitlementService:
    """Service for checking feature entitlements."""
    
    def __init__(self, db: Session):
        self.db = db
        self.cache = CacheService()
    
    def get_user_features(self, user_id: int) -> Set[str]:
        """
        Get all features available to a user.
        Checks cache first, then database if cache miss.
        """
        # Try cache first
        cached_features = self.cache.get_user_features(user_id)
        if cached_features is not None:
            return cached_features
        
        # Cache miss - query database
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return set()
        
        # Check if subscription is valid (including grace period)
        if not self._is_subscription_active(user):
            return set()
        
        # Get features for user's tier
        tier_features = (
            self.db.query(TierFeature)
            .filter(
                TierFeature.tier_id == user.tier_id,
                TierFeature.enabled == True
            )
            .all()
        )
        
        features = {tf.feature_slug for tf in tier_features}
        
        # Cache the result
        self.cache.set_user_features(user_id, features)
        
        return features
    
    def _is_subscription_active(self, user: User) -> bool:
        """Check if user's subscription is active, considering grace period."""
        if user.subscription_expires_at is None:
            # No expiration date means permanent subscription
            return True
        
        now = datetime.utcnow()
        grace_period = timedelta(days=user.grace_period_days)
        expiration_with_grace = user.subscription_expires_at + grace_period
        
        return now <= expiration_with_grace
    
    def has_feature(self, user_id: int, feature_slug: str) -> bool:
        """Check if a user has access to a specific feature."""
        features = self.get_user_features(user_id)
        return feature_slug in features


class FeatureGate:
    """
    Dependency for FastAPI routes to check feature entitlements.
    Usage:
        @app.get("/advanced-endpoint")
        async def advanced_endpoint(
            features: FeatureGate = Depends(FeatureGate(["can_access_advanced_integrations"]))
        ):
            # This route requires the specified feature
            return {"message": "Access granted"}
    """
    
    def __init__(self, required_features: list[str]):
        self.required_features = required_features
    
    async def __call__(
        self,
        user_id: int,  # In a real app, this would come from auth middleware
        db: Session = Depends(get_db)
    ) -> Set[str]:
        """
        Dependency that checks if user has required features.
        Returns the set of all user features if access is granted.
        Raises HTTPException if user doesn't have required features.
        """
        service = FeatureEntitlementService(db)
        user_features = service.get_user_features(user_id)
        
        # Check if user has all required features
        missing_features = set(self.required_features) - user_features
        if missing_features:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Missing required features: {', '.join(missing_features)}"
            )
        
        return user_features


def check_feature(
    user_id: int,
    feature_slug: str,
    db: Session = Depends(get_db)
) -> bool:
    """
    Simple dependency to check a single feature.
    Usage:
        @app.get("/check-feature")
        async def check_feature_endpoint(
            has_feature: bool = Depends(lambda: check_feature(user_id=1, feature_slug="unlimited_associates"))
        ):
            return {"has_feature": has_feature}
    """
    service = FeatureEntitlementService(db)
    return service.has_feature(user_id, feature_slug)
