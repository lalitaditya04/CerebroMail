"""
Database Manager
Handles SQLite database operations for the application
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
import os


class DatabaseManager:
    """Manages SQLite database operations"""
    
    def __init__(self, db_path='data/cerebro_mail.db'):
        """Initialize database connection"""
        self.db_path = db_path
        
        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # Initialize database
        self.init_database()
    
    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        return conn
    
    def init_database(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Chat history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email_id TEXT NOT NULL,
                user_email TEXT,
                messages TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(email_id, user_email)
            )
        ''')
        
        # Email drafts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS email_drafts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email_id TEXT NOT NULL,
                draft_id TEXT NOT NULL,
                title TEXT,
                content TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(email_id, draft_id)
            )
        ''')
        
        # User preferences table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_email TEXT UNIQUE,
                prompts TEXT,
                settings TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Email metadata table (for processed emails)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS email_metadata (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email_id TEXT UNIQUE NOT NULL,
                user_email TEXT,
                category TEXT,
                action_items TEXT,
                summary TEXT,
                processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        print(f"Database initialized at: {self.db_path}")
    
    # ==================== CHAT HISTORY ====================
    
    def save_chat(self, email_id, messages, user_email=None):
        """Save chat history"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        messages_json = json.dumps(messages)
        
        cursor.execute('''
            INSERT INTO chat_history (email_id, user_email, messages, updated_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(email_id, user_email) 
            DO UPDATE SET messages=?, updated_at=CURRENT_TIMESTAMP
        ''', (email_id, user_email, messages_json, messages_json))
        
        conn.commit()
        conn.close()
        return True
    
    def load_chat(self, email_id, user_email=None):
        """Load chat history"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT messages, updated_at FROM chat_history 
            WHERE email_id=? AND user_email IS ?
        ''', (email_id, user_email))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'messages': json.loads(row['messages']),
                'last_updated': row['updated_at']
            }
        return None
    
    def delete_chat(self, email_id, user_email=None):
        """Delete chat history"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM chat_history 
            WHERE email_id=? AND user_email IS ?
        ''', (email_id, user_email))
        
        deleted = cursor.rowcount
        conn.commit()
        conn.close()
        return deleted > 0
    
    def list_chats(self, user_email=None):
        """List all chats for a user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if user_email:
            cursor.execute('''
                SELECT email_id, updated_at, 
                       json_array_length(messages) as message_count
                FROM chat_history 
                WHERE user_email=?
                ORDER BY updated_at DESC
            ''', (user_email,))
        else:
            cursor.execute('''
                SELECT email_id, updated_at,
                       json_array_length(messages) as message_count
                FROM chat_history 
                WHERE user_email IS NULL
                ORDER BY updated_at DESC
            ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        return [{
            'email_id': row['email_id'],
            'last_updated': row['updated_at'],
            'message_count': row['message_count']
        } for row in rows]
    
    # ==================== EMAIL DRAFTS ====================
    
    def save_draft(self, email_id, draft_id, title, content):
        """Save email draft"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO email_drafts (email_id, draft_id, title, content, updated_at)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(email_id, draft_id)
            DO UPDATE SET title=?, content=?, updated_at=CURRENT_TIMESTAMP
        ''', (email_id, draft_id, title, content, title, content))
        
        conn.commit()
        conn.close()
        return True
    
    def load_drafts(self, email_id):
        """Load all drafts for an email"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT draft_id, title, content, created_at, updated_at
            FROM email_drafts 
            WHERE email_id=?
            ORDER BY updated_at DESC
        ''', (email_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [{
            'id': row['draft_id'],
            'title': row['title'],
            'content': row['content'],
            'timestamp': row['updated_at']
        } for row in rows]
    
    def delete_draft(self, email_id, draft_id):
        """Delete a draft"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM email_drafts 
            WHERE email_id=? AND draft_id=?
        ''', (email_id, draft_id))
        
        deleted = cursor.rowcount
        conn.commit()
        conn.close()
        return deleted > 0
    
    # ==================== EMAIL METADATA ====================
    
    def save_email_metadata(self, email_id, category=None, action_items=None, 
                           summary=None, user_email=None):
        """Save email processing metadata"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        action_items_json = json.dumps(action_items) if action_items else None
        
        cursor.execute('''
            INSERT INTO email_metadata (email_id, user_email, category, 
                                       action_items, summary)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(email_id)
            DO UPDATE SET category=?, action_items=?, summary=?, 
                         processed_at=CURRENT_TIMESTAMP
        ''', (email_id, user_email, category, action_items_json, summary,
              category, action_items_json, summary))
        
        conn.commit()
        conn.close()
        return True
    
    def load_email_metadata(self, email_id):
        """Load email metadata"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT category, action_items, summary, processed_at
            FROM email_metadata 
            WHERE email_id=?
        ''', (email_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'category': row['category'],
                'action_items': json.loads(row['action_items']) if row['action_items'] else None,
                'summary': row['summary'],
                'processed_at': row['processed_at']
            }
        return None
    
    # ==================== CLEANUP ====================
    
    def cleanup_old_data(self, days=30):
        """Delete data older than specified days"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM chat_history 
            WHERE updated_at < datetime('now', '-' || ? || ' days')
        ''', (days,))
        chats_deleted = cursor.rowcount
        
        cursor.execute('''
            DELETE FROM email_drafts 
            WHERE updated_at < datetime('now', '-' || ? || ' days')
        ''', (days,))
        drafts_deleted = cursor.rowcount
        
        conn.commit()
        conn.close()
        
        return {
            'chats_deleted': chats_deleted,
            'drafts_deleted': drafts_deleted
        }
