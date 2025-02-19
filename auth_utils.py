import os
import base64
import json
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials

def get_credentials(scopes, json_path=None):
    """Get credentials from file or environment variable.
    
    Args:
        scopes: List of Google API scopes needed
        json_path: Optional path to service account JSON file
        
    Returns:
        Google OAuth credentials object
    """
    if json_path:
        if not os.path.exists(json_path):
            raise FileNotFoundError(f"Credentials file not found: {json_path}")
        return service_account.Credentials.from_service_account_file(
            json_path,
            scopes=scopes
        )
    
    # Fall back to environment variable
    creds_b64 = os.getenv('GOOGLE_SERVICE_ACCOUNT_CREDENTIALS')
    if not creds_b64:
        raise EnvironmentError("No credentials file provided and GOOGLE_SERVICE_ACCOUNT_CREDENTIALS environment variable not set")
    
    # Decode base64 credentials
    creds_json = base64.b64decode(creds_b64).decode('utf-8')
    creds_dict = json.loads(creds_json)
    
    # Create credentials object
    return service_account.Credentials.from_service_account_info(
        creds_dict,
        scopes=scopes
    )
