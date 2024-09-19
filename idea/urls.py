from django.urls import path, include
from django.views.decorators.cache import cache_page

from . import views


urlpatterns = [
    path('', cache_page(60*15)(views.Index.as_view()), name='index'),
    path('search/', views.search_ideas, name='search_results'),
    path('idea_detail/<int:idea_id>/', views.IdeaDetail.as_view(), name='idea'),
    path('idea_detail/<int:idea_id>/comment/', views.AddComment .as_view(), name='add_comment'),
    path('category/<slug:category_slug>/', views.IdeaCategory.as_view(), name='category'),
    path('categories/', views.categories, name='categories'),
    path('add_idea/', views.AddIdea.as_view(), name='add_idea'),
    path('about/', views.about, name='about'),
]