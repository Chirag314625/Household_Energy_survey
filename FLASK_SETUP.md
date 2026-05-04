# Household Energy Survey - Setup & Run Guide (Flask)

## Prerequisites
- Python 3.8+ - [Download](https://www.python.org)
- MongoDB (local or cloud account) - [Download](https://www.mongodb.com/try/download/community)

## Installation

### 1. Install Python Dependencies
```bash
cd app/backend
pip install -r requirements.txt
```

This installs:
- Flask (web server)
- Flask-CORS (cross-origin requests)
- PyMongo (MongoDB driver)
- python-dotenv (environment variables)

### 2. Create `.env` File
In the project root directory, create a file named `.env`:

**For Local MongoDB:**
```
MONGODB_URI=mongodb://localhost:27017/household_energy
NODE_ENV=development
PORT=5000
```

**For MongoDB Atlas (Cloud):**
```
MONGODB_URI=mongodb+srv://username:password@your-cluster.mongodb.net/household_energy
NODE_ENV=development
PORT=5000
```

## Running the Application

### Start the Flask Server
```bash
python app/backend/app.py
```

You should see:
```
🚀 Starting Flask server on port 5000...
📊 Open http://localhost:5000 in your browser
✅ MongoDB connected successfully!
```

### Open in Browser
Go to: **http://localhost:5000**

You'll see the Home page with navigation to:
- 🏠 Home
- 📋 Survey
- ⚡ Analyzer  
- ✅ Thank You

## Project Structure

```
household_energy/
├── public/                    # Website pages (HTML, CSS, JS)
│   ├── home.html             # Landing page
│   ├── index.html            # Survey form
│   ├── analyzer.html         # Energy analyzer dashboard
│   ├── thankyou.html         # Thank you page
│   ├── script_analyzer.js    # Calls Flask API
│   ├── navigation.css        # Navigation styles
│   └── navigation.js         # Navigation logic
├── backend/
│   ├── app.py                # Flask application (main file)
│   └── requirements.txt       # Python dependencies
└── .env                       # Environment variables (create this)
```

## Available Pages

1. **Home** (http://localhost:5000/)
   - Landing page with survey introduction

2. **Survey** (http://localhost:5000/index.html)
   - Energy consumption survey form
   - Data saves to MongoDB

3. **Analyzer** (http://localhost:5000/analyzer.html)
   - Energy usage analysis dashboard
   - Real-time calculations

4. **Thank You** (http://localhost:5000/thankyou.html)
   - Completion message

## Features

✅ **All Appliances Calculated:**
- Refrigerator (duty cycle model)
- Air Conditioner (EER efficiency model)
- Washing Machine (thermal model)
- Ceiling Fan (speed-based model)
- Computer & Network (system + router)
- Kitchen Appliances (microwave + induction)
- Lighting (bulb type & quantity)
- Television (screen size model)
- Water Heater (thermodynamic calculation)

✅ **Analysis:**
- Daily/Monthly/Annual consumption
- Monthly cost (based on tariff)
- CO2 emissions (India grid factor)
- Energy distribution charts (doughnut, bar, line)
- Detailed appliance breakdown

✅ **Data Storage:**
- Survey responses stored in MongoDB
- Timestamp tracking
- API to retrieve all surveys

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "ModuleNotFoundError: No module named 'flask'" | Run `pip install -r backend/requirements.txt` from project root |
| "MongoDB connection error" | Create `.env` file with correct MongoDB URI and ensure MongoDB is running |
| "Address already in use" | Change PORT in `.env` to 5001, 5002, etc. |
| "CORS error" | Flask-CORS is configured in app.py, should work |
| "Cannot find module app.py" | Make sure you're in the project root directory |
| "ImportError: No module named 'dotenv'" | Run `pip install python-dotenv` |

## Development Tips

- **Auto-reload:** Flask automatically reloads when you change code (debug=True)
- **API Testing:** POST to http://localhost:5000/api/calculate with appliance data
- **Database:** Check MongoDB collections for survey responses
- **Energy Calculator:** Verify calculations on /analyzer.html page
- **View logs:** Check console output for debug information

## API Endpoints

### POST /api/calculate
Calculate energy consumption for appliances

**Request:**
```json
{
  "fridge": {
    "watts": 150,
    "duty": 0.65,
    "qty": 1
  },
  "ac": {
    "watts": 1500,
    "eer": 2.8,
    "star_factor": 0.7,
    "hours": 8,
    "qty": 1
  },
  "tariff": 7
}
```

**Response:**
```json
{
  "appliances": [
    {"name": "Refrigerator", "icon": "🧊", "daily": 3.6},
    {"name": "Air Conditioner", "icon": "❄️", "daily": 4.3}
  ],
  "total_daily": 15.2,
  "total_monthly": 456,
  "total_annual": 5547.8,
  "monthly_cost": 3192,
  "co2_monthly": 373.92,
  "tariff": 7
}
```

### POST /api/submit-survey
Submit survey form data to MongoDB

**Request:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "household_members": 4,
  "appliances": {...}
}
```

**Response:**
```json
{
  "message": "Survey submitted successfully!",
  "id": "507f1f77bcf86cd799439011"
}
```

### GET /api/surveys
Retrieve all submitted surveys

**Response:**
```json
{
  "total": 5,
  "surveys": [
    {"_id": "507f1f77bcf86cd799439011", "submitted_at": "2026-05-02T10:30:00"}
  ]
}
```

### GET /health
Health check endpoint

## Quick Start Checklist

- [ ] Install Python 3.8+
- [ ] Run `pip install -r app/backend/requirements.txt`
- [ ] Create `.env` file with MongoDB URI
- [ ] Run `python app/backend/app.py`
- [ ] Open http://localhost:5000
- [ ] Test Energy Analyzer with sample data
- [ ] Submit a survey
- [ ] Check MongoDB for stored data

---

**Everything ready!** Flask server is perfect for this project. 🚀
