from django.urls import path, include
from .views import ProductReviewList, SubmitReview, UserReviewList, ProductsReviewList

#Review urls
urlpatterns = [
    path('product/<int:product_id>/reviews/', ProductReviewList.as_view(), name='product-review'),
    path('reviews/', SubmitReview.as_view(), name='create-review'),
    path('users/reviews/', UserReviewList.as_view(), name='users-review'),
    path('products/reviews/', ProductsReviewList.as_view(), name='products_reviews'),
]