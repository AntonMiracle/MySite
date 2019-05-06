from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.forms import ModelForm, TextInput, ValidationError
from .models import LoginFormModel


class LoginForm(ModelForm):
    class Meta:
        model = LoginFormModel
        fields = ['username', 'password']
        widgets = {
            'username': TextInput(attrs={
                'type': 'text',
                'class': 'form-control text-center border border-success',
                'name': 'name',
                'id': 'inputUsername',
                'placeholder': '',
                'required': '',
                'aria-describedby': "inputUsernameHelp",
            }),
            'password': TextInput(attrs={
                'type': 'password',
                'class': 'form-control text-center border border-success',
                'name': 'password',
                'id': 'inputPassword',
                'placeholder': '',
                'required': '',
                'aria-describedby': "inputPasswordHelp",
            }),
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        if not User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise ValidationError(u'Name "%s" is not exist.' % username)
        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 6:
            raise ValidationError('Password to short')
        return password


class RegistrationForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']

        widgets = {
            'username': TextInput(attrs={
                'type': 'text',
                'class': 'form-control text-center border border-success',
                'name': 'name',
                'id': 'inputUsername',
                'placeholder': '',
                'required': '',
                'aria-describedby': "inputUsernameHelp",
            }),
            'password': TextInput(attrs={
                'type': 'password',
                'class': 'form-control text-center border border-success',
                'name': 'password',
                'id': 'inputPassword',
                'placeholder': '',
                'required': '',
                'aria-describedby': "inputPasswordHelp",
            }),
            'email': TextInput(attrs={
                'type': 'email',
                'class': 'form-control text-center border border-success',
                'name': 'email',
                'id': 'inputEmail',
                'placeholder': '',
                'aria-describedby': "inputEmailHelp",
            }),
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise ValidationError(u'Name "%s" is already in use.' % username)
        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 6:
            raise ValidationError('Password to short')
        return password
