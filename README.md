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
- Virtualenv
  
### 2️⃣ Clone the repository

```bash
git clone https://github.com/tuusuario/MyFinPlanner.git
cd MyFinPlanner
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```
### 4️⃣ 🔧 Create and configure the `.env` file

You must create a `.env` file in the root of the project and add your API key for OpenAI:

```env
OPENAI_API_KEY=your_openai_api_key_here
```
🔐 This key is required for enabling the **AI financial assistant** (MyFinancePal).
Get your API key at https://platform.openai.com

Important: Do NOT commit your .env file to version control, use a `.gitignore` file

### 5️⃣ Apply Migrations and prepare the database

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6️⃣ Initialize the server

```bash
python manage.py runserver
```

### 📁 Project Structure

```bash
MyFinPlanner/
├── accounts/                   # Django app for user authentication and management
│   ├── migrations/             # Migrations for user-related models
│   ├── static/                 # Static files (CSS, JS, images) specific to the app
│   ├── templates/              # HTML templates specific to the app
│   ├── __init__.py             # Marks this directory as a Python module
│   ├── admin.py                # Admin panel configuration for this app
│   ├── apps.py                 # Django app configuration
│   ├── forms.py                # Forms for user input and authentication
│   ├── models.py               # Models related to user profiles and authentication
│   ├── tests.py                # Unit tests for the app
│   ├── urls.py                 # App-specific URL routing
│   └── views.py                # View logic for handling requests

├── analytics/                  # Django app for data analytics (AI analisis and reports)
│   ├── migrations/             # Migrations for analytics models
│   ├── static/                 # Static files specific to the app
│   ├── templates/              # HTML templates specific to the app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py

├── finances/                   # Main app for financial management (Budgets, Transactions, Goals)
│   ├── migrations/             # Database migrations for this app
│   ├── static/                 # Static files specific to the app
│   ├── templates/              # HTML templates specific to the app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py

├── investments/                # Django app for investment management
│   ├── migrations/             # Migrations for investment-related models
│   ├── static/                 # Static files specific to the app
│   ├── templates/              # HTML templates specific to the app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py

├── myFinPlanner/               # Global project configuration for Django
│   ├── __pycache__/            # Compiled Python files (ignore in Git)
│   ├── __init__.py             # Marks this directory as a Python module
│   ├── asgi.py                 # ASGI server configuration
│   ├── settings.py             # Main project settings
│   ├── urls.py                 # Global project URL routing
│   ├── wsgi.py                 # WSGI server configuration

├── node_modules/               # Frontend dependencies installed by npm
│   └── ...                     # Contains libraries for frontend (CSS, JS)

├── .gitignore                  # Files and folders ignored by Git
├── db.sqlite3                  # SQLite database file for the project
├── manage.py                   # Django management script
├── package-lock.json           # Dependency lock file for npm
├── package.json                # npm configuration and dependencies
├── README.md                   # Project documentation
└── requirements.txt            # Python dependencies for the project

```

---

🚀 **Thank you for using MyFinPlanner!!**  
  






