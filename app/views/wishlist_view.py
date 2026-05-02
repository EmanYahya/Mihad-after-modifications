from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404

from products.models import Product
from ..models.wishlist import Wishlist


# ❤️ إضافة منتج للـ Wishlist
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    wishlist, created = Wishlist.objects.get_or_create(user=request.user)

    if wishlist.products.filter(id=product.id).exists():
        return Response({
            "success": True,
            "message": "Product already in wishlist"
        })

    wishlist.products.add(product)

    return Response({
        "success": True,
        "message": f"{product.name} added to wishlist",
        "wishlist_id": wishlist.id
    }, status=status.HTTP_201_CREATED)


# 📦 عرض الـ Wishlist
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def wishlist(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)

    products = wishlist.products.all()

    data = [
        {
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "stock": p.stock,
            "category": p.category.name if p.category else None
        }
        for p in products
    ]

    return Response({
        "success": True,
        "wishlist_id": wishlist.id,
        "products": data
    })


# ❌ حذف منتج من الـ Wishlist
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    wishlist, created = Wishlist.objects.get_or_create(user=request.user)

    if not wishlist.products.filter(id=product.id).exists():
        return Response({
            "success": False,
            "message": "Product not in wishlist"
        }, status=status.HTTP_400_BAD_REQUEST)

    wishlist.products.remove(product)

    return Response({
        "success": True,
        "message": f"{product.name} removed from wishlist"
    })