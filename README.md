# Residential Energy Consumption Survey

This project is a web-based application designed to collect data on household energy consumption patterns in India through a user-friendly survey. It aims to help researchers understand energy usage trends, appliance ownership, and preferences.

---

## ✨ Features

- **Interactive Survey:** A multi-step questionnaire to gather detailed information on household demographics, home characteristics, appliance ownership, and energy consumption habits.
- **Dynamic Question Loading:** Questions are loaded dynamically, allowing for easy expansion and modification of the survey.
- **Form Validation:** Client-side validation ensures data integrity before submission.
- **Backend API:** An Express.js backend handles survey submissions and stores data securely in MongoDB.
- **Rate Limiting:** Implemented to prevent abuse and protect the server from excessive requests.
- **Google Translate Integration:** Provides multi-language support for the survey interface (English, Hindi, Gujarati, Bengali, Tamil, Telugu, Malayalam, Kannada, Punjabi, Marathi).
- **Responsive Design:** Optimized for various screen sizes, ensuring a consistent experience on desktop and mobile devices.
- **Thank You Page:** Displays a confirmation message upon successful survey submission.
- **Health Check Endpoint:** For monitoring application status in deployment environments.

---

## 🚀 Technologies Used

### Frontend

- HTML5
- CSS3 (with custom variables and animations)
- JavaScript (Vanilla JS)
- Font Awesome (for icons)
- Google Translate API

### Backend

- Node.js
- Express.js (Web Framework)
- Mongoose (MongoDB ODM)
- dotenv (for environment variable management)
- express-rate-limit (for API rate limiting)

### Database

- MongoDB (NoSQL Database)

---

## 📦 Project Structure

```
.
├── .env                  # Environment variables (IGNORED by Git)
├── .gitignore            # Specifies intentionally untracked files to ignore
├── package.json          # Project dependencies and scripts
├── package-lock.json     # Records exact dependency versions
├── server.js             # Backend Express.js server
├── public/
│   ├── home.html         # Landing page for the survey
│   ├── home_script.js    # JavaScript for the landing page (e.g., Google Translate init)
│   ├── index.html        # The main survey form page
│   ├── script.js         # JavaScript for the survey form (question logic, submission)
│   └── styles.css        # Global styles for the survey and landing pages
└── README.md             # This file
```

---

## 🛠️ Setup Instructions

Follow these steps to get the project up and running on your local machine.

### Prerequisites

- Node.js (LTS version recommended)
- MongoDB Atlas account or a local MongoDB instance

### 1. Clone the repository

```bash
git clone https://github.com/Chirag314625/Household_Energy_survey.git
cd Household_Energy_survey
```

### 2. Install Dependencies

Install the necessary Node.js packages for the backend:

```bash
npm install
```

### 3. Configure Environment Variables

Create a `.env` file in the root directory of your project (the same level as `package.json`) and add your MongoDB connection URI:

```
MONGODB_URI="your_mongodb_connection_string_here"
```

Replace `"your_mongodb_connection_string_here"` with your actual MongoDB connection string (e.g., from MongoDB Atlas).

### 4. Run the Server

Start the Node.js server:

```bash
npm start
```

The server will typically run on [http://localhost:3000](http://localhost:3000) (or the port specified in your `server.js`).

---

## 🌐 Usage

Once the server is running:

1. Open your web browser and navigate to `http://localhost:3000/home.html` to access the landing page.
2. Click **"Start Survey Now"** to proceed to the survey form.
3. Fill out the survey questions and click **"Submit."**
4. Your responses will be saved to your MongoDB database.

---

# Household Energy Survey Data Analysis

This script (`Survey1.py`) processes household energy survey data from a CSV file, estimates electricity and total energy consumption, and visualizes energy breakdowns and trends by home characteristics.

---

## Features

- **Reads CSV Data**: Loads household survey responses.
- **Estimates Appliance Electricity Use**: Calculates annual kWh for typical appliances.
- **Scales to Reported Bills**: Adjusts estimates using reported electricity bills for accuracy.
- **Fuel-Based BTU Estimates**: Converts fuel use (gas, LPG, oil, wood) to BTU.
- **Combined Energy Breakdown**: Pie charts for electricity by appliance and total energy by source.
- **Trends by Home Age**: Bar/line chart compares energy use and home size by year built.


---

## Prerequisites

Install required libraries:

```sh
pip install pandas numpy matplotlib
```

---

## How to Use

1. **Prepare Data**: Ensure your CSV file uses the required column names (see below).
2. **Configure Script**: Save as `Survey1.py` and place your CSV file (e.g., `realistic_dummy_forms.csv`) in the same folder. Edit the filename in the script if needed.
3. **Run**:  
   ```sh
   python Survey1.py
   ```
   The script prints summary info and displays plots.

---

## Input CSV File Format

The script expects columns matching survey questions, such as:

- `Q0_name`, `Q1_City`, `Q2_num_adults`, `Q7_sq_ft_home`, `Q9_num_refrigerators`, `Q62_last_electricity_consumption`, etc.

**Tip:** See the script or the full documentation above for a detailed list of expected columns.

---

## How It Works (Brief)

- Loads and cleans the data.
- Estimates appliance electricity use and scales to match reported bill data.
- Converts fuel use to BTU and sums with electricity.
- Aggregates results for all households.
- Plots:
  - Pie charts: Appliance-wise and fuel-wise energy shares.
  - Bar/line chart: Energy and home size by year built.
- Handles missing or invalid data gracefully.

---

## Visualization

- **Pie Charts:**  
  - Appliance electricity breakdown  
  - Total energy by fuel type
- **Bar/Line Chart:**  
  - Avg. square footage (bars) and energy use (line) by year built/moved-in

---

## Notes

- The script is intended for survey data analysis and visualization.
- Ensure your CSV columns match the expected names for correct operation.

---

## 🤝 Contributing

Contributions are welcome! If you have suggestions for improvements or find any issues, please feel free to:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature-name`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add new feature'`).
5. Push to the branch (`git push origin feature/your-feature-name`).
6. Open a Pull Request.

---
