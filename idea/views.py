from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login

from .models import Idea, Category, User, Comment
from .forms import AddIdeaForm, RegisterUserForm, LoginUserForm, AddCommentForm
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from django.db.models import Q


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
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        context['categories'] = Category.objects.all()
        return context


class IdeaDetail(DetailView):
    model = Idea
    template_name = 'idea/idea_detail.html'
    context_object_name = 'idea'
    pk_url_kwarg = 'idea_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AddCommentForm()  # Передаем форму в контекст
        context['title'] = Idea.objects.get(id=self.kwargs['idea_id'])
        context['categories'] = Category.objects.all()
        context['comments'] = Comment.objects.filter(idea_id=self.object.pk)
        context['score'] = Comment.Score.choices
        return context


class AddComment(LoginRequiredMixin, CreateView):
    form_class = AddCommentForm
    model = Comment
    template_name = 'idea/idea_detail.html'
    login_url = reverse_lazy('login')  # Переход на страницу логина, если не авторизован
    pk_url_kwarg = 'idea_id'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.idea = get_object_or_404(Idea, pk=self.kwargs['idea_id'])
        form.save()
        return redirect('idea', idea_id=form.instance.idea.pk)

    def form_invalid(self, form):
        idea = get_object_or_404(Idea, pk=self.kwargs['idea_id'])
        context = self.get_context_data(object=idea)
        context['form'] = form
        return self.render_to_response(context)


def categories(request):
    categories = Category.objects.all()

    context = {
        'categories': categories,
        'title': 'Список категорий',
    }

    return render(request, 'idea/categories.html', context=context)

class IdeaCategory(ListView):
    model = Idea
    template_name = 'idea/category.html'
    slug_url_kwarg = 'category_slug'
    context_object_name = 'ideas'
    paginate_by = 3
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        category = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        context['title'] = category.name
        context['categories'] = categories
        return context

class AddIdea(LoginRequiredMixin, CreateView):
    form_class = AddIdeaForm
    template_name = 'idea/add_idea.html'
    success_url = reverse_lazy('index')
    login_url = reverse_lazy('index')
    raise_exception = True

    def form_valid(self, form):
        instance = form.instance
        instance.author_id = self.request.user.id
        instance.title = self.request.POST['title']
        instance.description = self.request.POST['description']
        instance.category = Category.objects.get(id=int(self.request.POST['category']))
        form.save()
        return super().form_valid(form)
    

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        context['title'] = 'Добавить идею'
        context['categories'] = categories

        return context

# DetailView
@login_required(login_url='/login/')
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
@login_required(login_url='/login/')
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


def search_ideas(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        ideas = Idea.objects.filter(
            Q(title__contains=searched) | Q(description__contains=searched))
        context = {
            'title': f"Поиск - {searched}",
            'ideas': ideas,
            'categories': Category.objects.all(),
        }
        return render(request, 'idea/search_results.html', context)
    else:
        return render(request, 'idea/search_results.html', {})
    
def about(request):
    categories = Category.objects.all()
    context = {
        'title': 'О нас',
        'categories': categories,
    }

    return render(request, 'idea/about.html', context)