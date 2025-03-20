# Django Stock Management System

This project is a **Django REST API** that manages stock transactions and calculates the **average buy price** using the **FIFO (First In, First Out) method**. It supports **BUY, SELL, and SPLIT transactions**.

## 🚀 Features

- Add stock transactions (**BUY, SELL, SPLIT**)
- Calculate **Average Buy Price** using **FIFO method**
- View **Balance Quantity** after transactions
- RESTful API using **Django REST Framework**

---

## 🛠️ Setup Instructions

### **1️⃣ Clone the Repository**
**First, download the project from GitHub using the git clone command.**
- *git clone https://github.com/your-username/django-stock-management.git*

**Navigate into the project directory:**
- *cd django-stock-management*


### **2️⃣ Create & Activate Virtual Environment**
**A virtual environment ensures that dependencies are installed locally without affecting the global Python environment.**

**For Windows**: 
- *python -m venv env*
- *env\Scripts\Activate.ps1*

**For macOS/Linux**
- *python3 -m venv env*
- *source env/bin/activate*

### **3️⃣ Install Dependencies**
**Install all required packages using requirements.txt:**
- *pip install -r requirements.txt*


### **4️⃣ Apply Migrations**
**Django uses migrations to create and manage database tables. Run the following commands:**
- *python manage.py makemigrations*
- *python manage.py migrate*


### **5️⃣ Run the Server**
**Start the Django development server:**
- *python manage.py runserver*

---

## 🔥 API Endpoints
**Open Postman or your browser and test these endpoints:**

### **1️⃣ Add a Transaction (BUY/SELL/SPLIT)**
**Method:- `POST`**

**API:- `http://127.0.0.1:8000/transactions/`**

**For Trade Type:- BUY**

Example JSON Body: `{"trade_date": "2023-01-08", "company": "ABC 2", "trade_type": 1, "quantity": 400, "price_per_share": 45}`

**For Trade Type:- SELL**

Example JSON Body: `{"trade_date": "2023-01-09", "company": "ABC 2", "trade_type": 2, "quantity": 50}`

**For Trade Type:- SPLIT**

Example JSON Body: `{"trade_date": "2023-01-08", "company": "ABC 2", "trade_type": 3, "split_ratio": "1:5"}`

### **2️⃣ Get Average Buy Price & Balance Quantity**
**Method:- `GET`**

**API:- `http://127.0.0.1:8000/holdings/?company=ABC`**

Example JSON Response: `{"average_buy_price": 36.67, "balance_quantity": 600}`

