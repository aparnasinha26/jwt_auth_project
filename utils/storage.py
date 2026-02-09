import json
import os
from typing import Dict, Optional
from datetime import datetime

USERS_FILE = 'users.json'

class Storage:
    """File-based storage for user data"""
    
    @staticmethod
    def load_users() -> Dict:
        """
        Load all users from storage
        
        Returns:
            Dictionary of users {username: {password, created_at, ...}}
        """
        # Create file if it doesn't exist
        if not os.path.exists(USERS_FILE):
            with open(USERS_FILE, 'w') as f:
                json.dump({}, f)
        
        try:
            with open(USERS_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    
    @staticmethod
    def save_users(users: Dict) -> None:
        """
        Save users to storage
        
        Args:
            users: Dictionary of users to save
        """
        with open(USERS_FILE, 'w') as f:
            json.dump(users, f, indent=2)
    
    @staticmethod
    def user_exists(username: str) -> bool:
        """
        Check if a user exists
        
        Args:
            username: Username to check
            
        Returns:
            True if user exists, False otherwise
        """
        users = Storage.load_users()
        return username in users
    
    @staticmethod
    def get_user(username: str) -> Optional[Dict]:
        """
        Get a specific user's data
        
        Args:
            username: Username to retrieve
            
        Returns:
            User data dict or None if not found
        """
        users = Storage.load_users()
        return users.get(username)
    
    @staticmethod
    def create_user(username: str, hashed_password: str) -> Dict:
        """
        Create a new user
        
        Args:
            username: Username for new user
            hashed_password: Already hashed password
            
        Returns:
            Created user data
        """
        users = Storage.load_users()
        
        user_data = {
            'password': hashed_password,
            'created_at': datetime.utcnow().isoformat(),
            'last_login': None
        }
        
        users[username] = user_data
        Storage.save_users(users)
        
        return user_data
    
    @staticmethod
    def update_last_login(username: str) -> None:
        """
        Update user's last login timestamp
        
        Args:
            username: Username to update
        """
        users = Storage.load_users()
        
        if username in users:
            users[username]['last_login'] = datetime.utcnow().isoformat()
            Storage.save_users(users)