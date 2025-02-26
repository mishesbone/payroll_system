from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def generate_payslip(employee_name, salary, deductions, net_pay, output_path):
    """Generate a PDF payslip for an employee."""
    if not os.path.exists(os.path.dirname(output_path)):
        os.makedirs(os.path.dirname(output_path))
    
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    
    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, height - 50, "Company Name - Payslip")
    c.setFont("Helvetica", 12)
    
    c.drawString(50, height - 100, f"Employee Name: {employee_name}")
    c.drawString(50, height - 130, f"Basic Salary: ${salary:.2f}")
    c.drawString(50, height - 160, f"Deductions: ${deductions:.2f}")
    c.drawString(50, height - 190, f"Net Pay: ${net_pay:.2f}")
    
    c.line(50, height - 210, 500, height - 210)
    c.drawString(50, height - 240, "Thank you for your service!")
    
    c.save()
    return output_path

if __name__ == "__main__":
    test_path = "output/payslip.pdf"
    generate_payslip("John Doe", 5000, 500, 4500, test_path)
    print(f"Payslip generated: {test_path}")
