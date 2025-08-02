from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.utils.translation import gettext as _, activate, get_language
from django.utils import timezone
from django.db.models import Q
from datetime import datetime, timedelta
from .models import (
    MalawiRegion, Crop, Farmer, WeatherData, CropAdvice, 
    FarmingCalendar, MarketPrice
)
from .forms import FarmerRegistrationForm, FarmerProfileForm
from .services import AdvisoryService, WeatherService
import json

def set_language(request):
    """Set user's preferred language"""
    language = request.GET.get('language', 'en')
    if language in ['en', 'ny']:
        activate(language)
        request.session['django_language'] = language
        
        # Update farmer's preferred language if logged in
        if request.user.is_authenticated and hasattr(request.user, 'farmer'):
            farmer = request.user.farmer
            farmer.preferred_language = language
            farmer.save()
    
    return redirect(request.META.get('HTTP_REFERER', '/'))

def homepage(request):
    """Homepage with language selection and basic info"""
    # Get current language from session or user preference
    if request.user.is_authenticated and hasattr(request.user, 'farmer'):
        language = request.user.farmer.preferred_language
        activate(language)
    else:
        language = request.session.get('django_language', 'en')
        activate(language)
    
    # Get some statistics for the homepage
    total_farmers = Farmer.objects.count()
    total_crops = Crop.objects.count()
    total_regions = MalawiRegion.objects.count()
    recent_advice = CropAdvice.objects.filter(
        created_at__gte=timezone.now() - timedelta(days=7)
    ).count()
    
    context = {
        'total_farmers': total_farmers,
        'total_crops': total_crops,
        'total_regions': total_regions,
        'recent_advice': recent_advice,
        'current_language': language,
    }
    
    return render(request, 'advisory/homepage.html', context)

def register_farmer(request):
    """Register a new farmer"""
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        farmer_form = FarmerRegistrationForm(request.POST)
        
        if user_form.is_valid() and farmer_form.is_valid():
            user = user_form.save()
            farmer = farmer_form.save(commit=False)
            farmer.user = user
            farmer.save()
            farmer_form.save_m2m()
            
            username = user_form.cleaned_data.get('username')
            messages.success(request, _('Account created for %(username)s') % {'username': username})
            
            # Auto login the user
            login(request, user)
            return redirect('farmer_dashboard')
    else:
        user_form = UserCreationForm()
        farmer_form = FarmerRegistrationForm()
    
    context = {
        'user_form': user_form,
        'farmer_form': farmer_form,
    }
    return render(request, 'advisory/register.html', context)

@login_required
def farmer_dashboard(request):
    """Farmer dashboard with personalized advice"""
    try:
        farmer = request.user.farmer
    except Farmer.DoesNotExist:
        messages.error(request, _('Please complete your farmer profile.'))
        return redirect('complete_profile')
    
    # Set language preference
    activate(farmer.preferred_language)
    
    # Get recent advice for this farmer
    recent_advice = CropAdvice.objects.filter(
        farmer=farmer,
        created_at__gte=timezone.now() - timedelta(days=30)
    )[:5]
    
    # Get current weather for farmer's location
    current_weather = None
    if farmer.location:
        current_weather = WeatherData.objects.filter(
            location=farmer.location,
            date=timezone.now().date()
        ).first()
    
    # Get farming calendar for current month
    current_month = timezone.now().month
    farming_activities = FarmingCalendar.objects.filter(
        region=farmer.location,
        month=current_month,
        crop__in=farmer.primary_crops.all()
    ) if farmer.location else []
    
    # Get market prices for farmer's crops
    market_prices = MarketPrice.objects.filter(
        crop__in=farmer.primary_crops.all(),
        location=farmer.location,
        date__gte=timezone.now().date() - timedelta(days=7)
    ).order_by('-date')[:10] if farmer.location else []
    
    context = {
        'farmer': farmer,
        'recent_advice': recent_advice,
        'current_weather': current_weather,
        'farming_activities': farming_activities,
        'market_prices': market_prices,
        'current_language': farmer.preferred_language,
    }
    
    return render(request, 'advisory/dashboard.html', context)

@login_required
def complete_profile(request):
    """Complete farmer profile"""
    try:
        farmer = request.user.farmer
        form = FarmerProfileForm(request.POST or None, instance=farmer)
    except Farmer.DoesNotExist:
        form = FarmerProfileForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        farmer = form.save(commit=False)
        farmer.user = request.user
        farmer.save()
        form.save_m2m()
        messages.success(request, _('Profile updated successfully!'))
        return redirect('farmer_dashboard')
    
    return render(request, 'advisory/complete_profile.html', {'form': form})

