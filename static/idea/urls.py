from django.urls import path, include

from . import views


urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('idea_detail/<int:idea_id>/', views.idea_detail, name='idea'),
    path('profile/<slug:username>/', views.profile, name='profile'),
    path('my_profile/<slug:username>/', views.my_profile, name='my_profile'),
    path('category/<int:category_id>/', views.idea_category, name='category'),
    path('categories/', views.categories, name='categories'),
    path('add_idea/', views.add_idea, name='add_idea'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('logout/', views.logout_user, name='logout'),
]