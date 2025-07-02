from flask import Blueprint, request, jsonify,send_from_directory
from .mongo import users_collection
from cryptography.fernet import Fernet
from werkzeug.utils import secure_filename
from .utils import allowed_file
from datetime import datetime
from .mongo import files_collection
import hashlib, os
from .email import send_email  

from bson import ObjectId
user_bp = Blueprint('user', __name__)
fernet = Fernet(os.getenv("SECRET_KEY").encode())

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# OPS SIGN UP
@user_bp.route('/ops/signup', methods=['POST'])
def ops_signup():
    data = request.get_json()
    email = data.get("email")
    password = hash_password(data.get("password"))

    if users_collection.find_one({"email": email}):
        return jsonify({"msg": "Email already exists"}), 400

    users_collection.insert_one({
        "email": email,
        "password": password,
        "is_verified": False,
        "is_ops": True
    })

    token = fernet.encrypt(email.encode()).decode()
    verify_url = f"http://localhost:5000/ops/verify/{token}"

    return jsonify({"msg": "Ops Signup successful", "verify_url": verify_url})


# OPS EMAIL VERIFICATION
@user_bp.route('/ops/verify/<token>', methods=['GET'])
def verify_ops_email(token):
    try:
        email = fernet.decrypt(token.encode()).decode()
        result = users_collection.update_one(
            {"email": email, "is_ops": True},
            {"$set": {"is_verified": True}}
        )
        if result.modified_count == 0:
            return jsonify({"msg": "Already verified or invalid email"}), 400
        return jsonify({"msg": "Ops email verified successfully"})
    except:
        return jsonify({"msg": "Invalid or expired link"}), 400


#  OPS LOGIN
@user_bp.route('/ops/login', methods=['POST'])
def ops_login():
    data = request.get_json()
    email = data.get("email")
    password = hash_password(data.get("password"))

    user = users_collection.find_one({
        "email": email,
        "password": password,
        "is_ops": True
    })

    if not user:
        return jsonify({"msg": "Invalid Ops credentials"}), 401
    if not user.get("is_verified"):
        return jsonify({"msg": "Email not verified"}), 403

    return jsonify({"msg": "Ops user logged in successfully"})





@user_bp.route('/ops/upload', methods=['POST'])
def ops_upload():
    email = request.form.get("email")
    password = hash_password(request.form.get("password"))

    user = users_collection.find_one({
        "email": email,
        "password": password,
        "is_ops": True,
        "is_verified": True
    })

    if not user:
        return jsonify({"msg": "Invalid or unverified Ops user"}), 403

    if 'file' not in request.files:
        return jsonify({"msg": "No file part in request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"msg": "No file selected"}), 400

    if allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filetype = filename.rsplit(".", 1)[-1].lower()
        upload_dir = os.getenv("UPLOAD_FOLDER", "uploads")
        os.makedirs(upload_dir, exist_ok=True)
        upload_path = os.path.join(upload_dir, filename)
        file.save(upload_path)

        file_url = f"http://localhost:5000/uploads/{filename}"

        files_collection.insert_one({
            "filename": filename,
            "filetype": filetype,
            "file_url": file_url,
            "uploaded_by": email,
            "uploaded_at": datetime.utcnow()
        })

        return jsonify({
            "msg": "File uploaded successfully",
            "filename": filename,
            "filetype": filetype,
            "file_url": file_url
        }), 200

    return jsonify({"msg": "Invalid file type"}), 400



# CLIENT SIGN UP
@user_bp.route('/client/signup', methods=['POST'])
def client_signup():
    data = request.get_json()
    email = data.get("email")
    password = hash_password(data.get("password"))

    if users_collection.find_one({"email": email}):
        return jsonify({"msg": "Email already exists"}), 400

    users_collection.insert_one({
        "email": email,
        "password": password,
        "is_verified": False,
        "is_ops": False
    })

    token = fernet.encrypt(email.encode()).decode()
    verify_url = f"http://localhost:5000/client/verify/{token}"

    subject = "Verify your Client Account"
    html = f'<p>Click to verify your email: <a href="{verify_url}">Verify Account</a></p>'
    email_sent = send_email(email, subject, html)

    return jsonify({
        "msg": "Signup successful",
        "email_sent": email_sent,
        "verify_url": verify_url
    })



# EMAIL VERIFICATION
@user_bp.route('/client/verify/<token>', methods=['GET'])
def verify_email(token):
    try:
        email = fernet.decrypt(token.encode()).decode()
        result = users_collection.update_one(
            {"email": email},
            {"$set": {"is_verified": True}}
        )
        if result.modified_count == 0:
            return jsonify({"msg": "Already verified or invalid email"}), 400
        return jsonify({"msg": "Email verified successfully"})
    
    
    
    
    
    except:
        return jsonify({"msg": "Invalid or expired link"}), 400


# CLIENT LOGIN
@user_bp.route('/client/login', methods=['POST'])
def client_login():
    data = request.get_json()
    email = data.get("email")
    password = hash_password(data.get("password"))

    user = users_collection.find_one({
        "email": email,
        "password": password,
        "is_ops": False
    })

    if not user:
        return jsonify({"msg": "Invalid credentials"}), 401
    if not user.get("is_verified"):
        return jsonify({"msg": "Email not verified"}), 403

    return jsonify({"msg": "Client login successful"})







@user_bp.route('/client/files', methods=['POST'])
def list_uploaded_files():
    data = request.get_json()
    email = data.get("email")
    password = hash_password(data.get("password"))

   
    user = users_collection.find_one({
        "email": email,
        "password": password,
        "is_ops": False,
        "is_verified": True
    })

    if not user:
        return jsonify({"msg": "Invalid or unverified client"}), 403

   
    files = files_collection.find({}, {"filename": 1}) 

  
    file_list = [{"id": str(file["_id"]), "name": file["filename"]} for file in files]

    return jsonify({"files": file_list})






@user_bp.route('/client/request-download', methods=['POST'])
def generate_download_url():
    data = request.get_json()
    email = data.get("email")
    password = hash_password(data.get("password"))
    file_id = data.get("file_id")

    user = users_collection.find_one({
        "email": email,
        "password": password,
        "is_ops": False,
        "is_verified": True
    })

    if not user:
        return jsonify({"msg": "Invalid or unverified client"}), 403

    file_doc = files_collection.find_one({"_id": ObjectId(file_id)})
    print(file_doc)
    print(file_id)
    if not file_doc:
        return jsonify({"msg": "File not found"}), 404

    payload = f"{email}|{file_doc['filename']}"
    token = fernet.encrypt(payload.encode()).decode()

    secure_url = f"http://localhost:5000/client/download/{token}"
    return jsonify({"download_link": secure_url, "message": "success"})







@user_bp.route('/client/download/<token>', methods=['GET'])
def client_download(token):
    try:
      
        payload = fernet.decrypt(token.encode()).decode()
        email, file_doc = payload.split("|")
      
      
        user = users_collection.find_one({
            "email": email,
            "is_ops": False,
            "is_verified": True
        })
         
        if not user:
            return jsonify({"msg": "Unauthorized or invalid client"}), 403

     
        upload_dir = os.path.join(os.getcwd(), 'uploads')
        full_path = os.path.join(upload_dir, file_doc)

        if not os.path.exists(full_path):
            return jsonify({"msg": "File not found"}), 404

        return send_from_directory(upload_dir, file_doc, as_attachment=True)

    except Exception as e:
        print("Error:", e)
        return jsonify({"msg": "Invalid or expired token"}), 400
