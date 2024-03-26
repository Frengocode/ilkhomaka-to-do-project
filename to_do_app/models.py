from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from datetime import datetime

class TodoUserProfile(AbstractUser):
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = 'Todo_user', null=True)
    profile_photo = models.ImageField(upload_to='to_do_user_profile_image/')



class ToDoModel(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = 'Todo_uploud_user', null=True)
    user_profile = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, null=True, related_name = 'To_uploud_userprofile'  )
    created_at = models.DateField(auto_now_add = True)
    to_do = models.CharField(verbose_name = 'Заметка', max_length = 50)
    clue = models.CharField(verbose_name = 'Подсказка', max_length = 50)
    email = models.EmailField()
    reminder_time = models.DateTimeField(verbose_name='Время напоминания', default=datetime.now)

    def __str__(self):
        return self.to_do

    class Meta:
        ordering = ['-created_at']