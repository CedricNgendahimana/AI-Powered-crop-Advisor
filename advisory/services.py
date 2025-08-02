import requests
from datetime import datetime, timedelta
from django.utils import timezone
from django.utils.translation import gettext as _
from .models import WeatherData, CropAdvice, FarmingCalendar, Crop, MalawiRegion
import random

class WeatherService:
    """Service for managing weather data"""
    
    def __init__(self):
        # In a real application, you would use a proper weather API
        # For demo purposes, we'll generate realistic weather data
        pass
    
    def get_current_weather(self, location):
        """Get current weather for a location"""
        try:
            weather = WeatherData.objects.filter(
                location=location,
                date=timezone.now().date()
            ).first()
            
            if not weather:
                # Generate mock weather data
                weather = self.generate_mock_weather(location)
            
            return weather
        except Exception as e:
            print(f"Error getting weather: {e}")
            return None
    
    def generate_mock_weather(self, location):
        """Generate realistic mock weather data for Malawi"""
        current_date = timezone.now().date()
        current_month = current_date.month
        
        # Malawi weather patterns by month
        weather_patterns = {
            1: {'temp_range': (23, 31), 'rainfall': (150, 250), 'humidity': (75, 85)},  # January - Rainy
            2: {'temp_range': (23, 30), 'rainfall': (120, 200), 'humidity': (75, 85)},  # February - Rainy
            3: {'temp_range': (22, 29), 'rainfall': (80, 150), 'humidity': (70, 80)},   # March - End of rains
            4: {'temp_range': (20, 28), 'rainfall': (20, 60), 'humidity': (65, 75)},    # April - Dry season
            5: {'temp_range': (17, 26), 'rainfall': (5, 20), 'humidity': (60, 70)},     # May - Cool dry
            6: {'temp_range': (15, 24), 'rainfall': (2, 10), 'humidity': (55, 65)},     # June - Cool dry
            7: {'temp_range': (15, 24), 'rainfall': (2, 10), 'humidity': (55, 65)},     # July - Cool dry
            8: {'temp_range': (17, 27), 'rainfall': (5, 15), 'humidity': (55, 65)},     # August - Warming
            9: {'temp_range': (20, 30), 'rainfall': (10, 30), 'humidity': (60, 70)},    # September - Hot dry
            10: {'temp_range': (23, 33), 'rainfall': (20, 50), 'humidity': (65, 75)},   # October - Hot, pre-rains
            11: {'temp_range': (24, 32), 'rainfall': (60, 120), 'humidity': (70, 80)},  # November - Early rains
            12: {'temp_range': (24, 31), 'rainfall': (120, 200), 'humidity': (75, 85)}, # December - Rainy
        }
        
        pattern = weather_patterns[current_month]
        
        # Generate weather data
        temp_min = random.randint(pattern['temp_range'][0], pattern['temp_range'][0] + 3)
        temp_max = random.randint(pattern['temp_range'][1] - 3, pattern['temp_range'][1])
        humidity = random.randint(pattern['humidity'][0], pattern['humidity'][1])
        rainfall = random.randint(0, 20) if current_month in [4, 5, 6, 7, 8] else random.randint(0, 50)
        
        conditions = ['Sunny', 'Partly Cloudy', 'Cloudy', 'Light Rain', 'Heavy Rain']
        if current_month in [4, 5, 6, 7, 8]:  # Dry season
            condition = random.choice(['Sunny', 'Partly Cloudy', 'Cloudy'])
        else:  # Rainy season
            condition = random.choice(conditions)
        
        weather = WeatherData.objects.create(
            location=location,
            date=current_date,
            temperature_max=temp_max,
            temperature_min=temp_min,
            humidity=humidity,
            rainfall=rainfall,
            wind_speed=random.randint(5, 25),
            weather_condition=condition
        )
        
        return weather

