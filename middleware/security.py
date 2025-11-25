"""
Security Middleware
Implements rate limiting, security headers, and API protection
"""

from flask import request, jsonify
from functools import wraps
from datetime import datetime, timedelta
import os
from collections import defaultdict
import time


# ==================== RATE LIMITING ====================

class RateLimiter:
    """Simple in-memory rate limiter"""
    
    def __init__(self):
        self.requests = defaultdict(list)
        self.cleanup_interval = 300  # Clean old entries every 5 minutes
        self.last_cleanup = time.time()
    
    def _cleanup_old_entries(self):
        """Remove old request timestamps"""
        current_time = time.time()
        if current_time - self.last_cleanup > self.cleanup_interval:
            for ip in list(self.requests.keys()):
                self.requests[ip] = [
                    timestamp for timestamp in self.requests[ip]
                    if current_time - timestamp < 3600  # Keep last hour
                ]
                if not self.requests[ip]:
                    del self.requests[ip]
            self.last_cleanup = current_time
    
    def is_allowed(self, identifier, limit, window):
        """
        Check if request is allowed
        
        Args:
            identifier: Unique identifier (IP address, user ID, etc.)
            limit: Maximum number of requests
            window: Time window in seconds
        
        Returns:
            Tuple of (allowed: bool, retry_after: int)
        """
        self._cleanup_old_entries()
        
        current_time = time.time()
        
        # Get timestamps for this identifier
        timestamps = self.requests[identifier]
        
        # Remove timestamps outside the window
        timestamps = [ts for ts in timestamps if current_time - ts < window]
        self.requests[identifier] = timestamps
        
        if len(timestamps) >= limit:
            # Calculate retry time
            oldest_in_window = min(timestamps)
            retry_after = int(window - (current_time - oldest_in_window)) + 1
            return False, retry_after
        
        # Add current timestamp
        self.requests[identifier].append(current_time)
        return True, 0


# Global rate limiter instance
rate_limiter = RateLimiter()


def rate_limit(limit=60, window=60, key_func=None):
    """
    Rate limiting decorator
    
    Args:
        limit: Maximum number of requests
        window: Time window in seconds
        key_func: Function to get identifier from request (default: IP address)
    
    Example:
        @rate_limit(limit=10, window=60)  # 10 requests per minute
        def my_endpoint():
            return 'OK'
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get identifier
            if key_func:
                identifier = key_func(request)
            else:
                # Use IP address as default
                identifier = request.remote_addr or 'unknown'
            
            # Check rate limit
            allowed, retry_after = rate_limiter.is_allowed(identifier, limit, window)
            
            if not allowed:
                return jsonify({
                    'error': 'Rate limit exceeded',
                    'message': f'Too many requests. Please try again in {retry_after} seconds.',
                    'retry_after': retry_after
                }), 429
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


# Predefined rate limit decorators for common use cases
def rate_limit_strict(f):
    """Strict rate limit: 10 requests per minute"""
    return rate_limit(limit=10, window=60)(f)


def rate_limit_moderate(f):
    """Moderate rate limit: 30 requests per minute"""
    return rate_limit(limit=30, window=60)(f)


def rate_limit_relaxed(f):
    """Relaxed rate limit: 60 requests per minute"""
    return rate_limit(limit=60, window=60)(f)


def rate_limit_ai(f):
    """AI endpoint rate limit: 5 requests per minute (expensive operations)"""
    return rate_limit(limit=5, window=60)(f)



def add_security_headers(app):
    """
    Add security headers to all responses
    Protects against common web vulnerabilities
    """
    @app.after_request
    def set_security_headers(response):
        # Prevent clickjacking
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        
        # Prevent MIME type sniffing
        response.headers['X-Content-Type-Options'] = 'nosniff'
        
        # Enable browser XSS protection
        response.headers['X-XSS-Protection'] = '1; mode=block'
        
        # Enforce HTTPS (only in production)
        if not app.debug and os.getenv('FLASK_ENV') != 'development':
            response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        
        # Content Security Policy (relaxed for development)
        if app.debug or os.getenv('FLASK_ENV') == 'development':
            response.headers['Content-Security-Policy'] = (
                "default-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.tailwindcss.com; "
                "img-src 'self' data: https:; "
                "connect-src 'self' https://generativelanguage.googleapis.com"
            )
        else:
            # Stricter CSP for production
            response.headers['Content-Security-Policy'] = (
                "default-src 'self'; "
                "script-src 'self' https://cdn.tailwindcss.com 'unsafe-inline'; "
                "style-src 'self' https://cdn.tailwindcss.com 'unsafe-inline'; "
                "img-src 'self' data: https:; "
                "connect-src 'self' https://generativelanguage.googleapis.com"
            )
        
        # Referrer Policy
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Permissions Policy (formerly Feature-Policy)
        response.headers['Permissions-Policy'] = (
            'geolocation=(), microphone=(), camera=()'
        )
        
        return response


def require_api_key(f):
    """
    Decorator to require API key for internal API endpoints
    Useful for protecting admin or sensitive endpoints
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        expected_key = os.getenv('INTERNAL_API_KEY')
        
        # Skip in development if no key is set
        if not expected_key and (os.getenv('FLASK_ENV') == 'development' or os.getenv('DEBUG') == 'true'):
            return f(*args, **kwargs)
        
        if not api_key or api_key != expected_key:
            return jsonify({
                'error': 'Unauthorized',
                'message': 'Invalid or missing API key'
            }), 401
        
        return f(*args, **kwargs)
    return decorated_function


def ip_whitelist(allowed_ips):
    """
    Decorator to restrict access to specific IP addresses
    Useful for admin endpoints in production
    
    Example:
        @ip_whitelist(['127.0.0.1', '192.168.1.100'])
        def admin_endpoint():
            return 'Admin access'
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            client_ip = request.remote_addr
            if client_ip not in allowed_ips:
                return jsonify({
                    'error': 'Forbidden',
                    'message': 'Access denied from your IP address'
                }), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator


# ==================== REQUEST SIZE LIMIT ====================

def limit_content_length(max_length):
    """
    Decorator to limit request body size
    Prevents DoS attacks via large payloads
    
    Args:
        max_length: Maximum size in bytes (e.g., 1024 * 1024 for 1MB)
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            content_length = request.content_length
            if content_length and content_length > max_length:
                return jsonify({
                    'error': 'Payload too large',
                    'message': f'Request body must not exceed {max_length} bytes',
                    'max_size': max_length
                }), 413
            return f(*args, **kwargs)
        return decorated_function
    return decorator
