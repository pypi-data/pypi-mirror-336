from setuptools import setup, find_packages
import os

from cloudweave.metadata import __version__, __author__, __email__, __description__

# Read the requirements file
requirements = []
req_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "requirements.txt")
try:
    with open(req_path, "r") as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]
except FileNotFoundError:
    requirements = [
        # Core dependencies
        "pydantic>=2.0.0",
        "typing-extensions>=4.0.0",

        # AWS dependencies
        "boto3>=1.26.0",
        "botocore>=1.29.0",
        "mypy_boto3_ecs",
        "mypy_boto3_ec2",
        "mypy_boto3_autoscaling",
        "mypy_boto3_dynamodb",
        "mypy_boto3_sqs",
        "mypy_boto3_s3",
        "mypy_boto3_secretsmanager",
        "mypy_boto3_ses",
        "mypy_boto3_logs",
        "mypy_boto3_cloudwatch",

        # Google dependencies
        "firebase-admin>=6.0.0",
        "google-cloud-firestore>=2.10.0",
        "google-auth",
        "google-cloud-storage",
        "google-cloud-bigquery",
        "google-cloud-pubsub",
        "google-cloud-datastore",
        "google-cloud-spanner",
        "google-cloud-translate",
        "google-cloud-logging",
        "google-cloud-vision",
        "google-cloud-language",
        "google-cloud-secret-manager",
        "google-cloud-monitoring",

        # MongoDB dependencies
        "pymongo>=4.3.0",

        # Optional helpers
        "uuid>=1.30.0",
    ]

# Read the README file if it exists
if os.path.exists('README.md'):
    with open('README.md', 'r', encoding='utf-8') as f:
        long_description = f.read()
else:
    long_description = __description__

setup(
    name="cloudweave",
    version=__version__,
    author=__author__,
    author_email=__email__,
    description=__description__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/macbee280/cloudweave",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
)