# import os
import django

django.setup()
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime
import os
import pyscreenshot
import time
import multiprocessing


def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Email is exist ')
                return redirect(register)
            else:
                user = User.objects.create_user(username=username,
                                                password=password, email=email, first_name=first_name,
                                                last_name=last_name)
                user.set_password(password)
                user.save()
                print("success")
                return redirect('login_user')
        else:
            messages.info(request, 'Both passwords are not matching')
            return redirect(register)
    else:
        # print("no post method")
        return render(request, 'register.html')


def take_screenshots():
    while True:
        datetimeNow = datetime.now()
        datetimeString = datetimeNow.strftime("%d-%m-%Y %H-%M-%S")
        save_path = "static/screenshots/"
        fileName = os.path.join(save_path, f"screenshort-{datetimeString}.png")
        image = pyscreenshot.grab()
        image.save(fileName)
        image = ""
        datetimeString = ""
        time.sleep(3)


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            global proc
            proc = multiprocessing.Process(target=take_screenshots, args=())
            proc.start()
            return render(request, 'home.html')

        else:
            messages.info(request, 'Invalid Username or Password')
            return redirect('login_user')

    else:
        return render(request, 'login.html')


def logout_user(request):
    logout(request)
    proc.terminate()
    return redirect('home')
