import pickle
import os
import logging
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class SalaryPredictor:
    """
    Model to predict future salary trends based on historical data
    """
    def __init__(self, model_path=None):
        self.model_path = model_path
        self.model = None
        self.scaler = None
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the model, load from file if exists, otherwise create new"""
        if self.model_path and os.path.exists(self.model_path):
            try:
                with open(self.model_path, 'rb') as f:
                    self.model = pickle.load(f)
                logger.info(f"Loaded salary prediction model from {self.model_path}")
            except Exception as e:
                logger.error(f"Failed to load model: {str(e)}")
                self._create_new_model()
        else:
            self._create_new_model()
    
    def _create_new_model(self):
        """Create a new model if no saved model exists"""
        self.model = Pipeline([
            ('scaler', StandardScaler()),
            ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
        ])
        logger.info("Created new salary prediction model")
    
    def train(self, payroll_data):
        """
        Train the model using historical payroll data
        
        Args:
            payroll_data: DataFrame with columns 'month', 'avg_gross', 'avg_net', etc.
        """
        if payroll_data.empty or len(payroll_data) < 6:
            logger.warning("Not enough data to train model (need at least 6 months)")
            return False
        
        try:
            # Convert month to datetime if string
            if isinstance(payroll_data['month'].iloc[0], str):
                payroll_data['month'] = pd.to_datetime(payroll_data['month'])
            
            # Sort by month
            payroll_data = payroll_data.sort_values('month')
            
            # Extract features
            X = self._extract_features(payroll_data)
            
            # Target variables
            y_gross = payroll_data['avg_gross'].values
            y_net = payroll_data['avg_net'].values
            
            # Train models
            self.model_gross = Pipeline([
                ('scaler', StandardScaler()),
                ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
            ])
            
            self.model_net = Pipeline([
                ('scaler', StandardScaler()),
                ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
            ])
            
            self.model_gross.fit(X, y_gross)
            self.model_net.fit(X, y_net)
            
            # Save model if path is specified
            if self.model_path:
                with open(self.model_path, 'wb') as f:
                    pickle.dump({'gross': self.model_gross, 'net': self.model_net}, f)
                logger.info(f"Saved salary prediction model to {self.model_path}")
                
            return True
            
        except Exception as e:
            logger.error(f"Error training model: {str(e)}")
            return False
    
    def _extract_features(self, df):
        """Extract features from payroll data"""
        # Create time-based features
        df = df.copy()
        df['month_num'] = df['month'].dt.month
        df['year'] = df['month'].dt.year
        
        # Create lag features (previous months)
        for i in range(1, 4):  # 3 months of lag features
            if len(df) > i:
                df[f'avg_gross_lag{i}'] = df['avg_gross'].shift(i)
                df[f'avg_net_lag{i}'] = df['avg_net'].shift(i)
        
        # Fill NAs with mean for lag features
        for col in df.columns:
            if 'lag' in col and df[col].isna().any():
                df[col] = df[col].fillna(df[col].mean())
        
        # Select features
        features = ['month_num', 'year']
        for i in range(1, 4):
            features.extend([f'avg_gross_lag{i}', f'avg_net_lag{i}'])
        
        # Return only complete rows
        return df[features].dropna().values
    
    def predict_next_month_payroll(self, historic_data):
        """
        Predict next month's payroll metrics
        
        Args:
            historic_data: DataFrame with historical payroll data
        
        Returns:
            Dictionary with predictions
        """
        try:
            # Train models if not already trained
            if not hasattr(self, 'model_gross') or not hasattr(self, 'model_net'):
                self.train(historic_data)
            
            # Get latest data and prepare features for next month prediction
            df = historic_data.copy()
            
            # Sort by month and get last row
            if isinstance(df['month'].iloc[0], str):
                df['month'] = pd.to_datetime(df['month'])
            
            df = df.sort_values('month')
            last_month = df['month'].iloc[-1]
            
            # Calculate next month
            next_month = last_month + pd.DateOffset(months=1)
            
            # Prepare test data for prediction
            test_data = pd.DataFrame({
                'month': [next_month],
                'avg_gross': [0],  # placeholder
                'avg_net': [0]     # placeholder
            })
            
            # Combine with historical data to create lag features
            combined = pd.concat([df, test_data]).reset_index(drop=True)
            combined = combined.sort_values('month')
            
            # Extract features for the last row (prediction row)
            X_pred = self._extract_features(combined).reshape(1, -1)
            
            # Make predictions
            gross_pred = self.model_gross.predict(X_pred)[0]
            net_pred = self.model_net.predict(X_pred)[0]
            
            # Calculate confidence based on model score
            # This is simplified - in production you would use proper confidence intervals
            confidence = 0.8  # Placeholder
            
            return {
                'avg_gross': float(gross_pred),
                'avg_net': float(net_pred),
                'next_month': next_month.strftime('%Y-%m'),
                'confidence': confidence
            }
            
        except Exception as e:
            logger.error(f"Error predicting next month: {str(e)}")
            return {
                'error': str(e),
                'avg_gross': None,
                'avg_net': None,
                'confidence': 0
            }


class AttendancePredictor:
    """
    Model to predict attendance patterns and anomalies
    """
    def __init__(self, model_path=None):
        self.model_path = model_path
        self.model = None
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the model, load from file if exists, otherwise create new"""
        if self.model_path and os.path.exists(self.model_path):
            try:
                with open(self.model_path, 'rb') as f:
                    self.model = pickle.load(f)
                logger.info(f"Loaded attendance prediction model from {self.model_path}")
            except Exception as e:
                logger.error(f"Failed to load model: {str(e)}")
                self._create_new_model()
        else:
            self._create_new_model()
    
    def _create_new_model(self):
        """Create a new model if no saved model exists"""
        self.model = LinearRegression()
        logger.info("Created new attendance prediction model")
    
    def detect_anomalies(self, attendance_data):
        """
        Detect anomalies in attendance data
        
        Args:
            attendance_data: DataFrame with attendance records
        
        Returns:
            Dictionary with anomalies and patterns
        """
        try:
            if attendance_data.empty:
                return {
                    'status': 'error',
                    'message': 'No attendance data provided'
                }
            
            # Analyze patterns by day of week
            if 'date' in attendance_data.columns:
                attendance_data['day_of_week'] = pd.to_datetime(attendance_data['date']).dt.dayofweek
                
                day_stats = attendance_data.groupby('day_of_week').agg({
                    'working_hours': ['mean', 'std'],
                    'status': lambda x: (x == 'late').mean() * 100  # Percentage of late arrivals
                })
                
                # Detect days with high late percentage
                late_threshold = 20  # 20% late is considered high
                high_late_days = day_stats['status'].loc[day_stats['status'] > late_threshold].index.tolist()
                
                # Detect employees with attendance issues
                if 'employee_id' in attendance_data.columns:
                    employee_stats = attendance_data.groupby('employee_id').agg({
                        'status': lambda x: (x == 'late').mean() * 100,  # Late %
                        'working_hours': 'mean'
                    })
                    
                    # Employees with high late percentage
                    late_employees = employee_stats.loc[employee_stats['status'] > late_threshold].index.tolist()
                    
                    # Employees with low working hours
                    hours_threshold = 7.0  # 7 hours is considered low
                    low_hours_employees = employee_stats.loc[employee_stats['working_hours'] < hours_threshold].index.tolist()
                    
                    return {
                        'status': 'success',
                        'day_patterns': {
                            'high_late_days': [self._day_name(day) for day in high_late_days],
                            'day_stats': day_stats.to_dict()
                        },
                        'employee_anomalies': {
                            'late_employees': late_employees,
                            'low_hours_employees': low_hours_employees
                        }
                    }
                else:
                    return {
                        'status': 'success',
                        'day_patterns': {
                            'high_late_days': [self._day_name(day) for day in high_late_days],
                            'day_stats': day_stats.to_dict()
                        }
                    }
            else:
                return {
                    'status': 'error',
                    'message': 'Attendance data missing date column'
                }
                
        except Exception as e:
            logger.error(f"Error detecting attendance anomalies: {str(e)}")
            return {
                'status': 'error',
                'message': f"Anomaly detection failed: {str(e)}"
            }
    
    def _day_name(self, day_number):
        """Convert day number to name"""
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        return days[int(day_number)]
    
    def predict_future_attendance(self, employee_id, historical_data, days=30):
        """
        Predict future attendance patterns for an employee
        
        Args:
            employee_id: Employee ID
            historical_data: DataFrame with historical attendance
            days: Number of days to predict
        
        Returns:
            Dictionary with predictions
        """
        try:
            # Filter data for this employee
            emp_data = historical_data[historical_data['employee_id'] == employee_id].copy()
            
            if len(emp_data) < 30:
                return {
                    'status': 'error',
                    'message': 'Not enough historical data for this employee'
                }
            
            # Prepare time series features
            emp_data['date'] = pd.to_datetime(emp_data['date'])
            emp_data = emp_data.sort_values('date')
            
            emp_data['day_of_week'] = emp_data['date'].dt.dayofweek
            emp_data['month'] = emp_data['date'].dt.month
            emp_data['day'] = emp_data['date'].dt.day
            
            # One-hot encode day of week
            for i in range(7):
                emp_data[f'dow_{i}'] = (emp_data['day_of_week'] == i).astype(int)
            
            # Create train data
            X = emp_data[['day_of_week', 'month', 'day'] + [f'dow_{i}' for i in range(7)]].values
            y_hours = emp_data['working_hours'].values
            
            # Train model
            model_hours = LinearRegression()
            model_hours.fit(X, y_hours)
            
            # Generate future dates
            last_date = emp_data['date'].max()
            future_dates = [last_date + timedelta(days=i+1) for i in range(days)]
            
            # Prepare test data
            future_data = pd.DataFrame({
                'date': future_dates,
                'day_of_week': [d.weekday() for d in future_dates],
                'month': [d.month for d in future_dates],
                'day': [d.day for d in future_dates]
            })
            
            # One-hot encode day of week for prediction data
            for i in range(7):
                future_data[f'dow_{i}'] = (future_data['day_of_week'] == i).astype(int)
            
            # Make predictions
            X_pred = future_data[['day_of_week', 'month', 'day'] + [f'dow_{i}' for i in range(7)]].values
            future_data['predicted_hours'] = model_hours.predict(X_pred)
            
            # Calculate probability of being present
            # Simplified approach - in production would use logistic regression
            dow_present_rate = emp_data.groupby('day_of_week')['status'].apply(
                lambda x: (x == 'present').mean()
            ).to_dict()
            
            future_data['present_probability'] = future_data['day_of_week'].map(dow_present_rate)
            
            # Fill missing probabilities
            future_data['present_probability'] = future_data['present_probability'].fillna(0.9)
            
            # Predict status (simple rule-based approach)
            def predict_status(row):
                if row['day_of_week'] >= 5:  # Weekend
                    return 'weekend'
                if row['present_probability'] < 0.7:
                    return 'likely_absent'
                if row['present_probability'] < 0.9:
                    return 'may_be_late'
                return 'likely_present'
            
            future_data['predicted_status'] = future_data.apply(predict_status, axis=1)
            
            return {
                'status': 'success',
                'predictions': future_data[['date', 'predicted_hours', 'present_probability', 'predicted_status']].to_dict('records')
            }
            
        except Exception as e:
            logger.error(f"Error predicting future attendance: {str(e)}")
            return {
                'status': 'error',
                'message': f"Prediction failed: {str(e)}"
            }