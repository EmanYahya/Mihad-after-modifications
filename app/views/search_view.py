from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.db.models import Q
from products.models import Product


# 🔍 Search API
@api_view(['GET'])
def search(request):
    query = request.GET.get('q', None)

    if not query:
        return Response({
            "success": False,
            "message": "Please provide a search query"
        })

    query_set = (
        Q(name__icontains=query) |
        Q(category__name__icontains=query) |
        Q(description__icontains=query)
    )

    products = Product.objects.filter(query_set)

    # filters (optional)
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    category = request.GET.get('category')

    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)

    if category:
        products = products.filter(category__slug=category)

    # sorting
    sort = request.GET.get('sort')

    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'name_asc':
        products = products.order_by('name')
    elif sort == 'name_desc':
        products = products.order_by('-name')

    # response data
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
        "query": query,
        "count": len(data),
        "data": data
    })