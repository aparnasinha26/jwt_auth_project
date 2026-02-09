from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.public import auth as public_auth
from api.private import user as private_user
from ui import routes as ui_routes

# Create FastAPI application with docs disabled
app = FastAPI(
    title="Authentication System",
    description="Secure authentication with JWT tokens",
    version="1.0.0"
)

# CORS middleware (if needed for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include UI routes (HTML pages)
app.include_router(ui_routes.router)

# Include public API routes
app.include_router(
    public_auth.router,
    prefix="/api/public"
)

# Include private API routes
app.include_router(
    private_user.router,
    prefix="/api/private"
)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Server is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)