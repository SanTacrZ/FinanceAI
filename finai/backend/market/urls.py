from django.urls import path
from . import views

urlpatterns = [
	path('tickers', views.list_tickers),
	path('scan', views.scan_market),
	path('indicators/<str:symbol>', views.get_indicators),
	path('me/preferences', views.my_preferences),
	path('me/preferences/save', views.save_preferences),
	path('portfolio', views.portfolio_get),
	path('portfolio/save', views.portfolio_save),
	path('news', views.news_list),
	path('chat/sessions', views.chat_sessions),
	path('chat/create', views.chat_create),
	path('chat/messages', views.chat_messages),
	path('chat/send', views.chat_add_message),
]