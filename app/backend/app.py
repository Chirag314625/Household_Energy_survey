"""
Flask Backend for Household Energy Survey
Handles web server, API endpoints, and MongoDB integration
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime
from pathlib import Path

# Import the proper energy models
from models.refrigerator import Refrigerator
from models.air_conditioner import AirConditioner
from models.washing_machine import Washing_Machine
from models.ceiling_fan import CeilingFan
from models.computer import ComputingLoad, ConnectivityLoad
from models.kitchen import KitchenAppliances
from models.lighting import LightingSystem
from models.television import Television
from models.water_heater import WaterHeater

BASE_DIR = Path(__file__).resolve().parents[2]

# Load environment variables from the project root, no matter where Flask is started.
load_dotenv(BASE_DIR / '.env')

app = Flask(__name__,
    static_folder='../frontend',
    static_url_path='',
    template_folder='../frontend/pages'
)

CORS(app)

# MongoDB Connection
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/household_energy')
if os.getenv('DISABLE_MONGODB') == '1':
    db = None
    surveys_collection = None
    print("MongoDB disabled by environment.")
else:
    try:
        client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        db = client['household_energy']
        surveys_collection = db['surveys']
        print("MongoDB connected successfully.")
    except Exception as e:
        print(f"MongoDB connection error: {e}")
        db = None
        surveys_collection = None

# ==================== ENERGY CALCULATION MODELS ====================

def calculate_refrigerator(data):
    """Refrigerator daily kWh based on wattage, duty cycle, and quantity."""
    watts = float(data.get('watts', 150))
    duty = float(data.get('duty', 0.65))
    qty = float(data.get('qty', 1))
    return (watts * 24 * duty * qty) / 1000

def calculate_air_conditioner(data):
    """Air conditioner daily kWh adjusted by EER/profile factor."""
    watts = float(data.get('watts', 1500))
    eer = max(float(data.get('eer', 2.8)), 0.1)
    star_factor = float(data.get('star_factor', 1))
    hours = float(data.get('hours', 8))
    qty = float(data.get('qty', 1))
    return (watts / eer * star_factor * hours * qty) / 1000

def calculate_washing_machine(data):
    """Washing machine daily kWh from wattage, cycle duration, and cycles."""
    watts = float(data.get('watts', 500))
    duration = float(data.get('duration', 45))
    cycles = float(data.get('cycles', 1))
    temp_factor = float(data.get('temp_factor', 1))
    return (watts * (duration / 60) * cycles * temp_factor) / 1000

def calculate_ceiling_fan(data):
    """Ceiling fan daily kWh from wattage, quantity, hours, and speed factor."""
    watts = float(data.get('watts', 75))
    qty = float(data.get('qty', 1))
    hours = float(data.get('hours', 10))
    speed = float(data.get('speed', 1))
    return (watts * qty * hours * speed) / 1000

def calculate_computer(data):
    """Computer plus always-on router daily kWh."""
    watts = float(data.get('watts', 200))
    monitor = float(data.get('monitor', 50))
    hours = float(data.get('hours', 8))
    router = float(data.get('router', 20))
    return ((watts + monitor) * hours + router * 24) / 1000

def calculate_kitchen(data):
    """Kitchen daily kWh from microwave minutes and induction hours."""
    micro_watts = float(data.get('micro_watts', 1000))
    micro_mins = float(data.get('micro_mins', 15))
    induction_watts = float(data.get('induction_watts', 2000))
    induction_hours = float(data.get('induction_hours', 1.5))
    return (micro_watts * (micro_mins / 60) + induction_watts * induction_hours) / 1000

def calculate_lighting(data):
    """Lighting daily kWh from bulb wattage, quantity, and usage hours."""
    watts = float(data.get('watts', 15))
    qty = float(data.get('qty', 10))
    hours = float(data.get('hours', 5))
    return (watts * qty * hours) / 1000

def calculate_television(data):
    """Television daily kWh from wattage, quantity, and hours."""
    watts = float(data.get('watts', 70))
    qty = float(data.get('qty', 1))
    hours = float(data.get('hours', 4))
    return (watts * qty * hours) / 1000

def calculate_water_heater(data):
    """Water heater daily kWh from hot-water volume and temperature rise."""
    liters = float(data.get('liters', 50))
    uses = float(data.get('uses', 2))
    target_temp = float(data.get('target_temp', 55))
    inlet_temp = float(data.get('inlet_temp', 25))
    efficiency = max(float(data.get('efficiency', 85)) / 100, 0.1)
    temp_rise = max(target_temp - inlet_temp, 0)
    return (liters * uses * 4.186 * temp_rise) / (3600 * efficiency)

# ==================== ROUTES ====================

# Serve HTML pages - Main routes
@app.route('/')
def home():
    return send_from_directory('../frontend/pages', 'home.html')

@app.route('/index.html')
@app.route('/survey')
@app.route('/survey.html')
def survey():
    return send_from_directory('../frontend/pages', 'index.html')

@app.route('/analyzer.html')
@app.route('/analyzer')
@app.route('/calculator')
@app.route('/calculator.html')
def analyzer():
    return send_from_directory('../frontend/pages', 'analyzer.html')

@app.route('/thankyou.html')
@app.route('/thankyou')
@app.route('/thanks')
@app.route('/complete')
@app.route('/complete.html')
def thankyou():
    return send_from_directory('../frontend/pages', 'thankyou.html')

# Catch-all route for any missing HTML files
@app.route('/<path:filename>')
def catch_all(filename):
    # If it's an HTML file, try to serve it from pages directory
    if filename.endswith('.html'):
        try:
            return send_from_directory('../frontend/pages', filename)
        except FileNotFoundError:
            return f"Page '{filename}' not found", 404

    # If it's a CSS, JS, or other static file, serve from frontend directory
    try:
        return send_from_directory('../frontend', filename)
    except FileNotFoundError:
        return f"File '{filename}' not found", 404

# Health check with navigation info
@app.route('/health')
def health():
    return {
        'status': 'OK',
        'server': 'Flask',
        'port': 5000,
        'routes': {
            'home': '/',
            'survey': '/index.html (or /survey)',
            'analyzer': '/analyzer.html (or /analyzer)',
            'thankyou': '/thankyou.html (or /thankyou)',
            'api_calculate': '/api/calculate (POST)',
            'api_submit': '/api/submit-survey (POST)'
        },
        'mongodb': 'connected' if db is not None else 'disconnected'
    }, 200

# ==================== API ENDPOINTS ====================

@app.route('/api/calculate', methods=['POST'])
def calculate():
    """
    Calculate household energy consumption
    POST data with appliance parameters
    """
    try:
        data = request.get_json(silent=True)
        tariff = data.get('tariff', 6.5)
        results = []

        # Calculate each appliance
        appliances = [
            ('fridge', 'Refrigerator', '', calculate_refrigerator),
            ('ac', 'Air Conditioner', '', calculate_air_conditioner),
            ('washer', 'Washing Machine', '', calculate_washing_machine),
            ('fan', 'Ceiling Fan', '', calculate_ceiling_fan),
            ('computer', 'Computer & Net', '', calculate_computer),
            ('kitchen', 'Kitchen', '', calculate_kitchen),
            ('lighting', 'Lighting', '', calculate_lighting),
            ('tv', 'Television', '', calculate_television),
            ('heater', 'Water Heater', '', calculate_water_heater),
        ]

        for key, name, icon, calc_func in appliances:
            if data.get(key):
                daily = calc_func(data[key])
                results.append({
                    'name': name,
                    'icon': icon,
                    'daily': round(daily, 4)
                })

        # Calculate totals
        total_daily = sum(r['daily'] for r in results)
        total_monthly = total_daily * 30
        total_annual = total_daily * 365
        monthly_cost = total_monthly * tariff
        co2_monthly = total_monthly * 0.82  # India grid emission factor

        return jsonify({
            'appliances': results,
            'total_daily': round(total_daily, 3),
            'total_monthly': round(total_monthly, 2),
            'total_annual': round(total_annual, 2),
            'monthly_cost': round(monthly_cost, 2),
            'co2_monthly': round(co2_monthly, 2),
            'tariff': tariff
        })

    except Exception as e:
        print(f"Error in energy calculation: {e}")
        return jsonify({'error': str(e)}), 400

@app.route('/api/submit-survey', methods=['POST'])
def submit_survey():
    """Save survey form data to MongoDB"""
    try:
        data = request.get_json(silent=True)
        
        if not data:
            return jsonify({'error': 'No form data provided'}), 400

        # Add timestamp
        data['submitted_at'] = datetime.now()

        if db is not None:
            result = surveys_collection.insert_one(data)
            print(f"Survey saved to MongoDB: {result.inserted_id}")
            return jsonify({
                'message': 'Survey submitted successfully!',
                'id': str(result.inserted_id)
            }), 200
        else:
            print("MongoDB not available, but form received")
            return jsonify({'message': 'Survey received (DB offline)'}), 200

    except Exception as e:
        print(f"Error saving survey: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/surveys', methods=['GET'])
def get_surveys():
    """Retrieve all surveys (optional - for admin dashboard)"""
    try:
        if db is None:
            return jsonify({'error': 'Database not connected'}), 500

        surveys = list(surveys_collection.find({}, {'_id': 1, 'submitted_at': 1}))
        for survey in surveys:
            survey['_id'] = str(survey['_id'])
            if 'submitted_at' in survey:
                survey['submitted_at'] = survey['submitted_at'].isoformat()
        
        return jsonify({
            'total': len(surveys),
            'surveys': surveys
        }), 200

    except Exception as e:
        print(f"Error retrieving surveys: {e}")
        return jsonify({'error': str(e)}), 500

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Page not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Server error'}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('NODE_ENV', 'development') == 'development'
    
    print(f"Starting Flask server on port {port}...")
    print(f"Open http://localhost:{port} in your browser")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
