"""
Utility functions for the MuopDB client.
"""
from typing import Any, Dict, Optional
import json
from urllib.parse import urljoin

def validate_url(url: str) -> str:
    """
    Validate and normalize a URL.
    
    Args:
        url: The URL to validate
        
    Returns:
        The normalized URL
        
    Raises:
        MuopDBValidationError: If the URL is invalid
    """
    if not url:
        raise ValueError("URL cannot be empty")
    return url.rstrip('/')

def build_url(base_url: str, path: str) -> str:
    """
    Build a complete URL from base URL and path.
    
    Args:
        base_url: The base URL
        path: The path to append
        
    Returns:
        The complete URL
    """
    return urljoin(base_url, path.lstrip('/'))

def prepare_request_data(data: Optional[Dict[str, Any]] = None) -> Optional[str]:
    """
    Prepare request data for sending to the server.
    
    Args:
        data: The data to prepare
        
    Returns:
        JSON string if data is provided, None otherwise
    """
    if data is None:
        return None
    return json.dumps(data) 