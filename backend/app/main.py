"""Main FastAPI application entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.routers import auth, transactions, investments, budget, tax, dashboard, sms_parser, market_data

settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Indian Personal Finance Management App - Combining Rich Dad principles with Indian Tax Planning",
)

# Configure CORS
origins = settings.ALLOWED_ORIGINS.split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(transactions.router)
app.include_router(investments.router)
app.include_router(budget.router)
app.include_router(tax.router)
app.include_router(dashboard.router)
app.include_router(sms_parser.router)
app.include_router(market_data.router)


@app.get("/")
def root():
    """Root endpoint."""
    return {
        "message": "Welcome to Indian Personal Finance Management App",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
