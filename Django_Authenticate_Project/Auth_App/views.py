from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from .models import EmailOTP
        



@login_required(login_url='login')
def Home_Page(request):
    return render(request, 'app/home.html')


def RegisterView(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect("register")

        user = User.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name, password=password, is_active=False)
        user.save()

        # Generate OTP
        otp = str(EmailOTP().generate_otp())
        EmailOTP.objects.create(user=user, otp=otp)

        # Send OTP to email
        send_mail(
            subject="Your OTP Code",
            message=f"Hello {username}, your OTP is {otp}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
        )

        messages.success(request, "Account created! Please check your email for OTP.")
        return redirect("verify_otp")

    return render(request, "app/register.html")



def verify_otp(request):
    if request.method == "POST":
        username = request.POST.get("username")
        otp_entered = request.POST.get("otp")

        try:
            user = User.objects.get(username=username)
            otp_obj = EmailOTP.objects.get(user=user)

            if otp_obj.otp == otp_entered:
                user.is_active = True
                user.save()
                otp_obj.delete()  # Remove used OTP
                login(request, user)

                messages.success(request, "Your account has been verified and logged in!")
                return redirect("login")
            else:
                messages.error(request, "Invalid OTP, please try again.")

        except User.DoesNotExist:
            messages.error(request, "User not found.")

        except EmailOTP.DoesNotExist:
            messages.error(request, "OTP not generated for this user.")

    return render(request, "app/verify_otp.html")


def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
     
        if not User.objects.filter(username=username).exists():
            messages.error(request, "username is not valid")
            return redirect('/login/')
        
        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, "Invalid Password")
            return redirect('/login/')
        else:
            login(request, user)
            return redirect('/')
    
    return render(request, 'app/login.html')


def logout_user(request):
    logout(request)
    return redirect('login')


