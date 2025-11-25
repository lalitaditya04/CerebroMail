"""
Gmail Routes
Handles Gmail OAuth 2.0 authentication and email operations
Single Responsibility: Gmail integration
"""

from flask import Blueprint, request, jsonify, redirect, session, url_for
import secrets
from services.gmail_service import GmailService
from services.user_service import user_service
from utils.error_handler import handle_errors
from utils.exceptions import ValidationError, AuthenticationError

bp = Blueprint('gmail', __name__, url_prefix='/api/gmail')

# Store Gmail services per user session
# In production, use Redis or database for session storage
gmail_services = {}


@bp.route('/auth/status', methods=['GET'])
@handle_errors
def auth_status():
    """Check Gmail authentication status and return user info"""
    # Get user from session
    user_email = session.get('gmail_user_email')
    user_id = session.get('gmail_user_id')
    
    # Check if user has active service in memory
    if user_id and user_id in gmail_services:
        gmail_service = gmail_services[user_id]
        if gmail_service.is_authenticated():
            return jsonify({
                'authenticated': True,
                'email': user_email,
                'name': session.get('gmail_user_name'),
                'picture': session.get('gmail_user_picture'),
                'user_id': user_id
            })
    
    return jsonify({'authenticated': False})


@bp.route('/auth/start', methods=['POST'])
@handle_errors
def start_auth():
    """
    Start Gmail OAuth 2.0 flow - works for any Google user
    Returns authorization URL for user to visit
    """
    # Generate redirect URI
    redirect_uri = request.json.get('redirect_uri', 'http://localhost:5000/api/gmail/auth/callback')
    
    # Create temporary service for auth flow (session-only, no persistence)
    temp_service = GmailService('temp', use_persistent_tokens=False)
    
    # Generate authorization URL
    auth_url, state = temp_service.get_authorization_url(redirect_uri)
    
    # Store state in session for security verification
    session['oauth_state'] = state
    
    return jsonify({
        'success': True,
        'auth_url': auth_url,
        'message': 'Please visit the authorization URL to grant access'
    })


@bp.route('/auth/callback', methods=['GET'])
def auth_callback():
    """
    OAuth 2.0 callback endpoint
    Handles the redirect after user authorizes
    """
    try:
        # Get authorization code and state
        code = request.args.get('code')
        state = request.args.get('state')
        
        if not code:
            return jsonify({'error': 'No authorization code received'}), 400
        
        # Verify state to prevent CSRF attacks
        if state != session.get('oauth_state'):
            return jsonify({'error': 'Invalid state parameter'}), 400
        
        # Create temporary service to complete auth (session-only, no persistence)
        temp_service = GmailService('temp', use_persistent_tokens=False)
        redirect_uri = url_for('gmail.auth_callback', _external=True)
        success = temp_service.authenticate_with_code(code, redirect_uri, state)
        
        if success:
            # Get user info from Google
            user_info = temp_service.get_user_info()
            if user_info:
                user_email = user_info['email']
                user_id = user_info['id']
                
                # Store this service in memory (session-based only)
                gmail_services[user_id] = temp_service
                
                # Store user in database
                try:
                    user_service.create_or_update_user({
                        'email': user_email,
                        'name': user_info.get('name'),
                        'phone': user_info.get('phone'),
                        'picture': user_info.get('picture'),
                        'user_id': user_id
                    })
                except Exception as db_error:
                    print(f"Error storing user in database: {db_error}")
                    # Continue even if DB storage fails
                
                # Store user info in session
                session.permanent = True  # Enable session timeout
                session['gmail_user_email'] = user_email
                session['gmail_user_id'] = user_id
                session['gmail_user_name'] = user_info.get('name')
                session['gmail_user_picture'] = user_info.get('picture')
                
                # Redirect to main app with success message
                return redirect('/?gmail_auth=success')
        
        return redirect('/?gmail_auth=failed')
            
    except Exception as e:
        print(f"OAuth callback error: {e}")
        return redirect('/?gmail_auth=error')


@bp.route('/emails/fetch', methods=['POST'])
def fetch_emails():
    """
    Fetch emails from Gmail - works for any authenticated user
    Supports filtering with query parameter
    """
    try:
        # Get user from session
        user_id = session.get('gmail_user_id')
        user_email = session.get('gmail_user_email')
        
        print(f"📧 Fetch request - User ID: {user_id}, Email: {user_email}")
        print(f"Session keys: {list(session.keys())}")
        
        if not user_id:
            print("❌ No user_id in session")
            return jsonify({
                'success': False,
                'error': 'Not authenticated. Please sign in with Google.'
            }), 401
        
        # Get or create Gmail service for this user
        if user_id not in gmail_services:
            print(f"Creating new Gmail service for user: {user_id}")
            gmail_services[user_id] = GmailService(user_id, use_persistent_tokens=True)
        
        gmail_service = gmail_services[user_id]
        
        # Load credentials for this user
        if not gmail_service.is_authenticated():
            print(f"Loading saved credentials for user: {user_id}")
            if not gmail_service.load_saved_credentials():
                print("❌ Failed to load credentials")
                return jsonify({
                    'success': False,
                    'error': 'Session expired. Please sign in again.'
                }), 401
        
        data = request.json or {}
        max_results = data.get('max_results', 50)
        query = data.get('query', '')  # e.g., 'is:unread', 'from:example@email.com'
        
        print(f"Fetching {max_results} emails with query: '{query}'")
        
        # Fetch emails
        emails = gmail_service.fetch_emails(max_results=max_results, query=query)
        
        print(f"✅ Fetched {len(emails)} emails")
        
        # Return user info along with emails
        return jsonify({
            'success': True,
            'emails': emails,
            'count': len(emails),
            'user': {
                'email': user_email,
                'name': session.get('gmail_user_name'),
                'picture': session.get('gmail_user_picture')
            }
        })
        
    except Exception as e:
        print(f"❌ Error fetching emails: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('/emails/send', methods=['POST'])
def send_email():
    """Send email via Gmail - works for any authenticated user"""
    try:
        user_id = session.get('gmail_user_id')
        if not user_id or user_id not in gmail_services:
            return jsonify({
                'success': False,
                'error': 'Not authenticated'
            }), 401
        
        gmail_service = gmail_services[user_id]
        
        data = request.json
        to = data.get('to')
        subject = data.get('subject')
        body = data.get('body')
        
        if not all([to, subject, body]):
            return jsonify({
                'success': False,
                'error': 'Missing required fields: to, subject, body'
            }), 400
        
        success = gmail_service.send_email(to, subject, body)
        
        return jsonify({
            'success': success,
            'message': 'Email sent successfully' if success else 'Failed to send email'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('/emails/mark-read/<gmail_id>', methods=['POST'])
def mark_email_read(gmail_id):
    """Mark email as read in Gmail"""
    try:
        user_id = session.get('gmail_user_id')
        if not user_id or user_id not in gmail_services:
            return jsonify({'success': False, 'error': 'Not authenticated'}), 401
        
        gmail_service = gmail_services[user_id]
        success = gmail_service.mark_as_read(gmail_id)
        return jsonify({'success': success})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@bp.route('/auth/logout', methods=['POST'])
def logout():
    """Logout and clear Gmail credentials"""
    try:
        user_id = session.get('gmail_user_id')
        
        # Clear user's Gmail service and delete token
        if user_id and user_id in gmail_services:
            gmail_services[user_id].logout()
            del gmail_services[user_id]
        
        # Clear all session data
        session.clear()
        
        return jsonify({
            'success': True,
            'message': 'Disconnected successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
