from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from .models import Idea, Category, Comment
from .forms import AddIdeaForm, AddCommentForm
from .utils import DataMixin


class Index(DataMixin, ListView):
    model = Idea
    template_name = 'idea/index.html'
    context_object_name = 'ideas'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница')
        return dict(list(context.items()) + list(c_def.items()))


class IdeaDetail(DataMixin, DetailView):
    model = Idea
    template_name = 'idea/idea_detail.html'
    context_object_name = 'idea'
    pk_url_kwarg = 'idea_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AddCommentForm()  # Передаем форму в контекст
        c_def = self.get_user_context(title=Idea.objects.get(
            id=self.kwargs['idea_id']))
        context['comments'] = Comment.objects.filter(idea_id=self.object.pk)
        context['score'] = Comment.Score.choices
        return dict(list(context.items()) + list(c_def.items()))


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
        messages.success(self.request, 'Комментарий добавлен')
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

class IdeaCategory(DataMixin, ListView):
    model = Idea
    template_name = 'idea/category.html'
    slug_url_kwarg = 'category_slug'
    context_object_name = 'ideas'
    allow_empty = False
    
    def get_queryset(self):
        return Idea.objects.filter(category__slug=self.kwargs['category_slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        c_def = self.get_user_context(title=f"Категория - {category.name}")
        return dict(list(context.items()) + list(c_def.items()))

class AddIdea(DataMixin, LoginRequiredMixin, CreateView):
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
        messages.success(self.request, 'Идея добавлена')
        return super().form_valid(form)
    

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавить идею')

        return dict(list(context.items()) + list(c_def.items()))


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

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
