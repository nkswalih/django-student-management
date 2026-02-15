# 🎓 Django Student Management System

A modern, full-featured **Student Management System** built with **Django**, **Tailwind CSS**, and **Alpine.js**.

This project includes role-based authentication (Principal, Teacher, Student), course enrollment, voice homework submission, dashboard analytics, and more.

---
## 📌 Overview

This project is a **full-featured Student Management Web Application** built using Django.  
It provides a complete academic workflow system with role-based access control and modern UI design.

### 🚀 Features

- 🔐 **Role-Based Authentication** (Principal, Teacher, Student)
- 📚 **Course Creation & Management**
- 🧑‍🎓 **Student Enrollment System**
- 🎤 **Voice Homework Submission** (Web Audio API / MediaRecorder)
- 📊 **Dashboard Analytics with Charts**
- 🧾 **Course Purchase & Approval Workflow**
- 👨‍🏫 **Homework Assignment System**
- 🛠 **Custom User Model using Email Authentication**

---

This system demonstrates real-world backend architecture, media handling (images & audio uploads), dynamic dashboards, and secure authentication workflows.

## 🚀 Features

### 👑 Principal
- Create, edit, and delete courses
- Manage students and teachers
- Approve or reject course enrollments
- Dashboard analytics overview

### 👨‍🏫 Teacher
- Assign homework
- Manage notes
- View students
- Review voice submissions

### 🎓 Student
- Browse available courses
- Purchase and enroll in courses
- Submit voice homework recordings
- Track approvals and progress

---

## 🧠 Tech Stack

- **Backend:** Django
- **Authentication:** Custom User Model (Email-based login)
- **Frontend:** Tailwind CSS
- **Interactivity:** Alpine.js
- **Charts:** Chart.js
- **Database:** SQLite (can switch to PostgreSQL)
- **Media Handling:** Django Media Files
- **Voice Recording:** Web MediaRecorder API

---

## 🔐 Authentication System

- Custom `Student` model extending `AbstractUser`
- Email used as `USERNAME_FIELD`
- Auto-generated username
- Role-based access control using Django Groups
- Custom decorator: `@role_required`

---

## 📂 Project Structure

```
student_management/
│
├── accounts/        # Custom user & authentication
├── principal/       # Principal dashboard & course management
├── teacher/         # Teacher features
├── school/          # Student dashboard & enrollment
├── media/           # Uploaded images & audio files
├── templates/
└── static/
```

---

## 📸 Screenshots

_Add screenshots here_

```
/screenshots/dashboard.png
/screenshots/course-list.png
/screenshots/voice-recorder.png
```

---

## ⚙️ Installation Guide

### 1️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/django-student-management-system.git
cd django-student-management-system
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

Activate:

**Windows**
```bash
venv\Scripts\activate
```

**Mac/Linux**
```bash
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5️⃣ Create Superuser

```bash
python manage.py createsuperuser
```

### 6️⃣ Run Server

```bash
python manage.py runserver
```

Visit:

```
http://127.0.0.1:8000/
```

---

## 🎤 Voice Homework Feature

- Uses browser MediaRecorder API
- Records audio in WebM format
- Uploads via Fetch API
- Stores recordings in Django media folder
- Teacher can review submissions

---

## 📊 SEO Keywords

- Django Student Management System
- Django Role Based Authentication
- Django Custom User Model
- Django Course Enrollment System
- Django Voice Recording Project
- Full Stack Django Project
- Tailwind CSS Django Dashboard

---

## 💡 Future Improvements

- Payment gateway integration
- Email verification
- JWT authentication
- REST API (Django REST Framework)
- Deployment (AWS / Render / Railway)

---

## 👨‍💻 Author

**Mohd Swalih N K**  
Full Stack Developer (Python | Django | React)

---

## 📜 License

This project is licensed under the MIT License.
