from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail,EmailMessage
from loginsystem import settings
from loginsystem.settings import EMAIL_HOST_USER
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from . tokens import generate_token
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
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
        myuser.is_active = False
        myuser.save()
        
        messages.success(request, 'Account successfully created')
        
        # sending emails
        subject = 'Welcome to login pages'
        message = "Hello " + myuser.first_name +" || \n Welcome to our website! \n We have lso sent you are confirmation code. Please check your email and confirm your account in order to activate your account! \n \n THANK YOU"
        from_email = EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list)
        
        # Confimation Email
        current_site = get_current_site(request)
        email_subject = 'Confirm your email'
        message2 = render_to_string('email_confirmation.html',{
            'name':myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email = EmailMessage(
            email_subject, message2, settings.EMAIL_HOST_USER,[myuser.email]
        )
        email.fail_silently = True
        email.send()
        
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
    
def activate(request, uidb64, token):
    try:
        uid= force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None
        
    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active =True
        myuser.save()
        login(request, myuser)
        return redirect('home')
    else:
        return render(request,'activation_failed.html')
        