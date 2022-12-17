from django.forms import Form, CharField, EmailField, PasswordInput, TextInput, EmailInput
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class RegisterForm(Form):
    username = CharField(label='Tài khoản', max_length=30, widget=TextInput(attrs={'placeholder': 'Your User Name'}))
    email = EmailField(label='Email', widget=EmailInput(attrs={'placeholder': 'Email'}))
    password = CharField(label='Mật khẩu', widget=PasswordInput(attrs={'placeholder': 'Password'}))
    confirm_password = CharField(label='Nhập lại mật khẩu', widget=PasswordInput(attrs={'placeholder': 'Confirm password'}))
    first_name = CharField(label='Tên', max_length=30, widget=TextInput(attrs={'placeholder': 'First name'}))
    last_name = CharField(label='Họ', max_length=30, widget=TextInput(attrs={'placeholder': 'Last name'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password', 'first_name', 'last_name']

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise ValidationError(f"User {username} đã tồn tại!")

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)

        except User.DoesNotExist:
            return email
        raise ValidationError(f"Email {email} đã tồn tại!")

        try:
            check_format = validate_email(email)
        except:
            return ValidationError("Email is not in correct format!")
        return email

    def clean_confirm_password(self):
        pas = self.cleaned_data['password']
        cpas = self.cleaned_data['confirm_password']
        MIN_LENGTH = 8
        if pas and cpas:
            if pas != cpas:
                raise ValidationError(f"Password and Confirm password are not matched!")
            else:
                if len(pas) < MIN_LENGTH:
                    raise ValidationError(f"Passwrd should have at least {MIN_LENGTH} character!")
                if pas.isdigit():
                    raise ValidationError("Password should not all numberic!")



    def save(self):
        User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            confirm_password=self.cleaned_data['confirm_password'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
        )


class LoginForm(Form):
    username = CharField(label='Tài khoản', max_length=30, widget=TextInput(attrs={'placeholder': ' Your Account'}))
    password = CharField(label='Mật khẩu', widget=PasswordInput(attrs={'placeholder': 'Password'}))


