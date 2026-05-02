from email.mime import image

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from app import models
from .models import Category, Product, ProductImage
from app.serializers import ProductSerializer 
from django.shortcuts import get_object_or_404

from products import models

# =========================
#  إضافة صورة للمنتج
@api_view(['POST'])
def upload_multiple_images(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    images = request.FILES.getlist('images')  # 👈 أهم سطر
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

# =========================
#  عرض صور المنتج
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

#--------------------------
#حذف صورة من صور المنتج

@api_view(['DELETE'])
def delete_image(request, image_id):
    image = get_object_or_404(ProductImage, id=image_id)
    image.delete()
    return Response({"message": "Deleted"})

@api_view(['GET'])
def low_stock_products(request):
    products = Product.objects.filter(stock__lte=models.F('low_stock_threshold'))

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


# 📦 تفاصيل منتج
@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


# ➕ إضافة منتج
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def product_upload(request):
    serializer = ProductSerializer(data=request.data)

    if serializer.is_valid():
        product = serializer.save(seller=request.user)
        return Response({"message": "Product uploaded", "id": product.id})

    return Response(serializer.errors)


# ✏️ تعديل منتج
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_product(request, id):
    product = get_object_or_404(Product, id=id)

    # optional: ownership check
    if product.seller != request.user:
        return Response({"error": "Not allowed"}, status=403)

    serializer = ProductSerializer(product, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Updated"})

    return Response(serializer.errors)

# ❌ حذف منتج
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_product(request, id):
    product = get_object_or_404(Product, id=id)

    if product.seller != request.user:
        return Response({"error": "Not allowed"}, status=403)

    product.delete()
    return Response({"message": "Deleted"})

# جلب قائمة الفئات (Categories)
@api_view(['GET'])
def category_list(request):
    categories = Category.objects.all()
    # ملحوظة: ستحتاجين لعمل Serializer للفئات إذا لم يكن موجوداً
    # حالياً سنقوم بإرجاع أسماء الفئات فقط كمثال بسيط
    data = [{"id": cat.id, "name": cat.name} for cat in categories]
    return Response(data)

# جلب المنتجات التابعة لفئة معينة (Category)
@api_view(['GET'])
def category_products(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

# جلب المنتجات التابعة لقسم فرعي (Subcategory)
@api_view(['GET'])
def subcategory_products(request, category_slug, subcategory_slug):
    # بنجيب المنتجات اللي تابعة للـ category والـ subcategory مع بعض من خلال الـ slug
    products = Product.objects.filter(
        category__slug=category_slug,
        subcategory__slug=subcategory_slug
    )
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)