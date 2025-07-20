// server.js
const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");
const path = require("path"); // path is now needed again
const rateLimit = require("express-rate-limit");
require("dotenv").config(); // Load environment variables from .env file

const app = express();

// -----------------------------------------------------------
// Rate Limiting Middleware
// -----------------------------------------------------------
const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 500, // Limit each IP to 500 requests per windowMs
  message: "Too many requests from this IP, please try again after 15 minutes."
});

// Apply the rate limiting middleware
app.use(apiLimiter);

// Middleware
// CORS is still needed if you access API routes from your frontend's client-side JS
// However, since both are on the *same domain* now, you can simplify it.
// We'll allow all origins for API routes for simplicity, or refine if needed.
app.use(cors()); // Allow all origins for API routes

app.use(express.json()); // For parsing application/json

// -----------------------------------------------------------
// Health Check Endpoint
// -----------------------------------------------------------
app.get("/health", (req, res) => {
    res.status(200).send("OK");
});

// -----------------------------------------------------------
// ✨ CRITICAL CHANGE: Re-enable serving static frontend files ✨
// Render will now host these files from your backend service.
// -----------------------------------------------------------

// Serve static files from the public directory (CSS, JS, etc.)
app.use(express.static(path.join(__dirname, "public")));

// Serve home.html at the root URL
app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "home.html"));
});

// Serve index.html when explicitly navigated to /index.html
app.get("/index.html", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "index.html"));
});

// MongoDB Connection
const mongoURI = process.env.MONGODB_URI;
if (!mongoURI) {
    console.error("FATAL ERROR: MONGODB_URI not defined in environment variables.");
    process.exit(1);
}

mongoose.connect(mongoURI)
    .then(() => console.log("✅ MongoDB connected successfully!"))
    .catch(err => console.error("MongoDB connection error:", err));

// MongoDB connection event listeners
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

// Helper to sanitize keys
function sanitizeKeys(obj) {
    const newObj = {};
    for (const key in obj) {
        if (Object.prototype.hasOwnProperty.call(obj, key)) {
            const safeKey = key.replace(/\./g, "_");
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
    console.log(`🚀 Server running on port ${PORT}`);
});