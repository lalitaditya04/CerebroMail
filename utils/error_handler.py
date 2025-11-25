"""
Error Handler Middleware
Global error handler for Flask application
"""

from flask import jsonify, request, session
from functools import wraps
import traceback
from utils.exceptions import (
    CerbroMailException, AuthenticationError, GmailAPIError,
    AIServiceError, ValidationError, ConfigurationError,
    DatabaseError, RateLimitError, SessionExpiredError
)
from utils.error_logger import error_logger


def handle_errors(f):
    """
    Decorator for route error handling
    Catches exceptions and returns proper JSON responses
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except CerbroMailException as e:
            return handle_cerbromail_exception(e)
        except Exception as e:
            return handle_generic_exception(e)
    return decorated_function


def handle_cerbromail_exception(exception):
    """Handle custom CerbroMail exceptions"""
    # Extract request context
    context = {
        'endpoint': request.endpoint,
        'method': request.method,
        'args': dict(request.args),
        'form': dict(request.form) if request.form else None,
        'json': request.get_json(silent=True),
        'details': exception.details
    }
    
    # Get user info from session
    user_id = session.get('gmail_user_id')
    
    # Log error to database
    error_id = error_logger.log_error(
        exception=exception,
        context=context,
        user_id=user_id,
        endpoint=request.endpoint,
        method=request.method,
        ip_address=request.remote_addr,
        user_agent=request.headers.get('User-Agent')
    )
    
    # Determine HTTP status code based on exception type
    status_code = get_status_code(exception)
    
    # Return user-friendly error response
    response = {
        'success': False,
        'error': {
            'code': exception.error_code,
            'message': exception.message,
            'type': type(exception).__name__
        }
    }
    
    # Add error ID for support reference
    if error_id:
        response['error']['reference_id'] = error_id
    
    # Add details if available (but sanitize sensitive info)
    if exception.details:
        response['error']['details'] = sanitize_details(exception.details)
    
    return jsonify(response), status_code


def handle_generic_exception(exception):
    """Handle unexpected exceptions"""
    # Extract request context
    context = {
        'endpoint': request.endpoint,
        'method': request.method,
        'args': dict(request.args),
        'form': dict(request.form) if request.form else None,
        'json': request.get_json(silent=True),
    }
    
    # Get user info from session
    user_id = session.get('gmail_user_id')
    
    # Log error to database
    error_id = error_logger.log_error(
        exception=exception,
        context=context,
        user_id=user_id,
        endpoint=request.endpoint,
        method=request.method,
        ip_address=request.remote_addr,
        user_agent=request.headers.get('User-Agent')
    )
    
    # Return generic error response (don't expose internal details)
    response = {
        'success': False,
        'error': {
            'code': 'INTERNAL_ERROR',
            'message': 'An unexpected error occurred. Please try again later.',
            'type': 'InternalServerError'
        }
    }
    
    # Add error ID for support reference
    if error_id:
        response['error']['reference_id'] = error_id
        response['error']['support_message'] = f'Please provide reference ID {error_id} when contacting support.'
    
    return jsonify(response), 500


def get_status_code(exception):
    """Determine HTTP status code based on exception type"""
    status_map = {
        AuthenticationError: 401,
        SessionExpiredError: 401,
        ValidationError: 400,
        ConfigurationError: 500,
        GmailAPIError: 503,
        AIServiceError: 503,
        DatabaseError: 500,
        RateLimitError: 429,
    }
    return status_map.get(type(exception), 500)


def sanitize_details(details):
    """Remove sensitive information from error details"""
    sensitive_keys = [
        'password', 'token', 'api_key', 'secret', 'authorization',
        'credentials', 'private_key', 'session_id'
    ]
    
    if not isinstance(details, dict):
        return details
    
    sanitized = {}
    for key, value in details.items():
        key_lower = key.lower()
        if any(sensitive in key_lower for sensitive in sensitive_keys):
            sanitized[key] = '[REDACTED]'
        elif isinstance(value, dict):
            sanitized[key] = sanitize_details(value)
        else:
            sanitized[key] = value
    
    return sanitized


def register_error_handlers(app):
    """Register global error handlers for Flask app"""
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors"""
        return jsonify({
            'success': False,
            'error': {
                'code': 'NOT_FOUND',
                'message': 'The requested resource was not found',
                'type': 'NotFound'
            }
        }), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        """Handle 405 errors"""
        return jsonify({
            'success': False,
            'error': {
                'code': 'METHOD_NOT_ALLOWED',
                'message': f'Method {request.method} not allowed for this endpoint',
                'type': 'MethodNotAllowed'
            }
        }), 405
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors"""
        # Log the error
        error_id = error_logger.log_error(
            exception=error,
            context={'endpoint': request.endpoint, 'method': request.method},
            user_id=session.get('gmail_user_id'),
            endpoint=request.endpoint,
            method=request.method,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent')
        )
        
        return jsonify({
            'success': False,
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'An internal server error occurred',
                'type': 'InternalServerError',
                'reference_id': error_id if error_id else None
            }
        }), 500
    
    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        """Catch-all for unexpected errors"""
        return handle_generic_exception(error)
