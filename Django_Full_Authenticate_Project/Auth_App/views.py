from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth import get_user_model

# import this for sending email to user
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .forms import RegistrationForm, UserLoginForm


# Create your views here.

@login_required(login_url='login')
def homepage(request):
    return render(request, 'home.html')


def register_page(request):
    form = RegistrationForm()
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # Send activation email
            current_site = get_current_site(request)
            mail_subject = "Activate your account"
            message = render_to_string('authentication/activate_email_message.html', {
                'user': user,  # pass the actual user object
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })

            to_email = form.cleaned_data['email']
            try:
                email = EmailMessage(mail_subject, message, to=[to_email])
                email.send()
                messages.success(request, "Account is created successfully.")
            except Exception as e:
                messages.error(request, f"Failed to send activation email: {e}")
            return redirect('check')
        else:
            messages.error(request, "Account creation failed. Please correct the errors below.")

    return render(request, 'register.html', {'form': form})


def email(request):
    return render(request, 'authentication/email_sent.html')


def login_page(request):
    if request.method == "POST":
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")


            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")  # or your dashboard
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = UserLoginForm()
    return render(request, "login.html", {"form": form})


def logout_page(request):
    logout(request)
    return redirect('login')


def activate(request, uidb64, token):
    User = get_user_model()
    
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'authentication/activation_successful.html')
    else:
        return render(request, 'authentication/activation_unsuccessful.html')