import os

def allowed_file(filename):
    allowed = os.getenv("ALLOWED_EXTENSIONS", "pptx,docx,xlsx").split(",")
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed
