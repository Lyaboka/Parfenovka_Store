import uuid
from datetime import timedelta

from django import forms
from django.contrib.auth.forms import (AuthenticationForm, UserChangeForm,
                                       UserCreationForm)
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.utils.timezone import now

from users.models import EmailVerification, User


# from users.tasks import send_email_verification


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите имя'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите фамилию'
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите имя пользователя'
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите email'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите пароль'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Подтвердите пароль'
    }))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=commit)
        # send_email_verification.delay(user.id) # Celery
        expiration = now() + timedelta(hours=48)
        record = EmailVerification.objects.create(code=uuid.uuid4(), user=user, expiration=expiration)
        record.send_verification_email()
        return user


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите имя пользователя'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите пароль'
    }))
    error_messages = {'not_verified': 'Ваш email не подтвержден! Повторите процесс авторизации после подтверждения.'}

    class Meta:
        model = User
        fields = ('username', 'password')

    def user_is_not_verified(self):
        return ValidationError(
            self.error_messages["not_verified"],
            code="not_verified",
            params={"username": self.username_field.verbose_name},
        )

    def clean(self):
        super().clean()
        user = get_object_or_404(User, username=self.cleaned_data['username'])
        if not user.is_verified_email:
            raise self.user_is_not_verified()
        else:
            self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data


class UserProfileForm(UserChangeForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'input-image-control'}), required=False)
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4', 'readonly': True}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control py-4', 'readonly': True}))

    class Meta:
        model = User
        fields = '__all__'
