"""
GCP Session Manager

A lightweight, portable Google Cloud Platform client manager implementing the Singleton pattern.
Provides multiple authentication methods and properly configured service clients.

Dependencies:
    - google-cloud-<service> packages
    - google-auth
    - os
    - logging
"""

import os
import logging
from typing import Any, Dict, Optional

from google.auth import default
from google.auth.credentials import Credentials
from google.auth.transport.requests import Request
from google.oauth2 import service_account


class GCPManager:
    """
    Singleton class for managing Google Cloud Platform clients with multiple authentication methods.
    
    Implements a hierarchical authentication strategy:
    1. Service account key file (if provided)
    2. Application Default Credentials (ADC)
    3. User account (via gcloud CLI)
    
    Usage:
        # Get instance with default settings
        gcp = GCPManager.instance()
        
        # Get a specific service client
        storage = gcp.get_client('storage')
        # Or via property for common services
        bigquery = gcp.bigquery
        
        # With custom options
        gcp = GCPManager.instance({
            'project_id': 'my-project',
            'credentials_path': '/path/to/service-account.json',
        })
    """
    
    _instance = None
    _clients = {}
    _logger = None
    _credentials = None
    
    def __new__(cls, options: Optional[Dict[str, Any]] = None):
        """
        Get or create the singleton instance.
        
        Args:
            options: Configuration options for GCP clients
        """
        if cls._instance is None:
            cls._instance = super(GCPManager, cls).__new__(cls)
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
            options: Configuration options for GCP clients
        """
        return cls(options)
    
    def _initialize(self, options: Dict[str, Any]):
        """Initialize the GCP manager instance."""
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
        
        # Set project ID (from options, env var, or ADC)
        self.project_id = options.get('project_id') or os.getenv('GOOGLE_CLOUD_PROJECT')
        
        # Initialize credentials
        self._init_credentials()
    
    def _update_options(self, options: Dict[str, Any]):
        """Update configuration with new options."""
        self._options.update(options)
        
        # Update project ID if provided
        if 'project_id' in options:
            self.project_id = options['project_id']
            
        # Refresh credentials if credentials path changed
        if 'credentials_path' in options:
            self._init_credentials()
            self._clients = {}  # Clear client cache
    
    def _init_credentials(self):
        """Initialize GCP credentials using authentication hierarchy."""
        try:
            # 1. Use service account key file if provided
            credentials_path = self._options.get('credentials_path') or os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
            if credentials_path:
                self._logger.debug(f"Using service account credentials from: {credentials_path}")
                self._credentials = service_account.Credentials.from_service_account_file(
                    credentials_path,
                    scopes=["https://www.googleapis.com/auth/cloud-platform"]
                )
                
                # Set project ID from credentials if not already set
                if not self.project_id and hasattr(self._credentials, 'project_id'):
                    self.project_id = self._credentials.project_id
                    
                return
            
            # 2. Use Application Default Credentials (ADC)
            self._logger.debug("Using Application Default Credentials")
            self._credentials, project_id = default()
            
            # Set project ID from ADC if not already set
            if not self.project_id and project_id:
                self.project_id = project_id
                
            # Refresh credentials if needed
            if hasattr(self._credentials, 'valid') and not self._credentials.valid:
                self._credentials.refresh(Request())
                
        except Exception as e:
            self._logger.error(f"Failed to initialize GCP credentials: {e}")
            raise
    
    def get_credentials(self, refresh: bool = False) -> Credentials:
        """
        Get existing credentials or initialize new ones if needed.
        
        Args:
            refresh: Force initialization of new credentials
        """
        if self._credentials is None or refresh:
            self._init_credentials()
        return self._credentials
    
    def get_client(self, service_name: str) -> Any:
        """
        Get or create a GCP service client.
        
        Args:
            service_name: Name of GCP service (e.g., 'storage', 'bigquery')
            
        Returns:
            GCP service client
            
        Note:
            The appropriate google-cloud-<service> package must be installed.
        """
        if service_name not in self._clients:
            # Import the appropriate client library dynamically
            try:
                credentials = self.get_credentials()
                
                if service_name == 'storage':
                    from google.cloud import storage
                    self._clients[service_name] = storage.Client(
                        project=self.project_id,
                        credentials=credentials
                    )
                    
                elif service_name == 'bigquery':
                    from google.cloud import bigquery
                    self._clients[service_name] = bigquery.Client(
                        project=self.project_id,
                        credentials=credentials
                    )
                    
                elif service_name == 'pubsub':
                    from google.cloud import pubsub_v1
                    self._clients[service_name] = {
                        'publisher': pubsub_v1.PublisherClient(credentials=credentials),
                        'subscriber': pubsub_v1.SubscriberClient(credentials=credentials)
                    }
                    
                elif service_name == 'datastore':
                    from google.cloud import datastore
                    self._clients[service_name] = datastore.Client(
                        project=self.project_id,
                        credentials=credentials
                    )
                    
                elif service_name == 'firestore':
                    from google.cloud import firestore
                    self._clients[service_name] = firestore.Client(
                        project=self.project_id,
                        credentials=credentials
                    )
                    
                elif service_name == 'spanner':
                    from google.cloud import spanner
                    self._clients[service_name] = spanner.Client(
                        project=self.project_id,
                        credentials=credentials
                    )
                    
                elif service_name == 'translate':
                    from google.cloud import translate_v2 as translate
                    self._clients[service_name] = translate.Client(
                        credentials=credentials
                    )
                    
                elif service_name == 'logging':
                    from google.cloud import logging
                    self._clients[service_name] = logging.Client(
                        project=self.project_id,
                        credentials=credentials
                    )
                    
                elif service_name == 'monitoring':
                    from google.cloud import monitoring_v3
                    self._clients[service_name] = monitoring_v3.MetricServiceClient()(
                        credentials=credentials
                    )
                    
                elif service_name == 'secretmanager':
                    from google.cloud import secretmanager
                    self._clients[service_name] = secretmanager.SecretManagerServiceClient(
                        credentials=credentials
                    )
                    
                else:
                    raise ValueError(f"Unsupported service: {service_name}")
                    
            except ImportError as e:
                self._logger.error(f"Failed to import client library for {service_name}: {e}")
                raise ImportError(f"You need to install google-cloud-{service_name} package")
                
            except Exception as e:
                self._logger.error(f"Failed to create {service_name} client: {e}")
                raise
                
        return self._clients[service_name]
    
    def refresh_credentials(self):
        """Force initialization of new credentials."""
        return self.get_credentials(refresh=True)
    
    # Properties for common GCP services
    @property
    def storage(self):
        """Get Cloud Storage client."""
        return self.get_client('storage')
    
    @property
    def bigquery(self):
        """Get BigQuery client."""
        return self.get_client('bigquery')
    
    @property
    def pubsub(self):
        """Get Pub/Sub clients (publisher and subscriber)."""
        return self.get_client('pubsub')
    
    @property
    def datastore(self):
        """Get Datastore client."""
        return self.get_client('datastore')
    
    @property
    def firestore(self):
        """Get Firestore client."""
        return self.get_client('firestore')
    
    @property
    def spanner(self):
        """Get Spanner client."""
        return self.get_client('spanner')
    
    @property
    def secretmanager(self):
        """Get Secret manager client."""
        return self.get_client('secretmanager')
    
    
if __name__ == "__main__":
    # Get the singleton instance
    gcp = GCPManager.instance()

    # Access services
    storage = gcp.storage
    bigquery = gcp.bigquery

    # Access Pub/Sub (returns both publisher and subscriber)
    publisher = gcp.pubsub['publisher']
    subscriber = gcp.pubsub['subscriber']

    # With custom configuration
    gcp = GCPManager.instance({
        'project_id': 'my-gcp-project',
        'credentials_path': '/path/to/service-account.json',
    })