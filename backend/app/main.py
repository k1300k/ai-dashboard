"""Main FastAPI application"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.redis import close_redis

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="AI-powered idea expansion platform with intelligent mindmapping",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    print(f"🚀 Starting {settings.APP_NAME} v{settings.VERSION}")
    print(f"📝 Environment: {settings.ENVIRONMENT}")
    print(f"🤖 AI Model: {settings.OPENAI_MODEL}")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("🛑 Shutting down...")
    await close_redis()


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": settings.APP_NAME,
        "version": settings.VERSION,
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT
    }


# Import and include routers
from app.api import boards, nodes, ai

app.include_router(boards.router, prefix="/api/boards", tags=["boards"])
app.include_router(nodes.router, prefix="/api/nodes", tags=["nodes"])
app.include_router(ai.router, prefix="/api/ai", tags=["ai"])
