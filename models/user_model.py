"""
User Model
Stores authenticated user information
"""

from datetime import datetime


class User:
    """User model for authenticated users"""
    
    def __init__(self, email, name=None, phone=None, picture=None, user_id=None, created_at=None):
        self.email = email
        self.name = name
        self.phone = phone
        self.picture = picture
        self.user_id = user_id or email.split('@')[0]
        self.created_at = created_at or datetime.now().isoformat()
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'email': self.email,
            'name': self.name,
            'phone': self.phone,
            'picture': self.picture,
            'user_id': self.user_id,
            'created_at': self.created_at
        }
    
    @staticmethod
    def from_dict(data):
        """Create user from dictionary"""
        return User(
            email=data.get('email'),
            name=data.get('name'),
            phone=data.get('phone'),
            picture=data.get('picture'),
            user_id=data.get('user_id'),
            created_at=data.get('created_at')
        )