@login_required
def get_advice(request):
    """Generate personalized crop advice"""
    try:
        farmer = request.user.farmer
    except Farmer.DoesNotExist:
        messages.error(request, _('Please complete your farmer profile first.'))
        return redirect('complete_profile')
    
    if request.method == 'POST':
        crop_id = request.POST.get('crop_id')
        advice_type = request.POST.get('advice_type', 'general')
        
        if crop_id:
            crop = get_object_or_404(Crop, id=crop_id)
            
            # Generate advice using the advisory service
            advisory_service = AdvisoryService()
            advice = advisory_service.generate_advice(farmer, crop, advice_type)
            
            if advice:
                messages.success(request, _('New advice generated!'))
                return redirect('farmer_dashboard')
            else:
                messages.error(request, _('Failed to generate advice. Please try again.'))
    
    # Get farmer's crops for the form
    crops = farmer.primary_crops.all()
    
    context = {
        'crops': crops,
        'advice_types': CropAdvice.ADVICE_TYPES,
    }
    
    return render(request, 'advisory/get_advice.html', context)

def crop_list(request):
    """List all available crops"""
    crops = Crop.objects.all()
    
    # Filter by region if specified
    region_id = request.GET.get('region')
    if region_id:
        region = get_object_or_404(MalawiRegion, id=region_id)
        crops = crops.filter(suitable_regions=region)
    
    # Filter by crop type if specified
    crop_type = request.GET.get('type')
    if crop_type:
        crops = crops.filter(crop_type=crop_type)
    
    regions = MalawiRegion.objects.all()
    crop_types = Crop.CROP_TYPES
    
    context = {
        'crops': crops,
        'regions': regions,
        'crop_types': crop_types,
        'selected_region': region_id,
        'selected_type': crop_type,
    }
    
    return render(request, 'advisory/crop_list.html', context)

def crop_detail(request, crop_id):
    """Detailed view of a specific crop"""
    crop = get_object_or_404(Crop, id=crop_id)
    
    # Get farming calendar for this crop
    farming_calendar = FarmingCalendar.objects.filter(crop=crop).order_by('month')
    
    # Get recent market prices
    market_prices = MarketPrice.objects.filter(
        crop=crop,
        date__gte=timezone.now().date() - timedelta(days=30)
    ).order_by('-date')[:10]
    
    context = {
        'crop': crop,
        'farming_calendar': farming_calendar,
        'market_prices': market_prices,
    }
    
    return render(request, 'advisory/crop_detail.html', context)

def weather_info(request):
    """Weather information for all regions"""
    regions = MalawiRegion.objects.all()
    weather_data = {}
    
    for region in regions:
        recent_weather = WeatherData.objects.filter(
            location=region,
            date__gte=timezone.now().date() - timedelta(days=7)
        ).order_by('-date')[:7]
        weather_data[region.id] = recent_weather
    
    context = {
        'regions': regions,
        'weather_data': weather_data,
    }
    
    return render(request, 'advisory/weather.html', context)

def farming_calendar_view(request):
    """Farming calendar for all crops and regions"""
    current_month = timezone.now().month
    
    # Get activities for current month
    current_activities = FarmingCalendar.objects.filter(month=current_month)
    
    # Get all months for navigation
    all_activities = FarmingCalendar.objects.all().order_by('month', 'crop__name_en')
    
    # Group by month
    activities_by_month = {}
    for activity in all_activities:
        if activity.month not in activities_by_month:
            activities_by_month[activity.month] = []
        activities_by_month[activity.month].append(activity)
    
    context = {
        'current_month': current_month,
        'current_activities': current_activities,
        'activities_by_month': activities_by_month,
        'months': FarmingCalendar.MONTHS,
    }
    
    return render(request, 'advisory/farming_calendar.html', context)

@login_required
def advice_history(request):
    """View farmer's advice history"""
    try:
        farmer = request.user.farmer
    except Farmer.DoesNotExist:
        messages.error(request, _('Please complete your farmer profile first.'))
        return redirect('complete_profile')
    
    advice_list = CropAdvice.objects.filter(farmer=farmer).order_by('-created_at')
    
    context = {
        'advice_list': advice_list,
    }
    
    return render(request, 'advisory/advice_history.html', context)

def api_weather(request, region_id):
    """API endpoint for weather data"""
    region = get_object_or_404(MalawiRegion, id=region_id)
    weather = WeatherData.objects.filter(
        location=region,
        date__gte=timezone.now().date() - timedelta(days=7)
    ).order_by('-date')
    
    data = []
    for w in weather:
        data.append({
            'date': w.date.isoformat(),
            'temp_max': w.temperature_max,
            'temp_min': w.temperature_min,
            'humidity': w.humidity,
            'rainfall': w.rainfall,
            'condition': w.weather_condition,
        })
    
    return JsonResponse({'weather_data': data})

def api_market_prices(request, crop_id):
    """API endpoint for market prices"""
    crop = get_object_or_404(Crop, id=crop_id)
    prices = MarketPrice.objects.filter(
        crop=crop,
        date__gte=timezone.now().date() - timedelta(days=30)
    ).order_by('-date')
    
    data = []
    for price in prices:
        data.append({
            'date': price.date.isoformat(),
            'price': float(price.price_per_kg),
            'market': price.market_name,
            'location': price.location.name,
        })
    
    return JsonResponse({'price_data': data})
