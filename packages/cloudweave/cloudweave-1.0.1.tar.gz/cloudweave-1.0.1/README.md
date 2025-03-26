# Cloudweave Utils

A unified, authenticated multi-cloud utility package for seamless integration with various cloud providers.

## Overview

Cloudweave provides a simple, secure interface for working with multiple cloud services through a single authentication point. This package streamlines access to databases, storage, logging, and notification services across AWS, GCP, and other cloud providers.

## Features

- **Single Authentication Point**: Access all cloud services through one authenticated manager
- **Cross-Cloud Support**: Work with multiple cloud providers using consistent interfaces
- **Modular Components**:
  - Database (DynamoDB, Firestore, MongoDB)
  - Storage (S3, GCS)
  - Logging (Local, CloudWatch, GCP Logging, Loki)
  - Notifications (Email via AWS SES, Google Gmail)
- **Secure Access Control**: API key-based authentication for all package functionality
- **Extensible Design**: Easily add support for additional cloud services

## Installation

```bash
pip install cloudweave
```

## Quick Start

```python
from cloudweave import get_auth_manager, DatabaseType, StorageType, LoggerType

# Initialize with your API key
auth = get_auth_manager("your-secret-api-key")

# Get a logger
logger = auth.get_logger(
    logger_type=LoggerType.LOCAL,
    namespace="my_app",
    log_level="info"
)

# Get a database
db = auth.get_database(
    db_type=DatabaseType.FIRESTORE,
    namespace="my_app",
    project_id="my-gcp-project"
)

# Get a storage instance
storage = auth.get_storage(
    storage_type=StorageType.S3,
    namespace="my_app",
    region="us-east-1",
    default_bucket="my-bucket"
)

# Log something
logger.info("Application started")

# Use the storage
storage.upload_file("local_file.txt", None, "destination_path/file.txt")

# Use the database with Pydantic models
from pydantic import BaseModel

class User(BaseModel):
    id: str = None
    name: str
    email: str

# Register model
db.register_model(User, "users")

# Create a user
user = User(name="Test User", email="test@example.com")
user_id = db.put_item(user)
```

## Components

### Authentication Manager

The central gateway to all package functionality:

```python
# Initialize
auth = get_auth_manager("your-secret-api-key")

# Alternative quick init
from cloudweave import init_auth
auth = init_auth("your-secret-api-key")
```

### Database

Support for multiple database backends with a unified interface:

```python
# Get Firestore instance
firestore_db = auth.get_database(
    db_type=DatabaseType.FIRESTORE,
    namespace="my_app",
    project_id="my-gcp-project"
)

# Get DynamoDB instance
dynamo_db = auth.get_database(
    db_type=DatabaseType.DYNAMODB,
    namespace="my_app",
    opt={"region": "us-east-1"}
)

# Get MongoDB instance
mongo_db = auth.get_database(
    db_type=DatabaseType.MONGODB,
    namespace="my_app",
    connection_string="mongodb://localhost:27017/",
    database_name="myapp"
)
```

### Storage

Unified interface for cloud storage services:

```python
# Get S3 storage
s3 = auth.get_storage(
    storage_type=StorageType.S3,
    namespace="my_app",
    region="us-east-1",
    default_bucket="my-bucket"
)

# Get GCS storage
gcs = auth.get_storage(
    storage_type=StorageType.GCS,
    namespace="my_app",
    project_id="my-gcp-project",
    default_bucket="my-gcs-bucket"
)

# Storage operations
s3.upload_file("local_file.txt", None, "path/in/bucket.txt")
s3.download_file(None, "path/in/bucket.txt", "local_destination.txt")
content = s3.read_file(None, "path/in/bucket.txt")
```

### Logging

Multi-destination logging with a consistent interface:

```python
# Local logging
local_logger = auth.get_logger(
    logger_type=LoggerType.LOCAL,
    namespace="my_app",
    log_level="info",
    log_file="app.log"
)

# AWS CloudWatch logging
aws_logger = auth.get_logger(
    logger_type=LoggerType.AWS,
    namespace="my_app",
    region="us-east-1",
    dimensions={"Service": "API"}
)

# GCP Cloud Logging
gcp_logger = auth.get_logger(
    logger_type=LoggerType.GCP,
    namespace="my_app",
    project_id="my-gcp-project"
)

# Log messages
local_logger.info("Application started")
local_logger.error("Something went wrong", {"path": "/api/users", "status": 500})
```

### Notifications

Email notifications with template support:

```python
# Get notification manager
notifier = auth.get_notification_manager(
    default_provider="aws",
    aws_options={
        "region": "us-east-1",
        "sender_email": "no-reply@example.com"
    }
)

# Send an email
notifier.send_email(
    recipient="user@example.com",
    subject="Welcome to Our Service",
    body="Hello! Thanks for signing up."
)

# Send with HTML template from storage
notifier.send_email(
    recipient="user@example.com",
    subject="Your Report is Ready",
    body={
        "template": {
            "storage_type": "s3",
            "bucket": "email-templates",
            "path": "welcome-email.html"
        }
    },
    options={
        "template_variables": {
            "user_name": "John Doe",
            "company_name": "Example Inc."
        }
    }
)
```

## Development

### Running Tests

```bash
# Test Firestore functionality
python tests/test_firestore.py --api-key "your-secret-api-key" --credentials "path/to/credentials.json"

# Test DynamoDB functionality
python tests/test_dynamodb.py --api-key "your-secret-api-key" --region "us-east-1"

# Test storage functionality
python tests/test_storage.py --api-key "your-secret-api-key" --storage-type "s3" --bucket "my-bucket" --source-path "test.txt" --local-path "downloaded.txt"
```

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Contact

Gabe DiMartino - gdimartino@gabedimartino.com

Project Link: [https://github.com/macbee280/cloudweave](https://github.com/macbee280/cloudweave)
