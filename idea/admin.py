from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *

# from .forms import RegisterUserForm, UserChangeForm
from .models import *

# class UserAdmin(UserAdmin):
#     model = User
#     list_display = ('email', 'username', 'avatar')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(User)
admin.site.register(Idea)
admin.site.register(Comment)
