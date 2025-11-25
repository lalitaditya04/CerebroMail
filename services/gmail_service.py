"""
Gmail Integration Service
Secure OAuth 2.0 authentication for Gmail API access
"""

import os
import json
import base64
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from utils.exceptions import (
    GmailAPIError, AuthenticationError, 
    ConfigurationError, ValidationError
)


class GmailService:
    """Secure Gmail API service with OAuth 2.0"""
    
    # OAuth 2.0 scopes - using readonly to minimize security risk
    SCOPES = [
        'https://www.googleapis.com/auth/gmail.readonly',
        'https://www.googleapis.com/auth/gmail.send',
        'https://www.googleapis.com/auth/userinfo.profile',
        'https://www.googleapis.com/auth/userinfo.email',
        'openid'
    ]
    
    def __init__(self, user_id=None, use_persistent_tokens=False):
        """Initialize Gmail service
        
        Args:
            user_id: User identifier
            use_persistent_tokens: If True, saves tokens to disk. If False, session-only (default: False)
        """
        self.credentials = None
        self.service = None
        self.user_id = user_id or 'default'
        self.use_persistent_tokens = use_persistent_tokens
        
        # Store tokens per user in tokens directory (only if persistence is enabled)
        self.token_file = f'tokens/token_{self.user_id}.json' if use_persistent_tokens else None
        self.credentials_file = 'credentials.json'
        
        # Try to load credentials from environment variable first (for Render)
        self.credentials_data = self._load_credentials()
        
        # Create tokens directory if it doesn't exist and persistence is enabled
        if use_persistent_tokens:
            import os
            os.makedirs('tokens', exist_ok=True)
    
    def _load_credentials(self):
        """Load OAuth credentials from environment variable or file
        
        Returns:
            dict: Credentials data
        """
        # First try environment variable (Render deployment)
        env_creds = os.getenv('GOOGLE_OAUTH_CREDENTIALS')
        if env_creds:
            try:
                return json.loads(env_creds)
            except json.JSONDecodeError:
                raise ConfigurationError(
                    "Invalid GOOGLE_OAUTH_CREDENTIALS format in environment variable",
                    details={'hint': 'Must be valid JSON string'}
                )
        
        # Fall back to credentials.json file (local development)
        if os.path.exists(self.credentials_file):
            try:
                with open(self.credentials_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                raise ConfigurationError(
                    f"Invalid JSON in {self.credentials_file}",
                    details={'file': self.credentials_file}
                )
        
        # No credentials found
        raise ConfigurationError(
            "Gmail OAuth credentials not found. Set GOOGLE_OAUTH_CREDENTIALS environment variable or add credentials.json file",
            details={
                'env_var': 'GOOGLE_OAUTH_CREDENTIALS',
                'file': self.credentials_file,
                'hint': 'Get credentials from Google Cloud Console'
            }
        )
    
    def get_authorization_url(self, redirect_uri):
        """
        Generate OAuth 2.0 authorization URL
        
        Args:
            redirect_uri: URL to redirect after authorization
            
        Returns:
            Tuple of (authorization_url, state)
        """
        try:
            # Use credentials data from memory (loaded from env or file)
            flow = Flow.from_client_config(
                self.credentials_data,
                scopes=self.SCOPES,
                redirect_uri=redirect_uri
            )
            
            authorization_url, state = flow.authorization_url(
                access_type='offline',
                include_granted_scopes='true',
                prompt='consent'
            )
            
            return authorization_url, state
            
        except Exception as e:
            raise ConfigurationError(
                f"Failed to generate authorization URL: {str(e)}",
                details={'error': str(e), 'hint': 'Check GOOGLE_OAUTH_CREDENTIALS or credentials.json'}
            )
    
    def authenticate_with_code(self, code, redirect_uri, state):
        """
        Complete OAuth 2.0 flow with authorization code
        
        Args:
            code: Authorization code from OAuth callback
            redirect_uri: Redirect URI used in authorization
            state: State parameter from authorization
            
        Returns:
            True if successful
        """
        try:
            # Use credentials data from memory (loaded from env or file)
            flow = Flow.from_client_config(
                self.credentials_data,
                scopes=self.SCOPES,
                redirect_uri=redirect_uri,
                state=state
            )
            
            flow.fetch_token(code=code)
            self.credentials = flow.credentials
            
            # Save credentials only if persistence is enabled
            if self.use_persistent_tokens:
                self._save_credentials()
            
            # Build service
            self.service = build('gmail', 'v1', credentials=self.credentials)
            
            return True
            
        except Exception as e:
            raise AuthenticationError(
                f"Failed to complete authentication: {str(e)}",
                details={'error': str(e), 'user_id': self.user_id}
            )
    
    def load_saved_credentials(self):
        """
        Load previously saved credentials
        
        Returns:
            True if credentials loaded and valid
        """
        # Don't load from disk if persistence is disabled
        if not self.use_persistent_tokens:
            return False
            
        if not self.token_file or not os.path.exists(self.token_file):
            return False
        
        try:
            self.credentials = Credentials.from_authorized_user_file(
                self.token_file,
                self.SCOPES
            )
            
            # Refresh if expired
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                self.credentials.refresh(Request())
                self._save_credentials()
            
            if self.credentials and self.credentials.valid:
                self.service = build('gmail', 'v1', credentials=self.credentials)
                return True
            
            return False
            
        except FileNotFoundError:
            # Not an error - just no saved credentials
            return False
        except Exception as e:
            raise AuthenticationError(
                f"Failed to load saved credentials: {str(e)}",
                details={'error': str(e), 'token_file': self.token_file}
            )
    
    def _save_credentials(self):
        """Save credentials to file (only if persistence is enabled)"""
        if self.use_persistent_tokens and self.token_file:
            with open(self.token_file, 'w') as token:
                token.write(self.credentials.to_json())
    
    def is_authenticated(self):
        """Check if service is authenticated"""
        return self.service is not None and self.credentials and self.credentials.valid
    
    def get_user_email(self):
        """Get authenticated user's email address"""
        if not self.is_authenticated():
            return None
        
        try:
            profile = self.service.users().getProfile(userId='me').execute()
            return profile.get('emailAddress')
        except Exception as e:
            print(f"Error getting user email: {e}")
            return None
    
    def get_user_info(self):
        """Get authenticated user's detailed profile information from Google"""
        if not self.is_authenticated():
            return None
        
        try:
            # Get email from Gmail API
            gmail_profile = self.service.users().getProfile(userId='me').execute()
            email = gmail_profile.get('emailAddress')
            
            # Get additional info from People API if available
            user_info = {
                'email': email,
                'id': email.split('@')[0],  # Use email prefix as ID
                'name': None,
                'phone': None,
                'picture': None
            }
            
            # Try to get more details from Google People API
            try:
                from google.oauth2.credentials import Credentials
                from googleapiclient.discovery import build
                
                people_service = build('people', 'v1', credentials=self.credentials)
                person = people_service.people().get(
                    resourceName='people/me',
                    personFields='names,emailAddresses,phoneNumbers,photos'
                ).execute()
                
                # Extract name
                if 'names' in person and len(person['names']) > 0:
                    user_info['name'] = person['names'][0].get('displayName')
                
                # Extract phone
                if 'phoneNumbers' in person and len(person['phoneNumbers']) > 0:
                    user_info['phone'] = person['phoneNumbers'][0].get('value')
                
                # Extract picture
                if 'photos' in person and len(person['photos']) > 0:
                    user_info['picture'] = person['photos'][0].get('url')
                    
            except Exception as e:
                print(f"Could not fetch extended user info: {e}")
                # Continue with basic info
            
            return user_info
            
        except Exception as e:
            print(f"Error getting user info: {e}")
            return None
    
    def fetch_emails(self, max_results=50, query=''):
        """
        Fetch emails from Gmail inbox
        
        Args:
            max_results: Maximum number of emails to fetch (default 50)
            query: Gmail search query (e.g., 'is:unread', 'from:example@email.com')
            
        Returns:
            List of email dictionaries
        """
        if not self.is_authenticated():
            raise Exception("Not authenticated. Please authenticate first.")
        
        emails = []
        
        try:
            # Get message list
            results = self.service.users().messages().list(
                userId='me',
                maxResults=max_results,
                q=query
            ).execute()
            
            messages = results.get('messages', [])
            
            for message in messages:
                # Get full message details
                msg = self.service.users().messages().get(
                    userId='me',
                    id=message['id'],
                    format='full'
                ).execute()
                
                email_data = self._parse_email(msg)
                emails.append(email_data)
            
            return emails
            
        except HttpError as error:
            status_code = error.resp.status if hasattr(error, 'resp') else None
            raise GmailAPIError(
                f"Gmail API request failed: {str(error)}",
                details={
                    'status_code': status_code,
                    'error': str(error),
                    'user_id': self.user_id
                }
            )
    
    def _parse_email(self, msg):
        """
        Parse Gmail API message into email dictionary
        
        Args:
            msg: Gmail API message object
            
        Returns:
            Email dictionary
        """
        headers = msg['payload']['headers']
        
        # Extract headers
        subject = self._get_header(headers, 'Subject')
        sender = self._get_header(headers, 'From')
        date = self._get_header(headers, 'Date')
        
        # Parse date
        try:
            from email.utils import parsedate_to_datetime
            timestamp = parsedate_to_datetime(date).isoformat()
        except:
            timestamp = datetime.now().isoformat()
        
        # Extract body
        body = self._get_body(msg['payload'])
        
        # Clean HTML from body if present
        body = self._clean_html(body)
        
        # Check if read
        is_read = 'UNREAD' not in msg.get('labelIds', [])
        
        return {
            'id': msg['id'],
            'sender': sender,
            'subject': subject,
            'timestamp': timestamp,
            'body': body,  # Full body, no truncation
            'isRead': is_read,
            'category': 'Unprocessed',
            'actionItems': [],
            'draftReply': None,
            'summary': None,
            'customAnalysis': None,
            'gmailId': msg['id'],  # Store Gmail ID for reference
            'threadId': msg.get('threadId')
        }
    
    def _clean_html(self, text):
        """Remove HTML tags and clean up text"""
        if not text:
            return ''
        
        try:
            import re
            # Remove HTML tags
            text = re.sub(r'<[^>]+>', '', text)
            # Decode HTML entities
            import html
            text = html.unescape(text)
            # Remove extra whitespace
            text = re.sub(r'\s+', ' ', text)
            # Remove leading/trailing whitespace
            text = text.strip()
            return text
        except Exception as e:
            print(f"Error cleaning HTML: {e}")
            return text
    
    def _get_header(self, headers, name):
        """Extract header value by name"""
        for header in headers:
            if header['name'].lower() == name.lower():
                return header['value']
        return ''
    
    def _get_body(self, payload):
        """Extract email body from payload"""
        body = ''
        
        # Try to get plain text first
        if 'parts' in payload:
            for part in payload['parts']:
                # Check for nested parts (multipart/alternative)
                if 'parts' in part:
                    for subpart in part['parts']:
                        if subpart['mimeType'] == 'text/plain':
                            if 'data' in subpart['body']:
                                body = base64.urlsafe_b64decode(
                                    subpart['body']['data']
                                ).decode('utf-8', errors='ignore')
                                return body
                
                if part['mimeType'] == 'text/plain':
                    if 'data' in part['body']:
                        body = base64.urlsafe_b64decode(
                            part['body']['data']
                        ).decode('utf-8', errors='ignore')
                        return body
            
            # If no plain text, try HTML
            for part in payload['parts']:
                if 'parts' in part:
                    for subpart in part['parts']:
                        if subpart['mimeType'] == 'text/html' and not body:
                            if 'data' in subpart['body']:
                                body = base64.urlsafe_b64decode(
                                    subpart['body']['data']
                                ).decode('utf-8', errors='ignore')
                                return body
                
                if part['mimeType'] == 'text/html' and not body:
                    if 'data' in part['body']:
                        body = base64.urlsafe_b64decode(
                            part['body']['data']
                        ).decode('utf-8', errors='ignore')
                        return body
        else:
            if 'body' in payload and 'data' in payload['body']:
                body = base64.urlsafe_b64decode(
                    payload['body']['data']
                ).decode('utf-8', errors='ignore')
        
        return body
    
    def send_email(self, to, subject, body):
        """
        Send email via Gmail
        
        Args:
            to: Recipient email address
            subject: Email subject
            body: Email body text
            
        Returns:
            True if sent successfully
        """
        if not self.is_authenticated():
            raise Exception("Not authenticated")
        
        try:
            message = MIMEText(body)
            message['to'] = to
            message['subject'] = subject
            
            raw = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
            
            self.service.users().messages().send(
                userId='me',
                body={'raw': raw}
            ).execute()
            
            return True
            
        except HttpError as error:
            status_code = error.resp.status if hasattr(error, 'resp') else None
            raise GmailAPIError(
                f"Failed to send email: {str(error)}",
                details={
                    'status_code': status_code,
                    'to': to,
                    'subject': subject,
                    'user_id': self.user_id
                }
            )
    
    def mark_as_read(self, gmail_id):
        """Mark email as read"""
        if not self.is_authenticated():
            return False
        
        try:
            self.service.users().messages().modify(
                userId='me',
                id=gmail_id,
                body={'removeLabelIds': ['UNREAD']}
            ).execute()
            return True
        except:
            return False
    
    def logout(self):
        """Clear credentials and logout"""
        self.credentials = None
        self.service = None
        
        # Delete token file only if it exists and persistence was enabled
        if self.token_file and os.path.exists(self.token_file):
            os.remove(self.token_file)
