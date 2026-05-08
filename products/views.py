from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.db.models import F
from django.shortcuts import get_object_or_404

from .models import Category, Product, ProductImage
from app.serializers import ProductSerializer


def can_manage_product_images(user, product):
    return user.is_staff or user.is_superuser or product.seller_id == user.id


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_multiple_images(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if not can_manage_product_images(request.user, product):
        return Response({"error": "Not allowed"}, status=403)

    images = request.FILES.getlist('images')
    color_id = request.data.get('color')

    if not images:
        return Response({"error": "No images provided"}, status=400)

    created_images = []

    for img in images:
        image_obj = ProductImage.objects.create(
            product=product,
            image=img,
            color_id=color_id if color_id else None
        )
        created_images.append({
            "id": image_obj.id,
            "image": image_obj.image.url
        })

    return Response({
        "message": "Images uploaded successfully",
        "images": created_images
    })


@api_view(['GET'])
def product_images(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    images = product.images.all()

    data = []
    for img in images:
        data.append({
            "id": img.id,
            "image": img.image.url,
            "color": img.color.name if img.color else None
        })

    return Response(data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_image(request, image_id):
    image = get_object_or_404(ProductImage.objects.select_related('product'), id=image_id)
    if not can_manage_product_images(request.user, image.product):
        return Response({"error": "Not allowed"}, status=403)
    image.delete()
    return Response({"message": "Deleted"})


@api_view(['GET'])
def low_stock_products(request):
    products = Product.objects.filter(stock__lte=F('low_stock_threshold'))

    data = [
        {
            "name": p.name,
            "stock": p.stock
        }
        for p in products
    ]

    return Response({
        "low_stock_products": data
    })


@api_view(['GET'])
def product_detail(request, category_slug, subcategory_slug, product_slug):
    product = get_object_or_404(
        Product,
        slug=product_slug,
        category__slug=category_slug,
        subcategory__slug=subcategory_slug
    )

    serializer = ProductSerializer(product)
    return Response(serializer.data)


@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def product_upload(request):
    serializer = ProductSerializer(data=request.data)

    if serializer.is_valid():
        product = serializer.save(seller=request.user)
        return Response({"message": "Product uploaded", "id": product.id})

    return Response(serializer.errors)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_product(request, id):
    product = get_object_or_404(Product, id=id)

    if product.seller != request.user:
        return Response({"error": "Not allowed"}, status=403)

    serializer = ProductSerializer(product, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Updated"})

    return Response(serializer.errors)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_product(request, id):
    product = get_object_or_404(Product, id=id)

    if product.seller != request.user:
        return Response({"error": "Not allowed"}, status=403)

    product.delete()
    return Response({"message": "Deleted"})


@api_view(['GET'])
def category_list(request):
    categories = Category.objects.all()
    data = [{"id": cat.id, "name": cat.name} for cat in categories]
    return Response(data)


@api_view(['GET'])
def category_products(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def subcategory_products(request, category_slug, subcategory_slug):
    products = Product.objects.filter(
        category__slug=category_slug,
        subcategory__slug=subcategory_slug
    )
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)
