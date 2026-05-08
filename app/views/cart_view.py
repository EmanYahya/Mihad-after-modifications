from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from app.models import Cart, Product, Order, Color, Size
from app.models.cart import OrderItem
from ..serializers import CartSerializer
from django.db import transaction
from django.db.models import Sum, Prefetch
from django.db.models.functions import TruncDay
from datetime import timedelta
from django.utils import timezone


@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_dashboard_analytics(request):
    total_sales = Order.objects.aggregate(Sum('total_price'))['total_price__sum'] or 0
    orders_count = Order.objects.count()
    low_stock_count = Product.objects.filter(stock__lte=5).count()

    recent_orders = Order.objects.select_related('user').prefetch_related(
        Prefetch('items', queryset=OrderItem.objects.select_related('product').order_by('id'))
    ).order_by('-created_at')[:10]

    orders_table_data = []
    for order in recent_orders:
        first_item = next(iter(order.items.all()), None)
        product = first_item.product if first_item else None
        image = product.main_image.url if product and product.main_image else None
        orders_table_data.append({
            "id": order.id,
            "customer": order.full_name,
            "total": order.total_price,
            "image": image,
            "status": order.get_status_display(),
            "date": order.created_at.strftime("%Y-%m-%d %H:%M"),
            "address": f"{order.city}, {order.address}",
            "phone": order.phone,
        })

    seven_days_ago = timezone.now() - timedelta(days=7)
    sales_over_time = Order.objects.filter(created_at__gte=seven_days_ago)\
        .annotate(day=TruncDay('created_at'))\
        .values('day')\
        .annotate(daily_total=Sum('total_price'))\
        .order_by('day')

    chart_data = [
        {
            "date": item['day'].strftime("%Y-%m-%d"),
            "amount": item['daily_total']
        } for item in sales_over_time
    ]

    return Response({
        "cards": {
            "total_sales": total_sales,
            "orders_count": orders_count,
            "low_stock_alert": low_stock_count
        },
        "recent_orders_table": orders_table_data,
        "sales_chart": chart_data
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cart_detail(request):
    cart_items = Cart.objects.filter(user=request.user).select_related('product', 'color', 'size')
    serializer = CartSerializer(cart_items, many=True)
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    return Response({
        "success": True,
        "data": {
            "items": serializer.data,
            "total_price": total_price
        }
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    product_id = request.data.get('product_id')
    if not product_id:
        return Response({"success": False, "message": "product_id required"}, status=status.HTTP_400_BAD_REQUEST)

    product = get_object_or_404(Product, id=product_id)
    color = None
    size = None
    color_id = request.data.get('color_id')
    size_id = request.data.get('size_id')

    if color_id:
        color = get_object_or_404(Color, id=color_id)
        if not product.available_colors.filter(id=color.id).exists():
            return Response({"success": False, "message": "Selected color is not available for this product"}, status=status.HTTP_400_BAD_REQUEST)

    if size_id:
        size = get_object_or_404(Size, id=size_id)
        if not product.available_sizes.filter(id=size.id).exists():
            return Response({"success": False, "message": "Selected size is not available for this product"}, status=status.HTTP_400_BAD_REQUEST)

    if product.stock <= 0:
        return Response({
            "success": False,
            "message": "المنتج غير متوفر في المخزن"
        }, status=status.HTTP_400_BAD_REQUEST)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product,
        color=color,
        size=size,
    )

    if not created:
        if cart_item.quantity + 1 > product.stock:
            return Response({
                "success": False,
                "message": "الكمية المطلوبة غير متوفرة"
            }, status=status.HTTP_400_BAD_REQUEST)
        cart_item.quantity += 1
        cart_item.save()

    return Response({"success": True, "message": "Added to cart", "cart_item_id": cart_item.id}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(Cart.objects.select_related('product'), id=cart_item_id, user=request.user)

    quantity = request.data.get('quantity', 1)
    try:
        quantity = int(quantity)
    except (ValueError, TypeError):
        return Response({"success": False, "message": "Invalid quantity"}, status=status.HTTP_400_BAD_REQUEST)

    if quantity > 0:
        if quantity > cart_item.product.stock:
            return Response({
                "success": False,
                "message": "الكمية غير متوفرة في المخزن"
            }, status=status.HTTP_400_BAD_REQUEST)
        cart_item.quantity = quantity
        cart_item.save()
        return Response({"success": True, "message": "Cart item updated", "quantity": cart_item.quantity})

    cart_item.delete()
    return Response({"success": True, "message": "Item removed from cart"})


@api_view(['DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)
    cart_item.delete()
    return Response({"message": "تم حذف المنتج من السلة بنجاح"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@transaction.atomic
def checkout(request):
    required_fields = ['full_name', 'email', 'phone', 'address', 'city']
    missing_fields = [field for field in required_fields if not request.data.get(field)]
    if missing_fields:
        return Response({"error": "Missing required shipping fields", "fields": missing_fields}, status=status.HTTP_400_BAD_REQUEST)

    cart_items = list(Cart.objects.filter(user=request.user).select_related('product', 'color', 'size'))
    if not cart_items:
        return Response({"error": "السلة فارغة"}, status=status.HTTP_400_BAD_REQUEST)

    locked_products = {
        product.id: product
        for product in Product.objects.select_for_update().filter(id__in=[item.product_id for item in cart_items])
    }
    missing_product_ids = [item.product_id for item in cart_items if item.product_id not in locked_products]
    if missing_product_ids:
        return Response({
            "error": "Some cart products are no longer available",
            "product_ids": missing_product_ids,
        }, status=status.HTTP_400_BAD_REQUEST)

    for item in cart_items:
        product = locked_products[item.product_id]
        if item.quantity > product.stock:
            return Response({
                "error": "Insufficient stock",
                "product_id": product.id,
                "available_stock": product.stock,
            }, status=status.HTTP_400_BAD_REQUEST)

    total_price = sum(locked_products[item.product_id].price * item.quantity for item in cart_items)

    order = Order.objects.create(
        user=request.user,
        full_name=request.data['full_name'],
        email=request.data['email'],
        phone=request.data['phone'],
        address=request.data['address'],
        city=request.data['city'],
        total_price=total_price,
    )

    for item in cart_items:
        product = locked_products[item.product_id]
        OrderItem.objects.create(
            order=order,
            product=product,
            color=item.color.name if item.color else None,
            size=item.size.name if item.size else None,
            price=product.price,
            quantity=item.quantity,
        )
        product.stock -= item.quantity
        product.save(update_fields=['stock'])

    Cart.objects.filter(id__in=[item.id for item in cart_items]).delete()

    return Response({
        "message": "تم تسجيل طلبك بنجاح",
        "order_id": order.id,
        "total_price": order.total_price,
    }, status=status.HTTP_201_CREATED)
