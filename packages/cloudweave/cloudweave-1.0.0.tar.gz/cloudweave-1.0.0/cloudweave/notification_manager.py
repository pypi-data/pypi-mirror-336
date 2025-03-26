"""
Notification Manager
A unified notification service that supports multiple email providers and template storage.
"""

import os
import sys
from typing import Dict, Any, Optional, List, Union, Tuple

# Import Logger for proper logging
from cloudweave.logging_manager import Logger, LoggerType

class NotificationManager:
    """
    A unified notification manager that provides email notifications through
    multiple backend providers (AWS SES, Google Gmail) with support for templates
    stored in cloud storage (S3, GCS).
    """

    def __init__(self, options: Dict[str, Any] = {}):
        """
        Initialize the NotificationManager with configuration options.
        
        Args:
            options (dict): Configuration options including:
                - default_provider: Default email provider to use ('aws' or 'google')
                - aws_options: Configuration for AWS email service
                - google_options: Configuration for Google email service
                - storage_options: Storage configuration options
                - logger_options: Logger configuration options
        """
        # Set up logger
        logger_options = options.get('logger_options', {})
        logger_type = logger_options.get('logger_type', 'local')
        
        self.logger = Logger(
            logger_type=logger_type,
            namespace=logger_options.get('namespace', 'notification-manager'),
            instance_id=logger_options.get('instance_id'),
            log_level=logger_options.get('log_level', 'info')
        )
        
        # Set default provider
        self.default_provider = options.get('default_provider', 'aws')
        
        # Store provider options
        self.aws_options = options.get('aws_options', {})
        self.google_options = options.get('google_options', {})
        self.storage_options = options.get('storage_options', {})
        
        # Initialize email service instances
        self._email_services = {}
        self._initialize_email_services()
        
        # Initialize storage instances
        self._storage_instances = {}
        self._initialize_storage_instances()
        
        self.logger.info(f"NotificationManager initialized with default provider: {self.default_provider}")
    
    def _initialize_email_services(self):
        """Initialize email service instances for supported providers."""
        # Initialize AWS email service if options provided
        if self.aws_options:
            try:
                from cloudweave.notification_utils import AWSEmailService
                self._email_services['aws'] = AWSEmailService(self.aws_options)
                self.logger.info("AWS Email Service initialized")
            except Exception as e:
                self.logger.error(f"Failed to initialize AWS Email Service: {e}")
        
        # Initialize Google email service if options provided
        if self.google_options:
            try:
                from cloudweave.notification_utils import GCPEmailService
                self._email_services['google'] = GCPEmailService(self.google_options)
                self.logger.info("Google Email Service initialized")
            except Exception as e:
                self.logger.error(f"Failed to initialize Google Email Service: {e}")
    
    def _initialize_storage_instances(self):
        """Initialize storage instances for template retrieval."""
        # Create storage instances based on configuration
        if not self.storage_options:
            return
            
        from storage_manager import Storage, StorageType
        
        # Initialize S3 storage if configured
        if 's3' in self.storage_options:
            try:
                s3_config = self.storage_options.get('s3', {})
                self._storage_instances['s3'] = Storage(
                    storage_type=StorageType.S3,
                    namespace=s3_config.get('namespace', 'notifications'),
                    instance_id='s3-templates',
                    **s3_config
                )
                self.logger.info("S3 Storage initialized for templates")
            except Exception as e:
                self.logger.error(f"Failed to initialize S3 Storage: {e}")
        
        # Initialize GCS storage if configured
        if 'gcs' in self.storage_options:
            try:
                gcs_config = self.storage_options.get('gcs', {})
                self._storage_instances['gcs'] = Storage(
                    storage_type=StorageType.GCS,
                    namespace=gcs_config.get('namespace', 'notifications'),
                    instance_id='gcs-templates',
                    **gcs_config
                )
                self.logger.info("GCS Storage initialized for templates")
            except Exception as e:
                self.logger.error(f"Failed to initialize GCS Storage: {e}")
    
    def get_service(self, provider: Optional[str] = None) -> Any:
        """
        Get the email service instance for the specified provider.
        
        Args:
            provider: Provider name ('aws' or 'google'), defaults to default_provider
            
        Returns:
            Email service instance
            
        Raises:
            ValueError: If provider is not supported or not initialized
        """
        provider = provider or self.default_provider
        
        if provider not in self._email_services:
            available = list(self._email_services.keys())
            error_msg = f"Provider '{provider}' not available. Available providers: {available}"
            self.logger.error(error_msg)
            raise ValueError(error_msg)
            
        return self._email_services[provider]
    
    def get_storage(self, storage_type: str) -> Any:
        """
        Get the storage instance for the specified type.
        
        Args:
            storage_type: Storage type ('s3' or 'gcs')
            
        Returns:
            Storage instance
            
        Raises:
            ValueError: If storage type is not supported or not initialized
        """
        if storage_type not in self._storage_instances:
            available = list(self._storage_instances.keys())
            error_msg = f"Storage type '{storage_type}' not available. Available types: {available}"
            self.logger.error(error_msg)
            raise ValueError(error_msg)
            
        return self._storage_instances[storage_type]
    
    def _get_template_content(self, template_info: Dict[str, Any]) -> Optional[str]:
        """
        Retrieve template content from storage.
        
        Args:
            template_info: Template information dictionary containing:
                - storage_type: Storage type ('s3' or 'gcs')
                - bucket: Storage bucket name
                - path: Template path in bucket
                
        Returns:
            Template content as string or None if retrieval failed
        """
        # Extract template location information
        storage_type = template_info.get('storage_type', 's3').lower()
        bucket = template_info.get('bucket')
        path = template_info.get('path')
        
        if not bucket or not path:
            self.logger.error("Missing bucket or path for template retrieval")
            return None
        
        # Get storage instance
        try:
            storage = self.get_storage(storage_type)
        except ValueError as e:
            self.logger.error(f"Storage error: {e}")
            return None
        
        # Read template content
        try:
            content = storage.read_file(bucket, path)
            if content:
                self.logger.info(f"Successfully retrieved template from {storage_type}://{bucket}/{path}")
            else:
                self.logger.error(f"Template at {storage_type}://{bucket}/{path} is empty or not found")
            return content
        except Exception as e:
            self.logger.error(f"Failed to read template from {storage_type}: {e}")
            return None
    
    def _apply_template_variables(self, template: str, variables: Dict[str, Any]) -> str:
        """
        Apply variables to a template string.
        
        Args:
            template: Template content
            variables: Variables to substitute
            
        Returns:
            Processed template
        """
        if not template or not variables:
            return template
            
        result = template
        for key, value in variables.items():
            placeholder = f"{{{{ {key} }}}}"
            result = result.replace(placeholder, str(value))
            
        self.logger.debug(f"Applied {len(variables)} variables to template")
        return result
    
    def send_email(self, 
                 recipient: str, 
                 subject: str, 
                 body: Union[str, Dict[str, Any]], 
                 options: Dict[str, Any] = {}) -> bool:
        """
        Send an email notification.
        
        Args:
            recipient: Email recipient
            subject: Email subject
            body: Email body content, which can be:
                - str: Direct text/HTML content
                - dict: Template reference with optional variables
            options: Additional options including:
                - provider: Email provider to use ('aws' or 'google')
                - sender: Sender email address
                - is_html: Whether body content is HTML (default: False)
                - template_variables: Variables for template substitution
                
        Returns:
            bool: True if sent successfully, False otherwise
        """
        # Extract options
        provider = options.get('provider', self.default_provider)
        sender = options.get('sender')
        is_html = options.get('is_html', False)
        template_variables = options.get('template_variables', {})
        
        self.logger.info(f"Sending email to {recipient} using {provider} provider")
        
        try:
            # Get email service
            service = self.get_service(provider)
            
            # Process body content
            if isinstance(body, dict) and 'template' in body:
                # Handle template retrieval
                template_info = body['template']
                self.logger.info(f"Using template from {template_info.get('storage_type', 's3')}://{template_info.get('bucket')}/{template_info.get('path')}")
                
                template_content = self._get_template_content(template_info)
                
                if not template_content:
                    self.logger.error("Failed to retrieve template content")
                    return False
                
                # Apply template variables
                processed_body = self._apply_template_variables(template_content, template_variables)
                is_html = True  # Templates are assumed to be HTML
            else:
                # Use body content directly
                processed_body = body
                body_preview = str(body)[:50] + "..." if len(str(body)) > 50 else str(body)
                self.logger.debug(f"Using direct body content: {body_preview}")
            
            # Send email
            result = service.send(
                recipient=recipient,
                subject=subject,
                body=processed_body,
                is_html=is_html,
                sender=sender
            )
            
            if result:
                self.logger.info(f"Successfully sent email to {recipient}")
            else:
                self.logger.error(f"Failed to send email to {recipient}")
                
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to send email: {e}")
            return False
    
    def send_batch_email(self, 
                       recipients: List[str], 
                       subject: str, 
                       body: Union[str, Dict[str, Any]], 
                       options: Dict[str, Any] = {}) -> Dict[str, bool]:
        """
        Send an email to multiple recipients.
        
        Args:
            recipients: List of email addresses
            subject: Email subject
            body: Email body (see send_email)
            options: Additional options (see send_email)
            
        Returns:
            dict: Mapping of recipient to success status
        """
        recipient_count = len(recipients)
        self.logger.info(f"Sending batch email to {recipient_count} recipients")
        
        results = {}
        
        for recipient in recipients:
            results[recipient] = self.send_email(
                recipient=recipient,
                subject=subject,
                body=body,
                options=options
            )
            
        success_count = sum(1 for success in results.values() if success)
        self.logger.info(f"Batch email results: {success_count}/{recipient_count} successful")
        
        return results
    
    def add_provider(self, provider: str, options: Dict[str, Any]) -> bool:
        """
        Add or update an email provider.
        
        Args:
            provider: Provider name ('aws' or 'google')
            options: Provider configuration options
            
        Returns:
            bool: True if provider was added successfully, False otherwise
        """
        self.logger.info(f"Adding/updating {provider} email provider")
        
        try:
            if provider == 'aws':
                from cloudweave.notification_utils import AWSEmailService
                self._email_services['aws'] = AWSEmailService(options)
            elif provider == 'google':
                from cloudweave.notification_utils import GCPEmailService
                self._email_services['google'] = GCPEmailService(options)
            else:
                self.logger.error(f"Unsupported provider: {provider}")
                return False
                
            self.logger.info(f"{provider.title()} Email Service added/updated")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to add {provider} provider: {e}")
            return False
    
    def add_storage(self, storage_type: str, options: Dict[str, Any]) -> bool:
        """
        Add or update a storage instance.
        
        Args:
            storage_type: Storage type ('s3' or 'gcs')
            options: Storage configuration options
            
        Returns:
            bool: True if storage was added successfully, False otherwise
        """
        self.logger.info(f"Adding/updating {storage_type} storage")
        
        try:
            from cloudweave.storage_manager import Storage, StorageType, create_storage_with_logger
            
            if storage_type == 's3':
                self._storage_instances['s3'] = create_storage_with_logger(
                    storage_type="s3",
                    namespace=options.get('namespace', 'notifications'),
                    instance_id='s3-templates',
                    logger_instance=self.logger,
                    **options
                )
            elif storage_type == 'gcs':
                self._storage_instances['gcs'] = create_storage_with_logger(
                    storage_type="gcs",
                    namespace=options.get('namespace', 'notifications'),
                    instance_id='gcs-templates',
                    logger_instance=self.logger,
                    **options
                )
            else:
                self.logger.error(f"Unsupported storage type: {storage_type}")
                return False
                
            self.logger.info(f"{storage_type.upper()} Storage added/updated")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to add {storage_type} storage: {e}")
            return False
    
    def set_default_provider(self, provider: str) -> bool:
        """
        Set the default email provider.
        
        Args:
            provider: Provider name ('aws' or 'google')
            
        Returns:
            bool: True if default was set, False otherwise
        """
        if provider not in self._email_services:
            available = list(self._email_services.keys())
            self.logger.error(f"Provider '{provider}' not available. Available providers: {available}")
            return False
            
        self.default_provider = provider
        self.logger.info(f"Default provider set to: {provider}")
        return True


