from flask_wtf import  FlaskForm
from wtforms import StringField,BooleanField,SubmitField,PasswordField
from  wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from flaskblog.models import User
from flask_login import current_user



class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(),
                                       Length(min=4,max=20)])
    email = StringField('Email',validators=[DataRequired(),Email()])

    password = PasswordField('Password',validators=[DataRequired(),
                                                    Length(min=4,max=16)])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),
                                                                    EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self,username):

        user = User.query.filter_by(username=username.data).first()

        if user:
            raise ValidationError(f"ეს სახელი - {RegistrationForm().username.data}  გამოყენებულია! გთხოვთ აირჩიოთ სხვა.")

    def validate_email(self,email):

        user = User.query.filter_by(email=email.data).first()

        if user:
            raise ValidationError(f"ეს მეილი - {RegistrationForm().email.data}  გამოყენებულია! გთხოვთ აირჩიოთ სხვა.")


class LoginForm(FlaskForm):

    email = StringField('Email',validators=[DataRequired(),Email()])

    password = PasswordField('Password',validators=[DataRequired(),
                                                    Length(min=4,max=16)])
    remember = BooleanField('Remember me!')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(),
                                       Length(min=4,max=20)])
    email = StringField('Email',validators=[DataRequired(),Email()])

    submit = SubmitField('Update')

    def validate_username(self,username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(f"ეს სახელი - {RegistrationForm().username.data}  გამოყენებულია! გთხოვთ აირჩიოთ სხვა.")

    def validate_email(self,email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(f"ეს მეილი - {RegistrationForm().email.data}  გამოყენებულია! გთხოვთ აირჩიოთ სხვა.")

