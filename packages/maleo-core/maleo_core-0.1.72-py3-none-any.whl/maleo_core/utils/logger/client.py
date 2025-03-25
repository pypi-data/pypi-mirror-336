import os
from google.auth import default
from google.cloud import logging
from google.oauth2 import service_account
from typing import Optional

class CloudLoggingClient:
    def __init__(self):
        """Initialize the Cloud Logging client."""
        self.project_id = os.getenv("GCP_PROJECT_ID")
        if not self.project_id:
            raise ValueError("Project ID must be provided or set in GCP_PROJECT_ID environment variable")

        # Setup credentials with fallback chain
        credentials = None
        try:
            if os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
                credentials = service_account.Credentials.from_service_account_file(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
            else:
                credentials, project = default()
        except Exception as e:
            raise ValueError(f"Failed to initialize credentials: {str(e)}")

        self.client = logging.Client(credentials=credentials)

cloud_logging_client:Optional[CloudLoggingClient] = None

def init_client():
    global cloud_logging_client
    if not cloud_logging_client: cloud_logging_client = CloudLoggingClient()
    return cloud_logging_client

def get_client():
    global cloud_logging_client
    if not cloud_logging_client: init_client()
    return cloud_logging_client

def dispose_client():
    global cloud_logging_client
    if cloud_logging_client: cloud_logging_client = None