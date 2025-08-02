# Malawi Crop Advisory System

A comprehensive Django-based web application that provides AI-powered farming advice to Malawian farmers. The system offers personalized crop recommendations, weather-based advice, farming calendars, and market price information in both English and Chichewa languages.

## 🌟 Features

### Core Functionality
- **AI-Powered Advice**: Intelligent farming recommendations based on crops, location, and weather conditions
- **Bilingual Support**: Full support for English and Chichewa languages
- **Location-Based Services**: Specific advice for all 28 districts of Malawi
- **Weather Integration**: Real-time weather data integration for informed farming decisions
- **Farming Calendar**: Seasonal activities and recommendations for different crops
- **Market Prices**: Current market price information for various crops

### User Features
- **Farmer Registration & Profiles**: Complete farmer profile management
- **Personalized Dashboard**: Customized dashboard with relevant information
- **Crop Management**: Track and get advice for multiple crops
- **Advice History**: Access to previously received farming advice
- **Mobile-Responsive Design**: Optimized for smartphones and tablets

### Administrative Features
- **Django Admin Interface**: Comprehensive admin panel for data management
- **Weather Data Management**: Tools for managing weather information
- **Crop Database**: Extensive database of Malawian crops with growing information
- **User Management**: Farmer profile and user account management

## 🗺️ Coverage

### Regions Covered
- **Northern Region**: Chitipa, Karonga, Nkhata Bay, Rumphi, Mzimba, Likoma
- **Central Region**: Kasungu, Nkhotakota, Ntchisi, Dowa, Salima, Lilongwe, Mchinji, Dedza, Ntcheu
- **Southern Region**: Mangochi, Machinga, Zomba, Chiradzulu, Blantyre, Mwanza, Thyolo, Chikwawa, Nsanje, Balaka, Neno, Phalombe

### Crops Supported
#### Cereals
- Maize (Chimanga)
- Rice (Mpunga)
- Sorghum (Mapira)
- Millet (Mawere)

#### Legumes
- Groundnuts (Mtedza)
- Common Beans (Nyemba)
- Cowpeas (Khobwe)
- Pigeon Peas (Nandolo)
- Soybeans (Soya)

#### Tubers
- Sweet Potato (Mbatata)
- Cassava (Chinangwa)
- Irish Potato (Mbatata ya Azungu)

#### Vegetables
- Tomato (Phwetekele)
- Onion (Anyezi)
- Cabbage (Kabichi)

#### Cash Crops
- Tobacco (Fodya)
- Cotton (Thonje)
- Sunflower (Mpendadzuwa)

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- Django 4.2+
- SQLite (included with Python)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd crop_advisor
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

4. **Populate sample data**
   ```bash
   python manage.py populate_data
   ```

5. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Main application: http://localhost:8000
   - Admin interface: http://localhost:8000/admin

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root (optional):
```
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///db.sqlite3
```

### Language Configuration
The application supports two languages:
- English (en) - Default
- Chichewa (ny)

Language switching is available through the navigation menu.

## 📱 Usage

### For Farmers

1. **Registration**
   - Visit the registration page
   - Create an account with username and password
   - Complete your farmer profile with location and crops
   - Select your preferred language

2. **Getting Advice**
   - Log in to your dashboard
   - Navigate to "Get Advice" 
   - Select a crop and advice type
   - Receive personalized recommendations

3. **Dashboard Features**
   - View recent advice
   - Check current weather for your location
   - See farming calendar activities
   - Monitor market prices for your crops

### For Administrators

1. **Access Admin Panel**
   - Navigate to `/admin`
   - Log in with superuser credentials

2. **Manage Data**
   - Add/edit crops and their information
   - Manage farmer profiles
   - Update weather data
   - Monitor advice generation

## 🛠️ Technical Architecture

### Backend
- **Framework**: Django 4.2
- **Database**: SQLite (development), PostgreSQL (production ready)
- **API**: Django REST Framework
- **Authentication**: Django built-in authentication

### Frontend
- **CSS Framework**: Bootstrap 5
- **Icons**: Font Awesome
- **Charts**: Chart.js
- **JavaScript**: Vanilla ES6+

### Key Components
- **Models**: Comprehensive data models for crops, regions, weather, and advice
- **Views**: Function-based views for handling requests
- **Services**: Advisory and weather services for business logic
- **Forms**: Django forms with crispy-forms for better UX
- **Admin**: Customized Django admin interface

## 🌍 Internationalization

The application supports bilingual functionality:
- All user-facing text is translatable
- Crop names available in both English and Chichewa
- Advice generated in the user's preferred language
- Dynamic language switching

## 📊 Data Models

### Core Models
- **MalawiRegion**: Districts and regional information
- **Crop**: Crop varieties with growing information
- **Farmer**: User profiles with farming details
- **WeatherData**: Weather information by location
- **CropAdvice**: AI-generated farming advice
- **FarmingCalendar**: Seasonal farming activities
- **MarketPrice**: Crop market price information

## 🔮 AI Advisory System

The advisory system provides intelligent recommendations based on:
- Farmer's location and crops
- Current weather conditions
- Seasonal farming calendar
- Crop-specific requirements
- Historical data patterns

### Advice Types
- **Planting Advice**: When and how to plant
- **Care & Maintenance**: Ongoing crop care
- **Disease Management**: Prevention and treatment
- **Harvest Advice**: Optimal harvest timing
- **Weather-based Advice**: Weather-specific recommendations
- **General Advice**: Best practices and tips

## 🚀 Deployment

### Production Deployment
1. Set DEBUG=False in settings
2. Configure proper database (PostgreSQL recommended)
3. Set up static file serving
4. Configure environment variables
5. Set up SSL/HTTPS
6. Configure proper domain settings

### Docker Deployment
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "crop_advisor.wsgi:application"]
```

## 📝 API Endpoints

- `/api/weather/<region_id>/` - Weather data for a region
- `/api/prices/<crop_id>/` - Market prices for a crop
- `/set-language/` - Language switching
- `/admin/` - Administrative interface

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is developed for educational and agricultural support purposes in Malawi.

## 🆘 Support

For support and questions:
- Check the Django documentation
- Review the code comments
- Contact the development team

## 🔄 Future Enhancements

- Real-time weather API integration
- SMS notification system
- Mobile app development
- Advanced AI/ML models
- Farmer community features
- Market integration
- Offline functionality

---

**Built with ❤️ for Malawian farmers**
