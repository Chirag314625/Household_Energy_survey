const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");
const app = express();

app.use(cors());
app.use(express.json());
app.use(express.static("public")); // Serve frontend

// Connect to MongoDB
mongoose.connect("mongodb://localhost:27017/forms", {
  useNewUrlParser: true,
  useUnifiedTopology: true,
});

// Define Schema & Model
const formSchema = new mongoose.Schema({
  name: String,
  email: String,
  feedback: String,
});
const Form = mongoose.model("Form", formSchema);

// Submit form route
app.post("/submit", async (req, res) => {
  try {
    const newForm = new Form(req.body);
    await newForm.save();
    res.json({ message: "Form submitted successfully!" });
  } catch (error) {
    res.status(500).json({ message: "Error saving form data." });
  }
});

// Start server
app.listen(3000, () => {
  console.log("Server running on http://localhost:3000");
});
