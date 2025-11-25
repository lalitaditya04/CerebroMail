"""
Models Package
"""
from .email_models import (
    EmailCategory,
    ActionItem,
    EmailData,
    CustomAnalyzer,
    PromptConfig,
    ChatMessage
)

__all__ = [
    'EmailCategory',
    'ActionItem',
    'EmailData',
    'CustomAnalyzer',
    'PromptConfig',
    'ChatMessage'
]
