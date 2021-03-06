from django.contrib.auth.models import User
from django.forms import ModelForm, TextInput, ValidationError
from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30,
                               widget=TextInput(attrs={
                                   'type': 'text',
                                   'class': 'form-control text-center border border-success',
                                   'name': 'name',
                                   'id': 'inputUsername',
                                   'placeholder': '',
                                   'required': '',
                                   'aria-describedby': "inputUsernameHelp",
                               }))
    password = forms.CharField(max_length=30,
                               widget=TextInput(attrs={
                                   'type': 'password',
                                   'class': 'form-control text-center border border-success',
                                   'name': 'password',
                                   'id': 'inputPassword',
                                   'placeholder': '',
                                   'required': '',
                                   'aria-describedby': "inputPasswordHelp",
                               }))


class RegistrationForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']

        widgets = {
            'username': TextInput(attrs={
                'type': 'text',
                'class': 'form-control text-center',
                'name': 'name',
                'id': 'inputUsername',
                'placeholder': '',
                'required': '',
                'aria-describedby': "inputUsernameHelp",
            }),
            'password': TextInput(attrs={
                'type': 'password',
                'class': 'form-control text-center',
                'name': 'password',
                'id': 'inputPassword',
                'placeholder': '',
                'required': '',
                'aria-describedby': "inputPasswordHelp",
            }),
            'email': TextInput(attrs={
                'type': 'email',
                'class': 'form-control text-center',
                'name': 'email',
                'id': 'inputEmail',
                'placeholder': '',
                'required': '',
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
