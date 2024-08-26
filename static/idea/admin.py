from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *

# from .forms import RegisterUserForm, UserChangeForm
from .models import User

# class UserAdmin(UserAdmin):
#     model = User
#     list_display = ('email', 'username', 'avatar')

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Idea)
admin.site.register(Comment)
