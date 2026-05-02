from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from products.models import Category
from ..serializers import CategorySerializer


# 📌 عرض كل الكاتيجوري
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def category_list(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


# 📌 إنشاء كاتيجوري جديدة (Admin only)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def category_create(request):
    serializer = CategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message": "Category created successfully", "data": serializer.data},
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 📌 تعديل كاتيجوري
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAdminUser])
def category_edit(request, slug):
    category = get_object_or_404(Category, slug=slug)
    serializer = CategorySerializer(category, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message": "Category updated successfully", "data": serializer.data}
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 📌 حذف كاتيجوري
@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def category_delete(request, slug):
    category = get_object_or_404(Category, slug=slug)
    category.delete()
    return Response({"message": "Category deleted successfully"}, status=status.HTTP_204_NO_CONTENT)