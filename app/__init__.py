from flask import Flask
from dotenv import load_dotenv
import os
from .user import user_bp

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    app.config['UPLOAD_FOLDER'] = 'uploads'
    
    app.register_blueprint(user_bp)

    return app
