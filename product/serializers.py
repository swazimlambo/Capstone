from rest_framework import serializers
from .models import Product, Category, ProductImage

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'created_by']
        read_only_fields = ['created_by']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']

# class ProductReviewSerializer(serializers.ModelSerializer):
#     user = UserReviewSerializer(read_only=True)

#     class Meta:
#         model = Review
#         fields = ['id', 'user', 'rating', 'review', 'created_at']

class ProductSerializer(serializers.ModelSerializer):
    #reviews = ProductReviewSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'stock_quantity', 'images', 'created_date', 'reviews']
        extra_kwargs = {
            'name': {'required': True},
            'price': {'required': True},
            'stock_quantity': {'required': True},
        }

    # A validation to ensure that you input a positive number of stock in product creation
    def validate_stock_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError('Stock quantity cannot be negative')
        return value
    
    # Creation of a product including multiple image upload
    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        product = Product.objects.create(**validated_data)
        for image_data in images_data:
            ProductImage.objects.create(product=product, **image_data)
        return product