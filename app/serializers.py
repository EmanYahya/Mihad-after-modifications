from rest_framework import serializers
# استيراد الأشياء الموجودة في ملف models الأساسي
from products.models import Product, Category, ProductImage, SubCategory, Size, Color

# استيراد الأشياء الموجودة في ملف cart.py
from .models.cart import Cart, Order 


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'color']


# =========================
# 📦 Product Serializer
# =========================
class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    subcategory_name = serializers.CharField(source='subcategory.name', read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'price',
            'main_image ',
            'slug',
            'stock',
            'low_stock_threshold',
            'is_featured',
            'is_newarrival',
            'category',
            'category_name',
            'subcategory',
            'subcategory_name',
            'available_sizes',
            'available_colors',
            'created_at'
        ]


# =========================
# 🛒 Cart Serializer
# =========================
class CartSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Cart
        fields = [
            'id',
            'user',
            'product',
            'product_name',
            'product_price',
            'quantity'
        ]


# =========================
# 📦 Order Serializer
# =========================
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'