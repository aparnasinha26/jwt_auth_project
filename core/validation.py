import re
from fastapi import HTTPException, status

class Validator:
    """Server-side validation for user inputs"""
    
    @staticmethod
    def validate_username(username: str) -> None:
        """
        Validate username on server side
        Rules:
        - Length: 3-20 characters
        - Format: alphanumeric and underscore only
        - Not empty or whitespace only
        """
        if not username or not username.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username cannot be empty"
            )
        
        if len(username) < 3:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username must be at least 3 characters long"
            )
        
        if len(username) > 20:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username cannot exceed 20 characters"
            )
        
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username can only contain letters, numbers, and underscore"
            )
        
        # Check for common reserved usernames
        reserved = ['admin', 'root', 'system', 'user', 'test']
        if username.lower() in reserved:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This username is reserved"
            )
    
    @staticmethod
    def validate_password(password: str) -> None:
        """
        Validate password strength on server side
        Rules:
        - Length: 6-100 characters
        - Must contain: uppercase, lowercase, number
        - Not empty or whitespace only
        """
        if not password or not password.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password cannot be empty"
            )
        
        if len(password) < 6:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must be at least 6 characters long"
            )
        
        if len(password) > 100:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password is too long"
            )
        
        if not re.search(r'[A-Z]', password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must contain at least one uppercase letter"
            )
        
        if not re.search(r'[a-z]', password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must contain at least one lowercase letter"
            )
        
        if not re.search(r'[0-9]', password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must contain at least one number"
            )
        
        # Check for common weak passwords
        weak_passwords = ['password', 'password123', '123456', 'qwerty']
        if password.lower() in weak_passwords:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This password is too common. Please choose a stronger password"
            )
    
    @staticmethod
    def validate_signup_input(username: str, password: str) -> None:
        """Validate both username and password for signup"""
        Validator.validate_username(username)
        Validator.validate_password(password)
    
    @staticmethod
    def validate_login_input(username: str, password: str) -> None:
        """Validate login inputs (less strict than signup)"""
        if not username or not username.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username is required"
            )
        
        if not password or not password.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password is required"
            )