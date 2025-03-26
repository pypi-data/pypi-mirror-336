"""
Test script for the NotificationManager
"""

import os, sys
import argparse
from typing import Dict, Any

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from cloudweave.logging_manager import Logger, LoggerType
from cloudweave.notification_manager import NotificationManager

def test_email_template(
    storage_type: str,
    bucket_name: str,
    template_path: str,
    recipient_email: str,
    subject: str,
    email_provider: str = "aws",
    region: str = "us-east-2",
    sender_email: str = "notifications@example.com"
) -> bool:
    """
    Test sending an email using a template from storage.
    
    Args:
        storage_type: Storage type ('s3' or 'gcs')
        bucket_name: Storage bucket name
        template_path: Path to the template in the bucket
        recipient_email: Email address to send the test to
        subject: Email subject
        email_provider: Email provider to use ('aws' or 'google')
        region: AWS region (for S3 and AWS SES)
        sender_email: Sender email address
        
    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    # Create logger for this test
    logger = Logger(
        logger_type=LoggerType.LOCAL,
        namespace="notification-test",
        instance_id="test-logger",
        log_level="info",
        log_file="logs/notification_test.log"
    )
    
    logger.info("=" * 50)
    logger.info(f"Starting email template test using {storage_type} and {email_provider}")
    logger.info(f"Template: {bucket_name}/{template_path}")
    logger.info(f"Recipient: {recipient_email}")
    
    # Configure notification manager
    config = {
        'default_provider': email_provider,
        'logger_options': {
            'logger_type': 'local',
            'namespace': 'notification-test',
            'log_level': 'info'
        }
    }
    
    # Set provider-specific options
    if email_provider == 'aws':
        config['aws_options'] = {
            'region': region,
            'sender_email': sender_email
        }
    elif email_provider == 'google':
        config['google_options'] = {
            'sender_email': sender_email,
            'credentials_path': os.environ.get('GOOGLE_CREDENTIALS_PATH', '')
        }
    
    # Set storage options
    config['storage_options'] = {}
    
    if storage_type == 's3':
        config['storage_options']['s3'] = {
            'region': region,
            'default_bucket': bucket_name
        }
    elif storage_type == 'gcs':
        config['storage_options']['gcs'] = {
            'project_id': os.environ.get('GCP_PROJECT_ID', ''),
            'default_bucket': bucket_name
        }
    
    # Initialize notification manager
    try:
        notification_manager = NotificationManager(config)
    except Exception as e:
        logger.error(f"Failed to initialize NotificationManager: {e}")
        return False
    
    # Template variables for testing
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
    
    # Send the test email
    success = notification_manager.send_email(
        recipient=recipient_email,
        subject=subject,
        body={
            'template': {
                'storage_type': storage_type,
                'bucket': bucket_name,
                'path': template_path
            }
        },
        options={
            'template_variables': template_variables,
            'provider': email_provider,
            'sender': sender_email
        }
    )
    
    if success:
        logger.info("✅ Test successful: Email was sent")
    else:
        logger.error("❌ Test failed: Email was not sent")
    
    logger.info("=" * 50)
    return success


if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Test notification manager")
    parser.add_argument("--storage-type", choices=["s3", "gcs"], required=True,
                      help="Storage type for templates (s3 or gcs)")
    parser.add_argument("--bucket", required=True,
                      help="Bucket name for templates")
    parser.add_argument("--template-path", required=True,
                      help="Path to email template in the bucket")
    parser.add_argument("--recipient", required=True,
                      help="Recipient email address")
    parser.add_argument("--subject", default="Test Email from Notification Manager",
                      help="Email subject")
    parser.add_argument("--provider", choices=["aws", "google"], default="aws",
                      help="Email provider to use (aws or google)")
    parser.add_argument("--region", default="us-east-1",
                      help="AWS region (for S3 and AWS SES)")
    parser.add_argument("--sender", default="notifications@example.com",
                      help="Sender email address")
    
    args = parser.parse_args()
    
    # Run the test
    success = test_email_template(
        storage_type=args.storage_type,
        bucket_name=args.bucket,
        template_path=args.template_path,
        recipient_email=args.recipient,
        subject=args.subject,
        email_provider=args.provider,
        region=args.region,
        sender_email=args.sender
    )
    
    # Exit with appropriate status code
    exit(0 if success else 1)