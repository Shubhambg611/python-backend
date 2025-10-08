from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.register import registration_router, verify_email_router, check_user_router
from app.routes.forgot_password import send_otp_router, verify_otp_router, reset_password_router
from app.routes.access import login_router, logout_router
from app.routes.ai_assistant import assistants_router
from app.config.database import Database
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create FastAPI app
app = FastAPI(
    title="Convis Labs Registration API",
    description="Python backend for user registration with OTP verification",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],  # Add your frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(registration_router, prefix="/api/register", tags=["Registration"])
app.include_router(verify_email_router, prefix="/api/register", tags=["Registration"])
app.include_router(check_user_router, prefix="/api/register", tags=["Registration"])

# Forgot password routers
app.include_router(send_otp_router, prefix="/api/forgot_password", tags=["Forgot Password"])
app.include_router(verify_otp_router, prefix="/api/forgot_password", tags=["Forgot Password"])
app.include_router(reset_password_router, prefix="/api/forgot_password", tags=["Forgot Password"])

# Access routers
app.include_router(login_router, prefix="/api/access", tags=["Access"])
app.include_router(logout_router, prefix="/api/access", tags=["Access"])

# AI Assistant routers
app.include_router(assistants_router, prefix="/api/ai-assistants", tags=["AI Assistants"])

@app.on_event("startup")
async def startup_event():
    """Connect to database on startup"""
    Database.connect()
    logging.info("Connected to MongoDB")

@app.on_event("shutdown")
async def shutdown_event():
    """Close database connection on shutdown"""
    Database.close()
    logging.info("Closed MongoDB connection")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "running",
        "message": "Convis Labs Registration API",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
