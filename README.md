# 🛍️ Mihad E-Commerce Backend

A professional backend system for an e-commerce platform built using Django and Django REST Framework.
The project handles products, categories, cart management, orders, and checkout processes with real-world business logic.

---

## 🚀 Features

* Product management (CRUD)
* Category & subcategory support
* Product variations (Size / Color)
* Cart system
* Order & checkout logic
* Handling missing products during checkout
* Secure settings (no hardcoded secrets)
* Clean project structure using Django apps

---

## 🧱 Tech Stack

* Python
* Django
* Django REST Framework (DRF)
* SQLite (can be replaced with PostgreSQL)
* Git & GitHub

---

## 📁 Project Structure

```
Mihad-after-modifications/
│
├── app/            # Core app (users, orders, cart)
├── products/       # Product logic (models, views, serializers)
├── config/         # Project settings
├── staticfiles/    # Static assets
├── manage.py
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/EmanYahya/Mihad-after-modifications.git
cd Mihad-after-modifications
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows
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

## 🔗 API Endpoints (Examples)

### Products

* `GET /products/` → Get all products
* `GET /products/<id>/` → Get product details

### Cart

* `POST /cart/` → Add to cart
* `GET /cart/` → View cart

### Orders

* `POST /checkout/` → Place order

---

## 🧠 Business Logic Highlights

* Prevents checkout with unavailable products
* Supports product variations (size & color)
* Handles edge cases in cart operations

---

## 🔐 Security

* Sensitive data is not hardcoded
* Environment-based configuration recommended

---

## 🚧 Future Improvements

* Add pagination & filtering
* Implement search functionality
* Add Swagger API documentation
* Optimize performance
* Deploy to cloud (Render / Railway)

---

