from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from .models import TodoUserProfile, ToDoModel
from .forms import  UserRegisterForm, Search, TodoUploudForm, UserProfileUpdateForm, DeleteToDoList, UserProfilePhotoUploudForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.http import JsonResponse
from datetime import datetime



class DeleteToDoListView(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, pk:int):

        todo_item = get_object_or_404(ToDoModel, pk=pk, user=request.user)
        
        if todo_item.user == request.user:
            todo_item.delete()
            return redirect('home')
        return JsonResponse({'messgae': 'Вы не подходите к этому пользователю'})
        
        
    def post(self, request, pk:int):
        todo_item = get_object_or_404(ToDoModel, pk=pk, user=request.user)
        
        if todo_item.user == request.user:
            todo_item.delete()
            return redirect('home')
        return JsonResponse({'messgae': 'Вы не подходите к этому пользователю'})

    

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = TodoUserProfile
    form_class = UserProfileUpdateForm
    template_name = 'auhofication/profile_update.html'
    success_url = reverse_lazy('user_profile')

    @method_decorator(login_required)
    def dispath(self, request,  *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.request.user


class PublicTodoList(View):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):

        now = datetime.now()

        todos_to_remind = ToDoModel.objects.filter(
            user=request.user, 
            reminder_time__hour=now.hour,  
            reminder_time__minute=now.minute 
        )

        
        return render(request, 'pages/to_do_list.html', {'to_do': todos_to_remind})
    

class ToDoUploud (View):
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        form = TodoUploudForm()
        return render(request, 'pages/to_do_uploud.html', {'form':form})
    
    def post(self, request,*args, **kwargs):
        form = TodoUploudForm(request.POST)
        if form.is_valid():
            new_ = form.save(commit=False)
            new_.user = request.user
            new_.user_profile = request.user
            messages.success(request, 'ToDo Is added Succses')
            new_.save()
            return redirect('home')
        return redirect('home')


class UserRegisterView(View):

    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'auhofication/register.html', {'form':form})

    def post(self, request):
        form = UserRegisterForm()
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('home')
        return render(request, 'auhofication/register.html', {'form':form})
    


class LoginView(View):
    
    def get(self, request):
        return render(request, 'auhofication/login.html')
    
    def post(self, request):
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'LOGIN IS SUCCESS!!!')
                return redirect('home')
        return render(request, 'auhofication/login.html')


class LogoutView(View):
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        logout(request)
        return redirect('login')


class SearchView(View):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        user = request.user
        form = Search(request.GET or None)
        to_lists = None
        if request.method == 'GET':
            if form.is_valid():
                search_to_do = form.cleaned_data['search']
                to_lists = ToDoModel.objects.filter(to_do__icontains = search_to_do)
        return render(request, 'pages/search.html', {'form':form, 'to_dos':to_lists})
    


class ToDoDeatail(View):

    @method_decorator(login_required)
    def dispatch(self, request, *args, pk:int, **kwargs):
        return super().dispatch(request, pk, *args, *kwargs)
    
    def get(self, request, pk:int):
        get_to_do = ToDoModel.objects.get(pk=pk)
        return render(request, 'detail_pages/to_do_detail.html', {'to_do':get_to_do})
    



class ChangePasswordView(View):
    form_class = PasswordChangeForm
    template_name = 'auhofication/change_password.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    

    def get(self, request):
        form = self.form_class(request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password Changed Successfully')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
        return render(request, self.template_name, {'form': form})
    


class UserProfileView(View):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        user = request.user
        user_obj = TodoUserProfile.objects.filter(user=user)

        return render(request, 'pages/user_profile.html', {'user_obj':user_obj})
    


class UserPhotoUploudView(View):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwrags):
        return super().dispatch(request, *args, **kwrags)
    
    def get(self, reqeust, *args, **kwrags):
        form = UserProfilePhotoUploudForm()
        return render(reqeust, 'uploud/profile_photo.html', {'form':form})
    
    def post(self, request, *args, **kwrags):
        
        user_profile, created = TodoUserProfile.objects.get_or_create(username = request.user)

        if not created and user_profile.profile_photo:
            messages.success(request, '')
        
        if request.method == 'POST':
            form = UserProfilePhotoUploudForm(request.POST, request.FILES, instance=user_profile)

            if form.is_valid():

                new_ = form.save(commit=False)
                new_.user = request.user
                new_.save()
                
                return redirect('home')
            
        return render(request, 'uploud/profile_photo.html', {'form':form})
    



class SettingView(View):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwrags):
        return super().dispatch(request, *args, **kwrags)
    
    def get(self, request, *args, **kwargs):
        return render(request, 'pages/setting.html',)
    


class GetAllUploudUserToDo(View):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwrags):
        return super().dispatch(request, *args, **kwrags)
    
    def get(self, request, *args, **kwrags):
        user = request.user
        user_uploud_to_do = ToDoModel.objects.filter(user=user)

        return render(request, 'uploud/all_to_do.html', {'to_do':user_uploud_to_do})