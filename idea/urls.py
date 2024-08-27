from django.urls import path, include

from . import views


urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('search/', views.search_ideas, name='search_results'),
    path('idea_detail/<int:idea_id>/', views.IdeaDetail.as_view(), name='idea'),
    path('idea_detail/<int:idea_id>/comment/', views.AddComment .as_view(), name='add_comment'),
    path('profile/<slug:username>/', views.profile, name='profile'),
    path('my_profile/<slug:username>/', views.my_profile, name='my_profile'),
    path('category/<slug:category_slug>/', views.IdeaCategory.as_view(), name='category'),
    path('categories/', views.categories, name='categories'),
    path('add_idea/', views.AddIdea.as_view(), name='add_idea'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('about/', views.about, name='about'),
]