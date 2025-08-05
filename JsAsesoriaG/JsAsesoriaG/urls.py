
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("inicio.urls")),
    path('interacciones/', include('interacciones.urls', namespace='interacciones')),
    path('accounts/', include('allauth.urls'))
]
