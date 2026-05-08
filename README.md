- register
  app/auth/register/
- login
  app/auth/login/
  app/auth/logout
- cart
  - app/api/cart/ (cart details)
  - app/api/cart/add/ (add cart)
  - app/api/cart/update/<int:cart_item_id>/ (update cart)
  - app/api/cart/remove/<int:cart_item_id>/ (remove cart)
  - app/api/cart/checkout/ (confirm purchase)

- home
  app/home/

- search
  app/search/

- wishlist
  app/wishlist/

- wishlist actions
  app/add-to-wishlist/<int:product_id>/ (add wishlist)
  app/remove-from-wishlist/<int:product_id>/ (remove wishlist)

- admin
  - app/api/admin/dashboard/ (GET)
  - products/add/ (POST)
  - products/<int:product_id>/upload-images/ (POST)

- products
  - products/<int:product_id>/images/ (GET)
  - products/product-list/ (GET)

- category
  - products/category-list/ (GET)
  - products/category/<slug:category_slug>/ (GET)
  - products/product/<slug:category_slug>/<slug:subcategory_slug>/<slug:product_slug>/ (GET product detail)

- subcategory
  - products/category/<slug:category_slug>/subcategory/<slug:subcategory_slug>/ (GET)

Setup:
1. Install dependencies: `pip install -r requirements.txt`
2. Configure environment variables as needed:
   - `SECRET_KEY` (required when `DEBUG=false`)
   - `DEBUG` (`true` for local development, `false` for production)
   - `ALLOWED_HOSTS` (comma-separated hosts, for example `example.com,www.example.com`)
   - `DB_ENGINE` (defaults to `django.db.backends.mysql`)
   - `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `DB_CHARSET`
   - `CORS_ALLOW_ALL_ORIGINS` or `CORS_ALLOWED_ORIGINS` (comma-separated origins)
3. Run migrations with the configured database.
