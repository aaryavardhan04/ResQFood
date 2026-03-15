# 🍱 ResQFood
### A Surplus Food Distribution & Management System

**ResQFood** is a Django-powered platform designed to connect **restaurants with surplus food** to **NGOs and volunteers**.  
Our mission is to **minimize food waste** and ensure that **excess meals reach people who need them most**.

---

# 🚀 Getting Started

Follow these instructions to set up the project locally for **development and testing**.

---

# 📋 Prerequisites

Make sure the following are installed on your system:

- **Python 3.10 or higher**
- **Git**
- **pip** (Python package manager)

---

# ⚙️ Installation & Setup

## 1️⃣ Clone the Repository

```powershell
git clone https://github.com/aaryavardhan04/ResQFood.git
cd ResQFood
```

---

## 2️⃣ Create & Activate Virtual Environment

### Create the environment
```powershell
python -m venv venv
```

### Activate it (Windows PowerShell)
```powershell
.\venv\Scripts\Activate.ps1
```

---

## 3️⃣ Install Dependencies

```powershell
pip install -r requirements.txt
```

---

# 🔐 Configuration (Environment Variables)

This project uses **python-dotenv** for security.

1. Create a file named `.env` in the **root directory**
2. Refer to `.env.example` for required keys

Add the following variables to your `.env` file:

```env
SECRET_KEY=your_django_secret_key_here
DEBUG=True
DB_PASS=your_database_password
EMAIL=your_email_address
PASSWORD=your_app_specific_password
```

---

# 🗄️ Database Initialization

Since the database file is **not tracked by Git**, you must recreate it locally.

### Generate migration files
```powershell
python manage.py makemigrations
```

### Apply migrations to create tables
```powershell
python manage.py migrate
```

---

# 👤 Create Administrative User (Optional)

To access the **Django Admin Dashboard** at `/admin`:

```powershell
python manage.py createsuperuser
```

---

# ▶️ Run the Application

```powershell
python manage.py runserver
```

Open your browser and visit:

```
http://127.0.0.1:8000/
```

---

# 📂 Project Structure

```
ResQFood/
│
├── core/          # Main application logic (food listings, NGO verification, users)
├── resqfood/      # Project settings, URLs, WSGI configuration
├── templates/     # HTML templates for dashboards and authentication
├── media/         # Uploaded food images (e.g., Biryani, Thali photos)
└── manage.py      # Django management script
```

---

# 🛠️ Tech Stack

**Backend**
- Python
- Django

**Database**
- SQLite (Development)
- MySQL (Production Ready)

**Frontend**
- HTML5
- CSS3
- JavaScript

**Security**
- python-dotenv (Environment Variable Management)

---

# 🎯 Project Goal

Reduce food waste by creating a **digital bridge between restaurants, NGOs, and volunteers**, ensuring surplus food reaches those in need quickly and efficiently.

---

⭐ If you like this project, consider **starring the repository**!