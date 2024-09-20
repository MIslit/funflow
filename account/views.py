from django.contrib import messages
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView


from idea.models import Idea, User
from .forms import RegisterUserForm, LoginUserForm, UpdateUserForm

class RegisterUser(CreateView):
    model = User
    form_class = RegisterUserForm
    template_name = 'account/register.html'
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
    template_name = 'account/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация'
        return context

    def get_success_url(self):
        return reverse_lazy('index')

def logout_user(request):
    logout(request)
    return redirect('index')

    # DetailView
@login_required(login_url='/login/')
def profile(request, username):
    user = get_object_or_404(User, username=username)
    ideas = Idea.objects.filter(author__username=username)
    context = {
        'user': user, 
        'ideas': ideas,
        'title': f"Профиль - {user.username}",
    }
    if user.is_authenticated:
        if user.username != request.user.username:
            return render(request, 'account/profile.html', context=context)
        else:
            return redirect('my_profile', username=user.username)
    else:
        return redirect('login')
    
# DetailView
@login_required(login_url='/login/')
def my_profile(request, username):
    user = get_object_or_404(User, username=username)
    ideas = Idea.objects.filter(author__username=username)
    context = {
        'user': user, 
        'ideas': ideas,
        'title': 'Мой профиль',
    }
    if user.is_authenticated:
        return render(request, 'account/my_profile.html', context=context)
    else:
        return redirect('login')


@login_required(login_url='/login/')
def edit_profile(request, username):
    user = get_object_or_404(User, username=username)
    ideas = Idea.objects.filter(author__username=username)
    if user.is_authenticated:
        if request.method == 'POST':
            profile_form = UpdateUserForm(request.POST, request.FILES, instance=request.user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Профиль изменен')
                return redirect(to='my_profile', username=username)
        else:
            profile_form = UpdateUserForm(instance=request.user)
        
        context = {
        'user': user, 
        'profile_form': profile_form,
        'ideas': ideas,
        'title': 'Редактировать профиль',
    }
        return render(request, 'account/edit_profile.html', context=context)
    else:
        return redirect('login')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'account/change_password.html'
    success_message = "Пароль успешно изменен"
    success_url = reverse_lazy('index')