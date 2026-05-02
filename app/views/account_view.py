from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


@api_view(['POST'])
def register_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    # validation
    if not username or not password:
        return Response({
            "success": False,
            "message": "username and password required"
        }, status=400)

    if len(password) < 6:
        return Response({
            "success": False,
            "message": "Password must be at least 6 characters"
        }, status=400)

    if User.objects.filter(username=username).exists():
        return Response({
            "success": False,
            "message": "User already exists"
        }, status=400)

    # create user
    user = User.objects.create_user(username=username, password=password)

    # create token مباشرة
    token = Token.objects.create(user=user)

    return Response({
        "success": True,
        "message": "User created successfully",
        "token": token.key
    }, status=201)


@api_view(['POST'])
def logout_view(request):
    try:
        request.user.auth_token.delete()
    except:
        pass

    return Response({
        "success": True,
        "message": "Logged out successfully"
    })