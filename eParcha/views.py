from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
# from django.db.models import Q
from django.utils.datastructures import MultiValueDictKeyError
# from django.contrib import messages
from users.models import User

def index(request):

    if request.method == "GET":
        return render(request,"index.html")

    elif request.method == "POST":
        # query = str(request.POST['book_name']).lower()
        # try:
        #     data = books.objects.filter(Q(name__contains=query) | Q(author_name__contains=query) | Q(subject__contains=query)).values('name','author_name','price').all()
        # except MultiValueDictKeyError:
        #     data = ""
        #     pass
        # context = {"books":data}
        # return render(request,"index.html",context)
        print(request.POST)
        return render(request,"index.html")
    else:
        return redirect('index')

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

        return redirect('index')

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

        return redirect('index')

def logout_user(request):
    logout(request)
    return redirect('index')