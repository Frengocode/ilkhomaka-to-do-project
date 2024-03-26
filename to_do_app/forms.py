from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import  forms
from django.forms import ModelForm, DateTimeInput
from .models import TodoUserProfile, ToDoModel

class DeleteToDoList(forms.Form):
    delete = forms.ModelMultipleChoiceField(
        queryset=None,
        widget = forms.CheckboxSelectMultiple,
        label = 'Delete'
    )

    def __init__(self, user, *args, **kwargs):
        super(DeleteToDoList, self).__init__(*args, **kwargs)
        self.fields['delete'].queryset = ToDoModel.objects.filter(user=user)


class UserProfileUpdateForm(UserChangeForm):
    class Meta:
        model = TodoUserProfile
        fields = ['username']

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = TodoUserProfile
        fields = ['username', 'password1', 'password2']


class Search(forms.Form):
    search = forms.CharField(max_length=50, label='Search...')

class TodoUploudForm(ModelForm):
    class Meta:
        model = ToDoModel
        fields = ['to_do', 'clue', 'reminder_time']
        widgets = {
            'reminder_time': DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }



class UserProfilePhotoUploudForm(ModelForm):
    class Meta:
        model = TodoUserProfile
        fields = ['profile_photo']
