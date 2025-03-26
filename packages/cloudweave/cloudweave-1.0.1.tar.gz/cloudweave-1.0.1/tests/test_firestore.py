#!/usr/bin/env python3
"""
Test script for Firestore Database operations.
This script tests the functionality of the unified Database interface with Firestore.
"""

import os
import sys
import uuid
import time
import argparse
import uuid
from typing import TYPE_CHECKING, Dict, Any, Optional, List, Union
from pydantic import BaseModel, Field

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# With this:
from cloudweave import get_auth_manager, DatabaseType, LoggerType, AuthenticationError


# Define test models
class TestUser(BaseModel):
    """Test user model for database operations."""
    id: Optional[str] = None
    name: str
    email: str
    age: Optional[int] = None
    is_active: bool = True
    tags: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class TestProduct(BaseModel):
    """Test product model for database operations."""
    id: Optional[str] = None
    name: str
    price: float
    description: Optional[str] = None
    category: str
    in_stock: bool = True
    attributes: Dict[str, Any] = Field(default_factory=dict)
    
def authenticate(api_key: str, logger_options: Dict[str, Any]):
    """
    Authenticate with the API key and get the auth manager.
    
    Args:
        api_key: Authentication API key
        logger_options: Logger configuration
        
    Returns:
        Authenticated manager instance
    """
    try:
        # Get auth manager
        auth = get_auth_manager(api_key)
        
        # Initialize a logger
        logger = auth.get_logger(
            logger_type=LoggerType.LOCAL,
            namespace="firestore-test",
            instance_id=f"test-{uuid.uuid4()}",
            log_level="info",
            **logger_options
        )
        
        logger.info("Authentication successful")
        return auth, logger
    except AuthenticationError as e:
        print(f"Authentication failed: {e}")
        sys.exit(1)


def setup_database(auth, logger, credentials_path: str, project_id: Optional[str] = None):
    """
    Set up a Firestore database connection using the authenticated manager.
    
    Args:
        auth: Authenticated manager
        logger: Logger instance
        credentials_path: Path to Firebase credentials file
        project_id: Google Cloud project ID (optional)
        
    Returns:
        Database instance
    """
    logger.info(f"Setting up Firestore database connection")
    
    try:
        # Create database instance through the auth manager
        db = auth.get_database(
            db_type=DatabaseType.FIRESTORE,
            namespace="db_test",
            instance_id=f"firestore-test-{uuid.uuid4()}",
            credentials_path=credentials_path,
            project_id=project_id
        )
        logger.info("Firestore database connection established successfully")
        return db
    except Exception as e:
        logger.error(f"Failed to set up Firestore connection: {e}")
        raise


def test_model_registration(db, logger) -> None:
    """
    Test registering models with the database.
    
    Args:
        db: Database instance
        logger: Logger instance
    """
    logger.info("Testing model registration")
    
    try:
        # Register test models
        db.register_model(
            TestUser, 
            "users", 
            indexed_fields=["email", "is_active"]
        )
        logger.info("Registered TestUser model")
        
        db.register_model(
            TestProduct, 
            "products", 
            indexed_fields=["category", "in_stock"]
        )
        logger.info("Registered TestProduct model")
        
        # Test collection name retrieval
        user_collection = db.get_collection_name(TestUser)
        assert user_collection == "users", f"Expected 'users', got '{user_collection}'"
        
        product_collection = db.get_collection_name(TestProduct)
        assert product_collection == "products", f"Expected 'products', got '{product_collection}'"
        
        logger.info("✅ Model registration test passed")
    except Exception as e:
        logger.error(f"❌ Model registration test failed: {e}")
        raise


