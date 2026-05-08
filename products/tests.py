from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from app.models.cart import Cart, Order, OrderItem
from app.serializers import ProductSerializer
from products.models import Category, Color, Product, ProductImage, Size, SubCategory


class ProductCartCheckoutTests(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='buyer', password='password')
        self.seller = User.objects.create_user(username='seller', password='password')
        self.other_user = User.objects.create_user(username='other', password='password')
        self.category = Category.objects.create(name='Clothes', slug='clothes')
        self.subcategory = SubCategory.objects.create(name='Shirts', slug='shirts', category=self.category)
        self.red = Color.objects.create(name='Red', code='ff0000')
        self.blue = Color.objects.create(name='Blue', code='0000ff')
        self.small = Size.objects.create(name='S')
        self.product = Product.objects.create(
            name='Test Shirt',
            description='A shirt',
            price=Decimal('10.00'),
            stock=5,
            category=self.category,
            subcategory=self.subcategory,
            seller=self.seller,
            slug='test-shirt',
        )
        self.product.available_colors.add(self.red)
        self.product.available_sizes.add(self.small)

    def test_product_serializer_uses_main_image_field(self):
        serializer = ProductSerializer(self.product)
        self.assertIn('main_image', serializer.data)
        self.assertNotIn('main_image ', serializer.data)

    def test_add_to_cart_keeps_variants_separate_and_validates_availability(self):
        self.client.force_authenticate(self.user)
        url = reverse('app:add_to_cart')

        response = self.client.post(url, {
            'product_id': self.product.id,
            'color_id': self.red.id,
            'size_id': self.small.id,
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(url, {
            'product_id': self.product.id,
            'color_id': self.blue.id,
            'size_id': self.small.id,
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        cart_item = Cart.objects.get(user=self.user, product=self.product, color=self.red, size=self.small)
        self.assertEqual(cart_item.quantity, 1)

    def test_update_cart_item_returns_success_response(self):
        self.client.force_authenticate(self.user)
        cart_item = Cart.objects.create(user=self.user, product=self.product, color=self.red, size=self.small, quantity=1)

        response = self.client.post(reverse('app:update_cart_item', args=[cart_item.id]), {'quantity': 2}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        cart_item.refresh_from_db()
        self.assertEqual(cart_item.quantity, 2)

    def test_checkout_requires_auth_and_shipping_fields(self):
        url = reverse('app:checkout')
        response = self.client.post(url, {}, format='json')
        self.assertIn(response.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

        self.client.force_authenticate(self.user)
        Cart.objects.create(user=self.user, product=self.product, color=self.red, size=self.small, quantity=1)
        response = self.client.post(url, {'full_name': 'Buyer'}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data['fields'])

    def test_checkout_creates_order_items_with_variant_names_and_updates_stock(self):
        self.client.force_authenticate(self.user)
        Cart.objects.create(user=self.user, product=self.product, color=self.red, size=self.small, quantity=2)

        response = self.client.post(reverse('app:checkout'), {
            'full_name': 'Buyer Name',
            'email': 'buyer@example.com',
            'phone': '123456',
            'address': '123 Main St',
            'city': 'Cairo',
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        order = Order.objects.get(id=response.data['order_id'])
        order_item = OrderItem.objects.get(order=order)
        self.assertEqual(order.full_name, 'Buyer Name')
        self.assertEqual(order_item.color, 'Red')
        self.assertEqual(order_item.size, 'S')
        self.assertFalse(Cart.objects.filter(user=self.user).exists())
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 3)

    def test_product_image_upload_requires_seller_staff_or_superuser(self):
        url = f'/products/{self.product.id}/upload-images/'
        upload = SimpleUploadedFile('image.jpg', b'file-content', content_type='image/jpeg')

        self.client.force_authenticate(self.other_user)
        response = self.client.post(url, {'images': [upload]}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(self.seller)
        upload = SimpleUploadedFile('image.jpg', b'file-content', content_type='image/jpeg')
        response = self.client.post(url, {'images': [upload]}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ProductImage.objects.filter(product=self.product).count(), 1)
