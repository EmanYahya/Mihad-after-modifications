# 1. استيراد الموديلات من ملف السلة والطلبات
from .cart import Cart, Order, OrderItem

# 2. استيراد الموديلات الأساسية (المنتجات والأقسام)
# ملاحظة: استبدلي 'product_models' بالاسم الحقيقي للملف الذي يحتوي على كلاس Product
from products.models import Product, Category, SubCategory, Size, Color