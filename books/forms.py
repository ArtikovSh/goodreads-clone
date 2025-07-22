from django import forms

from books.models import BookReview


class BookReviewForm(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = ('stars_given', 'comment')
        widgets = {
            'stars_given': forms.HiddenInput()
        }