class AdvisoryService:
    """Service for generating crop advice"""
    
    def __init__(self):
        self.weather_service = WeatherService()
    
    def generate_advice(self, farmer, crop, advice_type='general'):
        """Generate personalized crop advice for a farmer"""
        try:
            # Get current weather context
            weather_context = None
            if farmer.location:
                weather_context = self.weather_service.get_current_weather(farmer.location)
            
            # Generate advice based on type
            if advice_type == 'planting':
                advice = self._generate_planting_advice(farmer, crop, weather_context)
            elif advice_type == 'care':
                advice = self._generate_care_advice(farmer, crop, weather_context)
            elif advice_type == 'disease':
                advice = self._generate_disease_advice(farmer, crop, weather_context)
            elif advice_type == 'harvest':
                advice = self._generate_harvest_advice(farmer, crop, weather_context)
            elif advice_type == 'weather':
                advice = self._generate_weather_advice(farmer, crop, weather_context)
            else:
                advice = self._generate_general_advice(farmer, crop, weather_context)
            
            # Create and save the advice
            crop_advice = CropAdvice.objects.create(
                farmer=farmer,
                crop=crop,
                advice_type=advice_type,
                title_en=advice['title_en'],
                title_ny=advice.get('title_ny', ''),
                content_en=advice['content_en'],
                content_ny=advice.get('content_ny', ''),
                weather_context=weather_context,
                is_urgent=advice.get('is_urgent', False)
            )
            
            return crop_advice
            
        except Exception as e:
            print(f"Error generating advice: {e}")
            return None
    
    def _generate_planting_advice(self, farmer, crop, weather_context):
        """Generate planting advice"""
        current_month = timezone.now().month
        
        # Get farming calendar for this crop and region
        calendar_entry = FarmingCalendar.objects.filter(
            crop=crop,
            region=farmer.location,
            month=current_month
        ).first()
        
        title_en = f"Planting Advice for {crop.name_en}"
        title_ny = f"Malangizo a Kubzala {crop.name_ny or crop.name_en}"
        
        # Base planting advice
        content_en = f"""
        **Planting Recommendations for {crop.name_en}:**
        
        • **Planting Season:** {crop.planting_season}
        • **Growing Period:** {crop.growing_period_days} days
        • **Soil Requirements:** {crop.soil_type}
        • **Water Needs:** {crop.water_requirement}
        
        """
        
        # Add seasonal context
        if calendar_entry:
            content_en += f"**Current Month Activity:** {calendar_entry.activity_en}\n"
            content_en += f"{calendar_entry.description_en}\n\n"
        
        # Add weather context
        if weather_context:
            if weather_context.rainfall > 20:
                content_en += "**Weather Alert:** Good rainfall conditions for planting. Ensure proper drainage to prevent waterlogging.\n"
            elif weather_context.rainfall < 5:
                content_en += "**Weather Alert:** Low rainfall. Consider irrigation or wait for better rain conditions.\n"
        
        content_en += f"""
        **General Planting Tips:**
        • Prepare your land by clearing weeds and tilling
        • Use certified seeds for better yields
        • Plant at the recommended spacing
        • Apply base fertilizer if available
        • Monitor for pests and diseases early
        """
        
        # Chichewa translation (simplified)
        content_ny = f"""
        **Malangizo a Kubzala {crop.name_ny or crop.name_en}:**
        
        • **Nyengo ya Kubzala:** {crop.planting_season}
        • **Masiku a Kukula:** masiku {crop.growing_period_days}
        • **Mtundu wa Dothi:** {crop.soil_type}
        
        **Malangizo a Kubzala:**
        • Konzani munda wanu mochedwa
        • Gwiritsani ntchito mbewu zabwino
        • Bzalani molingana
        • Gwiritsani ntchito feteleza ngati mulina
        • Yangayang tizilombo ndi matenda
        """
        
        return {
            'title_en': title_en,
            'title_ny': title_ny,
            'content_en': content_en,
            'content_ny': content_ny,
            'is_urgent': False
        }
    
    def _generate_care_advice(self, farmer, crop, weather_context):
        """Generate crop care and maintenance advice"""
        title_en = f"Care Instructions for {crop.name_en}"
        title_ny = f"Kusamalira {crop.name_ny or crop.name_en}"
        
        content_en = f"""
        **Crop Care for {crop.name_en}:**
        
        **Watering:**
        • Water requirement: {crop.water_requirement}
        • Water early morning or late evening
        • Avoid watering during hot midday
        
        **Weeding:**
        • Remove weeds regularly to reduce competition
        • Be careful not to damage crop roots
        • Weed when soil is moist for easier removal
        
        **Fertilization:**
        • Apply top-dress fertilizer as needed
        • Use organic manure when available
        • Follow recommended application rates
        
        **Pest and Disease Monitoring:**
        • Check plants regularly for signs of damage
        • Remove affected plants immediately
        • Use integrated pest management approaches
        """
        
        # Add weather-specific care advice
        if weather_context:
            if weather_context.temperature_max > 30:
                content_en += "\n**Heat Stress Alert:** Provide shade during hottest parts of day. Increase watering frequency.\n"
            if weather_context.rainfall > 50:
                content_en += "\n**Heavy Rain Alert:** Ensure good drainage. Watch for fungal diseases.\n"
        
        content_ny = f"""
        **Kusamalira {crop.name_ny or crop.name_en}:**
        
        **Kuthirira:**
        • Thirirani mmawa kapena madzulo
        • Osathirira nthawi ya dzuwa lamphamvu
        
        **Kuchotsa udzu:**
        • Chotsani udzu nthawi zonse
        • Samalani kuti musawonongese mizu
        
        **Feteleza:**
        • Gwiritsirani ntchito feteleza monga momwe mwausizidwira
        • Gwiritsani ntchito manyowa a nyama
        
        **Tizilombo ndi Matenda:**
        • Yangayang mbewu nthawi zonse
        • Chotsani mbewu zowonongeka msanga
        """
        
        return {
            'title_en': title_en,
            'title_ny': title_ny,
            'content_en': content_en,
            'content_ny': content_ny,
            'is_urgent': False
        }
    
    def _generate_disease_advice(self, farmer, crop, weather_context):
        """Generate disease management advice"""
        title_en = f"Disease Prevention for {crop.name_en}"
        title_ny = f"Kupewa Matenda a {crop.name_ny or crop.name_en}"
        
        # Common diseases by crop type
        disease_info = {
            'cereal': {
                'diseases': ['Rust', 'Smut', 'Blight'],
                'prevention': 'Use resistant varieties, proper spacing, crop rotation'
            },
            'legume': {
                'diseases': ['Root rot', 'Leaf spot', 'Bacterial blight'],
                'prevention': 'Avoid waterlogging, use clean seeds, proper ventilation'
            },
            'tuber': {
                'diseases': ['Blight', 'Bacterial wilt', 'Virus diseases'],
                'prevention': 'Use certified planting material, hill properly, rotate crops'
            },
            'vegetable': {
                'diseases': ['Damping off', 'Powdery mildew', 'Bacterial spot'],
                'prevention': 'Good sanitation, proper spacing, avoid overhead watering'
            },
            'fruit': {
                'diseases': ['Fruit fly', 'Anthracnose', 'Root rot'],
                'prevention': 'Proper pruning, harvest timely, good drainage'
            }
        }
        
        crop_diseases = disease_info.get(crop.crop_type, disease_info['cereal'])
        
        content_en = f"""
        **Disease Management for {crop.name_en}:**
        
        **Common Diseases:**
        {', '.join(crop_diseases['diseases'])}
        
        **Prevention Strategies:**
        • {crop_diseases['prevention']}
        • Regular field inspection
        • Remove and destroy infected plants
        • Use clean tools and equipment
        • Practice crop rotation
        
        **Treatment:**
        • Apply appropriate fungicides if needed
        • Improve field drainage
        • Reduce plant density if overcrowded
        • Seek advice from agricultural extension officers
        """
        
        # Weather-based disease warnings
        if weather_context:
            if weather_context.humidity > 80:
                content_en += "\n**High Humidity Warning:** Increased risk of fungal diseases. Ensure good air circulation.\n"
                is_urgent = True
            else:
                is_urgent = False
        else:
            is_urgent = False
        
        content_ny = f"""
        **Kuletsa Matenda a {crop.name_ny or crop.name_en}:**
        
        **Matenda Ofala:**
        {', '.join(crop_diseases['diseases'])}
        
        **Njira za Kuletsa:**
        • Gwiritsani ntchito mbewu zabwino
        • Yangayang munda nthawi zonse
        • Chotsani mbewu zodwala msanga
        • Gwiritsani ntchito zipangizo zoyera
        """
        
        return {
            'title_en': title_en,
            'title_ny': title_ny,
            'content_en': content_en,
            'content_ny': content_ny,
            'is_urgent': is_urgent
        }
    
    def _generate_harvest_advice(self, farmer, crop, weather_context):
        """Generate harvest advice"""
        title_en = f"Harvest Guidelines for {crop.name_en}"
        title_ny = f"Malangizo a Kutcha {crop.name_ny or crop.name_en}"
        
        content_en = f"""
        **Harvest Information for {crop.name_en}:**
        
        **Harvest Season:** {crop.harvest_season}
        **Growing Period:** {crop.growing_period_days} days from planting
        
        **Signs of Maturity:**
        • Check for proper color development
        • Test firmness and texture
        • Monitor moisture content
        • Look for natural leaf yellowing
        
        **Harvest Tips:**
        • Harvest during cool parts of the day
        • Use clean, sharp tools
        • Handle produce carefully to avoid damage
        • Sort by quality and size
        
        **Post-Harvest:**
        • Dry properly if needed
        • Store in clean, dry conditions
        • Monitor for pests during storage
        • Market surplus quickly for best prices
        """
        
        if weather_context and weather_context.rainfall > 20:
            content_en += "\n**Weather Alert:** Rain expected. Harvest mature crops quickly to prevent damage.\n"
            is_urgent = True
        else:
            is_urgent = False
        
        content_ny = f"""
        **Malangizo a Kutcha {crop.name_ny or crop.name_en}:**
        
        **Nyengo ya Kutcha:** {crop.harvest_season}
        **Masiku a Kukula:** masiku {crop.growing_period_days}
        
        **Zizindikiro za Kucha:**
        • Yangayang kusintha kwa mtundu
        • Funsani kuuma kwa mbewu
        • Onani masamba akuchita yellow
        
        **Malangizo a Kutcha:**
        • Tchani nthawi yozizira
        • Gwiritsani ntchito zipangizo zakucha
        • Samalitsani mbewu musawonongeke
        • Sunganitsani mbewu monga mmene ziliri
        """
        
        return {
            'title_en': title_en,
            'title_ny': title_ny,
            'content_en': content_en,
            'content_ny': content_ny,
            'is_urgent': is_urgent
        }
    
    def _generate_weather_advice(self, farmer, crop, weather_context):
        """Generate weather-based advice"""
        title_en = f"Weather Advisory for {crop.name_en}"
        title_ny = f"Malangizo a Nyengo pa {crop.name_ny or crop.name_en}"
        
        if not weather_context:
            content_en = "Weather data not available. Please check local weather conditions."
            content_ny = "Zambiri za nyengo sizilipo. Funsani za nyengo m'dera lanu."
            return {
                'title_en': title_en,
                'title_ny': title_ny,
                'content_en': content_en,
                'content_ny': content_ny,
                'is_urgent': False
            }
        
        content_en = f"""
        **Weather-Based Recommendations for {crop.name_en}:**
        
        **Current Conditions ({weather_context.date}):**
        • Temperature: {weather_context.temperature_min}°C - {weather_context.temperature_max}°C
        • Humidity: {weather_context.humidity}%
        • Rainfall: {weather_context.rainfall}mm
        • Condition: {weather_context.weather_condition}
        
        **Recommendations:**
        """
        
        # Temperature-based advice
        if weather_context.temperature_max > 32:
            content_en += "• High temperatures expected. Increase watering and provide shade if possible.\n"
        elif weather_context.temperature_max < 18:
            content_en += "• Cool temperatures. Growth may slow down. Protect sensitive crops.\n"
        
        # Rainfall-based advice
        if weather_context.rainfall > 50:
            content_en += "• Heavy rainfall expected. Ensure good drainage and harvest mature crops.\n"
        elif weather_context.rainfall < 5:
            content_en += "• Low rainfall. Plan irrigation or wait for better conditions for planting.\n"
        
        # Humidity-based advice
        if weather_context.humidity > 85:
            content_en += "• High humidity increases disease risk. Improve ventilation and monitor crops closely.\n"
        
        content_ny = f"""
        **Malangizo a Nyengo pa {crop.name_ny or crop.name_en}:**
        
        **Nyengo Yamasiku ano ({weather_context.date}):**
        • Kutentha: {weather_context.temperature_min}°C - {weather_context.temperature_max}°C
        • Humidity: {weather_context.humidity}%
        • Mvula: {weather_context.rainfall}mm
        
        **Malangizo:**
        • Samalani mbewu zanu molingana ndi nyengo
        • Thirirani mbewu ngati kulibe mvula
        • Chenjerani ndi matenda nthawi ya chinyengo
        """
        
        is_urgent = (weather_context.rainfall > 50 or 
                     weather_context.temperature_max > 35 or 
                     weather_context.humidity > 90)
        
        return {
            'title_en': title_en,
            'title_ny': title_ny,
            'content_en': content_en,
            'content_ny': content_ny,
            'is_urgent': is_urgent
        }
    
    def _generate_general_advice(self, farmer, crop, weather_context):
        """Generate general farming advice"""
        title_en = f"General Advice for {crop.name_en}"
        title_ny = f"Malangizo Onse a {crop.name_ny or crop.name_en}"
        
        content_en = f"""
        **General Farming Tips for {crop.name_en}:**
        
        **Best Practices:**
        • Follow recommended planting dates
        • Use quality seeds and planting materials
        • Practice proper spacing and planting depth
        • Apply fertilizers as recommended
        • Control weeds, pests, and diseases promptly
        
        **Crop Information:**
        • Type: {crop.get_crop_type_display()}
        • Growing period: {crop.growing_period_days} days
        • Water requirement: {crop.water_requirement}
        • Suitable soil: {crop.soil_type}
        
        **Success Tips:**
        • Keep detailed farming records
        • Join farmer groups for shared learning
        • Seek advice from extension workers
        • Market your produce strategically
        • Practice crop rotation for soil health
        """
        
        content_ny = f"""
        **Malangizo Onse a {crop.name_ny or crop.name_en}:**
        
        **Njira Zabwino:**
        • Tsatirani masiku a kubzala
        • Gwiritsani ntchito mbewu zabwino
        • Bzalani mbewu molingana
        • Gwiritsani ntchito feteleza
        • Letsani udzu ndi tizilombo
        
        **Zambiri za Mbewu:**
        • Mtundu: {crop.get_crop_type_display()}
        • Masiku a kukula: masiku {crop.growing_period_days}
        
        **Malangizo a Chipambano:**
        • Lembani zonse zimene mukuchita mu munda
        • Lowani nawo m'magulu a alimi
        • Funsani malangizo kwa aphunzitsi a ulimi
        """
        
        return {
            'title_en': title_en,
            'title_ny': title_ny,
            'content_en': content_en,
            'content_ny': content_ny,
            'is_urgent': False
        }