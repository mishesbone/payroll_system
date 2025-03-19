from . import db
from .models import User

def create_default_users():
    try:
        admin = User(
            username='admin', 
            email='admin@example.com', 
            role='admin', 
            company='TestCompany',
            first_name='AdminFirstName', 
            last_name='AdminLastName'
        )
        admin.set_password('AdminPass123')
        
        employee = User(
            username='employee', 
            email='employee@example.com', 
            role='employee', 
            company='TestCompany',
            first_name='EmployeeFirstName', 
            last_name='EmployeeLastName'
        )
        employee.set_password('EmployeePass123')
        
        db.session.add(admin)
        db.session.add(employee)
        db.session.commit()
        print("Default users created successfully.")
    except db.exc.SQLAlchemyError as db_err:
        db.session.rollback()
        print(f"Database error occurred: {db_err}")
    except Exception as e:
        db.session.rollback()
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    create_default_users()
