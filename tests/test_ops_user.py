import hashlib
import os

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def test_ops_signup_and_login(client):
    # Signup
    client.post('/ops/signup', json={
        "email": "ops@example.com",
        "password": "ops123"
    })

    # Manually verify
    from app.mongo import users_collection
    users_collection.update_one({"email": "ops@example.com"}, {"$set": {"is_verified": True}})

    # Login
    response = client.post('/ops/login', json={
        "email": "ops@example.com",
        "password": "ops123"
    })
    assert response.status_code == 200
    assert "logged in successfully" in response.get_json()["msg"]

def test_ops_upload_file(client):
    from app.mongo import users_collection

    # Insert verified Ops user directly
    users_collection.insert_one({
        "email": "ops@example.com",
        "password": hash_password("ops123"),
        "is_ops": True,
        "is_verified": True
    })

    # Create dummy file
    test_file_path = "tests/test.docx"
    os.makedirs("tests", exist_ok=True)
    with open(test_file_path, "wb") as f:
        f.write(b"Test content")

    with open(test_file_path, "rb") as file_data:
        response = client.post('/ops/upload', data={
            "email": "ops@example.com",
            "password": "ops123",
            "file": (file_data, "test.docx")
        }, content_type='multipart/form-data')

    os.remove(test_file_path)
    assert response.status_code == 200
    assert "File uploaded successfully" in response.get_json()["msg"]
