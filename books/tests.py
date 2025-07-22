from django.test import TestCase
from django.urls import reverse

from books.models import Book
from users.models import CustomUser


class BooksTestCase(TestCase):
    def test_no_books(self):
        response = self.client.get(reverse("books:list"))

        self.assertContains(response, "No books found.")

    def test_books_list(self):
        book1 = Book.objects.create(title="Book1", description="Description1", isbn="111111")
        book2 = Book.objects.create(title="Book2", description="Description2", isbn="222222")
        book3 = Book.objects.create(title="Book3", description="Description3", isbn="333333")

        response = self.client.get(reverse("books:list") + "?page_size=2")

        for book in [book1, book2]:
            self.assertContains(response, book.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse("books:list") + "?page=2&page_size=2")

        self.assertContains(response, book3.title)

    def test_detail_page(self):
        book = Book.objects.create(title="Book1", description="Description1", isbn="111111")

        response = self.client.get(reverse("books:detail", kwargs={"id": book.id}))

        self.assertContains(response, book.title)
        self.assertContains(response, book.description)

    def test_search_books(self):
        book1 = Book.objects.create(title="Sport", description="Description1", isbn="111111")
        book2 = Book.objects.create(title="Guide", description="Description2", isbn="222222")
        book3 = Book.objects.create(title="Shoe Dog", description="Description3", isbn="333333")

        response = self.client.get(reverse("books:list") + "?q=sport")
        self.assertContains(response, book1.title)
        self.assertNotContains(response, book2.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse("books:list") + "?q=guide")
        self.assertContains(response, book2.title)
        self.assertNotContains(response, book1.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse("books:list") + "?q=shoe")
        self.assertContains(response, book3.title)
        self.assertNotContains(response, book2.title)
        self.assertNotContains(response, book1.title)


class BookReviewTestCase(TestCase):
    def setUp(self):
        self.book_db = Book.objects.create(title="Sport", description="Description1", isbn="111111")
        self.user_db = CustomUser.objects.create(
            username="Shokhrukh", first_name="Shohrux", last_name="Ortiqov", email="message@email.ru"
        )
        self.user_db.set_password("somepassword")
        self.user_db.save()

        self.client.login(username="Shokhrukh", password="somepassword")

        self.client.post(reverse("books:reviews", kwargs={"id": self.book_db.id}), data={
            "stars_given": 3,
            "comment": "Nice book"
        })

        self.book_reviews = self.book_db.bookreview_set.all()

    def test_add_review(self):
        self.assertEqual(self.book_reviews.count(), 1)
        self.assertEqual(self.book_reviews[0].stars_given, 3)
        self.assertEqual(self.book_reviews[0].comment, "Nice book")
        self.assertEqual(self.book_reviews[0].book, self.book_db)
        self.assertEqual(self.book_reviews[0].user, self.user_db)

    def test_edit_review(self):
        self.client.post(reverse("books:edit-review", kwargs={"book_id": self.book_db.id, "review_id": self.book_reviews[0].id}),
                                    data={"stars_given": 1, "comment": "Bad Book"}
                                    )

        self.assertEqual(self.book_reviews.count(), 1)
        self.assertEqual(self.book_reviews[0].stars_given, 1)
        self.assertEqual(self.book_reviews[0].comment, "Bad Book")
        self.assertEqual(self.book_reviews[0].book, self.book_db)
        self.assertEqual(self.book_reviews[0].user, self.user_db)

    def test_confirm_delete_review(self):
        book_review = self.book_reviews[0]

        response = self.client.get(reverse("books:confirm-delete-review", kwargs={"book_id": self.book_db.id, "review_id": book_review.id}))

        self.assertContains(response, self.book_db.title)
        self.assertContains(response, book_review.comment)

    def test_delete_review(self):
        book_review = self.book_reviews[0]

        response = self.client.get(reverse("books:delete-review", kwargs={"book_id": self.book_db.id, "review_id": book_review.id}))

        book_reviews = self.book_db.bookreview_set.all()

        self.assertEqual(response.url, reverse("books:detail", kwargs={"id": self.book_db.id}))
        self.assertEqual(book_reviews.count(), 0)