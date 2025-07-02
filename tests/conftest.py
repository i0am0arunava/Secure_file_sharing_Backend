import pytest
from dotenv import load_dotenv
from app import create_app
from app.mongo import users_collection, files_collection

# Load test environment
load_dotenv(dotenv_path=".env.test")

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    yield app.test_client()

# Auto-clear DB before each test
@pytest.fixture(autouse=True)
def clear_db():
    users_collection.delete_many({})
    files_collection.delete_many({})
