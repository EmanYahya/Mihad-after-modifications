from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404

from products.models import Product, Review


# ⭐ إنشاء Review
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    rating = request.data.get('rating')
    comment = request.data.get('comment')

    review = Review.objects.create(
        user=request.user,
        product=product,
        rating=rating,
        comment=comment
    )

    return Response({
        "success": True,
        "message": "Review added successfully",
        "data": {
            "id": review.id,
            "rating": review.rating,
            "comment": review.comment,
            "product": product.name
        }
    }, status=status.HTTP_201_CREATED)


# ✏️ تعديل Review (صاحبها فقط)
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    if review.user != request.user:
        return Response({
            "success": False,
            "message": "You do not have permission to edit this review"
        }, status=status.HTTP_403_FORBIDDEN)

    review.rating = request.data.get('rating', review.rating)
    review.comment = request.data.get('comment', review.comment)
    review.save()

    return Response({
        "success": True,
        "message": "Review updated successfully",
        "data": {
            "id": review.id,
            "rating": review.rating,
            "comment": review.comment
        }
    })


# ❌ حذف Review (صاحبها فقط)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    if review.user != request.user:
        return Response({
            "success": False,
            "message": "You do not have permission to delete this review"
        }, status=status.HTTP_403_FORBIDDEN)

    review.delete()

    return Response({
        "success": True,
        "message": "Review deleted successfully"
    }, status=status.HTTP_204_NO_CONTENT)