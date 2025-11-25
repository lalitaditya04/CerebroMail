"""
Error Logging Service
Logs errors to SQLite database with detailed context
"""

import sqlite3
import json
import traceback
from datetime import datetime
from pathlib import Path


class ErrorLogger:
    """Logs errors to database with context"""
    
    def __init__(self, db_path='logs/errors.db'):
        """Initialize error logger with database"""
        self.db_path = db_path
        self._ensure_db_exists()
    
    def _ensure_db_exists(self):
        """Create database and tables if they don't exist"""
        # Create logs directory if it doesn't exist
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create errors table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS errors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                error_code TEXT NOT NULL,
                error_type TEXT NOT NULL,
                message TEXT NOT NULL,
                stacktrace TEXT,
                context TEXT,
                user_id TEXT,
                endpoint TEXT,
                method TEXT,
                ip_address TEXT,
                user_agent TEXT,
                resolved BOOLEAN DEFAULT 0,
                resolution_notes TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create error statistics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS error_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                error_code TEXT NOT NULL,
                count INTEGER DEFAULT 1,
                first_occurrence TEXT NOT NULL,
                last_occurrence TEXT NOT NULL,
                UNIQUE(error_code)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def log_error(self, exception, context=None, user_id=None, endpoint=None, 
                  method=None, ip_address=None, user_agent=None):
        """
        Log an error to the database
        
        Args:
            exception: The exception object
            context: Additional context (dict)
            user_id: User ID if available
            endpoint: API endpoint where error occurred
            method: HTTP method (GET, POST, etc.)
            ip_address: Client IP address
            user_agent: Client user agent
            
        Returns:
            error_id: ID of the logged error
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Extract error details
            error_code = getattr(exception, 'error_code', 'UNKNOWN_ERROR')
            error_type = type(exception).__name__
            message = str(exception)
            stacktrace = traceback.format_exc()
            timestamp = datetime.now().isoformat()
            
            # Serialize context
            context_json = json.dumps(context) if context else None
            
            # Insert error
            cursor.execute('''
                INSERT INTO errors (
                    timestamp, error_code, error_type, message, stacktrace,
                    context, user_id, endpoint, method, ip_address, user_agent
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                timestamp, error_code, error_type, message, stacktrace,
                context_json, user_id, endpoint, method, ip_address, user_agent
            ))
            
            error_id = cursor.lastrowid
            
            # Update error statistics
            cursor.execute('''
                INSERT INTO error_stats (error_code, first_occurrence, last_occurrence)
                VALUES (?, ?, ?)
                ON CONFLICT(error_code) DO UPDATE SET
                    count = count + 1,
                    last_occurrence = ?
            ''', (error_code, timestamp, timestamp, timestamp))
            
            conn.commit()
            conn.close()
            
            return error_id
            
        except Exception as e:
            # Fallback: log to file if database fails
            self._log_to_file(exception, context, e)
            return None
    
    def _log_to_file(self, exception, context, db_error):
        """Fallback logging to file if database fails"""
        try:
            log_file = Path(self.db_path).parent / 'error_fallback.log'
            with open(log_file, 'a') as f:
                f.write(f"\n{'='*80}\n")
                f.write(f"Timestamp: {datetime.now().isoformat()}\n")
                f.write(f"Exception: {exception}\n")
                f.write(f"Context: {context}\n")
                f.write(f"DB Error: {db_error}\n")
                f.write(f"Stacktrace:\n{traceback.format_exc()}\n")
        except:
            # If even file logging fails, just print
            print(f"CRITICAL: Failed to log error: {exception}")
    
    def get_recent_errors(self, limit=50, unresolved_only=False):
        """Get recent errors from database"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            query = 'SELECT * FROM errors'
            if unresolved_only:
                query += ' WHERE resolved = 0'
            query += ' ORDER BY timestamp DESC LIMIT ?'
            
            cursor.execute(query, (limit,))
            errors = [dict(row) for row in cursor.fetchall()]
            
            conn.close()
            return errors
            
        except Exception as e:
            print(f"Error retrieving errors: {e}")
            return []
    
    def get_error_stats(self):
        """Get error statistics"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT error_code, count, first_occurrence, last_occurrence
                FROM error_stats
                ORDER BY count DESC
            ''')
            
            stats = [dict(row) for row in cursor.fetchall()]
            conn.close()
            return stats
            
        except Exception as e:
            print(f"Error retrieving stats: {e}")
            return []
    
    def mark_resolved(self, error_id, resolution_notes=None):
        """Mark an error as resolved"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE errors
                SET resolved = 1, resolution_notes = ?
                WHERE id = ?
            ''', (resolution_notes, error_id))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Error marking resolved: {e}")
            return False


# Global error logger instance
error_logger = ErrorLogger()
