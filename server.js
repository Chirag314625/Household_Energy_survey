// server.js
const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");
const path = require("path");
const rateLimit = require("express-rate-limit"); // Import rate-limit middleware
require("dotenv").config(); // Load environment variables from .env file

const app = express();

// -----------------------------------------------------------
// Rate Limiting Middleware
// This helps prevent "Too Many Requests" by limiting the number
// of requests an IP can make within a certain time window.
// Adjust windowMs and max according to your needs.
// -----------------------------------------------------------
const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 500, // Limit each IP to 100 requests per windowMs
  message: "Too many requests from this IP, please try again after 15 minutes."
});

// Apply the rate limiting middleware to all requests.
// Make sure this is applied BEFORE your specific routes.
app.use(apiLimiter);

// Middleware
app.use(cors());
app.use(express.json()); // For parsing application/json

// -----------------------------------------------------------
// Health Check Endpoint
// A simple endpoint for Render (or other monitoring services)
// to check if your application is alive and responding.
// Configure Render's Health Check Path to /health.
// -----------------------------------------------------------
app.get("/health", (req, res) => {
    res.status(200).send("OK");
});

// Serve home.html at the root URL (localhost:3000 will show home.html)
app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "home.html"));
});

// Serve index.html when explicitly navigated to /index.html
app.get("/index.html", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "index.html"));
});

// REMOVE THIS ROUTE: thankyou.html is now handled client-side within index.html
// app.get("/thankyou.html", (req, res) => {
//   res.sendFile(path.join(__dirname, "public", "thankyou.html"));
// });

// Serve static files from the public directory (CSS, JS, etc.)
app.use(express.static(path.join(__dirname, "public")));

// MongoDB Connection
const mongoURI = process.env.MONGODB_URI;
if (!mongoURI) {
    console.error("FATAL ERROR: MONGODB_URI not defined in .env file.");
    process.exit(1);
}

mongoose.connect(mongoURI)
    .then(() => console.log("✅ MongoDB connected successfully!"))
    .catch(err => console.error("MongoDB connection error:", err));

mongoose.connection.on("connected", () => {
    console.log("📡 Mongoose connected");
});
mongoose.connection.on("error", (err) => {
    console.error("❌ Mongoose error:", err);
});
mongoose.connection.on("disconnected", () => {
    console.log("🔌 Mongoose disconnected");
});

// Allow flexible schema for survey data
const formSchema = new mongoose.Schema({}, { strict: false });
const Form = mongoose.model("Form", formSchema);

// Helper to sanitize keys (replace dots with underscores, as dots are special in MongoDB)
function sanitizeKeys(obj) {
    const newObj = {};
    for (const key in obj) {
        if (Object.prototype.hasOwnProperty.call(obj, key)) {
            const safeKey = key.replace(/\./g, "_");
            // If the value is an object, recursively sanitize its keys
            if (typeof obj[key] === 'object' && obj[key] !== null && !Array.isArray(obj[key])) {
                newObj[safeKey] = sanitizeKeys(obj[key]);
            } else {
                newObj[safeKey] = obj[key];
            }
        }
    }
    return newObj;
}

// API route for form submission
app.post("/api/submit-survey", async (req, res) => {
    try {
        console.log("📥 Received form data:", req.body);

        if (!req.body || Object.keys(req.body).length === 0) {
            return res.status(400).json({ error: "Form data is empty." });
        }
        

        const sanitizedData = sanitizeKeys(req.body);
        const newForm = new Form(sanitizedData);
        const result = await newForm.save();

        console.log("✅ Saved to MongoDB:", result);
        res.status(200).json({ message: "Form submitted successfully!" });

    } catch (error) {
        console.error("❌ Error saving form data:", {
            message: error.message,
            stack: error.stack
        });
        res.status(500).json({
            error: "Internal server error",
            details: error.message
        });
    }
});

// Start server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`🚀 Server running at http://localhost:${PORT}`);
});