from typing import Any
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(render_value=True))


class EditProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=25)
    password1 = forms.CharField(
        label='New password (Not required)', required=False, widget=forms.PasswordInput(render_value=True))
    password2 = forms.CharField(
        label='Repeat new password', required=False, widget=forms.PasswordInput(render_value=True))
    password = forms.CharField(
        label='Enter current password to confirm changes', widget=forms.PasswordInput(render_value=True))

    class Meta:
        model = User
        fields = ['username']

    def clean_username(self):
        data = self.cleaned_data.get('username')
        if data == '':
            return self.instance.username
        else:
            return data

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if password != '':
            validate_password(password, user=self.instance)
        return password

    def clean(self):
        cleaned_data = super().clean()
        if len(self.errors) != 0:
            return cleaned_data
        password = cleaned_data['password']
        pass1 = cleaned_data['password1']
        pass2 = cleaned_data['password2']
        new_username = cleaned_data['username']

        authenticated = check_password(password, self.instance.password)
        if authenticated is False:
            self.add_error('password', 'Invalid password')

        if pass1 != '':
            if pass1 != pass2:
                self.add_error('password2', 'Passwords dont match')
            else:
                self.instance.set_password(pass1)
        return cleaned_data


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        css_error_label = 'errorlist'
