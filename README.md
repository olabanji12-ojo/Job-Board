# 🧑‍💼 Django Job Portal

A simple Django-powered web application that connects **employers** and **job seekers**. Employers can post jobs, and job seekers can search and apply for them.

---

## ✨ Features

- 👤 User authentication (Login, Logout, Registration)
- 🔐 Role-based access: `employer` and `employee`
- 📄 Job listings with search functionality
- 🔍 Job search by title, company, etc.
- 👥 Employee homepage and Employer dashboard
- 📨 Custom decorators to restrict unauthorized views
- 📦 Pagination for job listings
- 🔔 Flash messages for feedback
- 🎨 Bootstrap-based UI
- ⚡ Partial page updates using HTMX

---

## 🏗️ Tech Stack

- **Backend**: Python, Django
- **Database**: SQLite (default)
- **Frontend**: HTML, CSS (Bootstrap), HTMX
- **Other**: Custom decorators, Pagination, Django messages framework

---

## 🚀 Getting Started

1. **Clone the repository**

bash
git clone https://github.com/your-username/job-portal.git
cd job-portal

2. Create a virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows


3. Install dependencies
4. 
 pip install -r requirements.txt



5. Run migrations

python manage.py migrate


5. Start the development server

python manage.py runserver

