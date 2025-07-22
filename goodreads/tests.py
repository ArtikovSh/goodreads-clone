from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from books.models import BookReview, Book
from users.models import CustomUser


class HomePageTestCase(TestCase):
    def test_paginated_list(self):
        book = Book.objects.create(title="Book1", description="Description1", isbn="111111")
        user = CustomUser.objects.create(
            username="Shokhrukh", first_name="Shohrux", last_name="Ortiqov", email="message@email.ru"
        )
        user.set_password("somepassword")
        user.save()

        now = timezone.now()

        review1 = BookReview.objects.create(book=book, user=user, stars_given=3, comment="Very good book", created_at=now - timedelta(minutes=2))
        review2 = BookReview.objects.create(book=book, user=user, stars_given=4, comment="Useful book", created_at=now - timedelta(minutes=1))
        review3 = BookReview.objects.create(book=book, user=user, stars_given=5, comment="Nice book", created_at=now)

        response = self.client.get(reverse("home_page") + "?page_size=2")
        self.assertContains(response, review3.comment)
        self.assertContains(response, review2.comment)
        self.assertNotContains(response, review1.comment)

        response = self.client.get(reverse("home_page") + "?page=2&page_size=2")
        self.assertContains(response, review1.comment)
        self.assertNotContains(response, review2.comment)
        self.assertNotContains(response, review3.comment)
