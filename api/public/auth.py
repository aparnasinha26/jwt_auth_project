from fastapi import APIRouter, HTTPException, status
from models.user import UserSignup, UserLogin, TokenResponse, MessageResponse, TokenVerify
from core.security import Security
from core.validation import Validator
from utils.storage import Storage

router = APIRouter()

@router.post("/signup", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def signup(user: UserSignup):
    """
    Register a new user
    
    - **username**: 3-20 characters, alphanumeric and underscore only
    - **password**: Minimum 6 characters, must contain uppercase, lowercase, and number
    
    Validations performed:
    1. Pydantic model validation (automatic)
    2. Custom field validators in UserSignup model
    3. Server-side validation in Validator class
    4. Username uniqueness check
    """
    
    # Server-side validation (defense in depth)
    Validator.validate_signup_input(user.username, user.password)
    
    # Check if user already exists
    if Storage.user_exists(user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    
    # Hash password
    hashed_password = Security.hash_password(user.password)
    
    # Create user
    Storage.create_user(user.username, hashed_password)
    
    return MessageResponse(message="User created successfully")


@router.post("/login", response_model=TokenResponse)
async def login(user: UserLogin):
    """
    Authenticate user and return JWT token
    
    - **username**: User's username
    - **password**: User's password
    
    Returns JWT token valid for 24 hours
    """
    
    # Server-side validation
    Validator.validate_login_input(user.username, user.password)
    
    # Get user from storage
    stored_user = Storage.get_user(user.username)
    
    if not stored_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    # Verify password
    if not Security.verify_password(user.password, stored_user['password']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    # Update last login
    Storage.update_last_login(user.username)
    
    # Generate JWT token
    token = Security.create_access_token(user.username)
    
    return TokenResponse(
        message="Login successful",
        token=token,
        username=user.username
    )


@router.post("/verify-token")
async def verify_token(token_data: TokenVerify):
    """
    Verify if a JWT token is valid
    
    - **token**: JWT token to verify
    
    Returns token validity and username if valid
    """
    
    if not token_data.token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token is required"
        )
    
    payload = Security.verify_token(token_data.token)
    
    if payload:
        return {
            "valid": True,
            "message": "Token is valid",
            "username": payload['username'],
            "expires_at": payload.get('exp')
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is invalid or expired"
        )