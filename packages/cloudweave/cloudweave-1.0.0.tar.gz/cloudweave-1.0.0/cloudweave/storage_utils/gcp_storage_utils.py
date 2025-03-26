import json
import os, sys
from typing import Dict, Any, Optional, Union, List, BinaryIO

# Add the parent directory to sys.path to allow importing from cloud_session_utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class StorageManager:
    """
    A streamlined Google Cloud Storage manager.
    
    This class provides essential Cloud Storage operations including downloading files,
    uploading files, reading file content into variables, and checking file existence.
    It uses the GCPManager for handling GCP client connections.
    
    Usage:
        # Create StorageManager instance
        storage_manager = StorageManager()
        
        # Or with custom options
        storage_manager = StorageManager({
            'project_id': 'my-project',
            'credentials_path': '/path/to/service-account.json',
        })
        
        # Read a file directly into a variable
        data = storage_manager.read_file('my-bucket', 'path/to/file.json')
        
        # Download a file
        storage_manager.download_file('my-bucket', 'path/to/file.txt', 'local_file.txt')
    """
    
    def __init__(self, options: Optional[Dict[str, Any]] = None):
        """
        Initialize the StorageManager.
        
        Args:
            options: Configuration options for GCP connection
        """
        # Import here to avoid circular imports        
        from cloud_session_utils.gcp_session_manager import GCPManager

        self.gcp = GCPManager.instance(options)
        self.client = self.gcp.storage
    
    def get_bucket(self, bucket_name: str):
        """
        Get a bucket reference.
        
        Args:
            bucket_name: The name of the bucket
            
        Returns:
            google.cloud.storage.bucket.Bucket: Bucket object
        """
        return self.client.bucket(bucket_name)
    
    def download_file(self, bucket_name: str, blob_path: str, local_path: str) -> bool:
        """
        Download a file from Cloud Storage to a local destination.
        
        Args:
            bucket_name: Cloud Storage bucket name
            blob_path: Source file path in Cloud Storage
            local_path: Local destination file path
            
        Returns:
            bool: True if download was successful, False otherwise
        """
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(os.path.abspath(local_path)), exist_ok=True)
            
            # Get bucket and blob
            bucket = self.get_bucket(bucket_name)
            blob = bucket.blob(blob_path)
            
            # Download the file
            blob.download_to_filename(local_path)
            return True
        except Exception as e:
            print(f"Error downloading file from Cloud Storage: {e}")
            return False
    
    def upload_file(self, local_path: str, bucket_name: str, blob_path: str, 
                   content_type: Optional[str] = None) -> bool:
        """
        Upload a file to Cloud Storage.
        
        Args:
            local_path: Local file path
            bucket_name: Cloud Storage bucket name
            blob_path: Destination path in Cloud Storage
            content_type: Optional content type (e.g., 'application/json')
            
        Returns:
            bool: True if upload was successful, False otherwise
        """
        try:
            # Get bucket and blob
            bucket = self.get_bucket(bucket_name)
            blob = bucket.blob(blob_path)
            
            # Set content type if provided
            if content_type:
                blob.content_type = content_type
                
            # Upload the file
            blob.upload_from_filename(local_path)
            return True
        except Exception as e:
            print(f"Error uploading file to Cloud Storage: {e}")
            return False
    
    def read_file(self, bucket_name: str, blob_path: str, 
                 decode: bool = True) -> Optional[Union[str, bytes]]:
        """
        Read file content from Cloud Storage directly into a variable.
        
        Args:
            bucket_name: Cloud Storage bucket name
            blob_path: Path to file in Cloud Storage
            decode: Whether to decode the content as UTF-8 (for text files)
            
        Returns:
            File content as string or bytes, or None if operation failed
        """
        try:
            # Get bucket and blob
            bucket = self.get_bucket(bucket_name)
            blob = bucket.blob(blob_path)
            
            # Download the content
            content = blob.download_as_bytes()
            
            if decode:
                return content.decode('utf-8')
            return content
        except Exception as e:
            print(f"Error reading file from Cloud Storage: {e}")
            return None
    
    def read_json(self, bucket_name: str, blob_path: str) -> Optional[Dict[str, Any]]:
        """
        Read and parse JSON file from Cloud Storage.
        
        Args:
            bucket_name: Cloud Storage bucket name
            blob_path: Path to JSON file in Cloud Storage
            
        Returns:
            Parsed JSON content or None if operation failed
        """
        content = self.read_file(bucket_name, blob_path)
        if content:
            try:
                return json.loads(content)
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON: {e}")
        return None
    
    def write_text(self, content: str, bucket_name: str, blob_path: str,
                  content_type: Optional[str] = None) -> bool:
        """
        Write text content to Cloud Storage.
        
        Args:
            content: Text content to write
            bucket_name: Cloud Storage bucket name
            blob_path: Destination path in Cloud Storage
            content_type: Optional content type (e.g., 'text/plain')
            
        Returns:
            bool: True if operation was successful, False otherwise
        """
        try:
            # Get bucket and blob
            bucket = self.get_bucket(bucket_name)
            blob = bucket.blob(blob_path)
            
            # Set content type if provided
            if content_type:
                blob.content_type = content_type
                
            # Upload the content
            blob.upload_from_string(content)
            return True
        except Exception as e:
            print(f"Error writing text to Cloud Storage: {e}")
            return False
    
    def write_json(self, data: Dict[str, Any], bucket_name: str, blob_path: str) -> bool:
        """
        Write data as JSON to Cloud Storage.
        
        Args:
            data: Python dictionary to save as JSON
            bucket_name: Cloud Storage bucket name
            blob_path: Destination path in Cloud Storage
            
        Returns:
            bool: True if operation was successful, False otherwise
        """
        try:
            json_content = json.dumps(data)
            return self.write_text(
                json_content, 
                bucket_name, 
                blob_path, 
                content_type='application/json'
            )
        except Exception as e:
            print(f"Error writing JSON to Cloud Storage: {e}")
            return False
    
    def file_exists(self, bucket_name: str, blob_path: str) -> bool:
        """
        Check if a file exists in Cloud Storage.
        
        Args:
            bucket_name: Cloud Storage bucket name
            blob_path: Path to file in Cloud Storage
            
        Returns:
            bool: True if file exists, False otherwise
        """
        try:
            bucket = self.get_bucket(bucket_name)
            blob = bucket.blob(blob_path)
            return blob.exists()
        except Exception:
            return False
    
    def get_file_size(self, bucket_name: str, blob_path: str) -> Optional[int]:
        """
        Get the size of a file in Cloud Storage.
        
        Args:
            bucket_name: Cloud Storage bucket name
            blob_path: Path to file in Cloud Storage
            
        Returns:
            int: File size in bytes or None if file doesn't exist
        """
        try:
            bucket = self.get_bucket(bucket_name)
            blob = bucket.blob(blob_path)
            
            if not blob.exists():
                return None
                
            blob.reload()  # Fetch blob metadata
            return blob.size
        except Exception:
            return None
    
    def list_blobs(self, bucket_name: str, prefix: str = "",
                 delimiter: str = "") -> List[str]:
        """
        List blobs in a Cloud Storage bucket.
        
        Args:
            bucket_name: Cloud Storage bucket name
            prefix: Prefix to filter results
            delimiter: Delimiter for hierarchy (e.g., '/' for folders)
            
        Returns:
            list: List of blob names
        """
        try:
            blobs = []
            bucket = self.get_bucket(bucket_name)
            
            # List blobs with the specified prefix and delimiter
            blob_list = bucket.list_blobs(prefix=prefix, delimiter=delimiter)
            
            for blob in blob_list:
                blobs.append(blob.name)
                
            return blobs
        except Exception as e:
            print(f"Error listing blobs: {e}")
            return []
    
    def list_folders(self, bucket_name: str, prefix: str = "") -> List[str]:
        """
        List folders (prefixes) in a Cloud Storage bucket.
        
        Args:
            bucket_name: Cloud Storage bucket name
            prefix: Prefix to filter results
            
        Returns:
            list: List of folder names without trailing delimiter
        """
        try:
            folders = []
            bucket = self.get_bucket(bucket_name)
            
            # Use delimiter '/' to list folders
            _, prefixes = bucket.list_blobs(prefix=prefix, delimiter='/')
            
            for prefix_item in prefixes:
                # Remove trailing slash
                folder = prefix_item
                if folder.endswith('/'):
                    folder = folder[:-1]
                folders.append(folder)
                
            return folders
        except Exception as e:
            print(f"Error listing folders: {e}")
            return []
    
    def copy_blob(self, source_bucket: str, source_blob: str,
                 dest_bucket: str, dest_blob: str) -> bool:
        """
        Copy a blob from one location to another.
        
        Args:
            source_bucket: Source bucket name
            source_blob: Source blob path
            dest_bucket: Destination bucket name
            dest_blob: Destination blob path
            
        Returns:
            bool: True if copy was successful, False otherwise
        """
        try:
            source_bucket_obj = self.get_bucket(source_bucket)
            dest_bucket_obj = self.get_bucket(dest_bucket)
            
            source_blob_obj = source_bucket_obj.blob(source_blob)
            
            # Copy the blob
            source_bucket_obj.copy_blob(
                source_blob_obj, 
                dest_bucket_obj, 
                dest_blob
            )
            return True
        except Exception as e:
            print(f"Error copying blob: {e}")
            return False
    
    def delete_blob(self, bucket_name: str, blob_path: str) -> bool:
        """
        Delete a blob from a bucket.
        
        Args:
            bucket_name: Cloud Storage bucket name
            blob_path: Path to blob in Cloud Storage
            
        Returns:
            bool: True if deletion was successful, False otherwise
        """
        try:
            bucket = self.get_bucket(bucket_name)
            blob = bucket.blob(blob_path)
            
            # Delete the blob
            blob.delete()
            return True
        except Exception as e:
            print(f"Error deleting blob: {e}")
            return False
    
    def generate_signed_url(self, bucket_name: str, blob_path: str, 
                          expiration: int = 3600) -> Optional[str]:
        """
        Generate a signed URL for temporary access to a blob.
        
        Args:
            bucket_name: Cloud Storage bucket name
            blob_path: Path to blob in Cloud Storage
            expiration: URL expiration time in seconds (default: 1 hour)
            
        Returns:
            str: Signed URL or None if generation failed
        """
        try:
            bucket = self.get_bucket(bucket_name)
            blob = bucket.blob(blob_path)
            
            # Generate signed URL
            url = blob.generate_signed_url(
                expiration=expiration,
                method='GET'
            )
            return url
        except Exception as e:
            print(f"Error generating signed URL: {e}")
            return None