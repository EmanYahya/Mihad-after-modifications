# 🛍️ Mihad E-commerce Backend API

This project is a backend system for an e-commerce platform built using Django and Django REST Framework.

It provides APIs for managing products, categories, cart, and orders.

---

## 🚀 Features

* User Authentication (Login / Register)
* Product Management
* Product Images (Multiple images per product)
* Categories & Subcategories
* Cart System
* Order System

---

## 🛠️ Tech Stack

* Python
* Django
* Django REST Framework
* SQLite
* Pillow (Image handling)

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/EmanYahya/Mihad-after-modifications.git
cd Mihad-after-modifications
```

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run migrations

```bash
python manage.py migrate
```

### 5. Run server

```bash
python manage.py runserver
```

---

## 🌐 Base URL

```
http://127.0.0.1:8000/
```

---

## 📦 API Endpoints

### 🛍️ Products

#### Get all products

```
GET /products/
```

#### Get product details

```
GET /products/<id>/
```

#### Product Response Example

```json
{
  "id": 1,
  "name": "T-shirt",
  "price": 200,
  "description": "Cotton T-shirt",
  "images": [
    {
      "id": 1,
      "image": "/media/products/image1.jpg"
    }
  ]
}
```

---

### 🧾 Categories

```
GET /categories/
GET /subcategories/
```

---

### 🛒 Cart

#### Add to cart

```
POST /cart/
```

#### Get cart

```
GET /cart/
```

---

### 📦 Orders

```
POST /orders/
GET /orders/
```

---

### 🔐 Authentication

```
POST /login/
POST /register/
```

---

## 🖼️ Media Files

Images are stored in:

```
/media/
```

Make sure Django serves media during development.

---

## 🔐 Authentication

Protected endpoints require authentication token:

```
Authorization: Bearer <token>
```

---

## 🌐 CORS Configuration

To connect with frontend (React / Vue):

```bash
pip install django-cors-headers
```

In settings.py:

```python
CORS_ALLOW_ALL_ORIGINS = True
```

---

## 📁 Project Structure

```
Mihad/
│
├── app/            # users, cart, orders
├── products/       # products, categories, images
├── media/          # uploaded images
├── manage.py
```

---

## 🤝 For Frontend Developers

* All APIs return JSON
* Images are returned as URLs
* Use Base URL provided
* Handle authentication token for protected APIs

---

## 📌 Notes

* Backend is ready for frontend integration
* Future improvements:

  * Payment integration
  * Product filtering
  * Search

---

## 👩‍💻 Author

Eman Yahya
