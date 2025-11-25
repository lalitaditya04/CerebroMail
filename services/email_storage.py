"""
Email Storage Service
Handles email data persistence and category storage
"""

import sqlite3
import json
import os
from datetime import datetime


class EmailStorageService:
    """Service for storing and retrieving email data"""
    
    def __init__(self, db_path='database/emails.db'):
        """Initialize email storage service"""
        self.db_path = db_path
        self._ensure_db_exists()
    
    def _ensure_db_exists(self):
        """Create database and tables if they don't exist"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create emails table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS emails (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                sender TEXT NOT NULL,
                subject TEXT NOT NULL,
                body TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                is_read BOOLEAN DEFAULT 0,
                category TEXT DEFAULT 'Unprocessed',
                action_items TEXT,
                draft_reply TEXT,
                summary TEXT,
                custom_analysis TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')
        
        # Create indexes
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_id ON emails(user_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_category ON emails(category)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON emails(timestamp)')
        
        # Create email categories table (for dynamic categories)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS email_categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_name TEXT UNIQUE NOT NULL,
                description TEXT,
                color TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Insert default categories if not exist
        default_categories = [
            ('Important', 'High-priority emails', '#EF4444'),
            ('Newsletter', 'Newsletters and subscriptions', '#3B82F6'),
            ('Spam', 'Unwanted emails', '#6B7280'),
            ('To-Do', 'Emails with action items', '#F59E0B'),
            ('Project', 'Project-related emails', '#8B5CF6'),
            ('Unprocessed', 'Not yet categorized', '#9CA3AF')
        ]
        
        for cat_name, desc, color in default_categories:
            cursor.execute('''
                INSERT OR IGNORE INTO email_categories (category_name, description, color)
                VALUES (?, ?, ?)
            ''', (cat_name, desc, color))
        
        conn.commit()
        conn.close()
    
    def save_email(self, email_data, user_id):
        """
        Save or update an email in the database
        
        Args:
            email_data: Email dictionary
            user_id: User ID who owns this email
            
        Returns:
            True if successful
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Serialize complex fields
            action_items = json.dumps(email_data.get('actionItems', []))
            custom_analysis = json.dumps(email_data.get('customAnalysis', {}))
            
            cursor.execute('''
                INSERT OR REPLACE INTO emails 
                (id, user_id, sender, subject, body, timestamp, is_read, category, 
                 action_items, draft_reply, summary, custom_analysis, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                email_data['id'],
                user_id,
                email_data['sender'],
                email_data['subject'],
                email_data['body'],
                email_data['timestamp'],
                email_data.get('isRead', False),
                email_data.get('category', 'Unprocessed'),
                action_items,
                email_data.get('draftReply'),
                email_data.get('summary'),
                custom_analysis,
                datetime.now().isoformat()
            ))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Error saving email: {e}")
            return False
    
    def get_email(self, email_id, user_id):
        """Get a single email by ID"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM emails 
                WHERE id = ? AND user_id = ?
            ''', (email_id, user_id))
            
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return self._row_to_dict(row)
            return None
            
        except Exception as e:
            print(f"Error getting email: {e}")
            return None
    
    def get_user_emails(self, user_id, category=None, limit=100):
        """
        Get all emails for a user
        
        Args:
            user_id: User ID
            category: Optional category filter
            limit: Maximum number of emails to return
            
        Returns:
            List of email dictionaries
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            if category:
                cursor.execute('''
                    SELECT * FROM emails 
                    WHERE user_id = ? AND category = ?
                    ORDER BY timestamp DESC
                    LIMIT ?
                ''', (user_id, category, limit))
            else:
                cursor.execute('''
                    SELECT * FROM emails 
                    WHERE user_id = ?
                    ORDER BY timestamp DESC
                    LIMIT ?
                ''', (user_id, limit))
            
            rows = cursor.fetchall()
            conn.close()
            
            return [self._row_to_dict(row) for row in rows]
            
        except Exception as e:
            print(f"Error getting user emails: {e}")
            return []
    
    def update_email_category(self, email_id, user_id, category):
        """Update email category"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE emails 
                SET category = ?, updated_at = ?
                WHERE id = ? AND user_id = ?
            ''', (category, datetime.now().isoformat(), email_id, user_id))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Error updating category: {e}")
            return False
    
    def add_category(self, category_name, description=None, color=None):
        """Add a new category dynamically"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR IGNORE INTO email_categories (category_name, description, color)
                VALUES (?, ?, ?)
            ''', (category_name, description, color or '#6B7280'))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Error adding category: {e}")
            return False
    
    def get_all_categories(self):
        """Get all available categories"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM email_categories ORDER BY category_name')
            rows = cursor.fetchall()
            conn.close()
            
            return [dict(row) for row in rows]
            
        except Exception as e:
            print(f"Error getting categories: {e}")
            return []
    
    def _row_to_dict(self, row):
        """Convert database row to email dictionary"""
        return {
            'id': row['id'],
            'sender': row['sender'],
            'subject': row['subject'],
            'body': row['body'],
            'timestamp': row['timestamp'],
            'isRead': bool(row['is_read']),
            'category': row['category'],
            'actionItems': json.loads(row['action_items']) if row['action_items'] else [],
            'draftReply': row['draft_reply'],
            'summary': row['summary'],
            'customAnalysis': json.loads(row['custom_analysis']) if row['custom_analysis'] else {}
        }


# Global email storage instance
email_storage = EmailStorageService()
