from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView

from common.views import CommonContextMixin
from users.forms import UserLoginForm, UserProfileForm, UserRegisterForm
from users.models import EmailVerification, User


class UserRegisterView(CommonContextMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    success_message = 'Вы успешно зарегистрировались! Подтвердите адрес электронной почты для входа.'
    title = 'Parfenovka Store - Регистрация'


class UserLoginView(CommonContextMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'Parfenovka Store - Вход'


class UserProfileView(CommonContextMixin, SuccessMessageMixin, UpdateView):
    model = User
    template_name = 'users/profile.html'
    form_class = UserProfileForm
    success_message = 'Parfenovka Store - Личный кабинет'
    title = 'Parfenovka Store - Вход'

    def post(self, request, *args, **kwargs):
        a = request.FILES.get('custom-file')
        b = 1
        return super().post(request)

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))


class EmailVerificationView(CommonContextMixin, TemplateView):
    title = 'Parfenovka Store - Подтверждение электронной почты'
    template_name = 'users/email_verification.html'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verification = EmailVerification.objects.filter(user=user, code=code)
        if not email_verification.first().is_expired() and email_verification.exists():
            user.is_verified_email = True
            user.save()
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('index'))
