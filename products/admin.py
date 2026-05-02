from django.contrib import admin
from .models import Category, SubCategory, Product, Size, Color , ProductImage
from app.models.user import UserProfile, Notification
from app.models.cart import Order, OrderItem
from django.utils.html import format_html

#  Product Images Admin
# =========================

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image_preview', 'color')

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="60" height="60" style="object-fit:cover;border-radius:6px;" />',
                obj.image.url
            )
        return "-"

    image_preview.short_description = "الصورة"

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'colored_stock', 'stock_status')
    search_fields = ('name',)
    inlines = [ProductImageInline]

    def colored_stock(self, obj):
        if obj.stock == 0:
            color = 'red'
        elif obj.stock <= obj.low_stock_threshold:
            color = 'orange'
        else:
            color = 'green'

        return format_html(
            '<b style="color:{};">{}</b>',
            color,
            obj.stock
        )

    colored_stock.short_description = "المخزون"

    def stock_status(self, obj):
        if obj.stock == 0:
            return "❌ خلصان"
        elif obj.stock <= obj.low_stock_threshold:
            return "⚠️ قرب يخلص"
        return "✅ متوفر"

    stock_status.short_description = "الحالة"


# Register your models here.
admin.site.register(Category)
admin.site.register(SubCategory)
# admin.site.register(Product)
admin.site.register(Size)
admin.site.register(Color)
#admin.site.register(ProductImage)
admin.site.register(UserProfile)
admin.site.register(Notification)
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    can_delete = False
    readonly_fields = ('product', 'price', 'quantity')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # المعلومات اللي هتظهر في الجدول بره
    list_display = ['id', 'user', 'total_price', 'status', 'created_at']
    # الفلاتر اللي في الجنب
    list_filter = ['status', 'created_at']
    # ربط المنتجات بالطلب في نفس الصفحة
    inlines = [OrderItemInline]

#  Register Product Images
# =========================

admin.site.register(ProductImage, ProductImageAdmin)