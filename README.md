# Goodreads Clone 📚

A full-featured web application inspired by Goodreads, built using Django and Django REST Framework. Users can register, login, explore books, and write reviews. The project includes a secure REST API and asynchronous email notifications via Celery.

---

## 🚀 Features

### 🌐 Web Interface
- User registration and authentication
- Profile view and edit
- Browse and search books
- View book details and average ratings
- Add, update, or delete reviews (authenticated users only)
- Form rendering with Django Crispy Forms

### 🔐 REST API (Token protected)
- Authenticated users can:
  - Create book reviews
  - Update or delete their own reviews
  - Access paginated review data

### ⏱ Asynchronous Email
- Welcome email sent upon registration using **Celery + Redis**

---

## 🛠 Tech Stack

- Python 3.x
- Django 4.0
- Django REST Framework
- Celery (for async email tasks)
- PostgreSQL (or any preferred DB)
- Redis (as a message broker)
- Crispy Forms + Bootstrap5

---

## 📦 Requirements

Install dependencies:

```bash
pip install -r requirements.txt
