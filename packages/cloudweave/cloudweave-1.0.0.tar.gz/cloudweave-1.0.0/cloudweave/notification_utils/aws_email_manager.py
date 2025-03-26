"""
Simple Email Service using AWS SES
Provides a clean interface for sending emails with Amazon Simple Email Service.
"""

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, Dict, Any, Union
from mypy_boto3_ses.client import SESClient

# Import Logger for proper logging
from cloudweave.logging_manager import Logger, LoggerType

class AWSEmailService:
    """
    A simple service for sending emails using Amazon SES.
    Supports both HTML and plain text content.
    """

    def __init__(self, options: Dict[str, Any] = {}):
        """
        Initialize the EmailService and set up AWS connection.
        
        Args:
            options (dict): Configuration options including:
                - sender_email: Default sender email address
                - region: AWS region name
                - profile_name: AWS profile name (optional)
                - logger_instance: Optional logger instance to use
                - log_level: Logging level if creating a new logger
        """
        # Store options
        self.options = options
        
        # Default sender
        self.default_sender = options.get('sender_email', 'noreply@example.com')
        
        # AWS region
        self.region = options.get('region', 'us-east-1')
        
        # Set up logger
        self.logger = options.get('logger_instance')
        if not self.logger:
            # Create a new logger if one wasn't provided
            log_level = options.get('log_level', 'info')
            self.logger = Logger(
                logger_type=LoggerType.LOCAL,
                namespace="aws-email-service",
                instance_id=f"aws-ses-{self.region}",
                log_level=log_level
            )
        
        # Initialize AWS Manager for SES connection
        from cloudweave.cloud_session_utils import AWSManager
        
        # Get SES client
        try:
            aws_manager = AWSManager.instance(options)
            self._ses_client: SESClient = aws_manager.get_client("ses")
            self.logger.info(f"AWS SES client initialized in region {self.region}")
        except Exception as e:
            self.logger.error(f"Failed to initialize AWS SES client: {e}")
            raise
    
    def send(self, 
             recipient: str, 
             subject: str, 
             body: str,
             is_html: bool = False,
             sender: Optional[str] = None) -> bool:
        """
        Send an email with AWS SES.
        
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
            
            # Create message container
            message = MIMEMultipart('alternative')
            message['Subject'] = subject
            message['From'] = sender_email
            message['To'] = recipient
            
            # Create text or HTML version
            if is_html:
                # Create both plain text and HTML parts for better compatibility
                # Strip HTML for plain text
                import re
                plain_text = re.sub('<[^<]+?>', '', body)
                text_part = MIMEText(plain_text, 'plain')
                html_part = MIMEText(body, 'html')
                
                # Attach both parts to message
                message.attach(text_part)
                message.attach(html_part)
                self.logger.debug("Attached both plain text and HTML parts to message")
            else:
                # Just attach plain text
                text_part = MIMEText(body, 'plain')
                message.attach(text_part)
                self.logger.debug("Attached plain text part to message")
            
            # Send email
            self.logger.info(f"Sending email via AWS SES to {recipient}")
            response = self._ses_client.send_raw_email(
                Source=sender_email,
                Destinations=[recipient],
                RawMessage={
                    'Data': message.as_string()
                }
            )
            
            message_id = response.get('MessageId')
            self.logger.info(f"Email sent successfully, message_id: {message_id}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send email to {recipient}: {e}")
            return False
    
    def send_template(self,
                      recipient: str,
                      subject: str,
                      template_name: str,
                      template_data: Dict[str, Any],
                      sender: Optional[str] = None) -> bool:
        """
        Send an email using an AWS SES template.
        
        Args:
            recipient (str): Email recipient
            subject (str): Email subject
            template_name (str): Name of the SES template to use
            template_data (dict): Template data for variable substitution
            sender (str, optional): Sender email (defaults to service default)
            
        Returns:
            bool: True if sent successfully, False otherwise
        """
        try:
            # Set sender email
            sender_email = sender or self.default_sender
            
            self.logger.info(f"Preparing to send template email to {recipient} from {sender_email}")
            self.logger.debug(f"Using template: {template_name}")
            self.logger.debug(f"Template data keys: {list(template_data.keys())}")
            
            # Format template data as JSON
            formatted_data = self._format_template_data(template_data)
            
            # Send templated email
            self.logger.info(f"Sending templated email via AWS SES to {recipient}")
            response = self._ses_client.send_templated_email(
                Source=sender_email,
                Destination={
                    'ToAddresses': [recipient]
                },
                Template=template_name,
                TemplateData=formatted_data
            )
            
            message_id = response.get('MessageId')
            self.logger.info(f"Template email sent successfully, message_id: {message_id}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send template email to {recipient}: {e}")
            return False
    
    def _format_template_data(self, template_data: Dict[str, Any]) -> str:
        """
        Format template data dictionary as JSON string.
        
        Args:
            template_data (dict): Template data dictionary
            
        Returns:
            str: JSON-formatted template data
        """
        import json
        return json.dumps(template_data)
    
    def send_with_attachment(self,
                            recipient: str,
                            subject: str,
                            body: str,
                            attachments: list,
                            is_html: bool = False,
                            sender: Optional[str] = None) -> bool:
        """
        Send an email with attachments.
        
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
            
            # Create message container
            message = MIMEMultipart()
            message['Subject'] = subject
            message['From'] = sender_email
            message['To'] = recipient
            
            # Create message body part
            message_body = MIMEMultipart('alternative')
            
            # Create text or HTML version
            if is_html:
                # Create both plain text and HTML parts for better compatibility
                # Strip HTML for plain text
                import re
                plain_text = re.sub('<[^<]+?>', '', body)
                text_part = MIMEText(plain_text, 'plain')
                html_part = MIMEText(body, 'html')
                
                # Attach both parts to message body
                message_body.attach(text_part)
                message_body.attach(html_part)
                self.logger.debug("Attached both plain text and HTML parts to message")
            else:
                # Just attach plain text
                text_part = MIMEText(body, 'plain')
                message_body.attach(text_part)
                self.logger.debug("Attached plain text part to message")
            
            # Attach message body to container
            message.attach(message_body)
            
            # Add attachments
            from email.mime.application import MIMEApplication
            
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
            
            # Send email
            self.logger.info(f"Sending email with attachments via AWS SES to {recipient}")
            response = self._ses_client.send_raw_email(
                Source=sender_email,
                Destinations=[recipient],
                RawMessage={
                    'Data': message.as_string()
                }
            )
            
            message_id = response.get('MessageId')
            self.logger.info(f"Email with attachment(s) sent successfully, message_id: {message_id}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send email with attachment(s) to {recipient}: {e}")
            return False

    def verify_email_identity(self, email: str) -> bool:
        """
        Verify an email address with AWS SES.
        
        Args:
            email (str): Email address to verify
            
        Returns:
            bool: True if verification email was sent successfully, False otherwise
        """
        try:
            self.logger.info(f"Sending verification email to {email}")
            self._ses_client.verify_email_identity(EmailAddress=email)
            self.logger.info(f"Verification email sent to {email}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to send verification email to {email}: {e}")
            return False
    
    def get_send_quota(self) -> Dict[str, Union[float, int]]:
        """
        Get AWS SES sending quota information.
        
        Returns:
            dict: Dictionary containing quota information
        """
        try:
            self.logger.info("Retrieving AWS SES send quota")
            response = self._ses_client.get_send_quota()
            quota = {
                'max_24_hour_send': response.get('Max24HourSend'),
                'sent_last_24_hours': response.get('SentLast24Hours'),
                'send_rate': response.get('MaxSendRate')
            }
            self.logger.info(f"Quota retrieved: {quota['sent_last_24_hours']}/{quota['max_24_hour_send']} emails sent (rate: {quota['send_rate']}/sec)")
            return quota
        except Exception as e:
            self.logger.error(f"Failed to retrieve send quota: {e}")
            return {
                'max_24_hour_send': 0,
                'sent_last_24_hours': 0,
                'send_rate': 0
            }


# Example usage
if __name__ == "__main__":
    # Initialize logger for testing
    test_logger = Logger(
        logger_type=LoggerType.LOCAL,
        namespace="aws-email-test",
        instance_id="test-logger",
        log_level="info",
        log_file="aws_email_test.log"
    )
    
    # Initialize AWS email service with logger
    email_service = AWSEmailService({
        'sender_email': 'notifications@example.com',
        'region': 'us-east-1',
        'profile_name': 'default',  # Optional: Use specific AWS profile
        'logger_instance': test_logger
    })
    
    # Check sending quota
    quota = email_service.get_send_quota()
    test_logger.info(f"Current SES quota: {quota['sent_last_24_hours']}/{quota['max_24_hour_send']} emails sent")
    
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