def test_crud_operations(db, logger) -> Dict[str, Any]:
    """
    Test CRUD operations (Create, Read, Update, Delete).
    
    Args:
        db: Database instance
        logger: Logger instance
        
    Returns:
        Dictionary with created item IDs for use in other tests
    """
    logger.info("Testing CRUD operations")
    item_ids = {}
    
    try:
        # Create test user
        test_user = TestUser(
            id=str(uuid.uuid4()),
            name="Test User",
            email="test@example.com",
            age=30,
            tags=["test", "sample"],
            metadata={
                "login_count": 0,
                "created_via": "test_script"
            }
        )
        
        user_id = db.put_item(test_user)
        item_ids['user_id'] = user_id
        logger.info(f"Created test user with ID: {user_id}")
        
        # Create test product
        test_product = TestProduct(
            id=str(uuid.uuid4()),
            name="Test Product",
            price=99.99,
            description="A test product for database operations",
            category="test",
            attributes={
                "color": "blue",
                "weight": 1.5,
                "dimensions": {
                    "width": 10,
                    "height": 20,
                    "depth": 5
                }
            }
        )
        
        product_id = db.put_item(test_product)
        item_ids['product_id'] = product_id
        logger.info(f"Created test product with ID: {product_id}")
        
        # Read test user
        user_item = db.get_item(TestUser, user_id)
        assert user_item is not None, "User item not found"
        assert user_item['name'] == "Test User", f"Expected 'Test User', got '{user_item['name']}'"
        assert user_item['email'] == "test@example.com", f"Expected 'test@example.com', got '{user_item['email']}'"
        logger.info("Successfully retrieved test user")
        
        # Read test product
        product_item = db.get_item(TestProduct, product_id)
        assert product_item is not None, "Product item not found"
        assert product_item['name'] == "Test Product", f"Expected 'Test Product', got '{product_item['name']}'"
        assert product_item['price'] == 99.99, f"Expected 99.99, got '{product_item['price']}'"
        logger.info("Successfully retrieved test product")
        
        # Update test user
        db.update_document(
            user_id,
            "users",
            {
                'age': 31,
                'tags': user_item['tags'] + ["updated"],
                'metadata': {
                    **user_item['metadata'],
                    'login_count': 1
                }
            }
        )
        logger.info("Updated test user directly")
        
        # Read updated user
        updated_user = db.get_item(TestUser, user_id)
        assert updated_user['age'] == 31, f"Expected 31, got '{updated_user['age']}'"
        assert "updated" in updated_user['tags'], "Expected 'updated' tag to be present"
        assert updated_user['metadata']['login_count'] == 1, "Expected login_count to be 1"
        logger.info("Successfully verified user updates")
        
        # Test get_document method
        user_doc = db.get_document(user_id, "users")
        assert user_doc is not None, "User document not found"
        assert user_doc['name'] == "Test User", f"Expected 'Test User', got '{user_doc['name']}'"
        logger.info("Successfully retrieved document directly")
        
        # Test update_document method
        db.update_document(
            user_id, 
            "users", 
            {
                "is_active": False,
                "metadata": {
                    "login_count": 2,
                    "last_updated": int(time.time())
                }
            }
        )
        logger.info("Updated document directly")
        
        # Verify update
        updated_user = db.get_item(TestUser, user_id)
        assert updated_user['is_active'] is False, "Expected is_active to be False"
        assert updated_user['metadata']['login_count'] == 2, "Expected login_count to be 2"
        logger.info("Successfully verified direct document update")
        
        # Create another user for delete test
        temp_user = TestUser(
            name="Temporary User",
            email="temp@example.com"
        )
        temp_id = db.put_item(temp_user)
        logger.info(f"Created temporary user with ID: {temp_id}")
        
        # Delete the temporary user
        db.delete_document(temp_id, "users")
        logger.info(f"Deleted temporary user with ID: {temp_id}")
        
        # Verify deletion
        deleted_user = db.get_item(TestUser, temp_id)
        assert deleted_user is None, "Expected temporary user to be deleted"
        logger.info("Successfully verified user deletion")
        
        logger.info("✅ CRUD operations test passed")
        return item_ids
    except Exception as e:
        logger.error(f"❌ CRUD operations test failed: {e}")
        raise


