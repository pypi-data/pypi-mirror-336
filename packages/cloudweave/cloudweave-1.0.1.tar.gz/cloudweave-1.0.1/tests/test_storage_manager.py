import os, sys
import argparse
from typing import Optional

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import from your authenticated modules
from cloudweave import get_auth_manager, StorageType, LoggerType, AuthenticationError


def test_download_file(
    api_key: str,
    storage_type: str,
    bucket_name: str,
    source_path: str, 
    local_path: str,
    region: Optional[str] = "us-east-1",
    project_id: Optional[str] = None
) -> bool:
    """
    Test downloading a file from a bucket using authenticated storage.
    
    Args:
        api_key: Authentication API key
        storage_type: Type of storage (s3 or gcs)
        bucket_name: Storage bucket name
        source_path: Source file path in the bucket
        local_path: Local destination path
        region: AWS region (for S3)
        project_id: GCP project ID (for GCS)
        
    Returns:
        bool: True if download was successful, False otherwise
    """
    try:
        # Authenticate and get the auth manager
        auth = get_auth_manager(api_key)
        
        # Create a logger through the auth manager
        logger = auth.get_logger(
            logger_type=LoggerType.LOCAL,
            namespace="storage-test",
            instance_id="test-logger",
            log_level="info"
        )
        
        logger.info(f"Starting download test from {bucket_name}/{source_path} to {local_path}")
        
        # Get storage options based on storage type
        storage_kwargs = {
            'default_bucket': bucket_name,
        }
        
        if storage_type.lower() == "s3":
            storage_kwargs['region'] = region
        elif storage_type.lower() == "gcs":
            if not project_id:
                logger.error("GCS storage requires a project_id")
                return False
            storage_kwargs['project_id'] = project_id
        else:
            logger.error(f"Unsupported storage type: {storage_type}")
            return False
        
        # Get storage instance through the auth manager
        storage = auth.get_storage(
            storage_type=storage_type,
            namespace="test",
            instance_id=f"test-{storage_type}-storage",
            **storage_kwargs
        )
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(os.path.abspath(local_path)), exist_ok=True)
        
        # Perform the download
        success = storage.download_file(
            bucket_name=bucket_name,
            source_path=source_path,
            local_path=local_path
        )
        
        if success:
            logger.info(f"Successfully downloaded file to {local_path}")
            logger.info(f"File size: {os.path.getsize(local_path)} bytes")
        else:
            logger.error(f"Failed to download file to {local_path}")
        
        return success
        
    except AuthenticationError as e:
        print(f"Authentication failed: {e}")
        return False
    except Exception as e:
        print(f"Error during download test: {e}")
        return False


if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Test storage download functionality")
    parser.add_argument("--api-key", required=True,
                      help="API key for authentication")
    parser.add_argument("--storage-type", choices=["s3", "gcs"], required=True,
                      help="Storage type (s3 or gcs)")
    parser.add_argument("--bucket", required=True,
                      help="Bucket name")
    parser.add_argument("--source-path", required=True,
                      help="Source file path in the bucket")
    parser.add_argument("--local-path", required=True,
                      help="Local destination path")
    parser.add_argument("--region", default="us-east-1",
                      help="AWS region (for S3)")
    parser.add_argument("--project-id",
                      help="GCP project ID (for GCS)")
    
    args = parser.parse_args()
    
    # Run the test
    success = test_download_file(
        api_key=args.api_key,
        storage_type=args.storage_type,
        bucket_name=args.bucket,
        source_path=args.source_path,
        local_path=args.local_path,
        region=args.region,
        project_id=args.project_id
    )
    
    # Exit with appropriate status code
    exit(0 if success else 1)