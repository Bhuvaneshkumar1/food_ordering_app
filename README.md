# 🍔 CLI Food Delivery System

A simple **command-line food delivery system** built in Python using **CSV as the database**.
Supports **Admin** and **User** roles, cart-based ordering, and optional **PDF bill generation** (via ReportLab).

---

## ✨ Features

### 👨‍🍳 Admin

* View the menu (sorted alphabetically by name).
* Add new food items.
* Remove food items.
* Auto-created **Admin account** on first run (`admin@food.com / admin123`).

### 🧑‍💻 User

* Register a new account.
* Login and view menu.
* Place multiple items in cart and confirm order.
* View past orders with price breakdown.
* Orders saved permanently to CSV.

### 📂 Data Storage

* `users.csv` → stores user info (with role).
* `menu.csv` → stores food items (must be preloaded by you).
* `orders.csv` → stores placed orders.
* `order_items.csv` → stores each item inside orders.

👉 All CSV files (except `menu.csv`) are auto-generated with correct headers.

### 🧾 (Optional) PDF Bill

* If **ReportLab** is installed, users get a PDF bill for each order.
* Works on **64-bit Python 3.x** (Windows, macOS, Linux).

---

## ⚙️ Installation

1. Clone the repo:

   ```bash
   git clone https://github.com/your-username/food-delivery-cli.git
   cd food-delivery-cli
   ```

2. Install dependencies (for PDF support):

   ```bash
   pip install reportlab
   ```

3. (Optional) Create `menu.csv` with your food items. Example format:

   ```csv
   id,item_name,price
   1,Pizza,250
   2,Burger,150
   3,French Fries,100
   ```

---

## 🚀 Usage

Run the app:

```bash
python food_delivery_app.py
```

* Admin login: `admin@food.com / admin123`
* User can **register** and then log in.

---

## 📊 CSV Files (Auto-Generated)

* **users.csv**

  ```csv
  id,name,email,password,role
  1,admin,admin@food.com,admin123,ADMIN
  ```
* **orders.csv**

  ```csv
  id,user_id,date
  1,2,2025-09-30 12:15:00
  ```
* **order_items.csv**

  ```csv
  order_id,item_id,qty
  1,2,3
  ```

---

## 🛠️ Tech Stack

* **Python 3.x**
* **CSV** (for storage)
* **ReportLab** (for optional PDF bills)

---

## 👨‍💻 Contributing

1. Fork the repo
2. Create a feature branch (`git checkout -b feature-xyz`)
3. Commit changes (`git commit -m "Added xyz feature"`)
4. Push branch (`git push origin feature-xyz`)
5. Create a PR 🎉

---

## 📜 License

MIT License – free to use and modify.

---
