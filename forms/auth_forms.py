from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import InputRequired, Email, Length, EqualTo, DataRequired

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[('employee', 'Employee'), ('admin', 'Admin')], validators=[DataRequired()])
    company = StringField('Company', validators=[DataRequired()])
    accept_terms = BooleanField('I accept the Terms and Conditions', validators=[DataRequired()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(), Length(max=100)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6)])
    submit = SubmitField('Login')

class ResetPasswordForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(), Length(max=100)])
    submit = SubmitField('Reset Password')
