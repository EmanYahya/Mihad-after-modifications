from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from app.forms import EditProfileForm


# 👤 عرض البروفايل
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_detail(request):
    user = request.user

    return Response({
        "success": True,
        "data": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }
    })


# ✏️ تعديل البروفايل
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def edit_profile(request):
    user = request.user

    form = EditProfileForm(request.data, instance=user)

    if form.is_valid():
        form.save()
        return Response({
            "success": True,
            "message": "Profile updated successfully"
        })

    return Response({
        "success": False,
        "errors": form.errors
    }, status=400)