from django.urls import path

# from api.views import BookReviewDetailAPIView, BookReviewsAPIView
from rest_framework.routers import DefaultRouter
from api.views import BookReviewsViewSet

app_name = "api"

router =DefaultRouter()
router.register(r'reviews', BookReviewsViewSet, basename='review')


urlpatterns = [
    # path("reviews/", BookReviewsAPIView.as_view(), name="review-list"),
    # path("reviews/<int:id>/", BookReviewDetailAPIView.as_view(), name="review-detail"),
]

urlpatterns += router.urls