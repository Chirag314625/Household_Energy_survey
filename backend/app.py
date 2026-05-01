# backend/app.py

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from models.air_conditioner import calculate_daily as ac_daily
from models.ceiling_fan import calculate_daily as fan_daily
from models.computer import calculate_daily as computer_daily
from models.kitchen import calculate_daily as kitchen_daily
from models.lighting import calculate_daily as lighting_daily
from models.refrigerator import calculate_daily as fridge_daily
from models.television import calculate_daily as tv_daily
from models.washing_machine import calculate_daily as washer_daily
from models.water_heater import calculate_daily as heater_daily

app = Flask(__name__)
CORS(app)  # This allows your HTML file to talk to Flask

@app.route('/')
def index():
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('../frontend', path)

@app.route('/api/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    tariff = data.get('tariff', 6.5)
    results = []

    # ── Refrigerator ──
    if data.get('fridge'):
        daily = fridge_daily(data['fridge'])
        results.append({'name': 'Refrigerator', 'icon': '🧊', 'daily': round(daily, 4)})

    # ── Air Conditioner ──
    if data.get('ac'):
        daily = ac_daily(data['ac'])
        results.append({'name': 'Air Conditioner', 'icon': '❄️', 'daily': round(daily, 4)})

    # ── Washing Machine ──
    if data.get('washer'):
        daily = washer_daily(data['washer'])
        results.append({'name': 'Washing Machine', 'icon': '🫧', 'daily': round(daily, 4)})

    # ── Ceiling Fan ──
    if data.get('fan'):
        daily = fan_daily(data['fan'])
        results.append({'name': 'Ceiling Fan', 'icon': '💨', 'daily': round(daily, 4)})

    # ── Computer ──
    if data.get('computer'):
        daily = computer_daily(data['computer'])
        results.append({'name': 'Computer & Net', 'icon': '💻', 'daily': round(daily, 4)})

    # ── Kitchen ──
    if data.get('kitchen'):
        daily = kitchen_daily(data['kitchen'])
        results.append({'name': 'Kitchen', 'icon': '🍳', 'daily': round(daily, 4)})

    # ── Lighting ──
    if data.get('lighting'):
        daily = lighting_daily(data['lighting'])
        results.append({'name': 'Lighting', 'icon': '💡', 'daily': round(daily, 4)})

    # ── Television ──
    if data.get('tv'):
        daily = tv_daily(data['tv'])
        results.append({'name': 'Television', 'icon': '📺', 'daily': round(daily, 4)})

    # ── Water Heater ──
    if data.get('heater'):
        daily = heater_daily(data['heater'])
        results.append({'name': 'Water Heater', 'icon': '🚿', 'daily': round(daily, 4)})

    # ── Totals ──
    total_daily   = sum(r['daily'] for r in results)
    total_monthly = total_daily * 30
    total_annual  = total_daily * 365
    monthly_cost  = total_monthly * tariff
    co2           = total_monthly * 0.82  # India grid emission factor

    return jsonify({
        'appliances':     results,
        'total_daily':    round(total_daily, 3),
        'total_monthly':  round(total_monthly, 2),
        'total_annual':   round(total_annual, 2),
        'monthly_cost':   round(monthly_cost, 2),
        'co2_monthly':    round(co2, 2),
        'tariff':         tariff,
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)