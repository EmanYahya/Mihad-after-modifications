from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    # validation
    if not username or not password:
        return Response({
            "success": False,
            "message": "username and password required"
        }, status=400)

    # authenticate
    user = authenticate(username=username, password=password)

    if not user:
        return Response({
            "success": False,
            "message": "Invalid credentials"
        }, status=401)

    # generate token
    token, _ = Token.objects.get_or_create(user=user)

    return Response({
        "success": True,
        "token": token.key
    })