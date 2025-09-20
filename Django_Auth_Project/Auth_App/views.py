from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Employee_Data
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.hashers import check_password, make_password
from .models import Employee_Data
from .forms import EmployeePasswordChangeForm
from django.contrib.auth import update_session_auth_hash



def Home_Page(request):
    return render(request, 'app/home.html')


def Register_Page(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        mobile = request.POST['mobile']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        pincode = request.POST['pincode']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        user = Employee_Data.objects.filter(Email=email).exists()
        
        if user:
            messages.error(request, 'Email Already Exist')
            return render(request, 'app/register.html')
        
        elif password != confirm_password:
            messages.error(request, "Password and Confirm_Password don't Match!!")
            return render(request, 'app/register.html')
            
        else:
            new = Employee_Data.objects.create(First_Name=first_name, Last_Name=last_name, Email=email, Mobile=mobile, Address=address, City=city, State=state, Pincode=pincode, Password=password)
            new.save()
            messages.success(request, 'Register Successfully Done!!')
            return redirect('register')
    return render(request, 'app/register.html')


def Login_Page(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        user = Employee_Data.objects.filter(Email=email).first()
        if user is None:
            messages.error(request, "No account found with this email")
            return render(request, "app/login.html")
        
        if password == user.Password:
            request.session['id'] = user.id
            request.session['First_Name'] = user.First_Name
            request.session['Last_Name'] = user.Last_Name
            request.session['Email'] = user.Email
            request.session['Mobile'] = user.Mobile
            request.session['Address'] = user.Address
            request.session['City'] = user.City
            request.session['State'] = user.State
            request.session['Pincode'] = user.Pincode

            
            messages.success(request, f"Welcome back, {user.First_Name}!")
            return redirect('home')
        else:
            messages.error(request, "Incorrect password")
            return redirect('login')
        
           
    return render(request, "app/login.html")
        

def Logout_Page(request):
    logout(request)
    return redirect('login')


def change_password(request):
    if request.method == "POST":
        form = EmployeePasswordChangeForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']
            confirm_password = form.cleaned_data['confirm_password']

            # Get logged-in user from session
            user_id = request.session.get("id")
            if not user_id:
                messages.error(request, "You must be logged in to change password")
                return redirect("login")

            user = Employee_Data.objects.get(id=user_id)

            # Check old password
            if user.Password != old_password:
                messages.error(request, "Old password is incorrect")
                return render(request, "app/change_password.html", {"form": form})

            # Check new password match
            if new_password != confirm_password:
                messages.error(request, "New passwords do not match")
                return render(request, "app/change_password.html", {"form": form})

            # Update password
            user.Password = new_password
            user.save()

            messages.success(request, "Password updated successfully")
            return redirect("login")
    else:
        form = EmployeePasswordChangeForm()

    return render(request, "app/change_password.html", {"form": form})


