# Fayzy - Feature Entitlement System

A FastAPI-based feature entitlement system that allows querying user features by name rather than by plan name, enabling easy movement of features between tiers.

## Features

- **Config-Driven Entitlements**: Query features by name (e.g., 'unlimited_associates', 'can_access_advanced_integrations')
- **Database-Backed**: PostgreSQL/SQLite with tier-feature mapping
- **Redis Caching**: Fast entitlement checks with < 10ms overhead
- **Grace Periods**: Features remain active after subscription expiration
- **FastAPI Integration**: Easy-to-use FeatureGate dependency for route protection

## Installation

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # For development
```

## Quick Start

1. Start the application:

```bash
python -m app.main
```

2. Setup demo data:

```bash
curl -X POST http://localhost:8000/admin/setup-demo-data
```

3. Check user features:

```bash
# Get all features for a user
curl http://localhost:8000/users/3/features

# Check specific feature
curl http://localhost:8000/users/3/features/unlimited_associates
```

## Usage

### Basic Feature Check

```python
from app.feature_gate import FeatureEntitlementService

service = FeatureEntitlementService(db)
has_feature = service.has_feature(user_id=1, feature_slug="unlimited_associates")
```

### Protecting Routes with FeatureGate

```python
from fastapi import Depends
from app.feature_gate import FeatureGate

@app.get("/protected-endpoint")
async def protected_endpoint(
    user_id: int,
    features: set = Depends(FeatureGate(["unlimited_associates"]))
):
    return {"message": "Access granted"}
```

## Testing

Run the test suite:

```bash
pytest tests/ -v
```

Run specific tests:

```bash
pytest tests/test_feature_entitlement.py -v
pytest tests/test_api.py -v
```

## Architecture

### Database Models

- **Tier**: Subscription tiers (Free, Teams, Pro)
- **Feature**: Available features with unique slugs
- **TierFeature**: Mapping between tiers and features
- **User**: User accounts with tier assignment and subscription expiration

### Caching Strategy

- Redis caching with 5-minute TTL
- Cache keys: `user_features:{user_id}`
- Automatic cache invalidation support
- Graceful fallback if Redis unavailable

### Performance

- Entitlement checks: < 10ms overhead
- First check queries database + caches result
- Subsequent checks use Redis cache
- Bulk operations supported

## Configuration

Environment variables:

- `DATABASE_URL`: Database connection string (default: sqlite:///./fayzy.db)
- `REDIS_URL`: Redis connection string (default: redis://localhost:6379/0)

## API Endpoints

### User Features

- `GET /users/{user_id}/features` - Get all features for a user
- `GET /users/{user_id}/features/{feature_slug}` - Check specific feature

### Protected Endpoints (Examples)

- `GET /protected/unlimited-associates` - Requires 'unlimited_associates' feature
- `GET /protected/advanced-integrations` - Requires 'can_access_advanced_integrations' feature

### Admin

- `POST /admin/setup-demo-data` - Setup demo data for testing

## Acceptance Criteria

✅ Pro tier users have 'unlimited_associates' feature  
✅ Teams tier users do NOT have 'unlimited_associates' feature  
✅ Entitlement checks add < 10ms overhead  
✅ Grace periods supported for expired subscriptions  
✅ Redis caching minimizes database load  

## License

MIT
