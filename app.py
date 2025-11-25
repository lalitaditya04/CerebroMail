"""
CerbroMail - AI Email Intelligence
SOLID principles implementation with modular architecture
"""

from flask import Flask, render_template, session, redirect, url_for
from flask_cors import CORS
from datetime import timedelta
import os
from dotenv import load_dotenv
import secrets

# Load environment variables
load_dotenv()

# Import routes
from routes import email_routes, ai_routes, config_routes, gmail_routes, admin_routes, chat_routes

# Import error handling
from utils.error_handler import register_error_handlers

# Import security middleware
from middleware.security import add_security_headers

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Session configuration
app.secret_key = os.getenv('SECRET_KEY', secrets.token_hex(32))
app.config.update(
    PERMANENT_SESSION_LIFETIME=timedelta(minutes=45),  # 45-minute session
    SESSION_PERMANENT=False,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    SESSION_COOKIE_SECURE=False, #true during production cause uses HTTPS
    SESSION_REFRESH_EACH_REQUEST=True  # Refresh session on each request
)

# Register error handlers (MUST be done before blueprints)
register_error_handlers(app)

# Add security headers to all responses
add_security_headers(app)

# Register blueprints (modular routes)
app.register_blueprint(email_routes.bp)
app.register_blueprint(ai_routes.bp)
app.register_blueprint(config_routes.bp)
app.register_blueprint(gmail_routes.bp)
app.register_blueprint(admin_routes.bp)
app.register_blueprint(chat_routes.bp)


@app.route('/')
def index():
    """Serve the main application page"""
    return render_template('index.html')


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    app.run(debug=debug, host='0.0.0.0', port=port)
