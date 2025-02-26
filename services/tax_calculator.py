class TaxCalculator:
    def __init__(self, tax_brackets):
        """
        Initialize the tax calculator with given tax brackets.
        :param tax_brackets: List of tuples (income_threshold, tax_rate)
        """
        self.tax_brackets = sorted(tax_brackets, key=lambda x: x[0])
    
    def calculate_tax(self, salary):
        """
        Calculate tax based on progressive tax brackets.
        :param salary: Employee's gross salary
        :return: Tax amount
        """
        tax = 0.0
        previous_threshold = 0
        
        for threshold, rate in self.tax_brackets:
            if salary > threshold:
                tax += (threshold - previous_threshold) * rate
                previous_threshold = threshold
            else:
                tax += (salary - previous_threshold) * rate
                break
        
        return round(tax, 2)

# Example tax brackets (Nigeria PAYE Tax 2023 example)
nigeria_tax_brackets = [
    (300000, 0.07),  # 7% on first 300,000
    (600000, 0.11),  # 11% on next 300,000
    (1100000, 0.15), # 15% on next 500,000
    (1600000, 0.19), # 19% on next 500,000
    (3200000, 0.21), # 21% on next 1,600,000
    (float('inf'), 0.24) # 24% on remaining income
]

def calculate_employee_tax(salary):
    calculator = TaxCalculator(nigeria_tax_brackets)
    return calculator.calculate_tax(salary)

if __name__ == "__main__":
    sample_salary = 2500000
    print(f"Tax for salary {sample_salary}: NGN {calculate_employee_tax(sample_salary)}")
