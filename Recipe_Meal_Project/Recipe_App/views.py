from django.shortcuts import render, redirect, get_object_or_404
from .models import Recipe
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required(login_url='/login/')
def recipe(request):
    if request.method == 'POST':
        Data = request.POST
        Day = Data.get('Day')
        Name = Data.get('Name')
        Description = Data.get('Description')
        Recipe.objects.create(
            Day = Day,
            Name = Name,
            Description = Description
        )
        return redirect('/')
    
    queryset = Recipe.objects.all()
    if request.GET.get('Search'):
        queryset = queryset.filter(
            Day__icontains=request.GET.get('Search'))
        
    context = {'recipes': queryset}
    return render(request, 'Recipe.html', context)



@login_required(login_url='/login/')
def update_recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id)

    if request.method == 'POST':
        data = request.POST
        recipe.Day = data.get('day')
        recipe.Name = data.get('name')
        recipe.Description = data.get('description')
        recipe.save()
        return redirect('/')

    return render(request, 'Update_Recipe.html', {'recipe': recipe})

@login_required(login_url='/login/')
def delete_recipe(request, id):
    queryset = Recipe.objects.get(id=id)
    queryset.delete()
    return redirect('/')


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            if not User.objects.filter(username=username).exists():
                messages.error(request, 'Username not found')
                return redirect('/login/')

        
            user_obj = authenticate(username=username, password=password)
            if user_obj is not None:
                login(request, user_obj)
                return redirect('recipe')
            else:
                messages.error(request, 'Wrong password')
                return redirect('/login/')

        except Exception as e:
            messages.error(request, f'Something went wrong: {str(e)}')
            return redirect('/login/')

    return render(request, 'login.html')


def register_page(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user_obj = User.objects.filter(username=username)
            if user_obj.exists():
                messages.error(request, 'Username is Taken')
                return redirect('/register/')
            user_obj = User.objects.create(username=username)
            user_obj.set_password(password)
            user_obj.save()
            messages.success(request, 'Account is Created')
            return redirect('/login/')
        except Exception as e:
            messages.error(request, 'Something went wrong')
            return redirect('/register/')
    return render(request, 'Register.html')


def custom_logout(request):
    logout(request)
    return redirect('/login/')


@login_required(login_url='/login/')
def pdf(request):
    if request.method == 'POST':
        Data = request.POST
        Day = Data.get('Day')
        Name = Data.get('Name')
        Description = Data.get('Description')

        Recipe.objects.create(
            Day = Day,
            Name = Name,
            Description = Description,
        )
        return redirect('/pdf/')
    
    queryset = Recipe.objects.all()

    if request.GET.get('Search'):
        queryset = queryset.filter(
            Day__icontains=request.GET.get('Search'))
        
    context = {'recipe': queryset}
    return render(request, 'Pdf.html', context)

