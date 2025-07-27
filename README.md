Residential Energy Consumption Survey
This project is a web-based application designed to collect data on household energy consumption patterns in India through a user-friendly survey. It aims to help researchers understand energy usage trends, appliance ownership, and preferences.

✨ Features
Interactive Survey: A multi-step questionnaire to gather detailed information on household demographics, home characteristics, appliance ownership, and energy consumption habits.
Dynamic Question Loading: Questions are loaded dynamically, allowing for easy expansion and modification of the survey.
Form Validation: Client-side validation ensures data integrity before submission.
Backend API: An Express.js backend to handle survey submissions and store data securely in MongoD
Rate Limiting: Implemented to prevent abuse and protect the server from excessive requests.
Google Translate Integration: Provides multi-language support for the survey interface (English, Hindi, Gujarati, Bengali, Tamil, Telugu, Malayalam, Kannada, Punjabi, Marathi).
Responsive Design: Optimized for various screen sizes, ensuring a consistent experience on desktop and mobile devices.
Thank You Page: Displays a confirmation message upon successful survey submission.
Health Check Endpoint: For monitoring application status in deployment environments.

🚀 Technologies Used
Frontend:
HTML5
CSS3 (with custom variables and animations)
JavaScript (Vanilla JS)
Font Awesome (for icons)
Google Translate API

Backend:
Node.js
Express.js (Web Framework)
Mongoose (MongoDB ODM)
CORS (Middleware for cross-origin requests)
dotenv (for environment variable management)
express-rate-limit (for API rate limiting)

Database:
MongoDB (NoSQL Database)

📦 Project Structure
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

🛠️ Setup Instructions
Follow these steps to get the project up and running on your local machine.
Prerequisites
Node.js (LTS version recommended)
MongoDB Atlas account or a local MongoDB instance

1. Clone the repository
git clone https://github.com/Chirag314625/Household_Energy_survey.git
cd Household_Energy_survey

2. Install Dependencies
Install the necessary Node.js packages for the backend:

npm install

3. Configure Environment Variables
Create a .env file in the root directory of your project (the same level as package.json) and add your MongoDB connection URI:

MONGODB_URI="your_mongodb_connection_string_here"

Replace "your_mongodb_connection_string_here" with your actual MongoDB connection string (e.g., from MongoDB Atlas).

4. Run the Server
Start the Node.js server:

npm start

The server will typically run on http://localhost:3000 (or the port specified in your server.js).

🌐 Usage
Once the server is running:

Open your web browser and navigate to http://localhost:3000/home.html to access the landing page.

Click "Start Survey Now" to proceed to the survey form.

Fill out the survey questions and click "Submit."

Your responses will be saved to your MongoDB database.

🤝 Contributing
Contributions are welcome! If you have suggestions for improvements or find any issues, please feel free to:

Fork the repository.

Create a new branch (git checkout -b feature/your-feature-name).

Make your changes.

Commit your changes (git commit -m 'Add new feature').

Push to the branch (git push origin feature/your-feature-name).

Open a Pull Request.

📄 License
This project is licensed under the ISC License. See the LICENSE file (if you create one) for details.
