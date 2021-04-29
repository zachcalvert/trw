from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('production.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = "TRW Admin"
admin.site.site_title = "TRW Admin Portal"
admin.site.index_title = "Welcome to the TRW Work Order Admin"