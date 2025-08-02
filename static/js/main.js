// Malawi Crop Advisory - Main JavaScript Functions

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initializeLanguageSwitcher();
    initializeWeatherCharts();
    initializePriceCharts();
    initializeFormValidation();
    initializeTooltips();
    initializeAlerts();
    
    // Smooth scrolling for anchor links
    initializeSmoothScrolling();
});

// Language Switcher
function initializeLanguageSwitcher() {
    const languageLinks = document.querySelectorAll('[href*="set-language"]');
    languageLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const language = new URL(this.href).searchParams.get('language');
            
            // Store language preference
            localStorage.setItem('preferred_language', language);
            
            // Redirect to language setter
            window.location.href = this.href;
        });
    });
}

// Weather Charts
function initializeWeatherCharts() {
    const weatherChartElements = document.querySelectorAll('.weather-chart');
    
    weatherChartElements.forEach(element => {
        const regionId = element.dataset.regionId;
        if (regionId) {
            fetchWeatherData(regionId).then(data => {
                createWeatherChart(element, data);
            });
        }
    });
}

// Fetch weather data from API
async function fetchWeatherData(regionId) {
    try {
        const response = await fetch(`/api/weather/${regionId}/`);
        const data = await response.json();
        return data.weather_data;
    } catch (error) {
        console.error('Error fetching weather data:', error);
        return [];
    }
}

// Create weather chart
function createWeatherChart(element, weatherData) {
    const ctx = element.getContext('2d');
    
    const dates = weatherData.map(item => new Date(item.date).toLocaleDateString());
    const maxTemps = weatherData.map(item => item.temp_max);
    const minTemps = weatherData.map(item => item.temp_min);
    const rainfall = weatherData.map(item => item.rainfall);
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: dates,
            datasets: [{
                label: 'Max Temperature (°C)',
                data: maxTemps,
                borderColor: '#ff6384',
                backgroundColor: 'rgba(255, 99, 132, 0.1)',
                tension: 0.4
            }, {
                label: 'Min Temperature (°C)',
                data: minTemps,
                borderColor: '#36a2eb',
                backgroundColor: 'rgba(54, 162, 235, 0.1)',
                tension: 0.4
            }, {
                label: 'Rainfall (mm)',
                data: rainfall,
                type: 'bar',
                backgroundColor: 'rgba(75, 192, 192, 0.6)',
                yAxisID: 'y1'
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    title: {
                        display: true,
                        text: 'Temperature (°C)'
                    }
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    title: {
                        display: true,
                        text: 'Rainfall (mm)'
                    },
                    grid: {
                        drawOnChartArea: false,
                    },
                }
            },
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Weather Trends'
                }
            }
        }
    });
}

// Price Charts
function initializePriceCharts() {
    const priceChartElements = document.querySelectorAll('.price-chart');
    
    priceChartElements.forEach(element => {
        const cropId = element.dataset.cropId;
        if (cropId) {
            fetchPriceData(cropId).then(data => {
                createPriceChart(element, data);
            });
        }
    });
}

// Fetch price data from API
async function fetchPriceData(cropId) {
    try {
        const response = await fetch(`/api/prices/${cropId}/`);
        const data = await response.json();
        return data.price_data;
    } catch (error) {
        console.error('Error fetching price data:', error);
        return [];
    }
}

// Create price chart
function createPriceChart(element, priceData) {
    const ctx = element.getContext('2d');
    
    const dates = priceData.map(item => new Date(item.date).toLocaleDateString());
    const prices = priceData.map(item => item.price);
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: dates,
            datasets: [{
                label: 'Price (MWK/kg)',
                data: prices,
                borderColor: '#28a745',
                backgroundColor: 'rgba(40, 167, 69, 0.1)',
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Price (MWK/kg)'
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: 'Market Price Trends'
                }
            }
        }
    });
}

// Form Validation
function initializeFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(this)) {
                e.preventDefault();
                showAlert('Please fill in all required fields correctly.', 'danger');
            }
        });
        
        // Real-time validation
        const inputs = form.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                validateField(this);
            });
        });
    });
}

// Validate individual field
function validateField(field) {
    const value = field.value.trim();
    const isRequired = field.hasAttribute('required');
    const fieldType = field.type;
    
    // Remove existing error styling
    field.classList.remove('is-invalid', 'is-valid');
    
    if (isRequired && !value) {
        field.classList.add('is-invalid');
        return false;
    }
    
    // Type-specific validation
    if (fieldType === 'email' && value && !isValidEmail(value)) {
        field.classList.add('is-invalid');
        return false;
    }
    
    if (fieldType === 'tel' && value && !isValidPhone(value)) {
        field.classList.add('is-invalid');
        return false;
    }
    
    if (value) {
        field.classList.add('is-valid');
    }
    
    return true;
}

// Validate entire form
function validateForm(form) {
    const fields = form.querySelectorAll('input, select, textarea');
    let isValid = true;
    
    fields.forEach(field => {
        if (!validateField(field)) {
            isValid = false;
        }
    });
    
    return isValid;
}

// Email validation
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Phone validation (Malawi format)
function isValidPhone(phone) {
    const phoneRegex = /^(\+265|0)(1|9|8|7)\d{7}$/;
    return phoneRegex.test(phone.replace(/\s/g, ''));
}

