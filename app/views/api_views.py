from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from ..models import Product
from ..serializers import ProductSerializer

class ProductViewSet:
    queryset = Product.objects.all()
    serializer_class = ProductSerializer