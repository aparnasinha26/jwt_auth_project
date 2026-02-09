from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from core.security import Security

# Security scheme for token authentication
security_scheme = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme)
) -> dict:
    """
    Dependency to get current authenticated user from JWT token
    
    This dependency:
    1. Extracts token from Authorization header
    2. Verifies token validity
    3. Returns user payload if valid
    4. Raises 401 error if invalid
    
    Usage:
        @app.get("/protected")
        async def protected_route(user: dict = Depends(get_current_user)):
            return {"user": user["username"]}
    """
    token = credentials.credentials
    
    # Verify token
    payload = Security.verify_token(token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Additional check: ensure token type is 'access'
    if payload.get('type') != 'access':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return payload

async def get_optional_user(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme)
) -> dict | None:
    """
    Optional authentication - returns user if token is valid, None otherwise
    Doesn't raise error if token is invalid
    """
    try:
        token = credentials.credentials
        payload = Security.verify_token(token)
        return payload
    except Exception:
        return None