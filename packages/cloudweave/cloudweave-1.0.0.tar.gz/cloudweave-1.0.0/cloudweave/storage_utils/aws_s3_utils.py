import json
import os, sys
from typing import Dict, Any, Optional, Union, List

# Add the parent directory to sys.path to allow importing from cloud_session_utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class S3Manager:
    """
    A streamlined S3 manager for interacting with AWS S3 storage.
    
    This class provides essential S3 operations including downloading files,
    uploading files, reading file content into variables, and checking file existence.
    It uses the AWSManager for handling AWS client connections.
    
    Usage:
        # Create S3Manager instance
        s3_manager = S3Manager()
        
        # Or with custom options
        s3_manager = S3Manager({
            'region': 'us-west-2',
            'profile': 'dev',
        })
        
        # Read a file directly into a variable
        data = s3_manager.read_file('my-bucket', 'path/to/file.json')
        
        # Download a file
        s3_manager.download_file('my-bucket', 'path/to/file.txt', 'local_file.txt')
    """
    
    def __init__(self, options: Optional[Dict[str, Any]] = None):
        """
        Initialize the S3Manager.
        
        Args:
            options: Configuration options for AWS connection
        """
        # Import here to avoid circular imports
        from cloud_session_utils.aws_session_manager import AWSManager
        
        self.aws = AWSManager.instance(options)
        self.client = self.aws.s3
    
    def download_file(self, bucket: str, s3_path: str, local_path: str) -> bool:
        """
        Download a file from S3 to a local destination.
        
        Args:
            bucket: S3 bucket name
            s3_path: Source file path in S3
            local_path: Local destination file path
            
        Returns:
            bool: True if download was successful, False otherwise
        """
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(os.path.abspath(local_path)), exist_ok=True)
            
            # Download the file
            self.client.download_file(bucket, s3_path, local_path)
            return True
        except Exception as e:
            print(f"Error downloading file from S3: {e}")
            return False
    
    def upload_file(self, local_path: str, bucket: str, s3_path: str, 
                    extra_args: Optional[Dict[str, Any]] = None) -> bool:
        """
        Upload a file to S3.
        
        Args:
            local_path: Local file path
            bucket: S3 bucket name
            s3_path: Destination path in S3
            extra_args: Optional extra arguments for upload (e.g., ContentType)
            
        Returns:
            bool: True if upload was successful, False otherwise
        """
        try:
            self.client.upload_file(
                local_path, 
                bucket, 
                s3_path,
                ExtraArgs=extra_args
            )
            return True
        except Exception as e:
            print(f"Error uploading file to S3: {e}")
            return False
    
    def read_file(self, bucket: str, s3_path: str, 
                  decode: bool = True) -> Optional[Union[str, bytes]]:
        """
        Read file content from S3 directly into a variable.
        
        Args:
            bucket: S3 bucket name
            s3_path: Path to file in S3
            decode: Whether to decode the content as UTF-8 (for text files)
            
        Returns:
            File content as string or bytes, or None if operation failed
        """
        try:
            response = self.client.get_object(Bucket=bucket, Key=s3_path)
            content = response['Body'].read()
            
            if decode:
                return content.decode('utf-8')
            return content
        except Exception as e:
            print(f"Error reading file from S3: {e}")
            return None
    
    def read_json(self, bucket: str, s3_path: str) -> Optional[Dict[str, Any]]:
        """
        Read and parse JSON file from S3.
        
        Args:
            bucket: S3 bucket name
            s3_path: Path to JSON file in S3
            
        Returns:
            Parsed JSON content or None if operation failed
        """
        content = self.read_file(bucket, s3_path)
        if content:
            try:
                return json.loads(content)
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON: {e}")
        return None
    
    def write_json(self, data: Dict[str, Any], bucket: str, s3_path: str) -> bool:
        """
        Write data as JSON to S3.
        
        Args:
            data: Python dictionary to save as JSON
            bucket: S3 bucket name
            s3_path: Destination path in S3
            
        Returns:
            bool: True if operation was successful, False otherwise
        """
        try:
            json_content = json.dumps(data).encode('utf-8')
            self.client.put_object(
                Body=json_content,
                Bucket=bucket,
                Key=s3_path,
                ContentType='application/json'
            )
            return True
        except Exception as e:
            print(f"Error writing JSON to S3: {e}")
            return False
    
    def file_exists(self, bucket: str, s3_path: str) -> bool:
        """
        Check if a file exists in S3.
        
        Args:
            bucket: S3 bucket name
            s3_path: Path to file in S3
            
        Returns:
            bool: True if file exists, False otherwise
        """
        try:
            self.client.head_object(Bucket=bucket, Key=s3_path)
            return True
        except Exception:
            return False
    
    def get_file_size(self, bucket: str, s3_path: str) -> Optional[int]:
        """
        Get the size of a file in S3.
        
        Args:
            bucket: S3 bucket name
            s3_path: Path to file in S3
            
        Returns:
            int: File size in bytes or None if file doesn't exist
        """
        try:
            response = self.client.head_object(Bucket=bucket, Key=s3_path)
            return response.get('ContentLength')
        except Exception:
            return None
    
    def list_objects(self, bucket: str, prefix: str = "", 
                    delimiter: str = "") -> List[str]:
        """
        List objects in an S3 bucket with pagination support.
        
        Args:
            bucket: S3 bucket name
            prefix: Prefix to filter results
            delimiter: Delimiter for hierarchy (e.g., '/' for folders)
            
        Returns:
            list: List of object keys
        """
        objects = []
        paginator = self.client.get_paginator('list_objects_v2')
        
        # Set up parameters
        params = {'Bucket': bucket}
        if prefix:
            params['Prefix'] = prefix
        if delimiter:
            params['Delimiter'] = delimiter
            
        # Use paginator to handle large buckets
        page_iterator = paginator.paginate(**params)
        
        for page in page_iterator:
            if "Contents" in page:
                for obj in page['Contents']:
                    objects.append(obj['Key'])
                    
        return objects
    
    def list_folders(self, bucket: str, prefix: str = "") -> List[str]:
        """
        List folders (common prefixes) in an S3 bucket.
        
        Args:
            bucket: S3 bucket name
            prefix: Prefix to filter results
            
        Returns:
            list: List of folder names without trailing delimiter
        """
        try:
            params = {
                'Bucket': bucket,
                'Delimiter': '/'
            }
            
            if prefix:
                params['Prefix'] = prefix
                
            response = self.client.list_objects_v2(**params)
            
            folders = []
            if 'CommonPrefixes' in response:
                for common_prefix in response['CommonPrefixes']:
                    # Remove trailing slash
                    folder = common_prefix['Prefix']
                    if folder.endswith('/'):
                        folder = folder[:-1]
                    folders.append(folder)
                    
            return folders
        except Exception as e:
            print(f"Error listing folders: {e}")
            return []