def test_query_operations(db, logger, item_ids: Dict[str, Any]) -> None:
    """
    Test query operations.
    
    Args:
        db: Database instance
        logger: Logger instance
        item_ids: Dictionary with item IDs from CRUD test
    """
    logger.info("Testing query operations")
    
    try:
        # Create additional test users for querying
        users_to_create = [
            TestUser(
                name="Active User",
                email="active@example.com",
                is_active=True,
                tags=["active", "registered"]
            ),
            TestUser(
                name="Inactive User",
                email="inactive@example.com",
                is_active=False,
                tags=["inactive"]
            ),
            TestUser(
                name="Another Active User",
                email="another@example.com",
                is_active=True,
                age=25,
                tags=["active", "premium"]
            )
        ]
        
        for user in users_to_create:
            db.put_item(user)
            logger.info(f"Created user: {user.name}")
            
        # Create additional test products for querying
        products_to_create = [
            TestProduct(
                name="Electronics Product",
                price=299.99,
                category="electronics",
                in_stock=True
            ),
            TestProduct(
                name="Clothing Product",
                price=49.99,
                category="clothing",
                in_stock=True
            ),
            TestProduct(
                name="Out of Stock Product",
                price=149.99,
                category="electronics",
                in_stock=False
            )
        ]
        
        for product in products_to_create:
            db.put_item(product)
            logger.info(f"Created product: {product.name}")
            
        # Query active users
        active_users = db.query(TestUser, {"is_active": True})
        logger.info(f"Found {len(active_users)} active users")
        assert len(active_users) >= 2, f"Expected at least 2 active users, got {len(active_users)}"
        
        # Query electronics products
        electronics = db.query(TestProduct, {"category": "electronics"})
        logger.info(f"Found {len(electronics)} electronics products")
        assert len(electronics) >= 2, f"Expected at least 2 electronics products, got {len(electronics)}"
        
        # Query in-stock electronics
        in_stock_electronics = db.query(TestProduct, {"category": "electronics", "in_stock": True})
        logger.info(f"Found {len(in_stock_electronics)} in-stock electronics products")
        assert len(in_stock_electronics) >= 1, f"Expected at least 1 in-stock electronics product, got {len(in_stock_electronics)}"
        
        logger.info("✅ Query operations test passed")
    except Exception as e:
        logger.error(f"❌ Query operations test failed: {e}")
        raise


def test_get_or_create(db, logger) -> None:
    """
    Test get_or_create functionality.
    
    Args:
        db: Database instance
        logger: Logger instance
    """
    logger.info("Testing get_or_create functionality")
    
    try:
        # Generate a unique ID for a non-existent user
        unique_id = str(uuid.uuid4())
        logger.info(f"Testing with unique ID: {unique_id}")
        
        # Try to get a non-existent user, should create a new one
        user_item = db.get_or_create(
            TestUser,
            unique_id,
            {
                "name": "New User",
                "email": "new@example.com",
                "tags": ["new"],
                "metadata": {
                    "created_via": "get_or_create"
                }
            }
        )
        
        assert user_item is not None, "Expected user item to be created"
        assert user_item['id'] == unique_id, f"Expected ID {unique_id}, got {user_item['id']}"
        assert user_item['name'] == "New User", f"Expected name 'New User', got '{user_item['name']}'"
        logger.info("Successfully created new user via get_or_create")
        
        # Try to get the same user, should return existing one
        same_user = db.get_or_create(
            TestUser,
            unique_id,
            {
                "name": "Different Name",
                "email": "different@example.com"
            }
        )
        
        assert same_user is not None, "Expected user item to be retrieved"
        assert same_user['id'] == unique_id, f"Expected ID {unique_id}, got {same_user['id']}"
        assert same_user['name'] == "New User", f"Expected original name 'New User', got '{same_user['name']}'"
        logger.info("Successfully retrieved existing user via get_or_create")
        
        logger.info("✅ get_or_create test passed")
    except Exception as e:
        logger.error(f"❌ get_or_create test failed: {e}")
        raise


