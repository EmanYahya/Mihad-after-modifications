from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404
from django.db.models import Q

from products.models import Product, Category


# 📦 عرض كل المنتجات (للجميع)
@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()

    data = []
    for product in products:
        data.append({
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "stock": product.stock,
            "category": product.category.name if product.category else None,
        })

    return Response({
        "success": True,
        "data": data
    })


# 📦 تفاصيل منتج + منتجات مشابهة
@api_view(['GET'])
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)

    related_products = Product.objects.filter(
        category=product.category
    ).exclude(id=id)

    related_data = [
        {
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "stock": p.stock
        }
        for p in related_products
    ]

    return Response({
        "success": True,
        "data": {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "stock": product.stock,
            "category": product.category.name if product.category else None,
            "related_products": related_data
        }
    })


# 📦 منتجات حسب الكاتيجوري + search
@api_view(['GET'])
def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)

    products = Product.objects.filter(category=category)

    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    data = [
        {
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "stock": p.stock
        }
        for p in products
    ]

    return Response({
        "success": True,
        "data": {
            "category": category.name,
            "products": data
        }
    })


# ➕ إنشاء منتج (ADMIN فقط)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def product_create(request):
    product = Product.objects.create(
        name=request.data.get('name'),
        description=request.data.get('description'),
        price=request.data.get('price'),
        stock=request.data.get('stock'),
        category_id=request.data.get('category')
    )

    return Response({
        "success": True,
        "message": "Product created successfully",
        "id": product.id
    }, status=status.HTTP_201_CREATED)


# ✏️ تعديل منتج (ADMIN فقط)
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAdminUser])
def product_update(request, id):
    product = get_object_or_404(Product, id=id)

    product.name = request.data.get('name', product.name)
    product.description = request.data.get('description', product.description)
    product.price = request.data.get('price', product.price)
    product.stock = request.data.get('stock', product.stock)

    if request.data.get('category'):
        product.category_id = request.data.get('category')

    product.save()

    return Response({
        "success": True,
        "message": "Product updated successfully"
    })


# ❌ حذف منتج (ADMIN فقط)
@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def product_delete(request, id):
    product = get_object_or_404(Product, id=id)
    product.delete()

    return Response({
        "success": True,
        "message": "Product deleted successfully"
    }, status=status.HTTP_204_NO_CONTENT)