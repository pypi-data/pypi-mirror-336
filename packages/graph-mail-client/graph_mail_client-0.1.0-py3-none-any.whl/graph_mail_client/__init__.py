"""
Microsoft Graph API 邮件客户端

作者：Cascade
日期：2025-03-26
"""

from .client import (
    GraphMailClient, 
    get_emails, 
    get_tokens, 
    get_latest_unread_email,
    get_verification_code_from_email
)

__version__ = "0.1.0"
__all__ = [
    "GraphMailClient", 
    "get_emails", 
    "get_tokens", 
    "get_latest_unread_email", 
    "get_verification_code_from_email"
]
