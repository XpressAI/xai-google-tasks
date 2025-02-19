import os
import base64
import json
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials

def get_credentials(scopes):
    """Get credentials from environment variable or context.
    
    Args:
        scopes: List of Google API scopes needed
        
    Returns:
        Google OAuth credentials object
    """
    creds_b64 = os.getenv('GOOGLE_SERVICE_ACCOUNT_CREDENTIALS')
    if not creds_b64:
        raise EnvironmentError("GOOGLE_SERVICE_ACCOUNT_CREDENTIALS environment variable not set")
    
    # Decode base64 credentials
    creds_json = base64.b64decode(creds_b64).decode('utf-8')
    creds_dict = json.loads(creds_json)
    
    # Create credentials object
    creds = service_account.Credentials.from_service_account_info(
        creds_dict,
        scopes=scopes
    )
    
    return creds