# Example usage
if __name__ == "__main__":
    # Initialize notification manager with a logger
    notification_manager = NotificationManager({
        'default_provider': 'aws',
        'aws_options': {
            'region': 'us-east-1',
            'sender_email': 'notifications@example.com'
        },
        'google_options': {
            'sender_email': 'notifications@example.com',
            'credentials_path': '/path/to/service-account.json'
        },
        'storage_options': {
            's3': {
                'region': 'us-east-1',
                'default_bucket': 'notification-templates'
            }
        },
        'logger_options': {
            'logger_type': 'local',
            'namespace': 'notification-manager',
            'log_level': 'info'
        }
    })
    
    # Test sending an email with HTML template from S3
    notification_manager.logger.info("Testing email with HTML template from S3...")
    
    # Template variables for personalization
    template_variables = {
        'logo_url': 'https://cdn.prod.website-files.com/670f21b4cc3080d5a2982789/670f21b4cc3080d5a29827ef_Picture5-removebg-preview-p-500.png',
        'company_name': 'IntelliPat',
        'notification_title': 'Your Novelty Report is Ready!',
        'notification_message': 'Please visit your user dashboard to view the report.',
        'action_link': 'https://console.intellipat.ai/search/reports/abc123',
        'action_text': 'View Report',
        'website_url': 'https://www.intellipat.ai',
        'support_email': 'support@intellipat.ai',
        'current_year': '2025'
    }
    
    # Send the email
    success = notification_manager.send_email(
        recipient="jane.smith@example.com",
        subject="IntelliPat Search Request Update: ",
        body={
            'template': {
                'storage_type': 's3',
                'bucket': 'notification-templates',
                'path': 'email-templates/search-request-done.html'
            }
        },
        options={
            'template_variables': template_variables,
            'provider': 'aws',  # Explicitly use AWS SES
            'sender': 'orders@example.com'  # Override default sender
        }
    )
    
    if success:
        notification_manager.logger.info("✅ Success: Email with S3 HTML template sent successfully")
    else:
        notification_manager.logger.error("❌ Error: Failed to send email with S3 HTML template")
    
    # Optional: Log debug info about available services
    notification_manager.logger.debug("\nAvailable email providers:")
    for provider in notification_manager._email_services:
        notification_manager.logger.debug(f"- {provider}")
    
    notification_manager.logger.debug("\nAvailable storage instances:")
    for storage_type in notification_manager._storage_instances:
        notification_manager.logger.debug(f"- {storage_type}")