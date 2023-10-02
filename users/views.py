import random

from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView

from users.forms import CreateUserForm, UserForm, LoginUserForm
from users.models import User


class LoginView(BaseLoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'


class LogoutView(BaseLogoutView):
    pass


class RegistererView(CreateView):
    model = User
    form_class = CreateUserForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/register.html'

    def form_valid(self, form):
        new_user = form.save()
        verify_key = ''.join([str(random.randint(0, 9)) for _ in range(15)])
        new_user.verify_key = verify_key
        new_user.is_active = False
        send_mail(
            subject='Подтверждение регистрации',
            message=f'Пройдите по ссылке для подтверждения регистрации на сайте SkyChimp:\n'
                    f'http://127.0.0.1:8000/users/verify/{verify_key}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email]
        )
        return super().form_valid(form)


def verify_view(request, verify_key):
    for user in User.objects.all():
        if verify_key == user.verify_key:
            user.is_active = True
            user.save()
            return redirect(reverse('users:login'))

    return HttpResponse('Пользователь с такой почтой не регистрировался!')


class UserUpdateView(UpdateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


def user_password_recovery(request):
    context = {
        'title': 'Восстановление пароля'
    }
    users_set = User.objects.all()
    new_password = ''.join([str(random.randint(0, 9)) for _ in range(15)])

    if request.method == 'POST':
        email = request.POST.get('email')
        for user_ in users_set:
            if user_.email == email:
                send_mail(
                    subject='SkyChimp: Новый пароль',
                    message=f'Ваш новый пароль:\n'
                            f'{new_password}',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user_.email]
                )
                user_.set_password(new_password)
                user_.save()

    return render(request, 'users/user_password_recovery.html', context)


class UserListView(UserPassesTestMixin, ListView):
    model = User
    extra_context = {
        'title': 'Пользователи'
    }

    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.is_staff


@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def switch_status(request, pk):
    user = User.objects.get(pk=pk)

    if user.is_active:
        user.is_active = False
    else:
        user.is_active = True

    user.save()
    return redirect(reverse('users:user_list'))
