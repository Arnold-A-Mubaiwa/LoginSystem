from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

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
        # pass2 = request.POST['pass2']
        
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        
        myuser.save()
        
        messages.success(request, 'Account successfully created'
                         )
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
    