from fastapi import APIRouter, Depends
from core.dependencies import get_current_user
from models.user import UserResponse
from utils.storage import Storage

router = APIRouter()

@router.get("/profile", response_model=UserResponse)
async def get_profile(current_user: dict = Depends(get_current_user)):
    """
    Get current user's profile
    
    Requires valid JWT token in Authorization header:
    Authorization: Bearer <token>
    
    Returns user information
    """
    username = current_user['username']
    user_data = Storage.get_user(username)
    
    if not user_data:
        # This shouldn't happen if token is valid, but safety check
        return UserResponse(
            username=username,
            created_at="Unknown"
        )
    
    return UserResponse(
        username=username,
        created_at=user_data.get('created_at', 'Unknown')
    )