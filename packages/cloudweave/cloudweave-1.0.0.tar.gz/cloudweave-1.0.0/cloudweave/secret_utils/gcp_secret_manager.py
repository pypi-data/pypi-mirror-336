import json, os, sys
from typing import Any, Optional
from enum import Enum
from google.api_core.exceptions import NotFound, PermissionDenied, FailedPrecondition


from cloudweave.cloud_session_utils import GCPManager

from cloudweave.secret_utils.class_utils import SecretType, SecretsStoreError, SecretAccessError, SecretConversionError, SecretNotFoundError


class GCPSecretsStore:
    """A minimal class to interact with Google Cloud Secret Manager"""

    def __init__(self, project_id: str, credentials: str, **kwargs):
        """
        Initialize the SecretsStore with GCP configuration.
        
        Args:
            project_id: GCP project ID
            **kwargs: Additional GCP client configuration parameters
        """
        self.project_id = project_id
        gcp = GCPManager.instance()
        self.client = gcp.secretmanager
        
    def get_secret(self, secret_id: str, version_id: str = "latest", secret_type: str = "text") -> Any:
        """
        Retrieve and convert a secret from GCP Secret Manager.
        
        Args:
            secret_id: Name/ID of the secret
            version_id: Version of the secret (default: "latest")
            secret_type: Type of secret (text or json)
            
        Returns:
            The secret value
            
        Raises:
            SecretNotFoundError: If the secret cannot be found
            SecretAccessError: If access to the secret is denied
            SecretConversionError: If the secret cannot be converted
        """
        if secret_type not in [t.value for t in SecretType]:
            raise ValueError(f"Invalid secret type. Must be one of: {[t.value for t in SecretType]}")

        # Build the resource name of the secret version
        if version_id == "latest":
            name = f"projects/{self.project_id}/secrets/{secret_id}/versions/latest"
        else:
            name = f"projects/{self.project_id}/secrets/{secret_id}/versions/{version_id}"

        try:
            # Access the secret version
            response = self.client.access_secret_version(request={"name": name})
            secret_data = response.payload.data.decode("UTF-8")
            
            if not secret_data:
                return None
                
            # Convert the secret based on the requested type
            if secret_type == SecretType.JSON.value:
                try:
                    return json.loads(secret_data)
                except json.JSONDecodeError as e:
                    raise SecretConversionError(f"Failed to convert secret to JSON: {str(e)}")
            else:
                return secret_data
                
        except NotFound:
            raise SecretNotFoundError(f"Secret {secret_id} (version: {version_id}) not found")
        except PermissionDenied:
            raise SecretAccessError(f"Access denied to secret {secret_id} (version: {version_id})")
        except FailedPrecondition as e:
            raise SecretsStoreError(f"Secret is in a failed state: {str(e)}")
        except Exception as e:
            raise SecretsStoreError(f"Unexpected error retrieving secret: {str(e)}")


# Example usage
if __name__ == "__main__":
    # Create the secrets store
    secrets = GCPSecretsStore(project_id="my-gcp-project", credentials="path/to/credentials")
    
    # Get a text secret
    try:
        api_key = secrets.get_secret("api-key")
        print(f"API Key: {api_key}")
    except SecretNotFoundError:
        print("API key not found")
    
    # Get a JSON secret
    try:
        db_config = secrets.get_secret("database-config", secret_type="json")
        print(f"Database host: {db_config.get('host')}")
        print(f"Database user: {db_config.get('username')}")
    except SecretNotFoundError:
        print("Database config not found")
    except SecretConversionError:
        print("Failed to parse database config as JSON")