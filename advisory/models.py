from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class MalawiRegion(models.Model):
    """Malawi administrative regions and districts"""
    REGION_CHOICES = [
        ('northern', _('Northern Region')),
        ('central', _('Central Region')),
        ('southern', _('Southern Region')),
    ]
    
    name = models.CharField(max_length=100, verbose_name=_('District Name'))
    region = models.CharField(max_length=20, choices=REGION_CHOICES, verbose_name=_('Region'))
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    altitude = models.IntegerField(null=True, blank=True, verbose_name=_('Altitude (meters)'))
    annual_rainfall = models.IntegerField(null=True, blank=True, verbose_name=_('Annual Rainfall (mm)'))
    
    class Meta:
        verbose_name = _('Malawi District')
        verbose_name_plural = _('Malawi Districts')
    
    def __str__(self):
        return f"{self.name} - {self.get_region_display()}"

class Crop(models.Model):
    """Available crops for Malawi"""
    CROP_TYPES = [
        ('cereal', _('Cereals')),
        ('legume', _('Legumes')),
        ('tuber', _('Tubers')),
        ('vegetable', _('Vegetables')),
        ('fruit', _('Fruits')),
        ('cash', _('Cash Crops')),
    ]
    
    name_en = models.CharField(max_length=100, verbose_name=_('Name (English)'))
    name_ny = models.CharField(max_length=100, verbose_name=_('Name (Chichewa)'), blank=True)
    crop_type = models.CharField(max_length=20, choices=CROP_TYPES, verbose_name=_('Crop Type'))
    scientific_name = models.CharField(max_length=150, blank=True, verbose_name=_('Scientific Name'))
    planting_season = models.CharField(max_length=100, verbose_name=_('Planting Season'))
    harvest_season = models.CharField(max_length=100, verbose_name=_('Harvest Season'))
    water_requirement = models.CharField(max_length=50, verbose_name=_('Water Requirement'))
    soil_type = models.TextField(verbose_name=_('Suitable Soil Types'))
    growing_period_days = models.IntegerField(verbose_name=_('Growing Period (days)'))
    suitable_regions = models.ManyToManyField(MalawiRegion, verbose_name=_('Suitable Regions'))
    
    class Meta:
        verbose_name = _('Crop')
        verbose_name_plural = _('Crops')
    
    def __str__(self):
        return self.name_en

class Farmer(models.Model):
    """Farmer profile"""
    LANGUAGE_CHOICES = [
        ('en', _('English')),
        ('ny', _('Chichewa')),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, verbose_name=_('Phone Number'))
    location = models.ForeignKey(MalawiRegion, on_delete=models.SET_NULL, null=True, verbose_name=_('Location'))
    farm_size_acres = models.FloatField(verbose_name=_('Farm Size (acres)'))
    preferred_language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='en', verbose_name=_('Preferred Language'))
    primary_crops = models.ManyToManyField(Crop, verbose_name=_('Primary Crops'), blank=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Farmer')
        verbose_name_plural = _('Farmers')
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.location}"

class WeatherData(models.Model):
    """Weather information for locations"""
    location = models.ForeignKey(MalawiRegion, on_delete=models.CASCADE)
    date = models.DateField()
    temperature_max = models.FloatField(verbose_name=_('Max Temperature (°C)'))
    temperature_min = models.FloatField(verbose_name=_('Min Temperature (°C)'))
    humidity = models.FloatField(verbose_name=_('Humidity (%)'))
    rainfall = models.FloatField(default=0, verbose_name=_('Rainfall (mm)'))
    wind_speed = models.FloatField(null=True, blank=True, verbose_name=_('Wind Speed (km/h)'))
    weather_condition = models.CharField(max_length=50, verbose_name=_('Weather Condition'))
    
    class Meta:
        verbose_name = _('Weather Data')
        verbose_name_plural = _('Weather Data')
        unique_together = ['location', 'date']
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.location} - {self.date}"

class CropAdvice(models.Model):
    """AI-generated crop advice"""
    ADVICE_TYPES = [
        ('planting', _('Planting Advice')),
        ('care', _('Care & Maintenance')),
        ('disease', _('Disease Management')),
        ('harvest', _('Harvest Advice')),
        ('weather', _('Weather-based Advice')),
        ('general', _('General Advice')),
    ]
    
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    advice_type = models.CharField(max_length=20, choices=ADVICE_TYPES, verbose_name=_('Advice Type'))
    title_en = models.CharField(max_length=200, verbose_name=_('Title (English)'))
    title_ny = models.CharField(max_length=200, verbose_name=_('Title (Chichewa)'), blank=True)
    content_en = models.TextField(verbose_name=_('Content (English)'))
    content_ny = models.TextField(verbose_name=_('Content (Chichewa)'), blank=True)
    weather_context = models.ForeignKey(WeatherData, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_urgent = models.BooleanField(default=False, verbose_name=_('Urgent'))
    validity_days = models.IntegerField(default=7, verbose_name=_('Validity (days)'))
    
    class Meta:
        verbose_name = _('Crop Advice')
        verbose_name_plural = _('Crop Advice')
        ordering = ['-created_at', '-is_urgent']
    
    def __str__(self):
        return f"{self.title_en} - {self.farmer.user.username}"

class FarmingCalendar(models.Model):
    """Seasonal farming calendar for Malawi"""
    MONTHS = [
        (1, _('January')), (2, _('February')), (3, _('March')),
        (4, _('April')), (5, _('May')), (6, _('June')),
        (7, _('July')), (8, _('August')), (9, _('September')),
        (10, _('October')), (11, _('November')), (12, _('December')),
    ]
    
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    region = models.ForeignKey(MalawiRegion, on_delete=models.CASCADE)
    month = models.IntegerField(choices=MONTHS)
    activity_en = models.CharField(max_length=200, verbose_name=_('Activity (English)'))
    activity_ny = models.CharField(max_length=200, verbose_name=_('Activity (Chichewa)'), blank=True)
    description_en = models.TextField(verbose_name=_('Description (English)'))
    description_ny = models.TextField(verbose_name=_('Description (Chichewa)'), blank=True)
    
    class Meta:
        verbose_name = _('Farming Calendar Entry')
        verbose_name_plural = _('Farming Calendar Entries')
        unique_together = ['crop', 'region', 'month']
        ordering = ['month']
    
    def __str__(self):
        return f"{self.crop} - {self.get_month_display()} ({self.region})"

class MarketPrice(models.Model):
    """Market prices for crops"""
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    location = models.ForeignKey(MalawiRegion, on_delete=models.CASCADE)
    date = models.DateField()
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Price per KG (MWK)'))
    market_name = models.CharField(max_length=100, verbose_name=_('Market Name'))
    source = models.CharField(max_length=100, default='Manual Entry', verbose_name=_('Price Source'))
    
    class Meta:
        verbose_name = _('Market Price')
        verbose_name_plural = _('Market Prices')
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.crop} - MWK {self.price_per_kg}/kg ({self.date})"
