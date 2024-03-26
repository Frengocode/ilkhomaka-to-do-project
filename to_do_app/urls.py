from django.urls import path
from .views import UserRegisterView, LoginView, ToDoUploud, PublicTodoList, LogoutView, SearchView, ToDoDeatail, DeleteToDoListView, UserProfileView , UserPhotoUploudView, ProfileUpdateView, ChangePasswordView, SettingView, GetAllUploudUserToDo


urlpatterns = [
    path('',PublicTodoList.as_view(), name='home'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('to_do_uploud/', ToDoUploud.as_view(), name='todo_uploud'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('to_detail<int:pk>/', ToDoDeatail.as_view(), name='view_to_do'),
    path('delete/<int:pk>/', DeleteToDoListView.as_view(), name='to_do_delete'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('photo_uploud/', UserPhotoUploudView.as_view(), name='photo_uploud' ),
    path('profile_update_view/', ProfileUpdateView.as_view(), name='update_profile'),
    path('password_change/', ChangePasswordView.as_view(), name='change_password'),
    path('settings/', SettingView.as_view(), name='settings'),
    path('user_uploud_to_dos/', GetAllUploudUserToDo.as_view(), name='user_uploud_to_do'),



    

]