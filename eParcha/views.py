from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
# from django.db.models import Q
from django.utils.datastructures import MultiValueDictKeyError
from .pyscripts.emailpdf import *
# from django.contrib import messages
from users.models import User
from qr_code.qrcode.utils import QRCodeOptions


def home(request):
    return render(request, "home.html")

def index(request):

    if request.user.is_authenticated :
        if request.method == "GET":
            return render(request,"index.html",{"name": request.user.name, "mcin":request.user.mcin})

        if request.method == "POST":
            d = dict(request.POST)
            d.pop('csrfmiddlewaretoken')
            d.pop('submit')
            func({key:d[key][0] for key in d})
            text = "\n".join([f"{x} {d[x][0]}" for x in d])
            print(text)
            context = dict(
                my_options=QRCodeOptions(size='L', border=6, error_correction='L'),
                text=text
            )
            return render(request,"qr_code.html",context=context)

    return redirect('home')

    

def login_user(request):

    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('index')
        return render(request,"login.html")

    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['pass']
        print(email,password)
        # user = authenticate(request,email=email,password=password)
        check = User.objects.filter(email=email)
        # print(user)
        if len(check)==1 and check[0].password == password:
            login(request,check[0],backend='django.contrib.auth.backends.ModelBackend')
        else:
            return redirect('login')

        return redirect('home')

def register(request):

    if request.method == "GET":
        return render(request,"register.html")

    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        mobile_no = request.POST['mobile_no']
        check = User.objects.filter(email=email)

        if len(check) != 0:
            return redirect('register')

        password = request.POST['password']
        usr = User.objects.create(email=email,password=password,name=name,mobile_no=mobile_no)

        if usr is not None:
            usr.save()
            login(request,usr,backend='django.contrib.auth.backends.ModelBackend')
        else:
            return redirect('register')

        return redirect('home')

def logout_user(request):
    logout(request)
    return redirect('home')