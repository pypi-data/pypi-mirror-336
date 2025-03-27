import requests
from typing import Dict, Any, Optional

def make_request(
    method: str,
    url: str,
    headers: Optional[Dict[str, str]] = None,
    json: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Make an HTTP request and handle the response.
    """
    try:
        response = requests.request(method, url, headers=headers, json=json)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"API request failed: {str(e)}")