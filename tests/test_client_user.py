import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def test_client_signup_and_login(client):
    # Signup
    client.post('/client/signup', json={
        "email": "client@example.com",
        "password": "client123"
    })

    # Manually verify
    from app.mongo import users_collection
    users_collection.update_one({"email": "client@example.com"}, {"$set": {"is_verified": True}})

    # Login
    response = client.post('/client/login', json={
        "email": "client@example.com",
        "password": "client123"
    })
    assert response.status_code == 200
    assert "login successful" in response.get_json()["msg"]

def test_list_files(client):
    from app.mongo import users_collection, files_collection

    users_collection.insert_one({
        "email": "client@example.com",
        "password": hash_password("client123"),
        "is_ops": False,
        "is_verified": True
    })

    # Add fake file
    files_collection.insert_one({
        "filename": "sample.docx",
        "filetype": "docx",
        "file_url": "http://localhost:5000/uploads/sample.docx",
        "uploaded_by": "ops@example.com"
    })

    response = client.post('/client/files', json={
        "email": "client@example.com",
        "password": "client123"
    })
    assert response.status_code == 200
    assert "files" in response.get_json()

def test_request_download_url(client):
    from app.mongo import users_collection, files_collection

    users_collection.insert_one({
        "email": "client@example.com",
        "password": hash_password("client123"),
        "is_ops": False,
        "is_verified": True
    })

    file_id = files_collection.insert_one({
        "filename": "sample.docx",
        "filetype": "docx",
        "file_url": "http://localhost:5000/uploads/sample.docx",
        "uploaded_by": "ops@example.com"
    }).inserted_id

    response = client.post('/client/request-download', json={
        "email": "client@example.com",
        "password": "client123",
        "file_id": str(file_id)
    })
    assert response.status_code == 200
    assert "download_link" in response.get_json()

def test_invalid_download_token(client):
    response = client.get('/client/download/fake-invalid-token')
    assert response.status_code == 400
