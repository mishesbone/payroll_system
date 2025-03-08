-- Create database
CREATE DATABASE IF NOT EXISTS payroll_db;
USE payroll_db;

-- Create employees table
CREATE TABLE IF NOT EXISTS employees (
    employee_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(20),
    hire_date DATE,
    position VARCHAR(100),
    department VARCHAR(50),
    salary DECIMAL(10, 2) DEFAULT 0.00
);

-- Create timesheets table
CREATE TABLE IF NOT EXISTS timesheets (
    timesheet_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT NOT NULL,
    date DATE NOT NULL,
    hours_worked DECIMAL(5, 2) NOT NULL,
    is_overtime BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
);

-- Create payroll_records table
CREATE TABLE IF NOT EXISTS payroll_records (
    record_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT NOT NULL,
    payroll_date DATE NOT NULL,
    payroll_type VARCHAR(20) NOT NULL,
    gross_salary DECIMAL(10, 2) NOT NULL,
    income_tax DECIMAL(10, 2) NOT NULL,
    social_security DECIMAL(10, 2) NOT NULL,
    medicare DECIMAL(10, 2) NOT NULL,
    net_salary DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
);

-- Create user for application
CREATE USER IF NOT EXISTS 'payroll_user'@'localhost' IDENTIFIED BY 'securepassword';
GRANT ALL PRIVILEGES ON payroll_db.* TO 'payroll_user'@'localhost';
FLUSH PRIVILEGES;

-- Insert sample data (optional)
INSERT INTO employees (first_name, last_name, email, phone, hire_date, position, department, salary)
VALUES
    ('John', 'Doe', 'john.doe@example.com', '555-123-4567', '2020-01-15', 'Software Engineer', 'Engineering', 5000.00),
    ('Jane', 'Smith', 'jane.smith@example.com', '555-987-6543', '2019-03-20', 'HR Manager', 'Human Resources', 4500.00),
    ('Mike', 'Johnson', 'mike.johnson@example.com', '555-456-7890', '2021-05-10', 'Accountant', 'Finance', 4000.00),
    ('Sarah', 'Williams', 'sarah.williams@example.com', '555-789-0123', '2018-11-05', 'Sales Rep', 'Sales', 3500.00),
    ('Robert', 'Brown', 'robert.brown@example.com', '555-234-5678', '2022-02-18', 'Hourly Developer', 'Engineering', 25.00);

-- Insert sample timesheet data
INSERT INTO timesheets (employee_id, date, hours_worked, is_overtime)
VALUES
    (5, '2023-04-01', 8.0, FALSE),
    (5, '2023-04-02', 8.0, FALSE),
    (5, '2023-04-03', 8.0, FALSE),
    (5, '2023-04-04', 8.0, FALSE),
    (5, '2023-04-05', 10.0, TRUE);
