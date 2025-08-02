from django.core.management.base import BaseCommand
from django.utils import timezone
from advisory.models import MalawiRegion, Crop, FarmingCalendar, WeatherData
from datetime import date, timedelta
import random

class Command(BaseCommand):
    help = 'Populate the database with sample data for Malawi regions, crops, and farming calendar'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting data population...'))
        
        # Create Malawi regions and districts
        self.create_regions()
        
        # Create crops
        self.create_crops()
        
        # Create farming calendar entries
        self.create_farming_calendar()
        
        # Create sample weather data
        self.create_weather_data()
        
        self.stdout.write(self.style.SUCCESS('Data population completed successfully!'))

    def create_regions(self):
        """Create Malawi regions and districts"""
        regions_data = [
            # Northern Region
            {'name': 'Chitipa', 'region': 'northern', 'lat': -9.7, 'lng': 33.3, 'altitude': 1280, 'rainfall': 1000},
            {'name': 'Karonga', 'region': 'northern', 'lat': -9.9, 'lng': 33.9, 'altitude': 529, 'rainfall': 1200},
            {'name': 'Nkhata Bay', 'region': 'northern', 'lat': -11.6, 'lng': 34.3, 'altitude': 476, 'rainfall': 1400},
            {'name': 'Rumphi', 'region': 'northern', 'lat': -11.0, 'lng': 33.9, 'altitude': 980, 'rainfall': 1100},
            {'name': 'Mzimba', 'region': 'northern', 'lat': -11.9, 'lng': 33.6, 'altitude': 1340, 'rainfall': 1000},
            {'name': 'Likoma', 'region': 'northern', 'lat': -12.1, 'lng': 34.7, 'altitude': 520, 'rainfall': 1300},
            
            # Central Region
            {'name': 'Kasungu', 'region': 'central', 'lat': -13.0, 'lng': 33.5, 'altitude': 1060, 'rainfall': 900},
            {'name': 'Nkhotakota', 'region': 'central', 'lat': -12.9, 'lng': 34.3, 'altitude': 500, 'rainfall': 1100},
            {'name': 'Ntchisi', 'region': 'central', 'lat': -13.3, 'lng': 33.9, 'altitude': 1280, 'rainfall': 950},
            {'name': 'Dowa', 'region': 'central', 'lat': -13.7, 'lng': 33.9, 'altitude': 1200, 'rainfall': 1000},
            {'name': 'Salima', 'region': 'central', 'lat': -13.8, 'lng': 34.6, 'altitude': 512, 'rainfall': 850},
            {'name': 'Lilongwe', 'region': 'central', 'lat': -13.97, 'lng': 33.79, 'altitude': 1050, 'rainfall': 900},
            {'name': 'Mchinji', 'region': 'central', 'lat': -13.8, 'lng': 32.9, 'altitude': 1200, 'rainfall': 950},
            {'name': 'Dedza', 'region': 'central', 'lat': -14.4, 'lng': 34.3, 'altitude': 1600, 'rainfall': 1100},
            {'name': 'Ntcheu', 'region': 'central', 'lat': -14.7, 'lng': 34.6, 'altitude': 1100, 'rainfall': 1000},
            
            # Southern Region
            {'name': 'Mangochi', 'region': 'southern', 'lat': -14.5, 'lng': 35.3, 'altitude': 480, 'rainfall': 900},
            {'name': 'Machinga', 'region': 'southern', 'lat': -14.9, 'lng': 35.5, 'altitude': 760, 'rainfall': 1000},
            {'name': 'Zomba', 'region': 'southern', 'lat': -15.4, 'lng': 35.3, 'altitude': 915, 'rainfall': 1200},
            {'name': 'Chiradzulu', 'region': 'southern', 'lat': -15.7, 'lng': 35.1, 'altitude': 800, 'rainfall': 1100},
            {'name': 'Blantyre', 'region': 'southern', 'lat': -15.8, 'lng': 35.0, 'altitude': 1050, 'rainfall': 1200},
            {'name': 'Mwanza', 'region': 'southern', 'lat': -15.6, 'lng': 34.5, 'altitude': 1200, 'rainfall': 1000},
            {'name': 'Thyolo', 'region': 'southern', 'lat': -16.1, 'lng': 35.1, 'altitude': 800, 'rainfall': 1300},
            {'name': 'Chikwawa', 'region': 'southern', 'lat': -16.0, 'lng': 34.8, 'altitude': 100, 'rainfall': 700},
            {'name': 'Nsanje', 'region': 'southern', 'lat': -16.9, 'lng': 35.3, 'altitude': 40, 'rainfall': 600},
            {'name': 'Balaka', 'region': 'southern', 'lat': -14.9, 'lng': 34.9, 'altitude': 350, 'rainfall': 850},
            {'name': 'Neno', 'region': 'southern', 'lat': -15.4, 'lng': 34.6, 'altitude': 1200, 'rainfall': 1000},
            {'name': 'Phalombe', 'region': 'southern', 'lat': -15.8, 'lng': 35.7, 'altitude': 650, 'rainfall': 1100},
        ]
        
        for region_data in regions_data:
            region, created = MalawiRegion.objects.get_or_create(
                name=region_data['name'],
                defaults={
                    'region': region_data['region'],
                    'latitude': region_data['lat'],
                    'longitude': region_data['lng'],
                    'altitude': region_data['altitude'],
                    'annual_rainfall': region_data['rainfall'],
                }
            )
            if created:
                self.stdout.write(f'Created region: {region.name}')
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(regions_data)} regions'))

    def create_crops(self):
        """Create common Malawi crops"""
        crops_data = [
            # Cereals
            {
                'name_en': 'Maize', 'name_ny': 'Chimanga', 'crop_type': 'cereal',
                'scientific_name': 'Zea mays', 'planting_season': 'November-January',
                'harvest_season': 'April-July', 'water_requirement': 'Medium',
                'soil_type': 'Well-drained fertile soils', 'growing_period_days': 120
            },
            {
                'name_en': 'Rice', 'name_ny': 'Mpunga', 'crop_type': 'cereal',
                'scientific_name': 'Oryza sativa', 'planting_season': 'November-February',
                'harvest_season': 'April-August', 'water_requirement': 'High',
                'soil_type': 'Clay soils with good water retention', 'growing_period_days': 120
            },
            {
                'name_en': 'Sorghum', 'name_ny': 'Mapira', 'crop_type': 'cereal',
                'scientific_name': 'Sorghum bicolor', 'planting_season': 'November-January',
                'harvest_season': 'May-July', 'water_requirement': 'Low',
                'soil_type': 'Well-drained sandy loam', 'growing_period_days': 130
            },
            {
                'name_en': 'Millet', 'name_ny': 'Mawere', 'crop_type': 'cereal',
                'scientific_name': 'Pennisetum glaucum', 'planting_season': 'November-January',
                'harvest_season': 'April-June', 'water_requirement': 'Low',
                'soil_type': 'Sandy soils', 'growing_period_days': 90
            },
            
            # Legumes
            {
                'name_en': 'Groundnuts', 'name_ny': 'Mtedza', 'crop_type': 'legume',
                'scientific_name': 'Arachis hypogaea', 'planting_season': 'November-January',
                'harvest_season': 'April-June', 'water_requirement': 'Medium',
                'soil_type': 'Well-drained sandy loam', 'growing_period_days': 120
            },
            {
                'name_en': 'Common Beans', 'name_ny': 'Nyemba', 'crop_type': 'legume',
                'scientific_name': 'Phaseolus vulgaris', 'planting_season': 'November-February',
                'harvest_season': 'March-June', 'water_requirement': 'Medium',
                'soil_type': 'Well-drained fertile soils', 'growing_period_days': 90
            },
            {
                'name_en': 'Cowpeas', 'name_ny': 'Khobwe', 'crop_type': 'legume',
                'scientific_name': 'Vigna unguiculata', 'planting_season': 'November-February',
                'harvest_season': 'March-May', 'water_requirement': 'Low',
                'soil_type': 'Sandy soils', 'growing_period_days': 75
            },
            {
                'name_en': 'Pigeon Peas', 'name_ny': 'Nandolo', 'crop_type': 'legume',
                'scientific_name': 'Cajanus cajan', 'planting_season': 'November-January',
                'harvest_season': 'May-August', 'water_requirement': 'Low',
                'soil_type': 'Well-drained soils', 'growing_period_days': 180
            },
            {
                'name_en': 'Soybeans', 'name_ny': 'Soya', 'crop_type': 'legume',
                'scientific_name': 'Glycine max', 'planting_season': 'November-January',
                'harvest_season': 'April-June', 'water_requirement': 'Medium',
                'soil_type': 'Well-drained fertile soils', 'growing_period_days': 110
            },
            
            # Tubers
            {
                'name_en': 'Sweet Potato', 'name_ny': 'Mbatata', 'crop_type': 'tuber',
                'scientific_name': 'Ipomoea batatas', 'planting_season': 'October-February',
                'harvest_season': 'March-July', 'water_requirement': 'Medium',
                'soil_type': 'Well-drained sandy loam', 'growing_period_days': 120
            },
            {
                'name_en': 'Cassava', 'name_ny': 'Chinangwa', 'crop_type': 'tuber',
                'scientific_name': 'Manihot esculenta', 'planting_season': 'October-February',
                'harvest_season': 'Year-round after 8-12 months', 'water_requirement': 'Low',
                'soil_type': 'Well-drained soils', 'growing_period_days': 300
            },
            {
                'name_en': 'Irish Potato', 'name_ny': 'Mbatata ya Azungu', 'crop_type': 'tuber',
                'scientific_name': 'Solanum tuberosum', 'planting_season': 'April-August',
                'harvest_season': 'July-November', 'water_requirement': 'Medium',
                'soil_type': 'Well-drained fertile soils', 'growing_period_days': 90
            },
            
            # Vegetables
            {
                'name_en': 'Tomato', 'name_ny': 'Phwetekele', 'crop_type': 'vegetable',
                'scientific_name': 'Solanum lycopersicum', 'planting_season': 'Year-round',
                'harvest_season': 'Year-round', 'water_requirement': 'High',
                'soil_type': 'Well-drained fertile soils', 'growing_period_days': 80
            },
            {
                'name_en': 'Onion', 'name_ny': 'Anyezi', 'crop_type': 'vegetable',
                'scientific_name': 'Allium cepa', 'planting_season': 'April-August',
                'harvest_season': 'August-December', 'water_requirement': 'Medium',
                'soil_type': 'Well-drained sandy loam', 'growing_period_days': 120
            },
            {
                'name_en': 'Cabbage', 'name_ny': 'Kabichi', 'crop_type': 'vegetable',
                'scientific_name': 'Brassica oleracea', 'planting_season': 'Year-round',
                'harvest_season': 'Year-round', 'water_requirement': 'High',
                'soil_type': 'Rich, well-drained soils', 'growing_period_days': 90
            },
            
            # Cash Crops
            {
                'name_en': 'Tobacco', 'name_ny': 'Fodya', 'crop_type': 'cash',
                'scientific_name': 'Nicotiana tabacum', 'planting_season': 'September-November',
                'harvest_season': 'March-June', 'water_requirement': 'Medium',
                'soil_type': 'Well-drained fertile soils', 'growing_period_days': 180
            },
            {
                'name_en': 'Cotton', 'name_ny': 'Thonje', 'crop_type': 'cash',
                'scientific_name': 'Gossypium hirsutum', 'planting_season': 'November-January',
                'harvest_season': 'April-July', 'water_requirement': 'Medium',
                'soil_type': 'Well-drained fertile soils', 'growing_period_days': 150
            },
            {
                'name_en': 'Sunflower', 'name_ny': 'Mpendadzuwa', 'crop_type': 'cash',
                'scientific_name': 'Helianthus annuus', 'planting_season': 'November-January',
                'harvest_season': 'April-June', 'water_requirement': 'Medium',
                'soil_type': 'Well-drained soils', 'growing_period_days': 110
            },
        ]
        
        # Get all regions for assigning suitable regions
        all_regions = list(MalawiRegion.objects.all())
        
        for crop_data in crops_data:
            crop, created = Crop.objects.get_or_create(
                name_en=crop_data['name_en'],
                defaults=crop_data
            )
            if created:
                # Assign suitable regions based on crop type and characteristics
                if crop.crop_type == 'cereal' or crop.crop_type == 'legume':
                    # Most cereals and legumes can grow in all regions
                    crop.suitable_regions.set(all_regions)
                elif crop.crop_type == 'tuber':
                    # Tubers prefer certain regions
                    if crop.name_en == 'Irish Potato':
                        # Irish potatoes prefer higher altitudes
                        suitable = [r for r in all_regions if r.altitude and r.altitude > 800]
                    else:
                        suitable = all_regions
                    crop.suitable_regions.set(suitable)
                elif crop.crop_type == 'cash':
                    # Cash crops have specific regional preferences
                    if crop.name_en == 'Tobacco':
                        suitable = [r for r in all_regions if r.region in ['central', 'northern']]
                    else:
                        suitable = all_regions
                    crop.suitable_regions.set(suitable)
                else:
                    # Vegetables can generally grow everywhere
                    crop.suitable_regions.set(all_regions)
                
                self.stdout.write(f'Created crop: {crop.name_en}')
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(crops_data)} crops'))

    def create_farming_calendar(self):
        """Create farming calendar entries"""
        crops = Crop.objects.all()
        regions = MalawiRegion.objects.all()
        
        # Sample farming activities by month for different crops
        calendar_activities = {
            'Maize': {
                10: ('Land preparation', 'Konzani munda'),
                11: ('Planting', 'Kubzala'),
                12: ('First weeding', 'Kuchotsa udzu koyamba'),
                1: ('Second weeding and top dressing', 'Kuchotsa udzu kachiwiri ndi feteleza'),
                2: ('Pest and disease control', 'Kulimbana ndi tizilombo ndi matenda'),
                3: ('Monitoring and care', 'Kuyang\'anira'),
                4: ('Harvesting begins', 'Kuyamba kutcha'),
                5: ('Main harvesting', 'Kutcha kwa kanthawi'),
                6: ('Post-harvest processing', 'Kukonza mbewu'),
                7: ('Storage', 'Kusunga'),
            },
            'Groundnuts': {
                11: ('Land preparation and planting', 'Kukonza munda ndi kubzala'),
                12: ('Weeding and thinning', 'Kuchotsa udzu'),
                1: ('Second weeding', 'Kuchotsa udzu kachiwiri'),
                2: ('Flowering stage care', 'Kusamalira nthawi ya maluwa'),
                3: ('Pod development monitoring', 'Kuyang\'anira kukula kwa nsonga'),
                4: ('Harvesting preparation', 'Kukonzekera kutcha'),
                5: ('Harvesting', 'Kutcha'),
                6: ('Drying and processing', 'Kuuma ndi kukonza'),
            },
            'Sweet Potato': {
                10: ('Land preparation', 'Kukonza munda'),
                11: ('Planting vines', 'Kubzala mitengo'),
                12: ('Weeding', 'Kuchotsa udzu'),
                1: ('Ridge maintenance', 'Kukonza mipanda'),
                2: ('Pest control', 'Kulimbana ndi tizilombo'),
                3: ('Harvesting can begin', 'Kutcha kungayambe'),
                4: ('Main harvesting', 'Kutcha kwa kanthawi'),
                5: ('Continued harvesting', 'Kupitirizabe kutcha'),
                6: ('Final harvest', 'Kutcha komaliza'),
            },
            'Rice': {
                11: ('Nursery preparation', 'Kukonza malo ophukira'),
                12: ('Transplanting', 'Kusamutsa'),
                1: ('Water management', 'Kuyang\'anira madzi'),
                2: ('Weeding and fertilizer application', 'Kuchotsa udzu ndi feteleza'),
                3: ('Flowering stage', 'Nthawi ya maluwa'),
                4: ('Grain filling', 'Kudzaza kwa mbewu'),
                5: ('Harvesting', 'Kutcha'),
                6: ('Processing and storage', 'Kukonza ndi kusunga'),
            }
        }
        
        created_count = 0
        for crop in crops:
            if crop.name_en in calendar_activities:
                activities = calendar_activities[crop.name_en]
                for region in regions:
                    for month, (activity_en, activity_ny) in activities.items():
                        calendar_entry, created = FarmingCalendar.objects.get_or_create(
                            crop=crop,
                            region=region,
                            month=month,
                            defaults={
                                'activity_en': activity_en,
                                'activity_ny': activity_ny,
                                'description_en': f'{activity_en} for {crop.name_en} in {region.name}',
                                'description_ny': f'{activity_ny} wa {crop.name_ny or crop.name_en} ku {region.name}',
                            }
                        )
                        if created:
                            created_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'Created {created_count} farming calendar entries'))

    def create_weather_data(self):
        """Create sample weather data for the last 30 days"""
        regions = MalawiRegion.objects.all()
        created_count = 0
        
        # Create weather data for the last 30 days
        for i in range(30):
            current_date = date.today() - timedelta(days=i)
            current_month = current_date.month
            
            for region in regions:
                # Skip if weather data already exists
                if WeatherData.objects.filter(location=region, date=current_date).exists():
                    continue
                
                # Generate realistic weather based on month and region
                temp_base = self.get_base_temperature(current_month, region)
                rainfall_chance = self.get_rainfall_chance(current_month)
                
                weather_data = WeatherData.objects.create(
                    location=region,
                    date=current_date,
                    temperature_max=temp_base + random.randint(-3, 5),
                    temperature_min=temp_base - random.randint(5, 10),
                    humidity=random.randint(50, 90),
                    rainfall=random.randint(0, 30) if random.random() < rainfall_chance else 0,
                    wind_speed=random.randint(5, 25),
                    weather_condition=self.get_weather_condition(current_month)
                )
                created_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'Created {created_count} weather data entries'))

    def get_base_temperature(self, month, region):
        """Get base temperature based on month and region altitude"""
        base_temps = {
            1: 28, 2: 28, 3: 27, 4: 25, 5: 22, 6: 20,
            7: 20, 8: 23, 9: 26, 10: 29, 11: 30, 12: 29
        }
        base_temp = base_temps[month]
        
        # Adjust for altitude (temperature decreases with altitude)
        if region.altitude:
            altitude_adjustment = (region.altitude - 500) / 300  # Rough adjustment
            base_temp -= altitude_adjustment
        
        return max(15, min(35, int(base_temp)))

    def get_rainfall_chance(self, month):
        """Get rainfall probability based on month"""
        # Malawi rainy season probabilities
        rainfall_chances = {
            1: 0.8, 2: 0.7, 3: 0.6, 4: 0.3, 5: 0.1, 6: 0.05,
            7: 0.05, 8: 0.1, 9: 0.2, 10: 0.4, 11: 0.6, 12: 0.8
        }
        return rainfall_chances.get(month, 0.3)

    def get_weather_condition(self, month):
        """Get weather condition based on month"""
        if month in [5, 6, 7, 8]:  # Dry season
            conditions = ['Sunny', 'Partly Cloudy', 'Clear']
        elif month in [11, 12, 1, 2, 3]:  # Rainy season
            conditions = ['Cloudy', 'Light Rain', 'Heavy Rain', 'Partly Cloudy', 'Thunderstorms']
        else:  # Transition periods
            conditions = ['Partly Cloudy', 'Cloudy', 'Sunny', 'Light Rain']
        
        return random.choice(conditions)