def test_model_to_db_item(db, logger) -> None:
    """
    Test model_to_db_item functionality.
    
    Args:
        db: Database instance
        logger: Logger instance
    """
    logger.info("Testing model_to_db_item functionality")
    
    try:
        # Create a model instance with an ID
        unique_id = str(uuid.uuid4())
        logger.info(f"Testing with unique ID: {unique_id}")
        
        test_product = TestProduct(
            id=unique_id,
            name="Conversion Test Product",
            price=199.99,
            category="test",
            description="Testing model to db item conversion"
        )
        
        # Convert to database item
        db_item = db.model_to_db_item(test_product)
        
        assert db_item is not None, "Expected database item to be created"
        assert db_item['id'] == unique_id, f"Expected ID {unique_id}, got {db_item['id']}"
        assert db_item['name'] == "Conversion Test Product", f"Expected name 'Conversion Test Product', got '{db_item['name']}'"
        logger.info("Successfully converted model to database item with existing ID")
        
        # Create a model instance without an ID
        test_product = TestProduct(
            name="Auto-ID Product",
            price=299.99,
            category="test",
            description="Testing automatic ID assignment"
        )
        
        # Convert to database item
        db_item = db.model_to_db_item(test_product)
        
        assert db_item is not None, "Expected database item to be created"
        assert db_item['id'] is not None, "Expected an ID to be generated"
        assert db_item['name'] == "Auto-ID Product", f"Expected name 'Auto-ID Product', got '{db_item['name']}'"
        logger.info(f"Successfully converted model to database item with generated ID: {db_item['id']}")
        
        logger.info("✅ model_to_db_item test passed")
    except Exception as e:
        logger.error(f"❌ model_to_db_item test failed: {e}")
        raise


def test_batch_operations(db, logger) -> None:
    """
    Test batch operations.
    
    Args:
        db: Database instance
        logger: Logger instance
    """
    logger.info("Testing batch operations")
    
    try:
        # Create a list of operations to perform in a batch
        operations = []
        
        # Create a new user
        user_id = str(uuid.uuid4())
        operations.append({
            'type': 'set',
            'collection': 'users',
            'doc_id': user_id,
            'data': {
                'name': 'Batch User',
                'email': 'batch@example.com',
                'is_active': True,
                'tags': ['batch', 'test']
            }
        })
        
        # Create a new product
        product_id = str(uuid.uuid4())
        operations.append({
            'type': 'set',
            'collection': 'products',
            'doc_id': product_id,
            'data': {
                'name': 'Batch Product',
                'price': 399.99,
                'category': 'batch',
                'in_stock': True
            }
        })
        
        # Execute batch operations
        db.batch_operation(operations)
        logger.info(f"Executed batch operations to create user {user_id} and product {product_id}")
        
        # Verify the items were created
        user_item = db.get_item(TestUser, user_id)
        assert user_item is not None, "Expected batch user to be created"
        assert user_item['name'] == "Batch User", f"Expected name 'Batch User', got '{user_item['name']}'"
        
        product_item = db.get_item(TestProduct, product_id)
        assert product_item is not None, "Expected batch product to be created"
        assert product_item['name'] == "Batch Product", f"Expected name 'Batch Product', got '{product_item['name']}'"
        
        logger.info("Successfully verified batch creation")
        
        # Create a batch of update operations
        update_operations = [
            {
                'type': 'update',
                'collection': 'users',
                'doc_id': user_id,
                'data': {
                    'is_active': False,
                    'tags': ['batch', 'test', 'updated']
                }
            },
            {
                'type': 'update',
                'collection': 'products',
                'doc_id': product_id,
                'data': {
                    'price': 349.99,
                    'in_stock': False
                }
            }
        ]
        
        # Execute batch updates
        db.batch_operation(update_operations)
        logger.info("Executed batch update operations")
        
        # Verify the updates
        updated_user = db.get_item(TestUser, user_id)
        assert updated_user['is_active'] is False, "Expected is_active to be False"
        assert 'updated' in updated_user['tags'], "Expected 'updated' tag to be present"
        
        updated_product = db.get_item(TestProduct, product_id)
        assert updated_product['price'] == 349.99, f"Expected price 349.99, got {updated_product['price']}"
        assert updated_product['in_stock'] is False, "Expected in_stock to be False"
        
        logger.info("Successfully verified batch updates")
        
        # Create a batch of delete operations
        delete_operations = [
            {
                'type': 'delete',
                'collection': 'users',
                'doc_id': user_id
            },
            {
                'type': 'delete',
                'collection': 'products',
                'doc_id': product_id
            }
        ]
        
        # Execute batch deletes
        db.batch_operation(delete_operations)
        logger.info("Executed batch delete operations")
        
        # Verify the deletions
        deleted_user = db.get_item(TestUser, user_id)
        assert deleted_user is None, "Expected batch user to be deleted"
        
        deleted_product = db.get_item(TestProduct, product_id)
        assert deleted_product is None, "Expected batch product to be deleted"
        
        logger.info("Successfully verified batch deletions")
        
        logger.info("✅ batch operations test passed")
    except Exception as e:
        logger.error(f"❌ batch operations test failed: {e}")
        raise


