"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.api import reviews_router, reports_router, email_router

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description="API for Groww Reviews Weekly Pulse",
    version="1.0.0",
    debug=settings.debug,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(reviews_router)
app.include_router(reports_router)
app.include_router(email_router)


@app.get("/")
async def root():
    return {
        "message": "Groww Reviews API",
        "version": "1.0.0",
        "endpoints": {
            "reviews": "/api/reviews",
            "reports": "/api/reports/latest",
            "email": "/api/email/send-report",
        }
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )
