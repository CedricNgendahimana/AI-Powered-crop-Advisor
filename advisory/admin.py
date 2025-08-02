from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import MalawiRegion, Crop, Farmer, WeatherData, CropAdvice, FarmingCalendar, MarketPrice

@admin.register(MalawiRegion)
class MalawiRegionAdmin(admin.ModelAdmin):
    list_display = ['name', 'region', 'latitude', 'longitude', 'altitude', 'annual_rainfall']
    list_filter = ['region']
    search_fields = ['name']
    ordering = ['region', 'name']

@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ['name_en', 'name_ny', 'crop_type', 'planting_season', 'harvest_season', 'growing_period_days']
    list_filter = ['crop_type']
    search_fields = ['name_en', 'name_ny', 'scientific_name']
    filter_horizontal = ['suitable_regions']
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('name_en', 'name_ny', 'crop_type', 'scientific_name')
        }),
        (_('Growing Information'), {
            'fields': ('planting_season', 'harvest_season', 'growing_period_days', 'water_requirement', 'soil_type')
        }),
        (_('Regional Suitability'), {
            'fields': ('suitable_regions',)
        }),
    )

@admin.register(Farmer)
class FarmerAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'location', 'farm_size_acres', 'preferred_language', 'registration_date']
    list_filter = ['location', 'preferred_language', 'registration_date']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'phone_number']
    filter_horizontal = ['primary_crops']
    readonly_fields = ['registration_date']

@admin.register(WeatherData)
class WeatherDataAdmin(admin.ModelAdmin):
    list_display = ['location', 'date', 'temperature_max', 'temperature_min', 'humidity', 'rainfall', 'weather_condition']
    list_filter = ['location', 'date', 'weather_condition']
    search_fields = ['location__name']
    date_hierarchy = 'date'
    ordering = ['-date']

@admin.register(CropAdvice)
class CropAdviceAdmin(admin.ModelAdmin):
    list_display = ['title_en', 'farmer', 'crop', 'advice_type', 'is_urgent', 'created_at', 'validity_days']
    list_filter = ['advice_type', 'is_urgent', 'crop', 'created_at']
    search_fields = ['title_en', 'title_ny', 'farmer__user__username']
    readonly_fields = ['created_at']
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('farmer', 'crop', 'advice_type', 'is_urgent', 'validity_days')
        }),
        (_('English Content'), {
            'fields': ('title_en', 'content_en')
        }),
        (_('Chichewa Content'), {
            'fields': ('title_ny', 'content_ny'),
            'classes': ['collapse']
        }),
        (_('Context'), {
            'fields': ('weather_context', 'created_at')
        }),
    )

@admin.register(FarmingCalendar)
class FarmingCalendarAdmin(admin.ModelAdmin):
    list_display = ['crop', 'region', 'month', 'activity_en']
    list_filter = ['crop', 'region', 'month']
    search_fields = ['crop__name_en', 'region__name', 'activity_en', 'activity_ny']
    ordering = ['crop', 'region', 'month']

@admin.register(MarketPrice)
class MarketPriceAdmin(admin.ModelAdmin):
    list_display = ['crop', 'location', 'date', 'price_per_kg', 'market_name', 'source']
    list_filter = ['crop', 'location', 'date', 'source']
    search_fields = ['crop__name_en', 'location__name', 'market_name']
    date_hierarchy = 'date'
    ordering = ['-date']
