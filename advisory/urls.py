from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Main pages
    path('', views.homepage, name='homepage'),
    path('crops/', views.crop_list, name='crop_list'),
    path('crops/<int:crop_id>/', views.crop_detail, name='crop_detail'),
    path('weather/', views.weather_info, name='weather_info'),
    path('calendar/', views.farming_calendar_view, name='farming_calendar'),
    
    # Authentication
    path('register/', views.register_farmer, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Farmer dashboard and profile
    path('dashboard/', views.farmer_dashboard, name='farmer_dashboard'),
    path('profile/', views.complete_profile, name='complete_profile'),
    path('advice/get/', views.get_advice, name='get_advice'),
    path('advice/history/', views.advice_history, name='advice_history'),
    
    # Language switching
    path('set-language/', views.set_language, name='set_language'),
    
    # API endpoints
    path('api/weather/<int:region_id>/', views.api_weather, name='api_weather'),
    path('api/prices/<int:crop_id>/', views.api_market_prices, name='api_market_prices'),
]