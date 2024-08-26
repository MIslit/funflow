from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login

from .models import Idea, Category, User, Comment
from .forms import AddIdeaForm, RegisterUserForm, LoginUserForm, AddCommentForm
from django.http.response import HttpResponse


class RegisterUser(CreateView):
    model = User
    form_class = RegisterUserForm
    template_name = 'idea/register.html'
    success_url = reverse_lazy('index')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        return context

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password1'])
        user.save()
        login(self.request, user)

        return super().form_valid(form)


class LoginUser(LoginView): 
    form_class = LoginUserForm
    template_name = 'idea/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация'
        return context

    def get_success_url(self):
        return reverse_lazy('index')


def logout_user(request):
    logout(request)
    return redirect('index')

class Index(ListView):
    model = Idea
    template_name = 'idea/index.html'
    context_object_name = 'ideas'
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        context['title'] = 'Главная страница'
        context['categories'] = categories
        return context

# ListView
# def index(request):
#     categories = Category.objects.all()
#     ideas = Idea.objects.all()

#     context = {
#         'ideas': ideas,
#         'categories': categories,
#         'title': 'Главная страница',
#     }
#     return render(request, 'idea/index.html', context=context)

# class IdeaDetail(DetailView, CreateView):
#     model = Idea
#     form_class = AddCommentForm
#     template_name = 'idea/idea_detail.html'
#     context_object_name = 'idea'
#     success_url = reverse_lazy('idea')
#     raise_exception = True

#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         categories = Category.objects.all()
#         comments = Comment.objects.filter(idea_id=idea_id)

# DetailView
def idea_detail(request, idea_id):
    categories = Category.objects.all()
    comments = Comment.objects.filter(idea_id=idea_id)
    idea = get_object_or_404(Idea, id=idea_id)
    if request.method == 'POST':
        form = AddCommentForm(request.POST)
        obj = form.save(commit=False)
        obj.author_id = request.user.id
        obj.idea_id = idea.id
        obj.text = request.POST['text']
        obj.score = Comment.objects.get(score=request.POST['score'])
        if form.is_valid():            
            obj.save()
            return redirect('idea', idea.id)
    else:
        form = AddCommentForm()

    context = {
        'form': form,
        'idea': idea,
        'categories': categories,
        'comments': comments,
        'title': idea.title,
    }

    return render(request, 'idea/idea_detail.html', context=context)
# ListView
def idea_category(request, category_id):
    categories = Category.objects.all()
    category = get_object_or_404(Category, id=category_id)
    ideas = Idea.objects.filter(category_id=category_id)

    context = {
        'ideas': ideas,
        'categories': categories,
        'title': category.name,
    }
    return render(request, 'idea/category.html', context=context)
# CreateView
def add_idea(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        form = AddIdeaForm(request.POST)
        obj = form.save(commit=False)
        obj.author_id = request.user.id
        obj.title = request.POST['title']
        obj.description = request.POST['description']
        obj.category = Category.objects.get(id=int(request.POST['category']))
        if form.is_valid():
            obj.save()
            return redirect('index')
    else:
        form = AddIdeaForm()

    context = {
        'form': form,
        'categories': categories,
        'title': 'Добавление идеи',
    }
    return render(request, 'idea/add_idea.html', context=context)
# DetailView
def profile(request, username):
    user = get_object_or_404(User, username=username)
    context = {
        'user': user, 
        'title': f"Профиль - {user.username}",
    }
    if user.is_authenticated:
        if user.username != request.user.username:
            return render(request, 'idea/profile.html', context=context)
        else:
            return redirect('my_profile', username=user.username)
    else:
        return redirect('login')
# DetailView
def my_profile(request, username):
    user = get_object_or_404(User, username=username)
    context = {
        'user': user, 
        'title': 'Мой профиль',
    }
    if user.is_authenticated:
        return render(request, 'idea/my_profile.html', context=context)
    else:
        return redirect('login')

def categories(request):
    categories = Category.objects.all()

    context = {
        'categories': categories,
        'title': 'Список категорий',
    }

    return render(request, 'idea/categories.html', context=context)