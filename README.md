# MyFinPlanner 📊💰

**MyFinPlanner** MyFinPlanner is  a web application for individuals who want to manage effectively their personal finances. The app allows users to track income and expenses, set budgets, and gain insights into spending habits.  
It includes **MyFinancePal**, an AI-powered financial assistant that provides visualizations and recommendations based on spending patterns.

## 🚀 Features

- 📊 **Track income and expenses** with detailed reports.  
- 🎯 **Set monthly and custom budgets** to control spending.  
- 📈 **Financial analysis** with interactive visualizations.  
- 🤖 **MyFinancePal (AI Assistant)** offers recommendations and spending habit analysis.  
- 📡 **Investment support** with real-time stock price updates using the FinHub API.  

---

## 🛠 Installation & Setup

### 1️⃣ Prerequisites

Before starting the project, make sure you have installed:

- Python 3.10+ 👉 [Download here](https://www.python.org/downloads/)
- Git 👉 [Download here](https://git-scm.com/)
- Virtualenv (optional but recommended)  

### 2️⃣ Clone the repository

```bash
git clone https://github.com/tuusuario/MyFinPlanner.git
cd MyFinPlanner
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Apply Migrations and prepare the database

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5️⃣ Initialize the server

```bash
python manage.py runserver
```

### 📁 Project Structure

```bash
MyFinPlanner/  
│── finances/                  # Main Django application  
│   │── static/                 # Static files (CSS, JS, images)  
│   │── templates/              # HTML templates for the UI  
│   │── __init__.py             # Marks this directory as a Python module  
│   │── admin.py                # Django admin panel configuration  
│   │── apps.py                 # Application configuration in Django  
│   │── forms.py                # Forms for user data input  
│   │── models.py               # Database models for the application  
│   │── tests.py                # Unit tests for the application  
│   │── urls.py                 # Application-specific URL routing  
│   │── views.py                # View logic for handling requests  
│  
│── myFinPlanner/               # Global project configuration for Django  
│   │── __pycache__/            # Compiled Python files (ignore)  
│   │── __init__.py             # Marks this directory as a Python module  
│   │── asgi.py                 # ASGI server configuration  
│   │── settings.py             # Main project settings  
│   │── urls.py                 # Global project URL routing  
│   │── wsgi.py                 # WSGI server configuration  
│  
│── .gitignore                  # Files and folders to be ignored by Git  
│── db.sqlite3                   # SQLite database file for the project  
│── manage.py                    # Django management script  
│── README.md                    # Project documentation  
│── requirements.txt              # Project dependencies  


```

---

🚀 **Thank you for using MyFinPlanner!!**
