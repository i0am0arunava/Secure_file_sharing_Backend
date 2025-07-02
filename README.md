# 🔐 Secure File Sharing Backend
    🧰 Tech Stack

1. **Python**
2. **Flask**
3. **MongoDB (Atlas)**
4. **Docker**

This is a secure file-sharing system backend built using Flask and MongoDB, supporting role-based access for Ops and Client users.

## 📬 Postman Collection

You can import the Postman dump file to test all API endpoints easily.


> 📁 **Postman Dump File:**>
> [https://drive.google.com/file/d/1yAR88rk222WybUoJoqMGIsh3QSZ-R9T_/view?usp=sharing](https://drive.google.com/file/d/1yAR88rk222WybUoJoqMGIsh3QSZ-R9T_/view?usp=sharing)

---

## Installation

You can either run the app using **Docker** or manually with **Python venv**.

### ✅ Option 1: Docker

```bash
git clone https://github.com/i0am0arunava/Secure_file_sharing_Backend.git
cd Secure_file_sharing_Backend
docker-compose up --build
pip install pytest
```

### ✅ Option 2: Manual Setup (Python venv)

```bash
git clone https://github.com/i0am0arunava/Secure_file_sharing_Backend.git
cd Secure_file_sharing_Backend

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
pip install pytest

python run.py
```

---

## 📌 Usage

Once the server is up and running, access it at:

```
http://localhost:5000/
```

### ✅ Available Endpoints

#### 🛠️ OPS Endpoints
- `POST /ops/signup` - Sign up an Ops user
- `POST /ops/login` - Login for Ops user
- `POST /ops/upload` - Upload `.pptx`, `.docx`, `.xlsx` files

#### 👤 Client Endpoints
- `POST /client/signup` - Sign up a Client user
- `POST http://localhost:5000/client/verify/<token>`- Verify Email
- `POST /client/login` - Login for Client user
- `POST /client/files` - List uploaded files (requires auth)
- `POST /client/request-download` - Request secure download link
- `GET  /client/download/<token>` - Download file via secure tokenized URL

---

## 📬 Postman Collection

You can import the Postman dump file to test all API endpoints easily.


> 📁 **Postman Dump File:**>
> [https://drive.google.com/file/d/1yAR88rk222WybUoJoqMGIsh3QSZ-R9T_/view?usp=sharing](https://drive.google.com/file/d/1yAR88rk222WybUoJoqMGIsh3QSZ-R9T_/view?usp=sharing)

To import in Postman:
1. Open Postman
2. Click on **Import**
3. Upload the `postman_collection.json` file
4. follow the screenshot to add environment variable for POSTMAN

---

## 🖼️ Screenshots

Add envirnment vriable like this ,add the key as it is ,no need to add value 
![Screenshot from 2025-07-02 18-41-46](https://github.com/user-attachments/assets/9c84b50d-23be-4c25-927b-22e3f3fbfd39)


upload any file inside postman like this 
![Screenshot from 2025-07-02 18-45-58](https://github.com/user-attachments/assets/9f5c0b74-6a4c-42a2-9e27-9884068214bd)

Verification email will be sent to the given emailid

![varificationemail](https://github.com/user-attachments/assets/550c0f62-445a-427d-bd7d-8a0743885083)

here is the received email for verification 
![WhatsApp Image 2025-07-02 at 6 51 03 PM](https://github.com/user-attachments/assets/a3637e89-1c35-459e-a4ad-259e718caa01)

Here is the encrypted file download link received for client

![request](https://github.com/user-attachments/assets/fed1d449-f566-4104-adbd-5f0402f984f3)

here is the all testcases result
![Screenshot from 2025-07-02 17-53-17](https://github.com/user-attachments/assets/e45c2da2-f63c-4a5b-ae11-0773f64aeb23)
![Screenshot from 2025-07-02 17-53-23](https://github.com/user-attachments/assets/4f2d55eb-ce4f-488b-8d8a-13409c651614)




---

## Extra Points

### ✅ Testing

```bash
pip install pytest
pytest tests/
```
here is the screenshot of test result 
![Screenshot from 2025-07-02 17-31-40](https://github.com/user-attachments/assets/c024ebfb-a03f-4f01-83e0-1c5a601449b4)






### ✅ Production
## 🏗️ Deployment Plan (Production)

1. **Rate Limiting for Abuse Prevention**  
   Implement rate limiting using Flask-Limiter or Nginx to protect APIs from brute-force and abuse.

2. **Use Gunicorn with Nginx**  
   Replace the Flask development server with Gunicorn for better performance and stability. Nginx will act as a reverse proxy and handle SSL termination.

3. **MongoDB Atlas**  
   Use MongoDB Atlas for cloud-hosted, scalable, and managed NoSQL database services.

4. **Environment Variables**  
   Securely store all secrets and credentials using `.env` files or secret managers like AWS Secrets Manager or Docker Secrets.

5. **Hosting Options**  
   Deploy on cloud providers like **Render**, **Railway**, **Heroku**, **AWS EC2**, or set up your own server with **uWSGI + Nginx**.







---
