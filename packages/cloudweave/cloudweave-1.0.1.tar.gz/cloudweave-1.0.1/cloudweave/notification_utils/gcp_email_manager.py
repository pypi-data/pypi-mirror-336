"""
Simple Email Service using Gmail API
Provides a clean interface for sending emails with Google's Gmail API.
"""

import base64
from email.message import EmailMessage
from typing import Optional, Dict, Any, Union
import sys, os

# Import Logger for proper logging
from cloudweave.logging_manager import Logger, LoggerType


class GCPEmailService:
    """
    A simple service for sending emails using Gmail API.
    Supports both HTML and plain text content.
    """

    def __init__(self, options: Dict[str, Any] = {}):
        """
        Initialize the EmailService and set up authentication.
        
        Args:
            options (dict): Configuration options including:
                - sender_email: Default sender email address
                - credentials_path: Path to service account credentials file
                - project_id: Google Cloud project ID
                - logger_instance: Optional logger instance to use
                - log_level: Logging level if creating a new logger
        """
        # Store options
        self.options = options
        
        # Default sender
        self.default_sender = options.get('sender_email', 'noreply@example.com')
        
        # Set up logger
        self.logger = options.get('logger_instance')
        if not self.logger:
            # Create a new logger if one wasn't provided
            log_level = options.get('log_level', 'info')
            self.logger = Logger(
                logger_type=LoggerType.LOCAL,
                namespace="gcp-email-service",
                instance_id=f"gmail-api-{self.default_sender}",
                log_level=log_level
            )
        
        # Initialize GCP Manager for Gmail API connection
        try:
            from cloudweave.cloud_session_utils import GCPManager
            self.gcp = GCPManager.instance({
                'project_id': options.get('project_id'),
                'credentials_path': options.get('credentials_path')
            })
            
            self.logger.info(f"GCP Manager initialized for Gmail API")
        except Exception as e:
            self.logger.error(f"Failed to initialize GCP Manager: {e}")
            raise
        
        # Initialize and authenticate Gmail service
        self._gmail_service = None
        self._authenticate()
    
    def _authenticate(self):
        """
        Authenticate with Gmail API using service account credentials.
        """
        try:
            from googleapiclient.discovery import build
            from google.oauth2 import service_account
            
            self.logger.info("Authenticating with Gmail API")
            
            # Gmail API scopes
            scopes = [
                'https://mail.google.com/',
                'https://www.googleapis.com/auth/gmail.send'
            ]
            
            # Get credentials
            if self.options.get('credentials_path'):
                self.logger.debug(f"Using service account credentials from {self.options.get('credentials_path')}")
                # Use service account with delegation to send as the specified email
                credentials = service_account.Credentials.from_service_account_file(
                    self.options['credentials_path'],
                    scopes=scopes,
                    subject=self.default_sender
                )
            else:
                self.logger.debug("Using GCP Manager credentials")
                # Use GCPManager credentials
                credentials = self.gcp.get_credentials()
            
            # Build Gmail service
            self._gmail_service = build('gmail', 'v1', credentials=credentials)
            self.logger.info("Successfully authenticated with Gmail API")
            
        except Exception as e:
            self.logger.error(f"Authentication with Gmail API failed: {e}")
            raise
    
    def send(self, 
             recipient: str, 
             subject: str, 
             body: str,
             is_html: bool = False,
             sender: Optional[str] = None) -> bool:
        """
        Send an email with Gmail API.
        
        Args:
            recipient (str): Email recipient
            subject (str): Email subject
            body (str): Email body content
            is_html (bool): Whether the body is HTML (default: False)
            sender (str, optional): Sender email (defaults to service default)
            
        Returns:
            bool: True if sent successfully, False otherwise
        """
        try:
            # Set sender email
            sender_email = sender or self.default_sender
            
            self.logger.info(f"Preparing to send email to {recipient} from {sender_email}")
            self.logger.debug(f"Email subject: '{subject[:30]}...' (truncated)")
            self.logger.debug(f"Email format: {'HTML' if is_html else 'Plain text'}")
            
            # Create message
            message = EmailMessage()
            message['To'] = recipient
            message['From'] = sender_email
            message['Subject'] = subject
            
            # Set content based on type
            if is_html:
                message.set_content(body, subtype='html')
                self.logger.debug("Set HTML content for email")
            else:
                message.set_content(body)
                self.logger.debug("Set plain text content for email")
            
            # Encode for Gmail API
            encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            
            # Send message
            self.logger.info(f"Sending email via Gmail API to {recipient}")
            sent_message = self._gmail_service.users().messages().send(
                userId='me',
                body={'raw': encoded_message}
            ).execute()
            
            message_id = sent_message.get('id')
            self.logger.info(f"Email sent successfully, message_id: {message_id}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send email to {recipient}: {e}")
            return False
    
    def send_with_attachment(self,
                            recipient: str,
                            subject: str,
                            body: str,
                            attachments: list,
                            is_html: bool = False,
                            sender: Optional[str] = None) -> bool:
        """
        Send an email with attachments using Gmail API.
        
        Args:
            recipient (str): Email recipient
            subject (str): Email subject
            body (str): Email body content
            attachments (list): List of attachment dictionaries, each containing:
                - filename: Name of the file to attach
                - content: File content (bytes or string)
                - mimetype: MIME type of the file (optional)
            is_html (bool): Whether the body is HTML (default: False)
            sender (str, optional): Sender email (defaults to service default)
            
        Returns:
            bool: True if sent successfully, False otherwise
        """
        try:
            # Set sender email
            sender_email = sender or self.default_sender
            
            self.logger.info(f"Preparing to send email with attachments to {recipient} from {sender_email}")
            self.logger.debug(f"Email subject: '{subject[:30]}...' (truncated)")
            self.logger.debug(f"Email format: {'HTML' if is_html else 'Plain text'}")
            self.logger.debug(f"Number of attachments: {len(attachments)}")
            
            # Create message
            from email.mime.multipart import MIMEMultipart
            from email.mime.text import MIMEText
            from email.mime.application import MIMEApplication
            
            # Create message container
            message = MIMEMultipart()
            message['Subject'] = subject
            message['From'] = sender_email
            message['To'] = recipient
            
            # Create message body
            if is_html:
                # Create both plain text and HTML parts for better compatibility
                # Strip HTML for plain text
                import re
                plain_text = re.sub('<[^<]+?>', '', body)
                
                # Create multipart/alternative for text and HTML versions
                alt_part = MIMEMultipart('alternative')
                alt_part.attach(MIMEText(plain_text, 'plain'))
                alt_part.attach(MIMEText(body, 'html'))
                
                # Attach to main message
                message.attach(alt_part)
                self.logger.debug("Attached both plain text and HTML parts to message")
            else:
                # Just attach plain text
                message.attach(MIMEText(body, 'plain'))
                self.logger.debug("Attached plain text part to message")
            
            # Add attachments
            for i, attachment in enumerate(attachments):
                filename = attachment.get('filename')
                content = attachment.get('content')
                mimetype = attachment.get('mimetype', 'application/octet-stream')
                
                self.logger.debug(f"Processing attachment {i+1}/{len(attachments)}: {filename} ({mimetype})")
                
                # Create attachment part
                if isinstance(content, str):
                    content = content.encode('utf-8')
                    
                att = MIMEApplication(content)
                att.add_header('Content-Disposition', 'attachment', filename=filename)
                
                # Attach to message
                message.attach(att)
                self.logger.debug(f"Added attachment: {filename}")
            
            # Encode for Gmail API
            encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            
            # Send message
            self.logger.info(f"Sending email with attachments via Gmail API to {recipient}")
            sent_message = self._gmail_service.users().messages().send(
                userId='me',
                body={'raw': encoded_message}
            ).execute()
            
            message_id = sent_message.get('id')
            self.logger.info(f"Email with attachment(s) sent successfully, message_id: {message_id}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send email with attachment(s) to {recipient}: {e}")
            return False
    
    def get_send_limits(self) -> Dict[str, Any]:
        """
        Get Gmail API sending limits information.
        These are fixed limits from Google, not dynamic quota.
        
        Returns:
            dict: Dictionary containing limit information
        """
        # Gmail API limits are fixed
        limits = {
            'daily_limit': 2000,  # Gmail API daily sending limit
            'recipient_limit': 100,  # Max recipients per message
            'attachment_size_limit': 25 * 1024 * 1024  # 25MB max attachment size
        }
        
        self.logger.info(f"Retrieved Gmail API sending limits: {limits['daily_limit']} emails per day")
        return limits


