# 🌍 Enhanced Inter-Faith Ethics Assessment System

An AI-powered ethical decision analysis platform that evaluates moral dilemmas using perspectives from major world religions and generates an Ethics Score with detailed explanations, charts, and recommendations.

---

# 📌 Project Overview

The Enhanced Inter-Faith Ethics Assessment System is an intelligent web-based application designed to analyze ethical situations submitted by users through text or PDF uploads.

The system uses Artificial Intelligence APIs to:
- Analyze ethical dilemmas
- Generate an Ethics Score
- Compare perspectives from different religions
- Provide moral suggestions and reasoning
- Visualize results using charts and graphs

This project was developed as an Industry Internship Project focused on:
- Ethical AI
- Inclusive Decision Making
- Religious Perspective Analysis
- AI Governance

---

# ✨ Features

## 🔐 Authentication System
- User Login & Signup
- Password Validation
- Email Validation
- Google OAuth Login
- Session Management
- MySQL Database Integration

---

## 🤖 AI-Powered Ethics Evaluation
- Accepts:
  - User Text Input
  - PDF File Uploads
- Uses DeepSeek API for AI Analysis
- Generates:
  - Ethics Score
  - Religious Perspective Analysis
  - Recommendations
  - Moral Interpretation

---

## 📊 Result Dashboard
- Ethics Score Visualization
- Pie Charts & Graphs
- Religious Comparison
- Dynamic Result Cards
- Modern Responsive UI

---

## 🎨 Modern Frontend UI
- Animated Landing Page
- Smooth Transitions
- Interactive Dashboard
- Responsive Design
- Sidebar Navigation
- Clean User Experience

---

# 🛠️ Technologies Used

## Frontend
- HTML5
- CSS3
- JavaScript
- Bootstrap

## Backend
- Python
- Flask

## Database
- MySQL Workbench

## APIs & Libraries
- DeepSeek API
- Flask-MySQLdb
- Flask-Login
- Flask-WTF
- PyPDF2
- Werkzeug
- python-dotenv

---

# 📂 Project Structure

```bash
Enhanced-InterFaith-Ethics-System/
│
├── static/
│   ├── css/
│   ├── js/
│   ├── images/
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── signup.html
│   ├── dashboard.html
│   ├── result.html
│
├── uploads/
│
├── app.py
├── db_config.py
├── requirements.txt
├── workbench.sql
├── .env
├── .gitignore
├── README.md
```

---

# ⚙️ Installation Guide

## 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/Enhanced-InterFaith-Ethics-System.git

cd Enhanced-InterFaith-Ethics-System
```

---

## 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

#### Windows
```bash
venv\Scripts\activate
```

#### Linux/Mac
```bash
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 📦 requirements.txt

```txt
Flask
Flask-MySQLdb
Flask-WTF
Flask-Login
mysqlclient
requests
PyPDF2
python-dotenv
Werkzeug
authlib
oauthlib
gunicorn
```

---

# 🗄️ MySQL Database Configuration

## Create Database

Open MySQL Workbench and run:

```sql
CREATE DATABASE ethics_system;
```

Import your SQL file:

```bash
workbench.sql
```

---

# 🔑 Environment Configuration

Create a `.env` file in the root directory.

## 📄 .env File

```env
# ================================
# FLASK SECRET CONFIGURATION
# ================================
SECRET_KEY=your_secret_key_here

# ================================
# MYSQL DATABASE CONFIGURATION
# ================================
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password
MYSQL_DB=ethics_system

# ================================
# GOOGLE OAUTH CONFIGURATION
# ================================
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret

# ================================
# DEEPSEEK API CONFIGURATION
# ================================
DEEPSEEK_API_KEY=your_deepseek_api_key

# ================================
# FILE UPLOAD CONFIGURATION
# ================================
UPLOAD_FOLDER=uploads

# ================================
# FLASK DEBUG MODE
# ================================
FLASK_ENV=development
FLASK_DEBUG=True
```

---

# 🔒 .gitignore File

Create a `.gitignore` file:

```gitignore
venv/
__pycache__/
.env
uploads/
*.pyc
*.pyo
*.pyd
.DS_Store
.idea/
.vscode/
```

---

# 🚀 Running the Project

```bash
python app.py
```

Application will run on:

```bash
http://127.0.0.1:5000
```

---

# 📥 PDF Upload Feature

Users can upload PDF files containing:
- Ethical situations
- Decision-making scenarios
- Case studies

The system extracts the text and sends it to the AI model for ethical analysis.

---

# 🧠 AI Ethics Analysis Workflow

```text
User Input / PDF Upload
            ↓
Text Extraction
            ↓
DeepSeek API Processing
            ↓
Ethical Analysis
            ↓
Religion-wise Interpretation
            ↓
Ethics Score Generation
            ↓
Dashboard Visualization
```

---

# 🌐 Religious Perspectives Included

The system evaluates ethical viewpoints based on:
- Hinduism
- Islam
- Christianity
- Buddhism
- Sikhism
- Jainism

---

# 📊 Example Output

## Ethics Score

```text
8.7 / 10
```

## Analysis Includes
- Moral Reasoning
- Religious Interpretation
- Ethical Suggestions
- Comparative Ethical Perspectives

---

# ☁️ Deployment Guide

## Recommended Platforms
- Render
- Railway
- PythonAnywhere
- AWS
- Azure

---

# 🌍 Deploy on Render

## Create `render.yaml`

```yaml
services:
  - type: web
    name: ethics-system
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "gunicorn app:app"
```

---

# 🔐 Security Recommendations

⚠️ Never upload:
- `.env`
- API Keys
- Secret Keys
- Database Passwords

Always use environment variables for:
- Database Credentials
- API Keys
- OAuth Secrets

---

# 🎯 Future Enhancements

- Voice Input Support
- AI Chatbot Assistant
- Multi-language Support
- User History Tracking
- Admin Dashboard
- Cloud AI Processing
- Advanced Analytics

---

# 👨‍💻 Developed By

Himanshu Kumawat

Industry Internship Project  
Passion Infotech Company

---

# 📜 License

This project is developed for educational and internship purposes only.

---

# ⭐ GitHub Push Commands

```bash
git init

git add .

git commit -m "Initial Commit"

git branch -M main

git remote add origin https://github.com/your-username/Enhanced-InterFaith-Ethics-System.git

git push -u origin main
```

---

# 🙌 Acknowledgements

Special Thanks To:
- Passion Infotech
- DeepSeek AI
- Flask Documentation
- Open Source Community
- MySQL Documentation

---

# 📧 Contact

```text
Email: your-email@example.com
```
