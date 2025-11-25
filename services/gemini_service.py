"""
Gemini AI Service
Handles all AI operations using Google Gemini API
"""

import google.generativeai as genai
from google.generativeai.types import GenerationConfig
import json
import os
from models.email_models import EmailCategory
from utils.exceptions import AIServiceError, ConfigurationError, ValidationError


class GeminiService:
    """Service class for interacting with Google Gemini API"""
    
    def __init__(self, api_key: str, model_name: str = None):
        """Initialize the Gemini service with API key and model selection
        
        Args:
            api_key: Google Gemini API key
            model_name: Model name from environment or default
        """
        if not api_key:
            raise ConfigurationError(
                "GEMINI_API_KEY must be set in environment variables",
                details={'env_var': 'GEMINI_API_KEY'}
            )
        
        # Get model name from parameter or environment, default to gemini-1.5-flash
        self.model_name = model_name or os.getenv('AI_MODEL', 'gemini-1.5-flash')
        
        try:
            genai.configure(api_key=api_key)
            self.model_fast = genai.GenerativeModel(self.model_name)
            print(f"Initialized Gemini with model: {self.model_name}")
        except Exception as e:
            raise AIServiceError(
                f"Failed to initialize Gemini service: {str(e)}",
                details={'error': str(e), 'model': self.model_name}
            )
    
    def categorize_email(self, email: dict, prompt_template: str) -> str:
        """
        Categorize an email using the user-defined prompt
        
        Args:
            email: Email data dictionary
            prompt_template: User-defined categorization prompt
            
        Returns:
            Category name as determined by AI
        """
        try:
            prompt = f"""
{prompt_template}

Email Content:
Subject: {email['subject']}
Body: {email['body']}
Sender: {email['sender']}

Return ONLY the category name, nothing else.
"""
            
            response = self.model_fast.generate_content(
                prompt,
                generation_config=GenerationConfig(
                    temperature=0.1,
                )
            )
            
            # Return the AI's category directly (cleaned)
            category = response.text.strip()
            
            # Remove quotes if present
            category = category.strip('"').strip("'")
            
            return category
            
        except Exception as e:
            raise AIServiceError(
                f"Email categorization failed: {str(e)}",
                details={
                    'error': str(e),
                    'email_id': email.get('id'),
                    'subject': email.get('subject')
                }
            )
    
    def extract_action_items(self, email: dict, prompt_template: str) -> list:
        """
        Extract action items from an email using JSON mode
        
        Args:
            email: Email data dictionary
            prompt_template: User-defined action extraction prompt
            
        Returns:
            List of action items
        """
        try:
            prompt = f"""
{prompt_template}

Email Content:
Subject: {email['subject']}
Body: {email['body']}
"""
            
            response = self.model_fast.generate_content(
                prompt,
                generation_config=GenerationConfig(
                    response_mime_type="application/json",
                )
            )
            
            result = json.loads(response.text)
            return result.get('tasks', [])
            
        except json.JSONDecodeError as e:
            raise AIServiceError(
                f"Failed to parse AI response as JSON: {str(e)}",
                details={
                    'error': str(e),
                    'response': response.text if 'response' in locals() else None
                }
            )
        except Exception as e:
            raise AIServiceError(
                f"Action extraction failed: {str(e)}",
                details={
                    'error': str(e),
                    'email_id': email.get('id')
                }
            )
    
    def summarize_email(self, email: dict) -> str:
        """
        Generate a summary of the email
        
        Args:
            email: Email data dictionary
            
        Returns:
            Summary text
        """
        try:
            prompt = f"""
Please provide a concise summary of the following email in 2-3 sentences.
Focus on the main point, any deadlines, and the tone of the sender.

Email Content:
Subject: {email['subject']}
Body: {email['body']}
Sender: {email['sender']}
"""
            
            response = self.model_fast.generate_content(prompt)
            return response.text or "Could not generate summary."
            
        except Exception as e:
            print(f"Summarization failed: {e}")
            return "Error summarizing email."
    
    def generate_draft_reply(self, email: dict, prompt_template: str, extra_instructions: str = "") -> str:
        """
        Generate a draft reply for an email
        
        Args:
            email: Email data dictionary
            prompt_template: User-defined auto-reply prompt
            extra_instructions: Optional additional instructions
            
        Returns:
            Draft reply text
        """
        try:
            extra_text = f"\nAdditional User Instructions: {extra_instructions}" if extra_instructions else ""
            
            prompt = f"""
{prompt_template}
{extra_text}

Original Email:
From: {email['sender']}
Subject: {email['subject']}
Body: {email['body']}
"""
            
            response = self.model_fast.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            raise AIServiceError(
                f"Draft generation failed: {str(e)}",
                details={
                    'error': str(e),
                    'email_id': email.get('id')
                }
            )
    
    def run_custom_analyzer(self, email: dict, prompt_template: str) -> str:
        """
        Run a custom analyzer prompt against an email
        
        Args:
            email: Email data dictionary
            prompt_template: Custom analyzer prompt
            
        Returns:
            Analysis result text
        """
        try:
            prompt = f"""
{prompt_template}

Email Content:
Sender: {email['sender']}
Subject: {email['subject']}
Body: {email['body']}
"""
            
            response = self.model_fast.generate_content(prompt)
            return response.text or "No analysis generated."
            
        except Exception as e:
            print(f"Custom analysis failed: {e}")
            return "Error running analysis."
    
    def chat_with_email_agent(self, email: dict, history: list, user_message: str) -> str:
        """
        Chat with the email agent about a specific email
        
        Args:
            email: Email data dictionary
            history: List of previous messages [{'role': 'user'/'model', 'text': '...'}]
            user_message: Current user message
            
        Returns:
            Agent response text
        """
        try:
            system_instruction = f"""You are a helpful Email Assistant. You are currently looking at a specific email.

Current Email Context:
Sender: {email.get('sender', 'Unknown')}
Subject: {email.get('subject', 'No subject')}
Body: {email.get('body', 'No content')[:1000]}

Answer the user's questions based on this email. Be concise and helpful."""
            
            # Create chat session with configured model
            chat_model = genai.GenerativeModel(
                self.model_name,
                system_instruction=system_instruction
            )
            
            # Convert history to proper format
            formatted_history = []
            for msg in history:
                role = 'user' if msg['role'] == 'user' else 'model'
                formatted_history.append({
                    'role': role,
                    'parts': [msg['text']]
                })
            
            chat = chat_model.start_chat(history=formatted_history)
            response = chat.send_message(user_message)
            
            return response.text or "I couldn't understand that."
            
        except Exception as e:
            print(f"Chat failed: {e}")
            return "Sorry, I'm having trouble connecting to the brain right now."
