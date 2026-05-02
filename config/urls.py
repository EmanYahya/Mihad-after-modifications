from django.contrib import admin
from django.urls import path, include
from app.views.home_view import home
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('app/', include('app.urls')),
    path('products/', include('products.urls')),
    path('', home, name='home'),
   # path('about/', TemplateView.as_view(template_name='about.html'), name='abou
]

# Se.rve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
