from django.urls import path
from . import views

urlpatterns = [
	path('tickers', views.list_tickers),
	path('scan', views.scan_market),
	path('indicators/<str:symbol>', views.get_indicators),
	path('me/preferences', views.my_preferences),
	path('me/preferences/save', views.save_preferences),
]