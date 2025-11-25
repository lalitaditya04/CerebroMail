"""
User Service
Handles user authentication and data storage
"""

import sqlite3
import os
from models.user_model import User


class UserService:
    """Service for managing user data"""
    
    def __init__(self, db_path='database/users.db'):
        """Initialize user service with database"""
        self.db_path = db_path
        self._ensure_db_exists()
    
    def _ensure_db_exists(self):
        """Create database and tables if they don't exist"""
        # Create database directory if it doesn't exist
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                name TEXT,
                phone TEXT,
                picture TEXT,
                created_at TEXT NOT NULL,
                last_login TEXT,
                UNIQUE(email)
            )
        ''')
        
        # Create index for faster lookups
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_email ON users(email)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_user_id ON users(user_id)
        ''')
        
        conn.commit()
        conn.close()
    
    def create_or_update_user(self, user_data):
        """
        Create new user or update existing user
        
        Args:
            user_data: Dictionary with user information
            
        Returns:
            User object
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            email = user_data.get('email')
            name = user_data.get('name')
            phone = user_data.get('phone')
            picture = user_data.get('picture')
            user_id = user_data.get('user_id') or email.split('@')[0]
            created_at = user_data.get('created_at')
            
            from datetime import datetime
            last_login = datetime.now().isoformat()
            
            # Try to insert, update if exists
            cursor.execute('''
                INSERT INTO users (user_id, email, name, phone, picture, created_at, last_login)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(email) DO UPDATE SET
                    name = excluded.name,
                    phone = excluded.phone,
                    picture = excluded.picture,
                    last_login = excluded.last_login
            ''', (user_id, email, name, phone, picture, created_at or last_login, last_login))
            
            conn.commit()
            conn.close()
            
            return User(email=email, name=name, phone=phone, picture=picture, user_id=user_id, created_at=created_at or last_login)
            
        except Exception as e:
            print(f"Error creating/updating user: {e}")
            raise
    
    def get_user_by_email(self, email):
        """
        Get user by email
        
        Args:
            email: User email address
            
        Returns:
            User object or None
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
            row = cursor.fetchone()
            
            conn.close()
            
            if row:
                return User(
                    email=row['email'],
                    name=row['name'],
                    phone=row['phone'],
                    picture=row['picture'],
                    user_id=row['user_id'],
                    created_at=row['created_at']
                )
            
            return None
            
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
    
    def get_user_by_id(self, user_id):
        """
        Get user by user_id
        
        Args:
            user_id: User ID
            
        Returns:
            User object or None
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
            row = cursor.fetchone()
            
            conn.close()
            
            if row:
                return User(
                    email=row['email'],
                    name=row['name'],
                    phone=row['phone'],
                    picture=row['picture'],
                    user_id=row['user_id'],
                    created_at=row['created_at']
                )
            
            return None
            
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
    
    def get_all_users(self):
        """
        Get all users
        
        Returns:
            List of User objects
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM users ORDER BY last_login DESC')
            rows = cursor.fetchall()
            
            conn.close()
            
            return [User(
                email=row['email'],
                name=row['name'],
                phone=row['phone'],
                picture=row['picture'],
                user_id=row['user_id'],
                created_at=row['created_at']
            ) for row in rows]
            
        except Exception as e:
            print(f"Error getting users: {e}")
            return []


# Global user service instance
user_service = UserService()
