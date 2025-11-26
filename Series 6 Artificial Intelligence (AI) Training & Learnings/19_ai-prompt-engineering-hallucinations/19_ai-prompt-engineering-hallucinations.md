# Project 19: AI Prompt Engineering & Hallucinations
# --------------------------------------------------
# --------------------------------------------------
# Folder:
19_ai-prompt-engineering-hallucinations

🔑 Key Metrics Returned
similarity_score → How close the model’s answer is to the reference.
hallucination_detected → Boolean flag if similarity is below threshold.
model_answer vs reference_answer → Direct comparison for inspection.

⚠️ Notes
This is a basic prototype. Real hallucination detection often uses:
Fact-checking pipelines (retrieval-augmented generation, RAG).
Knowledge graphs or curated datasets.
Multiple sources for cross-verification.
Thresholds (like 0.5) should be tuned depending on your use case.

📊 What’s New
Claim Extraction → Splits the model’s answer into factual statements.
Multi‑source Verification → Each claim is checked against a web search result.
Precision/Recall →
Precision: fraction of claims supported by sources.
Recall: same here unless you have a gold‑standard dataset.
Confidence Score → Average similarity across claims.

🎯 Precision Explained
Definition: Out of all the claims your checker marked as supported, how many were actually correct?
Intuition: Precision tells you how trustworthy your “supported” label is.
Example: If the model made 10 claims, and you marked 6 as supported, but only 4 were truly correct → precision = 4/6 = 0.67.

📈 Recall Explained
Definition: Out of all the claims that were truly correct, how many did your checker successfully mark as supported?
Intuition: Recall tells you how complete your checker is at catching correct claims.
Example: If there were 8 correct claims in reality, and you marked 6 of them as supported → recall = 6/8 = 0.75.

🔒 Confidence Score Explained
Definition: The average similarity score across all claims.
Intuition: It’s a measure of how strongly the claims align with the reference text overall.
Example: If your similarity scores were [0.8, 0.7, 0.6], the confidence score = (0.8+0.7+0.6)/3 = 0.7.
Use: Helps you see whether claims are borderline or strongly supported.

🧩 Why they matter for hallucination detection
Precision → Avoids false positives (claims marked supported when they’re not).
Recall → Avoids false negatives (claims that are correct but missed).
Confidence → Gives a sense of overall alignment strength, useful for threshold tuning.

# Why this worked
Longer Wikipedia snippet gave enough context (directors + release date).
Semantic embeddings captured the meaning overlap, not just string matches.
Entity overlap fallback ensured that even if the exact phrasing differed, the claim was still marked supported.

# What you’ve achieved
A functioning hallucination checker that can:
Break down model answers into factual claims.
Verify each claim against external sources.
Compute precision, recall, and confidence metrics.
Visualize supported vs unsupported claims and confidence distribution.

# You should see:
Reference topic inferred → "The Matrix"
✅ Model Answer → The AI’s response.
✅ Claim Verification → Each claim marked supported/unsupported with similarity.
✅ Metrics → Precision, recall, confidence score.
Visualizations → Bar chart + histogram + precision–recall curve pop up in separate windows.

# But ...
This gives you a signal about hallucinations (unsupported or fabricated claims), but it’s not a perfect hallucination detector because:
If your reference source is incomplete (e.g., Wikipedia summary doesn’t mention the exact release date), 
a true claim may be marked unsupported.
If the model gives a claim that’s technically correct but phrased differently, similarity scores can be misleading.
Real hallucination testing in research often uses curated datasets with gold‑standard answers, not just live web snippets.

# To make it closer to “true hallucination testing” - 
Use a benchmark dataset (e.g., TruthfulQA, FactScore, or FEVER) where claims are labeled true/false.
Compare model outputs against that dataset for precision/recall.
Add multi‑source verification (Wikipedia + Wikidata + news APIs) to reduce false negatives.

# Each time, the pipeline will:
[ Get User Prompt ]
       |
       v
[ Query OpenAI Model ]
       |
       v
[ Model Answer ]
       |
       v
[ Extract Claims ]
       |
       v
[ Verify Claims ]
   ├─ Semantic Similarity (SentenceTransformers)
   └─ Entity Overlap (spaCy NER + Wikipedia)
       |
       v
[ Compute Metrics ]
   ├─ Precision
   ├─ Recall
   └─ Confidence Score
       |
       v
[ Visualize Results ]
   ├─ Bar Chart (Supported vs Unsupported)
   ├─ Histogram (Similarity Distribution)
   └─ Precision–Recall Curve

# 🧾 What is spaCy NER ?
NER stands for Named Entity Recognition.
In spaCy, NER is a component of the NLP pipeline that automatically identifies and classifies named entities in text. Named entities are real-world objects such as:
👤 People (e.g., Barack Obama)
🌍 Locations (e.g., Paris, Mount Everest)
🏢 Organizations (e.g., Microsoft, UNESCO)
📅 Dates & times (e.g., 21 November 2025)
💰 Monetary values (e.g., $1 billion)
📏 Quantities

# Install venv
python3.12 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install python-dotenv openai==0.27.8 matplotlib.pyplot
pip install sentence-transformers wikipedia spacy

# SentenceTransformers library trying to fetch the model weights from Hugging Face
python -m sentence_transformers all-MiniLM-L6-v2

# Install english language model using spacy
python -m spacy download en_core_web_sm
OR
pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.1/en_core_web_sm-3.7.1-py3-none-any.whl

python3 hallucinations.py