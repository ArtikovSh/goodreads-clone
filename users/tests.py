from django.contrib.auth import get_user
from users.models import CustomUser
from django.test import TestCase
from django.urls import reverse


class RegistrationTestCase(TestCase):
    def test_user_account_is_created(self):
        self.client.post(
            reverse("users:register"),
            data={
                "username": "Shokhrukh",
                "first_name": "Shohrux",
                "last_name": "Artikov",
                "email": "shartikov@mail.com",
                "password": "somepassword"
            }
        )

        user = CustomUser.objects.get(username="Shokhrukh")

        self.assertEqual(user.first_name, "Shohrux")
        self.assertEqual(user.last_name, "Artikov")
        self.assertEqual(user.email, "shartikov@mail.com")
        self.assertNotEqual(user.password, "somepassword")
        self.assertTrue(user.check_password("somepassword"))

    def test_required_fields(self):
        response = self.client.post(
            reverse("users:register"),
            data={
                "first_name": "Shohrux",
                "email": "shartikov@mail.com"
            }
        )

        users_count = CustomUser.objects.count()

        self.assertEqual(users_count, 0)
        self.assertFormError(response, "form", "username", "This field is required.")
        self.assertFormError(response, "form", "password", "This field is required.")

    def test_invalid_email(self):
        response = self.client.post(
            reverse("users:register"),
            data={
                "username": "Shokhrukh",
                "first_name": "Shohrux",
                "last_name": "Artikov",
                "email": "invalid-email",
                "password": "somepassword"
            }
        )

        users_count = CustomUser.objects.count()

        self.assertEqual(users_count, 0)
        self.assertFormError(response, "form", "email", "Enter a valid email address.")

    def test_unique_username(self):
        self.client.post(
            reverse("users:register"),
            data={
                "username": "Shokhrukh",
                "first_name": "Shohrux",
                "last_name": "Artikov",
                "email": "shartikov@mail.com",
                "password": "somepassword"
            }
        )

        response = self.client.post(
            reverse("users:register"),
            data={
                "username": "Shokhrukh",
                "first_name": "Shohrux",
                "last_name": "Artikov",
                "email": "shartikov@mail.com",
                "password": "somepassword"
            }
        )

        users_count = CustomUser.objects.count()

        self.assertEqual(users_count, 1)
        self.assertFormError(response, "form", "username", "A user with that username already exists.")


class LoginTestCase(TestCase):
    def setUp(self):
        # DRY - Dont repeat yourself
        self.user_db = CustomUser.objects.create(username="Shokhrukh", first_name="Shohrux")
        self.user_db.set_password("somepassword")
        self.user_db.save()

    def test_successful_login(self):
        self.client.post(
            reverse("users:login"),
            data={
                "username": "Shokhrukh",
                "password": "somepassword"
            }
        )

        user = get_user(self.client)

        self.assertTrue(user.is_authenticated)

    def test_wrong_credentials(self):
        self.client.post(
            reverse("users:login"),
            data={
                "username": "wrong-username",
                "password": "somepassword"
            }
        )

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

        self.client.post(
            reverse("users:login"),
            data={
                "username": "Shokhrukh",
                "password": "wrong-password"
            }
        )
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

    def test_logout(self):
        self.client.login(username="Shokhrukh", password="somepassword")

        self.client.get(reverse("users:logout"))
        user = get_user(self.client)

        self.assertFalse(user.is_authenticated)


class ProfileTestCase(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse("users:profile"))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("users:login") + "?next=/users/profile/")

    def test_profile_details(self):
        user = CustomUser.objects.create(username="Shokhrukh", first_name="Shohrux", last_name="Ortiqov", email="@email.ru")
        user.set_password("somepassword")
        user.save()

        self.client.login(username="Shokhrukh", password="somepassword")

        response = self.client.get(reverse("users:profile"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, user.username)
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.last_name)
        self.assertContains(response, user.email)

    def test_update_profile(self):
        user = CustomUser.objects.create(username="Shokhrukh", first_name="Shohrux", last_name="Ortiqov", email="message@email.ru")
        user.set_password("somepassword")
        user.save()

        self.client.login(username="Shokhrukh", password="somepassword")

        response = self.client.post(
            reverse("users:profile-edit"),
            data={
                "username": "Shokhrukh",
                "first_name": "Shohrux",
                "last_name": "Doe",
                "email": "message@gmail.com"
            }
        )

        user.refresh_from_db()

        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.email, "message@gmail.com")
        self.assertEqual(response.url, reverse("users:profile"))