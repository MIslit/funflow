from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('change_password', views.ChangePasswordView.as_view(), name='change_password'),
    path('profile/<slug:username>/', views.profile, name='profile'),
    path('my_profile/<slug:username>/', views.my_profile, name='my_profile'),
    path('edit_profile/<slug:username>/', views.edit_profile, name='edit_profile'),
    path('logout/', views.logout_user, name='logout'),
]