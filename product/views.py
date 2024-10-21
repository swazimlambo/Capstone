from django.shortcuts import render
from rest_framework import generics, permissions, filters, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django_filters import rest_framework as filter
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer

class ProductPagination(PageNumberPagination):
    page_size = 10
    page_size_query_params = 'page_size'
    max_page_size = 50

class ProductFilter(filter.FilterSet):
    min_price = filter.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filter.NumberFilter(field_name='price', lookup_expr='lte')
    category = filter.ModelChoiceFilter(queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = ['category', 'min_price', 'max_price']

class ProductRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        message = "Product deleted successfully."
        response_data = {
        'message': message,
        'data': instance.data
        }
        return Response(response_data, status=status.HTTP_204_NO_CONTENT)

# A view to list all the products 
class ProductList(generics.ListAPIView):
    queryset = Product.objects.all().order_by('name')
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filter.DjangoFilterBackend]
    filterset_class = ProductFilter
    pagination_class = ProductPagination
    search_fields = ['name', 'category__name']

# A view to create the product
class ProductCreate(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    # A method to handle creation and errors for bad request for product
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            message = "Product successfully created."
            response_data = {
            'message': message,
            'data': serializer.data,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#Category
#category view to list and create categories
class CategoryListCreate(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    # A creation override for categories
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user)  # Set the created_by field to the current user
        message = "Category successfully created."
        response_data = {
            'message': message,
            'data': serializer.data,
        }
        return Response(response_data, status=status.HTTP_201_CREATED)  # Return the created category data and status

# A View to retrieve, delete and update your categories 
class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    # A deletion method for categories
    def destroy(self, request, *args, **kwargs):
        category = self.get_object()
        # only the owner of the category can delete the category
        if category.created_by != request.user:
            return Response({"error": "You do not have permission to delete this category."},
                            status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(category)
        message = "Category successfully deleted."
        response_data = {
            'message': message,
            'data': category.data,
        }
        return Response(response_data, status=status.HTTP_204_NO_CONTENT)