- regester
app/auth/register/
- login
  app/auth/login/
  app/auth/logout
-post cart
 -app/api/cart/         ( cart details )
 -app/api/cart/add/     ( add cart )
 -app/api/cart/update/<int:cart_item_id>/  (update cart )
 -app/api/cart/remove/<int:cart_item_id>/  (remove cart )
 -app/api/cart/checkout/     ( تاكيد الشراء )

  -Get home
  app/home/

  - Get search
    app/search/

  -Get Wishlist
   app/wishlist/

  -post wishlist
   app/add-to-wishlist/<int:product_id>/     (add-wishlist)
   app/remove-from-wishlist/<int:product_id>/  (remove wishlist)

  for admin
  - app/api/admin/dashboard/   (get) 
  - product/add/     ( post )
  - product/<int:product_id>/upload-images/    (post)

  - product
  - product/<int:product_id>/images/   (GET) عرض الصور
  - product/product-list/              (GET) عرض المنتجات 

  category 
  - product/categoey-list/    (GET)
  - product/category/<slug:category_slug>/  (get)
  - product/<slug:category_slug>/<slug:subcategory_slug>/<slug:product_slug>/   (GET) تفاصيل المنتج 

  subcategory
   - product/category/<slug:category_slug>/subcategory/<slug:subcategory_slug>/   ( get ) 
  
