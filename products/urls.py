from django.urls import path
from app.views.product_view import *
from app.views.category_view import *
from . import views
app_name = 'products'

urlpatterns = [
    #category
    path('category-list/', views.category_list, name='category_list'),
    path('category/<slug:category_slug>/', views.category_products, name='category_products'),
    
    #SubCategory
    path(
        'category/<slug:category_slug>/subcategory/<slug:subcategory_slug>/',
        views.subcategory_products,
        name='subcategory_products'
    ),

    #Add Product Image
     path('<int:product_id>/upload-images/', views.upload_multiple_images),
    # عرض صور المنتج
    path('<int:product_id>/images/', views.product_images, name='product_images'),
     # Products
    path('product-list/', views.product_list, name='product_list'),
    path('product/<slug:category_slug>/<slug:subcategory_slug>/<slug:product_slug>/',views.product_detail,name='product_detail'),
    #Add Product (Admin/Seller)
    path('add/', views.product_upload, name='product_upload'),


]

