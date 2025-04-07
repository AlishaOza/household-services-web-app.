from flask_wtf import FlaskForm
from wtforms import DecimalField, FileField, FloatField, IntegerField, Label, StringField, PasswordField, SelectField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, DataRequired, Length, NumberRange ,Email, EqualTo
from flask_wtf.file import FileRequired, FileAllowed
import re

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', [
        DataRequired(),
        Length(min=12)
    ])
    confirm_password = PasswordField('Confirm Password', [
       DataRequired(),
       EqualTo('password', message='Passwords must match')
    ])
    role = SelectField('Role', choices=[('customer', 'Customer'), ('professional', 'Service Professional')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    submit = SubmitField('Login')

class ServiceForm(FlaskForm):
    service_type = SelectField('Service Type', choices=[('haircut', 'Hair Cut'), ('cleaning', 'Cleaning Services'), ('electrical', 'Electrical Services'),('painting', 'Painting Services'),('plumbing', 'Plumbing Services')])
    name = StringField('Service Name', validators=[DataRequired()])
    price = DecimalField('Price', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')

class ProfessionalProfileForm(FlaskForm):
    user_id = StringField('User Id',validators=[DataRequired()])
    user_name = StringField('User Name',validators=[DataRequired()])
    full_name = StringField('Full Name',validators=[DataRequired()])
    service_type = SelectField('Service Type', choices=[], validators=[DataRequired()])
    file = FileField('Upload File', validators=[FileRequired(),FileAllowed(['jpg', 'png', 'pdf', 'jpeg', 'gif'], 'Images and PDFs only!')])
    experience = IntegerField('Experience (in years)', validators=[DataRequired()])
    address = TextAreaField('Address', validators=[DataRequired()])
    pin_code = IntegerField('Pin Code', validators=[DataRequired()])
    
    submit = SubmitField('Update Profile')

    def __init__(self, *args, **kwargs):
        super(ProfessionalProfileForm, self).__init__(*args, **kwargs)
        # Populate the choices dynamically from the database
        self.service_type.choices = [(service.id, service.name) for service in Service.query.all()]

class CustomerProfileForm(FlaskForm):
    user_id = StringField('User Id',validators=[DataRequired()])
    user_name = StringField('User Name(e-mail)',validators=[DataRequired()])
    full_name = StringField('Full Name',validators=[DataRequired()])
    address = TextAreaField('Address', validators=[DataRequired()])
    pin_code = IntegerField('Pin Code', validators=[DataRequired()])
    submit = SubmitField('Update Customer Profile')

class ServiceRemarksForm(FlaskForm):
    request_id = StringField('Request Id',validators=[DataRequired()])
    service_name = StringField('Service Name',validators=[DataRequired()])
    service_description = StringField('Service Description',validators=[DataRequired()])
    full_name = StringField('User Name',validators=[DataRequired()])
    rating = FloatField('Rating', validators=[NumberRange(min=0, max=5, message="Rating must be between 0 and 5.")])
    remarks = TextAreaField('Remarks', validators=[DataRequired()])
    submit = SubmitField('Submit Remarks')

class SearchForm(FlaskForm):
    search_type = SelectField('Search Type', choices=[('service', 'Service'), ('professional', 'Professional'),('customer','Customer'),('service_request','Service Request')])
    search_text = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Search')


class ProfessionalSearchForm(FlaskForm):
    search_type = SelectField('Search Type', choices=[('date', 'Date'), ('location', 'Location'),('pin', 'PIN')])
    search_text = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Search')

    def validate_search_text(self, field):
        # Validate based on the search type
        if self.search_type.data == 'date':
            # For date, expect a valid format (YYYY-MM-DD)
            if not re.match(r'^\d{4}-\d{2}-\d{2}$', field.data):
                raise ValidationError('Invalid date format. Use YYYY-MM-DD.')
                
        
        elif self.search_type.data == 'location':
            # For location, we expect it to be alphabetic 
            if not field.data.isalpha():
                raise ValidationError('Location must contain only alphabetic characters.')

        elif self.search_type.data == 'pin':
            # For PIN, expect only numbers (and a certain length if necessary, e.g., 6 digits)
            if not field.data.isdigit() or len(field.data) != 6:
                raise ValidationError('PIN must be a 6-digit number.')
            
class CustomerSearchForm(FlaskForm):
    search_type = SelectField('Search Type', choices=[('service', 'Service Name'), ('location', 'Location'),('pin', 'PIN')])
    search_text = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Search')

    def validate_search_text(self, field):
        # Validate based on the search type        
        if self.search_type.data == 'location':
            # For location, we expect it to be alphabetic 
            if not field.data.isalpha():
                raise ValidationError('Location must contain only alphabetic characters.')

        elif self.search_type.data == 'pin':
            # For PIN, expect only numbers (and a certain length if necessary, e.g., 6 digits)
            if not field.data.isdigit() or len(field.data) != 6:
                raise ValidationError('PIN must be a 6-digit number.')
        
        elif self.search_type.data == 'service':
            # For location, we expect it to be alphabetic 
            if not field.data.isalpha():
                raise ValidationError('Location must contain only alphabetic characters.')
class ForgotPasswordForm(FlaskForm):
    email = StringField('Username', validators=[InputRequired(), Length(min=4, max=50)])
    submit = SubmitField('Send Reset Link')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', [
        DataRequired(),
        Length(min=12)
    ])
    confirm_password = PasswordField('Confirm Password', [
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Reset Password')
