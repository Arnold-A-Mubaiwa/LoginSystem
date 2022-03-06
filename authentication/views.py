from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from loginsystem.settings import EMAIL_HOST_USER
# from django.http import HttpResponse
# Create your views here.
def home(request):
    return render(request,'authentication/index.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        # Tests and validations
        if User.objects.filter(username=username):
            messages.error(request, "Username already exists")
            return redirect('home')
        
        if User.objects.filter(email=email):
            messages.error(request, "Email already registered")
            return redirect('home')
        
        if len(username)>10:
            messages.error(request,"Username must have less that 10 letters")
            
        if pass1 != pass2:
            messages.error(request,"Passwords does not match")
            
        if not username.isalnum():
            messages.error(request, 'Your username must contain letters and numbers only')
            return redirect('home')
        
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        
        myuser.save()
        
        messages.success(request, 'Account successfully created')
        
        # sending emails
        subject = 'Welcome to login pages'
        message = "Hello " + myuser.first_name +" || \n Welcome to our website! \n We have lso sent you are confirmation code. Please check your email and confirm your account in order to activate your account! \n \n THANK YOU"
        from_email = EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list)
        
        return redirect('signin')
        
    return render(request,'authentication/signup.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        
        user = authenticate(username= username, password = pass1)
        
        if user is not None:
            
            login(request, user)
            fname = user.first_name
            return render(request, 'authentication/index.html',{'fname': fname})
            
        else:
            messages.error(request, 'User cridentials are wrong')
            return render(request,'home')
    return render(request,'authentication/signin.html')

def signout(request):
    logout(request)
    messages.success(request,'Logged out succeefully')
    return redirect ('home')
    