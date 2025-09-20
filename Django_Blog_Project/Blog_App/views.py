from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm, UserEditForm, UserAdminForm
from django.views import generic, View
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth import login, logout, authenticate
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class homeview(ListView):
    model = Post
    template_name = 'home.html'
    ordering = ['-Post_Date']


class articleview(DetailView):
    model = Post
    template_name = 'article_detail.html'


class Create_Post(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'create_post.html'
    #fields = '__all__'


class Update_view(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'update.html'
    #fields = '__all__'

class Delete_view(DeleteView):
    model = Post
    template_name = 'delete.html'
    success_url = '/'


class UserRegisterView(generic.CreateView):
    form_class = UserCreationForm
    success_url = '/login/'
    template_name = 'register.html'



class User_login(generic.View):
    def get(self, request):
        fm = AuthenticationForm()
        return render(request, 'login.html', {'form':fm})
    

    def post(self, request):
        fm = AuthenticationForm(request.user, data=request.POST)
        if fm.is_valid():
            uname = fm.cleaned_data['username']
            upass = fm.cleaned_data['password']
            user = authenticate(request, username=uname, password=upass)
            if user is not None:
                login(request, user)
                return redirect('add_post')
        
        else:
            fm = AuthenticationForm()
        return render(request, 'login.html', {'form':fm})


class User_logout(generic.View):
    def get(self, request):
        logout(request)
        return redirect('home')
    

class User_dashboard(generic.View):
    def get(self, request):
        form = UserEditForm(instance=request.user)
        return render(request, 'dashboard.html', {'form':form})
    

    def post(self, request):
        if request.method == 'POST':
            if request.user.is_superuser == True:
               form = UserAdminForm(request.POST, instance=request.user)
               users = User.objects.all()

            else:
                form = UserEditForm(request.POST, instance=request.user)
                users = None
                if form.is_valid():
                    form.save
        else:
            if request.user.is_superuser == True:
                form = UserAdminForm(instance=request.user)
                users = User.objects.all()
            else:
                form = UserEditForm(instance=request.user)
                users = None
        return render(request, 'dashboard.html', {'name':request.user, 'form':form, 'users':users})
    


class TaskList(LoginRequiredMixin, ListView):
    model = Post
    context_object_name = 'tasks'
    template_name = 'home.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(title__icontains=query)
        return queryset
