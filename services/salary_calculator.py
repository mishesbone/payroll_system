class SalaryCalculator:
    """
    This class provides utility functions to calculate salary components such as gross salary,
    total deductions, and net salary based on payroll details.
    """

    def __init__(self, base_salary, bonuses=0, deductions=0, tax_rate=0.1, pension_rate=0.05):
        """
        Initialize salary calculator with base salary, bonuses, deductions,
        tax rate, and pension contribution rate.
        """
        self.base_salary = base_salary
        self.bonuses = bonuses
        self.deductions = deductions
        self.tax_rate = tax_rate
        self.pension_rate = pension_rate

    def calculate_gross_salary(self):
        """Calculate gross salary before deductions."""
        return self.base_salary + self.bonuses

    def calculate_tax(self):
        """Calculate tax deductions based on the tax rate."""
        return self.calculate_gross_salary() * self.tax_rate

    def calculate_pension(self):
        """Calculate pension contribution based on pension rate."""
        return self.base_salary * self.pension_rate

    def calculate_net_salary(self):
        """Calculate net salary after deductions, tax, and pension."""
        gross_salary = self.calculate_gross_salary()
        tax = self.calculate_tax()
        pension = self.calculate_pension()
        net_salary = gross_salary - (tax + pension + self.deductions)
        return net_salary

    def generate_salary_breakdown(self):
        """Return a dictionary breakdown of salary components."""
        return {
            "Base Salary": self.base_salary,
            "Bonuses": self.bonuses,
            "Gross Salary": self.calculate_gross_salary(),
            "Tax Deduction": self.calculate_tax(),
            "Pension Contribution": self.calculate_pension(),
            "Other Deductions": self.deductions,
            "Net Salary": self.calculate_net_salary()
        }

    @staticmethod
    def calculate_overtime(overtime_hours, overtime_rate):
        """Calculate overtime payment."""
        return overtime_hours * overtime_rate

    @staticmethod
    def calculate_gross_salary_static(basic_salary, overtime_amount, allowances, bonuses):
        """Calculate gross salary using static method."""
        return basic_salary + overtime_amount + allowances + bonuses

    @staticmethod
    def calculate_total_deductions(tax_deduction, insurance_deduction, other_deductions):
        """Calculate total deductions."""
        return tax_deduction + insurance_deduction + other_deductions

    @staticmethod
    def calculate_net_salary_static(gross_salary, total_deductions):
        """Calculate net salary after deductions using static method."""
        return gross_salary - total_deductions

    @classmethod
    def process_payroll(cls, payroll):
        """Compute all salary components and update the payroll record."""
        payroll.overtime_amount = cls.calculate_overtime(payroll.overtime_hours, payroll.overtime_rate)
        payroll.gross_salary = cls.calculate_gross_salary_static(
            payroll.basic_salary, payroll.overtime_amount, payroll.allowances, payroll.bonuses
        )
        payroll.total_deductions = cls.calculate_total_deductions(
            payroll.tax_deduction, payroll.insurance_deduction, payroll.other_deductions
        )
        payroll.net_salary = cls.calculate_net_salary_static(payroll.gross_salary, payroll.total_deductions)
        return payroll


# Example usage:
if __name__ == "__main__":
    salary_calc = SalaryCalculator(base_salary=5000, bonuses=500, deductions=200)
    print(salary_calc.generate_salary_breakdown())
