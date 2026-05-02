from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

# استيراد الدوال مباشرة (يفضل تحديد الأسماء بوضوح)
from .views.api_views import get_products
from .views.home_view import home
from .views.category_view import category_list, category_create, category_edit, category_delete
# from .views.product_view import (product_list, product_detail, product_create, product_update, product_delete, category_products)
from .views.cart_view import admin_dashboard_analytics, update_cart_item, cart_detail, remove_from_cart, add_to_cart, checkout
from .views.wishlist_view import wishlist, add_to_wishlist, remove_from_wishlist
from .views.search_view import search
from .views.account_view import register_view, logout_view
from .views.user_view import login_view

app_name = 'app'

urlpatterns = [
           # categories - تم حذف كلمة views.
    #path('categories/', category_list),
    #path('categories/create/', category_create),
    #path('categories/<slug:slug>/edit/', category_edit),
   # path('categories/<slug:slug>/delete/', category_delete),


    #path('products/', product_list), 
    #path('products/<int:id>/', product_detail),
    #path('products/create/', product_create),
    #path('products/<int:id>/update/', product_update),
    #path('products/<int:id>/delete/', product_delete),
    #path('categories/<slug:slug>/products/', category_products),

    # Login & register
    path('auth/register/', register_view, name='register'),
    path('auth/login/', login_view, name='login'),
    path('auth/logout/', logout_view, name='logout'),

    # cart_view
    # الرابط الجديد للـ Dashboard
    path('api/admin/dashboard/', admin_dashboard_analytics, name='admin_dashboard_analytics'),
    path('api/cart/', cart_detail, name='cart_detail'),
    path('api/cart/add/', add_to_cart, name='add_to_cart'),
    path('api/cart/update/<int:cart_item_id>/', update_cart_item, name='update_cart_item'),
    path('api/cart/remove/<int:cart_item_id>/', remove_from_cart, name='remove_from_cart'),
    path('api/cart/checkout/', checkout, name='checkout'),

    # wishlist_view
    path('wishlist/', wishlist, name='wishlist'),
    path('add-to-wishlist/<int:product_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('remove-from-wishlist/<int:product_id>/', remove_from_wishlist, name='remove_from_wishlist'),

    # SEARCH
    path('search/', search, name='search'),

    # HOME
    path('', home, name='home'),
    path('home/', home, name='home_explicit'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)