from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import (authenticate, login as dj_login, logout as dj_logout)
from django.forms import ValidationError

@login_required()
def main(request):
    return render(request, 'multiply/main.html', )
