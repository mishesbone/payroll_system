import logging
from models import Employee

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename='payroll_system.log')
logger = logging.getLogger('salary_calculator')

# Constants for tax calculations
TAX_BRACKETS = [
    (0, 9950, 0.10),        # 10% tax rate for income $0-$9,950
    (9951, 40525, 0.12),    # 12% tax rate for income $9,951-$40,525
    (40526, 86375, 0.22),   # 22% tax rate for income $40,526-$86,375
    (86376, 164925, 0.24),  # 24% tax rate for income $86,376-$164,925
    (164926, 209425, 0.32), # 32% tax rate for income $164,926-$209,425
    (209426, 523600, 0.35), # 35% tax rate for income $209,426-$523,600
    (523601, float('inf'), 0.37)  # 37% tax rate for income over $523,600
]

# Social Security tax rate (6.2% up to wage base)
SOCIAL_SECURITY_RATE = 0.062
SOCIAL_SECURITY_WAGE_BASE = 142800

# Medicare tax rate (1.45% on all wages)
MEDICARE_RATE = 0.0145

def calculate_gross_salary(employee, hours_worked=0, overtime_hours=0, overtime_rate=1.5):
    """
    Calculate gross salary for an employee
    
    For salaried employees, just return the monthly salary
    For hourly employees, calculate based on hours worked and overtime
    """
    try:
        if not isinstance(employee, Employee):
            logger.error("Invalid employee object provided")
            return 0.0
            
        # Calculate based on position type (assume position contains "hourly" for hourly employees)
        if "hourly" in employee.position.lower():
            # Hourly employee
            regular_pay = employee.salary * hours_worked
            overtime_pay = employee.salary * overtime_hours * overtime_rate
            return regular_pay + overtime_pay
        else:
            # Salaried employee - return monthly salary
            return employee.salary
    except Exception as e:
        logger.error(f"Error calculating gross salary: {e}")
        return 0.0

def calculate_income_tax(annual_salary):
    """Calculate income tax based on tax brackets"""
    try:
        if annual_salary <= 0:
            return 0.0
            
        tax_amount = 0.0
        remaining_income = annual_salary
        
        for lower, upper, rate in TAX_BRACKETS:
            if remaining_income <= 0:
                break
                
            # Calculate taxable amount in this bracket
            taxable_in_bracket = min(upper - lower + 1, remaining_income)
            tax_amount += taxable_in_bracket * rate
            remaining_income -= taxable_in_bracket
            
        return tax_amount
    except Exception as e:
        logger.error(f"Error calculating income tax: {e}")
        return 0.0

def calculate_social_security_tax(annual_salary):
    """Calculate social security tax"""
    try:
        # Social security tax is capped at the wage base
        taxable_amount = min(annual_salary, SOCIAL_SECURITY_WAGE_BASE)
        return taxable_amount * SOCIAL_SECURITY_RATE
    except Exception as e:
        logger.error(f"Error calculating social security tax: {e}")
        return 0.0

def calculate_medicare_tax(annual_salary):
    """Calculate medicare tax"""
    try:
        # Medicare tax applies to all wages (no cap)
        return annual_salary * MEDICARE_RATE
    except Exception as e:
        logger.error(f"Error calculating medicare tax: {e}")
        return 0.0

def calculate_net_salary(employee, gross_salary, annual_salary):
    """Calculate net salary after taxes"""
    try:
        if not isinstance(employee, Employee) or gross_salary <= 0:
            logger.error("Invalid parameters for net salary calculation")
            return 0.0
            
        # Calculate taxes
        income_tax = calculate_income_tax(annual_salary) / 12  # Monthly income tax
        social_security = calculate_social_security_tax(annual_salary) / 12  # Monthly social security
        medicare = calculate_medicare_tax(annual_salary) / 12  # Monthly medicare
        
        # Calculate net salary
        net_salary = gross_salary - (income_tax + social_security + medicare)
        
        # Ensure net salary is not negative
        return max(0.0, net_salary)
    except Exception as e:
        logger.error(f"Error calculating net salary: {e}")
        return 0.0

def calculate_payroll(employee, is_monthly=True, hours_worked=0, overtime_hours=0):
    """Calculate payroll for an employee"""
    try:
        if not isinstance(employee, Employee):
            logger.error("Invalid employee object provided")
            return None
            
        result = {}
        
        # Calculate gross salary
        if is_monthly:
            # For monthly payroll (salaried employees)
            gross_salary = employee.salary
            annual_salary = employee.salary * 12
        else:
            # For hourly employees
            gross_salary = calculate_gross_salary(employee, hours_worked, overtime_hours)
            annual_salary = gross_salary * 26  # Assuming bi-weekly pay periods (26 per year)
        
        # Calculate net salary
        net_salary = calculate_net_salary(employee, gross_salary, annual_salary)
        
        # Create result dictionary
        result = {
            'employee_id': employee.employee_id,
            'employee_name': employee.full_name,
            'gross_salary': round(gross_salary, 2),
            'income_tax': round(calculate_income_tax(annual_salary) / 12, 2),
            'social_security': round(calculate_social_security_tax(annual_salary) / 12, 2),
            'medicare': round(calculate_medicare_tax(annual_salary) / 12, 2),
            'net_salary': round(net_salary, 2)
        }
        
        return result
    except Exception as e:
        logger.error(f"Error calculating payroll: {e}")
        return None
