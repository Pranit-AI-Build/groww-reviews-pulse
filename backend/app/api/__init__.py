"""API routes."""
from .reviews import router as reviews_router
from .reports import router as reports_router
from .email import router as email_router

__all__ = ["reviews_router", "reports_router", "email_router"]
