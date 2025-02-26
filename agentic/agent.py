import os
import logging
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from sqlalchemy import func

from app import db
from models.employee import Employee
from models.payroll import Payroll
from models.attendance import Attendance
from models.leave import Leave
from .predictive_models import SalaryPredictor, AttendancePredictor
from .nlp_processor import NLPProcessor

logger = logging.getLogger(__name__)

class PayrollAgent:
    """
    AI agent that handles intelligent payroll processing and analysis
    """
    def __init__(self):
        self.nlp_processor = NLPProcessor()
        self.salary_predictor = SalaryPredictor()
        self.attendance_predictor = AttendancePredictor()
    
    def analyze_payroll_trends(self, months=12):
        """
        Analyze payroll trends over the specified number of months
        """
        try:
            # Get current date
            now = datetime.now()
            start_date = now - timedelta(days=30 * months)
            
            # Query payroll data
            payroll_data = db.session.query(
                Payroll.month,
                Payroll.year,
                func.avg(Payroll.gross_salary).label('avg_gross'),
                func.avg(Payroll.net_salary).label('avg_net'),
                func.avg(Payroll.tax_deduction).label('avg_tax'),
                func.count(Payroll.id).label('count')
            ).filter(
                Payroll.payment_date >= start_date
            ).group_by(
                Payroll.year, Payroll.month
            ).all()
            
            # Convert to DataFrame for analysis
            df = pd.DataFrame([
                {
                    'month': f"{row.year}-{row.month:02d}",
                    'avg_gross': float(row.avg_gross),
                    'avg_net': float(row.avg_net),
                    'avg_tax': float(row.avg_tax),
                    'count': int(row.count)
                }
                for row in payroll_data
            ])
            
            if df.empty:
                return {
                    'status': 'error',
                    'message': 'No payroll data available for analysis'
                }
            
            # Perform trend analysis
            df['month'] = pd.to_datetime(df['month'] + '-01')
            df = df.sort_values('month')
            
            # Calculate growth rates
            df['gross_growth'] = df['avg_gross'].pct_change() * 100
            df['net_growth'] = df['avg_net'].pct_change() * 100
            
            # Identify anomalies
            mean_gross = df['avg_gross'].mean()
            std_gross = df['avg_gross'].std()
            df['is_anomaly'] = np.abs(df['avg_gross'] - mean_gross) > 2 * std_gross
            
            anomalies = df[df['is_anomaly']].to_dict('records')
            
            # Generate insights
            insights = []
            if len(df) >= 3:
                recent_trend = df['avg_gross'].iloc[-3:].pct_change().mean() * 100
                if recent_trend > 5:
                    insights.append(f"Payroll costs are trending upward ({recent_trend:.1f}% on average in the last quarter)")
                elif recent_trend < -5:
                    insights.append(f"Payroll costs are trending downward ({-recent_trend:.1f}% on average in the last quarter)")
                
                # Tax analysis
                tax_ratio = df['avg_tax'].iloc[-1] / df['avg_gross'].iloc[-1] * 100
                avg_tax_ratio = (df['avg_tax'] / df['avg_gross'] * 100).mean()
                if abs(tax_ratio - avg_tax_ratio) > 2:
                    insights.append(f"Current tax ratio ({tax_ratio:.1f}%) differs from historical average ({avg_tax_ratio:.1f}%)")
            
            # Future predictions
            if len(df) >= 6:
                next_month_prediction = self.salary_predictor.predict_next_month_payroll(df)
                
                return {
                    'status': 'success',
                    'data': df.to_dict('records'),
                    'anomalies': anomalies,
                    'insights': insights,
                    'prediction': {
                        'next_month': {
                            'avg_gross': float(next_month_prediction['avg_gross']),
                            'avg_net': float(next_month_prediction['avg_net']),
                            'confidence': float(next_month_prediction['confidence'])
                        }
                    }
                }
            else:
                return {
                    'status': 'success',
                    'data': df.to_dict('records'),
                    'anomalies': anomalies,
                    'insights': insights,
                    'prediction': {
                        'message': 'Not enough data for prediction (need at least 6 months)'
                    }
                }
                
        except Exception as e:
            logger.error(f"Error in analyze_payroll_trends: {str(e)}")
            return {
                'status': 'error',
                'message': f"Analysis failed: {str(e)}"
            }
    
    def optimize_payroll_process(self, employee_ids=None):
        """
        Analyze and optimize the payroll processing for specified employees
        """
        try:
            # If no employee IDs are specified, get all active employees
            if not employee_ids:
                employees = Employee.query.filter_by(employment_status='active').all()
                employee_ids = [emp.id for emp in employees]
            else:
                employees = Employee.query.filter(Employee.id.in_(employee_ids)).all()
            
            # Current month and year
            now = datetime.now()
            current_month = now.month
            current_year = now.year
            
            results = []
            for employee in employees:
                # Get attendance data for current month
                attendance_data = Attendance.query.filter(
                    Attendance.employee_id == employee.id,
                    func.extract('month', Attendance.date) == current_month,
                    func.extract('year', Attendance.date) == current_year
                ).all()
                
                # Calculate working days, overtime, etc.
                working_days = len([a for a in attendance_data if a.status in ['present', 'late']])
                overtime_hours = sum([a.overtime_hours for a in attendance_data])
                
                # Get leave data
                leave_data = Leave.query.filter(
                    Leave.employee_id == employee.id,
                    Leave.status == 'approved',
                    (func.extract('month', Leave.start_date) == current_month or 
                     func.extract('month', Leave.end_date) == current_month),
                    (func.extract('year', Leave.start_date) == current_year or 
                     func.extract('year', Leave.end_date) == current_year)
                ).all()
                
                leave_days = sum([l.days for l in leave_data])
                
                # Calculate salary based on working days and base salary
                working_days_in_month = 22  # Approximate
                base_salary = employee.base_salary
                
                # Calculate proportional salary if employee didn't work full month
                effective_days = min(working_days + leave_days, working_days_in_month)
                proportional_salary = (base_salary / working_days_in_month) * effective_days
                
                # Calculate overtime pay
                overtime_rate = base_salary / (working_days_in_month * 8) * 1.5  # Assuming 8-hour workday and 1.5x rate
                overtime_pay = overtime_rate * overtime_hours
                
                # Calculate gross salary
                gross_salary = proportional_salary + overtime_pay
                
                # Simple tax calculation (for demonstration)
                tax_rate = 0.2  # 20%
                tax_deduction = gross_salary * tax_rate
                
                # Calculate net salary
                net_salary = gross_salary - tax_deduction
                
                # Store results
                results.append({
                    'employee_id': employee.id,
                    'employee_name': employee.full_name,
                    'base_salary': base_salary,
                    'working_days': working_days,
                    'leave_days': leave_days,
                    'overtime_hours': overtime_hours,
                    'proportional_salary': proportional_salary,
                    'overtime_pay': overtime_pay,
                    'gross_salary': gross_salary,
                    'tax_deduction': tax_deduction,
                    'net_salary': net_salary,
                    'optimization_suggestions': []
                })
                
                # Generate optimization suggestions
                suggestions = []
                
                # Check for overtime patterns
                if overtime_hours > 20:
                    suggestions.append("High overtime detected. Consider reviewing workload or hiring additional staff.")
                
                # Check for leave patterns
                if leave_days > 5:
                    suggestions.append("High leave usage. May want to review scheduling.")
                
                # Check for salary anomalies
                avg_salary = db.session.query(func.avg(Payroll.gross_salary)).filter(
                    Payroll.employee_id == employee.id,
                    Payroll.payment_status == 'paid'
                ).scalar() or 0
                
                if abs(gross_salary - avg_salary) > 0.2 * avg_salary and avg_salary > 0:
                    suggestions.append(f"Salary deviation of {abs(gross_salary - avg_salary) / avg_salary:.1%} from average. Verify calculations.")
                
                results[-1]['optimization_suggestions'] = suggestions
            
            return {
                'status': 'success',
                'optimization_results': results
            }
                
        except Exception as e:
            logger.error(f"Error in optimize_payroll_process: {str(e)}")
            return {
                'status': 'error',
                'message': f"Optimization failed: {str(e)}"
            }
    
    def process_natural_language_query(self, query):
        doc = self.nlp(query)
        
        # Extract named entities
        entities = {ent.label_: ent.text for ent in doc.ents}
        
        # Identify key terms
        key_terms = [token.text.lower() for token in doc if token.pos_ in ["NOUN", "PROPN", "NUM"]]
        
        # Process the query based on extracted entities and key terms
        if "DATE" in entities:
            date = parser.parse(entities["DATE"]).strftime("%Y-%m-%d")
            result = [entry for entry in self.payroll_data if entry.get("date") == date]
        elif "MONEY" in entities:
            amount = float(re.sub(r'[^0-9.]', '', entities["MONEY"]))
            result = [entry for entry in self.payroll_data if entry.get("salary", 0) == amount]
        elif "PERSON" in entities:
            name = entities["PERSON"].lower()
            result = [entry for entry in self.payroll_data if entry.get("employee_name", "").lower() == name]
        else:
            result = "I'm not sure how to process that query. Can you rephrase?"
        
        return result