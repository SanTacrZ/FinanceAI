from django.contrib import admin
from django.urls import path, include
from market.views import health

urlpatterns = [
	path('admin/', admin.site.urls),
	path('api/health', health),
	path('api/colcap/', include('market.urls')),
]