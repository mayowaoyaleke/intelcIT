from django.shortcuts import render,redirect
from .models import UserTable
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as Login,logout as Logout

# Create your views here.
def dash(request):

    return render(request,'home.html',context={})
def logout(request):
    Logout(request)

    return redirect('login')


def login(request):
    if request.POST:
        print(request.POST)
        Password = request.POST['password']
        Email =  request.POST['email']
        user = authenticate(username=Email,password=Password)
        print(user)
        if user is not None:
            Login(request,user)
            return redirect('dash')
        else:
            return  redirect('signup')
    return render(request,'login.html',context={})


def signup(request):
    if request.POST:
        print(request.POST)
        FirstName =request.POST['FirstName']
        LastName = request.POST['LastName']
        Email =  request.POST['Email']
        Password =request.POST.getlist('Password')
        if Password[0]==Password[1]:
            user = User.objects.create(username=Email,first_name= FirstName,last_name=LastName,password=Password[0],email=Email)
            usertabale = UserTable.objects.create(User=user,FirstName=FirstName,LastName=LastName,Password=Password[0],Email=Email)

    return render(request,'signup.html',context={})