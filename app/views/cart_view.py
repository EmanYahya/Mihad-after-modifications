from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from app.models import Cart, Product, Order
from app.models.cart import OrderItem 
from ..serializers import CartSerializer # تأكدي من المسار الصحيح للسيرياليزر
from django.db import transaction
from django.db.models import Sum, Count
from django.db.models.functions import TruncDay
from datetime import timedelta
from django.utils import timezone


@api_view(['GET'])
@permission_classes([IsAdminUser]) # للأدمن فقط
def admin_dashboard_analytics(request):
    # 1. الـ Cards (إحصائيات سريعة)
    total_sales = Order.objects.aggregate(Sum('total_price'))['total_price__sum'] or 0
    orders_count = Order.objects.count()
    # تنبيه المخزون من المنتجات (أقل من 5 قطع)
    low_stock_count = Product.objects.filter(stock__lte=5).count()

    # 2. الـ Table (جدول الطلبات بالتواريخ)
    # بنجيب آخر 10 طلبات مرتبة من الأحدث للأقدم
    recent_orders = Order.objects.select_related('user').order_by('-created_at')[:10]
    orders_table_data = [
        {
            "id": order.id,
            "customer": order.full_name, # من موديل Order
            "total": order.total_price,
            "image": OrderItem.product.main_image.url if OrderItem.product.main_image else None,
            "status": order.get_status_display(), # يعرض (تم الشحن، قيد الانتظار...)
            "date": order.created_at.strftime("%Y-%m-%d %H:%M"),
            "address": f"{order.city}, {order.address}", # 👈 تم إضافة المدينة والعنوان هنا
            "phone": order.phone 
        } for order in recent_orders
    ]

    # 3. الـ Charts (بيانات الرسم البياني لآخر 7 أيام)
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

# ==========================================
# 🛒 دوال خاصة بالمستخدم المسجل فقط (IsAuthenticated)
# ==========================================

# 1. عرض محتويات السلة
@api_view(['GET'])
@permission_classes([IsAuthenticated]) # حماية: لا يراها إلا صاحب الحساب
def cart_detail(request):
    cart_items = Cart.objects.filter(user=request.user).select_related('product')
    
    # يفضل استخدام السيرياليزر الذي قمتِ بتعريفه في serializers.py
    serializer = CartSerializer(cart_items, many=True)
    
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    return Response({
        "success": True,
        "data": {
             "items": serializer.data,
             "total_price": total_price
        }
    })

# 2. إضافة منتج للسلة
@api_view(['POST'])
@permission_classes([IsAuthenticated]) # حماية: لا يمكن إضافة منتج إلا لمستخدم مسجل
def add_to_cart(request):
    product_id = request.data.get('product_id')
    if not product_id:
        return Response({"success": False, "message": "product_id required"}, status=status.HTTP_400_BAD_REQUEST)

    product = get_object_or_404(Product, id=product_id)

    #  تحقق من المخزون
    if product.stock <= 0:
        return Response({
            "success": False,
            "message": "المنتج غير متوفر في المخزن"
        }, status=status.HTTP_400_BAD_REQUEST)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )

    #  تحقق من الكمية قبل الزيادة
    if not created:
        if cart_item.quantity + 1 > product.stock:
            return Response({
                "success": False,
                "message": "الكمية المطلوبة غير متوفرة"
            }, status=status.HTTP_400_BAD_REQUEST)

        cart_item.quantity += 1
        cart_item.save()

    return Response({"success": True, "message": "Added to cart"}, status=status.HTTP_201_CREATED)

# 3. تحديث الكمية في السلة
@api_view(['POST'])
@permission_classes([IsAuthenticated]) # حماية: المستخدم يحدث سلته الشخصية فقط
def update_cart_item(request, cart_item_id):
    # التأكد أن العنصر يخص المستخدم الحالي (user=request.user)
    cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)

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
     
    else:
        cart_item.delete()
        return Response({"success": True, "message": "Item removed from cart"})

# 4. حذف منتج من السلة
@api_view(['DELETE', 'POST'])
@permission_classes([IsAuthenticated]) # حماية: لا يحذف إلا صاحب السلة
def remove_from_cart(request, cart_item_id):
    # تم دمج الحماية هنا من خلال الفلترة بالمستخدم الحالي مباشرة
    cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)
    cart_item.delete()
    return Response({"message": "تم حذف المنتج من السلة بنجاح"}, status=status.HTTP_204_NO_CONTENT)


# ==========================================
# 💳 دالة إتمام الطلب (Checkout)
# ==========================================
@api_view(['POST'])
@transaction.atomic
def checkout(request):
    # 1. بنجيب الحاجات اللي العميل اختارها في السلة فعلاً
    cart_items = Cart.objects.filter(user=request.user).select_related('product', 'color', 'size')
    
    if not cart_items.exists():
        return Response({"error": "السلة فارغة"})

    # 2. بنحسب السعر الإجمالي أوتوماتيك
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    # 3. بنعمل الأوردر
    order = Order.objects.create(
        user=request.user,
        total_price=total_price,
        # باقي بيانات الشحن بتيجي من request.data
    )

    # 4. السطر ده هو اللي "بيسحب" الاختيارات أوتوماتيك للأوردر
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            color=item.color,      # سحب اللون اللي العميل اختاره في السلة أوتوماتيك
            size=item.size,        # سحب المقاس اللي العميل اختاره في السلة أوتوماتيك
            price=item.product.price, # سحب السعر الحالي للمنتج أوتوماتيك
            quantity=item.quantity
        )
        
        # خصم المخزون أوتوماتيك
        item.product.stock -= item.quantity
        item.product.save()

    # 5. فضي السلة
    cart_items.delete()

    return Response({"message": "تم تسجيل طلبك بنجاح"})