# Example usage
if __name__ == "__main__":
    # Initialize logger for testing
    test_logger = Logger(
        logger_type=LoggerType.LOCAL,
        namespace="gcp-email-test",
        instance_id="test-logger",
        log_level="info",
        log_file="gcp_email_test.log"
    )
    
    # Initialize GCP email service with logger
    email_service = GCPEmailService({
        'sender_email': 'notifications@example.com',
        'credentials_path': '/path/to/service-account.json',
        'project_id': 'my-project',
        'logger_instance': test_logger
    })
    
    # Check sending limits
    limits = email_service.get_send_limits()
    test_logger.info(f"Gmail API limits: {limits['daily_limit']} emails per day, {limits['recipient_limit']} recipients per message")
    
    # Send plain text email
    test_logger.info("Testing plain text email...")
    success = email_service.send(
        recipient="user@example.com",
        subject="Plain Text Email",
        body="This is a plain text email body.",
        is_html=False
    )
    
    if success:
        test_logger.info("✅ Plain text email test successful")
    else:
        test_logger.error("❌ Plain text email test failed")
    
    # Send HTML email
    test_logger.info("Testing HTML email...")
    html_body = """
    <html>
        <body>
            <h1>HTML Email</h1>
            <p>This is an <b>HTML</b> email with <span style="color: blue;">formatted</span> content.</p>
        </body>
    </html>
    """
    
    success = email_service.send(
        recipient="user@example.com",
        subject="HTML Email Example",
        body=html_body,
        is_html=True
    )
    
    if success:
        test_logger.info("✅ HTML email test successful")
    else:
        test_logger.error("❌ HTML email test failed")