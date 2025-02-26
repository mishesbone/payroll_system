
---

# 🏢 Payroll Management System  

## 📌 Overview  
The **Payroll Management System** is a web-based application built with **Flask** that enables organizations to manage employee payroll, attendance, and company records efficiently. It features **role-based access control**, allowing users to register, join companies, and manage payroll operations.  

## 🚀 Features  
✅ **User Authentication** – Secure login and registration with role-based access control.  
✅ **Company Management** – Users can search for existing companies or create new ones.  
✅ **Admin Privileges** – Company creators automatically become admins with management rights.  
✅ **Employee Onboarding** – Admins can invite users to join their company as employees.  
✅ **Payroll & Attendance Tracking** – Employees can view payroll records and attendance history.  
✅ **Support System** – Companies can contact **EOY Support** for business-related assistance.  

---

## 🛠 Installation & Setup  

### 📌 Prerequisites  
Ensure you have the following installed:  
- Python 3.8+  
- Flask  
- Flask-Login  
- Flask-SQLAlchemy  

### 🔧 Steps to Set Up Locally  

1️⃣ **Clone the repository**  
```sh
git clone https://github.com/mishesbone/payroll_system.git
cd payroll_system
```

2️⃣ **Create and activate a virtual environment**  
```sh
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3️⃣ **Install dependencies**  
```sh
pip install -r requirements.txt
```

4️⃣ **Set up the database**  
```sh
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

5️⃣ **Run the application**  
```sh
python app.py
```
🌐 Access the app at **`http://127.0.0.1:5000/`**  

---

## 🚀 Deployment  

To push changes to GitHub:  
```sh
git add .
git commit -m "Updated README and project setup"
git push -u origin main
```

For deployment, you can use **Heroku, Render, or DigitalOcean**. Let me know if you need help setting it up!

---

## 🤝 Contributing  
Contributions are welcome! To contribute:  
1. **Fork the repository**  
2. **Create a feature branch** (`git checkout -b feature-branch`)  
3. **Commit your changes** (`git commit -m "Add new feature"`)  
4. **Push to GitHub** (`git push origin feature-branch`)  
5. **Submit a Pull Request** 🚀  

---

## 📜 License  
This project is licensed under the [MIT License](LICENSE).  

---

This improved version:  
✅ **Uses clear sections** for readability  
✅ **Adds proper formatting** (icons, bold text)  
✅ **Provides structured setup instructions**  
