import boto3
import os
import logging
from botocore.config import Config
from botocore.exceptions import ClientError, NoCredentialsError, NoRegionError, ProfileNotFound
from typing import Any, Dict, Optional
from mypy_boto3_ecs.client import ECSClient
from mypy_boto3_ec2.client import EC2Client
from mypy_boto3_autoscaling.client import AutoScalingClient
from mypy_boto3_dynamodb import DynamoDBClient
from mypy_boto3_sqs.client import SQSClient
from mypy_boto3_s3.client import S3Client


class AWSManager:
    """
    Singleton class for managing AWS sessions and clients with multiple authentication methods.
    
    Implements a hierarchical authentication strategy:
    1. Temporary credentials (if provided)
    2. Environment variables
    3. Specified AWS profile
    4. Default credentials (instance role, etc.)
    
    Usage:
        # Get instance with default settings
        aws = AWSManager.instance()
        
        # Use a specific service
        dynamodb = aws.get_client('dynamodb')
        # Or via property for common services
        ec2 = aws.ec2
        
        # With custom options
        aws = AWSManager.instance({
            'region': 'us-west-2',
            'profile': 'dev',
        })
    """
    
    _instance = None
    _session = None
    _clients: Dict[str, Any] = {}
    _logger = None
    
    def __new__(cls, options: Optional[Dict[str, Any]] = None):
        """
        Get or create the singleton instance.
        
        Args:
            options: Configuration options for AWS session
        """
        if cls._instance is None:
            cls._instance = super(AWSManager, cls).__new__(cls)
            cls._instance._initialize(options or {})
        elif options:
            # Update existing instance with new options
            cls._instance._update_options(options)
        return cls._instance
    
    @classmethod
    def instance(cls, options: Optional[Dict[str, Any]] = None):
        """
        Get or create the singleton instance.
        
        Args:
            options: Configuration options for AWS session
        """
        return cls(options)
    
    def _initialize(self, options: Dict[str, Any]):
        """Initialize the AWS manager instance."""
        # Set up logger
        self._logger = logging.getLogger(__name__)
        if not self._logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self._logger.addHandler(handler)
            self._logger.setLevel(logging.INFO)
        
        # Store options
        self._options = options
        self._clients = {}
        
        # Set region (from options, env var, or default)
        self.region = options.get('region') or os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
        
        # Configure client settings
        self._client_config = Config(
            retries={'max_attempts': options.get('retry_attempts', 3)},
            max_pool_connections=options.get('pool_connections', 10),
            connect_timeout=options.get('timeout', 30),
            read_timeout=options.get('timeout', 30),
            region_name=self.region
        )
    
    def _update_options(self, options: Dict[str, Any]):
        """Update configuration with new options."""
        self._options.update(options)
        
        # Update region if provided
        if 'region' in options:
            self.region = options['region']
            self._client_config = Config(
                retries={'max_attempts': self._options.get('retry_attempts', 3)},
                max_pool_connections=self._options.get('pool_connections', 10),
                connect_timeout=self._options.get('timeout', 30),
                read_timeout=self._options.get('timeout', 30),
                region_name=self.region
            )
            
            # Clear session and clients when region changes
            self._session = None
            self._clients = {}
    
    def get_session(self, refresh: bool = False):
        """
        Get existing session or create new one if needed.
        
        Args:
            refresh: Force creation of new session
        """
        if self._session is None or refresh:
            self._create_session()
        return self._session
    
    def _create_session(self):
        """Create AWS session using authentication hierarchy."""
        region = self.region
        profile = self._options.get('profile', os.getenv('AWS_PROFILE'))
        
        try:
            # 1. Use temporary credentials if provided
            if all(key in self._options for key in ['aws_access_key_id', 'aws_secret_access_key']):
                self._logger.debug("Using provided credentials")
                self._session = boto3.Session(
                    aws_access_key_id=self._options['aws_access_key_id'],
                    aws_secret_access_key=self._options['aws_secret_access_key'],
                    aws_session_token=self._options.get('aws_session_token'),
                    region_name=region
                )
                return
            
            # 2. Use environment variables if available
            if os.getenv('AWS_ACCESS_KEY_ID') and os.getenv('AWS_SECRET_ACCESS_KEY'):
                self._logger.debug("Using environment variable credentials")
                self._session = boto3.Session(region_name=region)
                return
            
            # 3. Use specified profile
            if profile:
                try:
                    self._logger.debug(f"Using profile: {profile}")
                    self._session = boto3.Session(profile_name=profile, region_name=region)
                    return
                except ProfileNotFound:
                    self._logger.warning(f"Profile {profile} not found, falling back to default")
            
            # 4. Use default credentials
            self._logger.debug("Using default credentials")
            self._session = boto3.Session(region_name=region)
            
        except (NoCredentialsError, NoRegionError) as e:
            self._logger.error(f"Failed to create session: {e}")
            raise
    
    def get_client(self, service_name: str) -> Any:
        """
        Get or create an AWS service client.
        
        Args:
            service_name: Name of AWS service (e.g., 's3', 'dynamodb')
        """
        # Create new client if it doesn't exist
        if service_name not in self._clients:
            session = self.get_session()
            self._clients[service_name] = session.client(
                service_name, 
                config=self._client_config
            )
        return self._clients[service_name]
    
    def refresh_session(self):
        """Force creation of new session."""
        return self.get_session(refresh=True)
    
    # Properties for common AWS services
    @property
    def s3(self) -> S3Client:
        """Get S3 client."""
        return self.get_client('s3')
    
    @property
    def ecs(self) -> ECSClient:
        """Get ECS client."""
        return self.get_client('ecs')
        
    @property
    def ec2(self) -> EC2Client:
        """Get EC2 client."""
        return self.get_client('ec2')
        
    @property
    def asg(self) -> AutoScalingClient:
        """Get AutoScaling client."""
        return self.get_client('autoscaling')
        
    @property
    def sqs(self) -> SQSClient:
        """Get SQS client."""
        return self.get_client('sqs')
        
    @property
    def dynamodb(self) -> DynamoDBClient:
        """Get DynamoDB client."""
        return self.get_client('dynamodb')