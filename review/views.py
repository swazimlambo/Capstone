from rest_framework import generics, status, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import NotFound
from product.serializers import ProductSerializer
from .models import Product, Review
from .serializers import ReviewSerializer, ProductReviewSerializer

#Pagination
class ProductPagination(PageNumberPagination):
    page_size = 10 # Number of products per page
    page_size_query_param = 'page_size'
    max_page_size = 50  # Maximum limit for page size

#creating a review
class SubmitReview(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

#list all the reviews per product id, user id and ratings
class ProductReviewList(generics.ListAPIView):
    serializer_class = ProductReviewSerializer

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        try:
            product = Product.objects.get(id=product_id)  # This will raise DoesNotExist if the product doesn't exist
            return Review.objects.filter(product=product)
        except Product.DoesNotExist:
            raise NotFound(detail="Product not found.", code=status.HTTP_404_NOT_FOUND)

#list all the reviews and reviewer for all the products with product details 
class ProductsReviewList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPagination

#list all users review
class UserReviewList(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)