// Initialize tooltips
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Alert system
function initializeAlerts() {
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        if (alert.classList.contains('alert-success') || alert.classList.contains('alert-info')) {
            setTimeout(() => {
                alert.style.transition = 'opacity 0.5s';
                alert.style.opacity = '0';
                setTimeout(() => {
                    alert.remove();
                }, 500);
            }, 5000);
        }
    });
}

// Show custom alert
function showAlert(message, type = 'info') {
    const alertContainer = document.querySelector('.container');
    const alertElement = document.createElement('div');
    alertElement.className = `alert alert-${type} alert-dismissible fade show mt-3`;
    alertElement.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    alertContainer.insertBefore(alertElement, alertContainer.firstChild);
    
    // Auto-dismiss
    setTimeout(() => {
        alertElement.remove();
    }, 5000);
}

// Smooth scrolling
function initializeSmoothScrolling() {
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Loading spinner
function showSpinner(element) {
    element.innerHTML = `
        <div class="d-flex justify-content-center">
            <div class="spinner-border spinner-border-custom" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>
    `;
}

// Hide spinner
function hideSpinner(element, content) {
    element.innerHTML = content;
}

// Format date for display
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-GB', {
        day: '2-digit',
        month: 'short',
        year: 'numeric'
    });
}

// Format currency (Malawi Kwacha)
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-MW', {
        style: 'currency',
        currency: 'MWK'
    }).format(amount);
}

// Debounce function for search inputs
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Search functionality
function initializeSearch() {
    const searchInputs = document.querySelectorAll('.search-input');
    
    searchInputs.forEach(input => {
        const debouncedSearch = debounce((value) => {
            performSearch(value, input.dataset.searchType);
        }, 300);
        
        input.addEventListener('input', function() {
            debouncedSearch(this.value);
        });
    });
}

// Perform search
async function performSearch(query, searchType) {
    if (query.length < 2) return;
    
    try {
        const response = await fetch(`/api/search/?q=${encodeURIComponent(query)}&type=${searchType}`);
        const results = await response.json();
        displaySearchResults(results, searchType);
    } catch (error) {
        console.error('Search error:', error);
    }
}

// Display search results
function displaySearchResults(results, searchType) {
    const resultsContainer = document.querySelector(`.search-results-${searchType}`);
    if (!resultsContainer) return;
    
    if (results.length === 0) {
        resultsContainer.innerHTML = '<p class="text-muted">No results found.</p>';
        return;
    }
    
    const resultsHTML = results.map(result => `
        <div class="search-result-item">
            <a href="${result.url}" class="text-decoration-none">
                <strong>${result.title}</strong>
                <p class="text-muted small">${result.description}</p>
            </a>
        </div>
    `).join('');
    
    resultsContainer.innerHTML = resultsHTML;
}

// Weather condition icons
function getWeatherIcon(condition) {
    const iconMap = {
        'Sunny': 'fas fa-sun',
        'Clear': 'fas fa-sun',
        'Partly Cloudy': 'fas fa-cloud-sun',
        'Cloudy': 'fas fa-cloud',
        'Light Rain': 'fas fa-cloud-rain',
        'Heavy Rain': 'fas fa-cloud-showers-heavy',
        'Thunderstorms': 'fas fa-bolt'
    };
    
    return iconMap[condition] || 'fas fa-cloud';
}

// Crop type icons
function getCropIcon(cropType) {
    const iconMap = {
        'cereal': 'fas fa-seedling',
        'legume': 'fas fa-leaf',
        'tuber': 'fas fa-carrot',
        'vegetable': 'fas fa-pepper-hot',
        'fruit': 'fas fa-apple-alt',
        'cash': 'fas fa-coins'
    };
    
    return iconMap[cropType] || 'fas fa-seedling';
}

// Mobile menu toggle
function initializeMobileMenu() {
    const navbarToggle = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    if (navbarToggle && navbarCollapse) {
        navbarToggle.addEventListener('click', function() {
            navbarCollapse.classList.toggle('show');
        });
        
        // Close menu when clicking outside
        document.addEventListener('click', function(e) {
            if (!navbarToggle.contains(e.target) && !navbarCollapse.contains(e.target)) {
                navbarCollapse.classList.remove('show');
            }
        });
    }
}

// Initialize components that need to be loaded after page content
function initializeDynamicComponents() {
    initializeSearch();
    initializeMobileMenu();
    
    // Lazy load images
    const images = document.querySelectorAll('img[data-src]');
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        images.forEach(img => imageObserver.observe(img));
    }
}

// Call dynamic components initialization
document.addEventListener('DOMContentLoaded', initializeDynamicComponents);

// Service Worker for offline functionality
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        navigator.serviceWorker.register('/sw.js')
            .then(function(registration) {
                console.log('SW registered: ', registration);
            })
            .catch(function(registrationError) {
                console.log('SW registration failed: ', registrationError);
            });
    });
}

// Export functions for external use
window.CropAdvisory = {
    showAlert,
    formatDate,
    formatCurrency,
    getWeatherIcon,
    getCropIcon,
    showSpinner,
    hideSpinner
};