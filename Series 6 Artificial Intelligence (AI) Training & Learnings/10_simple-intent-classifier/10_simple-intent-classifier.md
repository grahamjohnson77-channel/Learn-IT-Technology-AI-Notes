# Project 10: Simple Intent Classifier (from CoPilot)
# ------------------------------------------------------
# ------------------------------------------------------
# Background to Intents
Building a sample AI app that classifies user intent is a great way to dive into natural language processing (NLP) and machine learning. Here's a roadmap to help you get started:

# 🧠 Step 1: Define the Problem
Intent classification means identifying what the user wants to do based on their input. Common intents include:

Greeting: “Hi there!”
Question: “What’s the weather like?”
Command: “Play some music.”
Complaint: “This app is so slow.”

You’ll need to decide:
What intents you want to classify
Whether you want to use predefined categories or allow dynamic learning

# 🗂️ Step 2: Prepare Your Dataset
You’ll need labeled examples of user inputs and their corresponding intents. You can:
Create your own dataset (e.g., 100 examples per intent)
Use public datasets like CLINC150, SNIPS, or ATIS

Example format:
json
{
  "text": "Book a flight to New York",
  "intent": "book_flight"
}

# 🤖 Step 3: Choose a Model
You can start simple or go advanced:
Simple: Logistic Regression or Naive Bayes with TF-IDF
Intermediate: LSTM or GRU models
Advanced: Transformers like BERT or DistilBERT

Libraries to use:
scikit-learn for traditional ML
TensorFlow or PyTorch for deep learning
Hugging Face Transformers for pretrained models

# 🛠️ Step 4: Build the App
You can use:
Python backend with Flask or FastAPI
Frontend with HTML/JS or React
Streamlit for a quick interactive UI

Example with Flask:

python
from flask import Flask, request, jsonify
from your_model import predict_intent

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    user_input = request.json['text']
    intent = predict_intent(user_input)
    return jsonify({'intent': intent})

# 🚀 Step 5: Test and Improve
Evaluate accuracy, precision, recall
Add more data to improve performance
Consider edge cases and ambiguous inputs

# Setup virtual env in local folder
python3 -m venv .venv
source .venv/bin/activate

# FIRST CLASSIFIER APP (FILES IN SAME FOLDER)
# ###########################################
# Folder:
10_simple-intent-classifier/1_webapp

# Requirements
cd 10_simple-intent-classifier/1_webapp
pip3 install streamlit scikit-learn pandas

# Copy code from CoPilot

# To Run
streamlit run intent_classifier_webapp.py

# Uses TfidfVectorizer
The TfidfVectorizer is a feature extraction tool in scikit-learn that converts raw text (like sentences or documents) into numerical vectors that machine learning models can understand.

🧩 What it stands for
TF-IDF = Term Frequency – Inverse Document Frequency
It measures how important each word is to a document in a collection (corpus).

⚙️ How it works:
1. Term Frequency (TF) — how often a word appears in a document.
Example: if “chatbot” appears 3 times in a message of 100 words,
→ TF("chatbot") = 3 / 100 = 0.03

2. Inverse Document Frequency (IDF) — how unique or rare a word is across all documents.
Common words (like “the”, “is”) get lower weights.
Rare words (like “refund”, “shipment”) get higher weights.

3. TF-IDF = TF × IDF
→ So frequent but uninformative words are downweighted, and rare, informative ones are boosted.

🧠 Example
Suppose you have:

from sklearn.feature_extraction.text import TfidfVectorizer

docs = ["I love chatbots", "Chatbots are helpful", "I love AI"]
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(docs)

vectorizer learns the vocabulary and computes TF-IDF scores for each word.
X is a sparse matrix of numbers representing how important each word is in each document.

📦 Why it's useful
Converts text into a numeric form for ML algorithms (which can’t handle raw text).
Reduces the impact of common, less meaningful words.
Keeps features interpretable — you can see which words matter most.

# SECOND CLASSIFIER APP (FILES IN SAME FOLDER)
# ############################################
intent_classifier_app/
│
├── app.py                # Flask app
├── model.py              # ML model training and prediction
├── intents.json          # Sample training data
└── requirements.txt      # Dependencies

# Requirements
cd 10_simple-intent-classifier/2_more_advanced_using_matplotlib
pip3 install flask scikit-learn streamlit

# App Includes
✅ Top predicted intent with confidence
📊 Bar chart of top 5 intents
🌡️ Progress bar for top intent
🧠 Color-coded feedback

# To run:
cd 2_more_advanced_using_matplotlib
streamlit run ui.py