from django.shortcuts import render, redirect
from .forms import RegistrationForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import (authenticate, login as dj_login, logout as dj_logout)
from django.forms import ValidationError


def main(request):
    return render(request, 'main/main.html', )


def about(request):
    return render(request, 'main/about.html', )


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()
            dj_login(request,user)
            return redirect('home')
        else:
            return render(request, 'main/registration.html', {'form': form})

    form = RegistrationForm()
    ctx = {'form': form}
    return render(request, 'main/registration.html', ctx)


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user == None:
                form.add_error('username', ValidationError('Incorrect password or name.'))
                return render(request, 'main/login.html', {'form': form})
            dj_login(request, user)
            return redirect('home')
        else:
            return render(request, 'main/login.html', {'form': form})

    form = LoginForm()
    ctx = {'form': form}
    return render(request, 'main/login.html', ctx)


def logout(request):
    user = request.user
    if user != None:
        dj_logout(request)
    return render(request, 'main/main.html')


@login_required
def home(request):
    return render(request, 'main/home.html')