def test_firestore_specific(db, logger) -> None:
    """
    Test Firestore-specific functionality like timestamps.
    
    Args:
        db: Database instance
        logger: Logger instance
    """
    logger.info("Testing Firestore-specific functionality")
    
    try:
        # Create a user with no timestamps
        user = TestUser(
            name="Timestamp Test User",
            email="timestamps@example.com"
        )
        user_id = db.put_item(user)
        logger.info(f"Created user for timestamp test with ID: {user_id}")
        
        # Get the user and check for timestamps
        user_item = db.get_item(TestUser, user_id)
        assert user_item is not None, "Expected user item to be created"
        
        # Check for created_at and updated_at fields
        # These are added automatically by the FirestoreManager
        assert 'created_at' in user_item.to_dict(), "Expected created_at timestamp to be present"
        assert 'updated_at' in user_item.to_dict(), "Expected updated_at timestamp to be present"
        
        logger.info("Successfully verified Firestore timestamps")
        
        # Clean up
        db.delete_document(user_id, "users")
        
        logger.info("✅ Firestore-specific functionality test passed")
    except Exception as e:
        logger.error(f"❌ Firestore-specific functionality test failed: {e}")
        raise


def cleanup_test_data(db, logger, item_ids: Dict[str, Any]) -> None:
    """
    Clean up test data.
    
    Args:
        db: Database instance
        logger: Logger instance
        item_ids: Dictionary with item IDs to clean up
    """
    logger.info("Cleaning up test data")
    
    try:
        # Delete created users and products
        for user_id in [item_ids.get('user_id')]:
            if user_id:
                db.delete_document(user_id, "users")
                logger.info(f"Deleted test user with ID: {user_id}")
        
        for product_id in [item_ids.get('product_id')]:
            if product_id:
                db.delete_document(product_id, "products")
                logger.info(f"Deleted test product with ID: {product_id}")
                
        logger.info("Test data cleanup completed")
    except Exception as e:
        logger.error(f"Error during test data cleanup: {e}")


def main():
    """Main function to run the test."""
    parser = argparse.ArgumentParser(description="Test Firestore Database functionality")
    parser.add_argument("--credentials", required=True, help="Path to Firebase credentials JSON file")
    parser.add_argument("--project-id", help="Google Cloud project ID (optional)")
    parser.add_argument("--log-file", default="logs/firestore_test.log", help="Log file path")
    parser.add_argument("--api-key", required=True, help="API key for authentication")
    args = parser.parse_args()
    
    # Set up logger options
    log_dir = os.path.dirname(args.log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    logger_options = {
        'log_file': args.log_file,
        'stdout': True
    }
    
    # Authenticate and get logger
    auth, logger = authenticate(args.api_key, logger_options)
    
    logger.info("=" * 50)
    logger.info("Starting Firestore Database test")
    logger.info(f"Credentials path: {args.credentials}")
    if args.project_id:
        logger.info(f"Project ID: {args.project_id}")
    logger.info("=" * 50)
    
    item_ids = {}
    try:
        # Setup database
        db = setup_database(auth, logger, args.credentials, args.project_id)
        
        # Run tests
        test_model_registration(db, logger)
        item_ids = test_crud_operations(db, logger)
        test_query_operations(db, logger, item_ids)
        test_get_or_create(db, logger)
        test_model_to_db_item(db, logger)
        test_batch_operations(db, logger)
        test_firestore_specific(db, logger)
        
        logger.info("=" * 50)
        logger.info("All tests completed successfully!")
        logger.info("=" * 50)
    except Exception as e:
        logger.error(f"Test execution failed: {e}")
    finally:
        # Clean up test data
        if 'db' in locals() and item_ids:
            cleanup_test_data(db, logger, item_ids)


if __name__ == "__main__":
    main()