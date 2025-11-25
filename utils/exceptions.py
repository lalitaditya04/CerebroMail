"""
Custom Exception Classes
Defines specific exceptions for different error scenarios
"""

class CerbroMailException(Exception):
    """Base exception for all CerbroMail errors"""
    def __init__(self, message, error_code=None, details=None):
        self.message = message
        self.error_code = error_code or 'UNKNOWN_ERROR'
        self.details = details or {}
        super().__init__(self.message)


class AuthenticationError(CerbroMailException):
    """Raised when authentication fails"""
    def __init__(self, message="Authentication failed", details=None):
        super().__init__(message, 'AUTH_ERROR', details)


class GmailAPIError(CerbroMailException):
    """Raised when Gmail API operations fail"""
    def __init__(self, message="Gmail API error", details=None):
        super().__init__(message, 'GMAIL_API_ERROR', details)


class AIServiceError(CerbroMailException):
    """Raised when AI service (Gemini) fails"""
    def __init__(self, message="AI service error", details=None):
        super().__init__(message, 'AI_SERVICE_ERROR', details)


class ValidationError(CerbroMailException):
    """Raised when input validation fails"""
    def __init__(self, message="Validation error", details=None):
        super().__init__(message, 'VALIDATION_ERROR', details)


class ConfigurationError(CerbroMailException):
    """Raised when configuration is missing or invalid"""
    def __init__(self, message="Configuration error", details=None):
        super().__init__(message, 'CONFIG_ERROR', details)


class DatabaseError(CerbroMailException):
    """Raised when database operations fail"""
    def __init__(self, message="Database error", details=None):
        super().__init__(message, 'DATABASE_ERROR', details)


class RateLimitError(CerbroMailException):
    """Raised when API rate limits are exceeded"""
    def __init__(self, message="Rate limit exceeded", details=None):
        super().__init__(message, 'RATE_LIMIT_ERROR', details)


class SessionExpiredError(CerbroMailException):
    """Raised when user session expires"""
    def __init__(self, message="Session expired", details=None):
        super().__init__(message, 'SESSION_EXPIRED', details)
