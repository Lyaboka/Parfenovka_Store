from datetime import timedelta
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now

from users.models import EmailVerification, User


class UserRegisterViewTestCase(TestCase):

    def setUp(self) -> None:
        self.path = reverse('users:register')
        self.data = {
            'first_name': 'John', 'last_name': 'Sranium',
            'username': 'lyaboka', 'email': 'thelacoste2000@gmail.com',
            'password1': 'parfenov2000', 'password2': 'parfenov2000',
        }

    def test_user_register_get(self):
        response = self.client.get(self.path)
        self.assertEqual(
            first=response.context_data['title'],
            second='Parfenovka Store - Регистрация')
        self.assertTemplateUsed(response, 'users/register.html')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_user_registration_post_success(self):
        username = self.data['username']
        self.assertFalse(User.objects.filter(username=username).exists())
        response = self.client.post(self.path, self.data)

        self.assertRedirects(response, reverse('users:login'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        # check creating of user
        self.assertTrue(User.objects.filter(username=username).exists())

        # check creating of email verification
        email_verification = EmailVerification.objects.filter(user__username=username)
        self.assertTrue(email_verification.exists())
        self.assertEqual(
            first=email_verification.first().expiration.date(),
            second=(now() + timedelta(hours=48)).date()
        )

    def test_user_register_post_error(self):
        username = self.data['username']
        User.objects.create(username=username)
        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        # проверка в response.content
        self.assertContains(response, 'Пользователь с таким именем уже существует.', html=True)
