from rest_framework.decorators import api_view
from rest_framework.response import Response

from products.models import Product, Category


# 🏠 Home API
@api_view(['GET'])
def home(request):
    # Featured products
    featured_products = Product.objects.filter(is_featured=True)

    # New arrivals
    new_products = Product.objects.filter(is_newarrival=True)[:6]

    # Categories
    categories = Category.objects.all()

    return Response({
        "success": True,
        "data": {
            "featured_products": [
                {
                    "id": p.id,
                    "name": p.name,
                    "price": p.price,
                    "stock": p.stock,
                    "category": p.category.name if p.category else None
                }
                for p in featured_products
            ],

            "new_products": [
                {
                    "id": p.id,
                    "name": p.name,
                    "price": p.price,
                    "stock": p.stock
                }
                for p in new_products
            ],

            "categories": [
                {
                    "id": c.id,
                    "name": c.name,
                    "slug": c.slug
                }
                for c in categories
            ]
        }
    })