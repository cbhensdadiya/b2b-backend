from fastapi import APIRouter
from app.api.v1.endpoints import auth, buyers, public, buyer_quotes
from app.api.v1.endpoints.admin import auth as admin_auth, users, categories as admin_categories, dashboard, quote_requests

api_router = APIRouter()

# Buyer authentication routes
api_router.include_router(
    auth.router,
    prefix="/buyer/auth",
    tags=["Buyer Authentication"]
)

# Buyer quote requests
api_router.include_router(
    buyer_quotes.router,
    prefix="/buyer",
    tags=["Buyer - Quote Requests"]
)

# Admin - Buyer management routes
api_router.include_router(
    buyers.router,
    prefix="/admin/buyers",
    tags=["Admin - Buyers"]
)

# Master Admin - Authentication
api_router.include_router(
    admin_auth.router,
    prefix="/admin/auth",
    tags=["Master Admin - Authentication"]
)

# Master Admin - User Management
api_router.include_router(
    users.router,
    prefix="/admin",
    tags=["Master Admin - Users"]
)

# Master Admin - Category Management
api_router.include_router(
    admin_categories.router,
    prefix="/admin",
    tags=["Master Admin - Categories & Subcategories"]
)

# Master Admin - Dashboard & Reports
api_router.include_router(
    dashboard.router,
    prefix="/admin",
    tags=["Master Admin - Dashboard & Reports"]
)

# Master Admin - Quote Requests
api_router.include_router(
    quote_requests.router,
    prefix="/admin",
    tags=["Master Admin - Quote Requests"]
)

# Public routes
api_router.include_router(
    public.router,
    prefix="/public",
    tags=["Public"]
)
