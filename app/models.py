from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()


class Tier(Base):
    """Subscription tier model."""
    __tablename__ = "tiers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    description = Column(String)
    
    features = relationship("TierFeature", back_populates="tier")


class Feature(Base):
    """Feature model."""
    __tablename__ = "features"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    
    tier_features = relationship("TierFeature", back_populates="feature")


class TierFeature(Base):
    """Mapping table between tiers and features."""
    __tablename__ = "tier_features"

    id = Column(Integer, primary_key=True, index=True)
    tier_id = Column(Integer, ForeignKey("tiers.id"), nullable=False, index=True)
    feature_slug = Column(String, ForeignKey("features.slug"), nullable=False, index=True)
    enabled = Column(Boolean, default=True, nullable=False)
    
    tier = relationship("Tier", back_populates="features")
    feature = relationship("Feature", back_populates="tier_features")


class User(Base):
    """User model with subscription information."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    tier_id = Column(Integer, ForeignKey("tiers.id"), nullable=False, index=True)
    subscription_expires_at = Column(DateTime, nullable=True)
    grace_period_days = Column(Integer, default=7, nullable=False)
    
    tier = relationship("Tier")
