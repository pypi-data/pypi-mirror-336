import json, sys, os
from typing import Dict, Any, Optional
from botocore.exceptions import ClientError
from mypy_boto3_secretsmanager.client import SecretsManagerClient

# Import AWSManager from cloud_session_utils
from cloudweave.cloud_session_utils import AWSManager
from cloudweave.secret_utils.class_utils import SecretType, SecretsStoreError, SecretConversionError, SecretNotFoundError


class AWSSecretsStore:
    """A minimal class to interact with AWS Secrets Manager"""

    def __init__(self, region: Optional[str] = None, profile: Optional[str] = None, **kwargs):
        """
        Initialize the SecretsStore with AWS configuration.
        
        Args:
            region_name: AWS region
            **kwargs: Additional AWS configuration parameters
        """
        self._aws_options = {
            'region': region,
            'profile': profile
        }
        
        
        aws = AWSManager.instance(self._aws_options)
        self._secrets_client: SecretsManagerClient = aws.get_client('secretsmanager')
        
    def get_secret(self, secret_id: str, secret_type: str = "text") -> Any:
        """
        Retrieve and convert a secret from AWS Secrets Manager.
        
        Args:
            secret_id: Name/ID of the secret
            secret_type: Type of secret (text or json)
            
        Returns:
            The secret value
            
        Raises:
            SecretNotFoundError: If the secret cannot be found
            SecretConversionError: If the secret cannot be converted
        """
        if secret_type not in [t.value for t in SecretType]:
            raise ValueError(f"Invalid secret type. Must be one of: {[t.value for t in SecretType]}")

        try:
            response = self._secrets_client.get_secret_value(SecretId=secret_id)
            secret_string = response.get('SecretString')
            
            if not secret_string:
                return None
                
            if secret_type == SecretType.JSON.value:
                try:
                    return json.loads(secret_string)
                except json.JSONDecodeError as e:
                    raise SecretConversionError(f"Failed to convert secret to JSON: {str(e)}")
            else:
                return secret_string
                
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', 'Unknown')
            if error_code == 'ResourceNotFoundException':
                raise SecretNotFoundError(f"Secret {secret_id} not found")
            raise SecretsStoreError(f"Failed to retrieve secret: {str(e)}")
        except Exception as e:
            raise SecretsStoreError(f"Unexpected error retrieving secret: {str(e)}")


# Example usage
if __name__ == "__main__":
    # Create the secrets store
    secrets = AWSSecretsStore(region="us-west-2")
    
    # Get a text secret
    try:
        api_key = secrets.get_secret("my/api/key")
        print(f"API Key: {api_key}")
    except SecretNotFoundError:
        print("API key not found")
    
    # Get a JSON secret
    try:
        db_config = secrets.get_secret("database/config", secret_type="json")
        print(f"Database host: {db_config.get('host')}")
        print(f"Database user: {db_config.get('username')}")
    except SecretNotFoundError:
        print("Database config not found")
    except SecretConversionError:
        print("Failed to parse database config as JSON")