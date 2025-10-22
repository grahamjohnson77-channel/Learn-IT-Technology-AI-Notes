# Project 6: Sementic Book Recommender (Vector DB & LLM)
# ------------------------------------------------------
# ------------------------------------------------------
# Folder:
6_book-recommender-working-example

# Course code
https://github.com/t-redactyl/llm-semantic-book-recommender/tree/main

# DataSet used
https://www.kaggle.com/datasets/dylanjcastillo/7k-books-with-metadata

# List of ollama models here:
https://ollama.com/library

# Tools used:
venv in pycharm (python 3.11)
kaggle for dataset
Chroma for vectordb & various python packages!
Use Hugging Face Model for text classification
Transformers Python package
Gradio for Dashboard

# Youtube reference
https://www.youtube.com/watch?v=Q7mS1VHm3Yw

# NOTE:
I used 3.11 for Python version for the project, same as video!

# Download Pycharm (to work with DataSet)
https://www.jetbrains.com/pycharm/data-science/?utm_campaign=pycharm&utm_content=freecodecamp_course&utm_medium=referral&utm_source=youtube.com

# 01 DATA EXPLORATION
1. Create new Jupyter Project in Pycharm (Virtual Environment!) - 
Name: 6_book-recommender-working-example
e.g. /Users/gjohnson/PycharmProjects/PythonProject/6_book-recommender-working-example

NOTE: I am using Python 3.11 for the project in Pycharm

2. In Python Packages (on left hand side) - Install the following dependencies:
kagglehub (for data) - v0.3.13
pandas (for data tabular) - v2.3.3
pandas-hints (for data tabular) - accept default
matplotlib (for visualization) - v3.10.7
seaborn (for analysis of data) - v0.13.2
python-dotenv (for OpenAI credentials) - v1.1.1
langchain-community (for LLM) - v1.0.0a1
langchain-openai (for openai) - v1.0.0
langchain-chroma (for database) - v1.0.0
transformers (for huggingface models) - v4.57.1
datasets (for huggingface models) - v4.2.0
torch (for huggingface models) - v2.9.0
gradio (for display) - v6.0.0dev0
notebook (for Jupyter) - v7.5.0b1
ipywidgets (for Jupyter) - v8.1.7

# TIPs
pip3 install --upgrade pip
pip3 install -r requirements.txt
Use 'pip list' to get install packages!

3. Right click project and get new Jupiter notebook called 1-data-exploration

Issues:
/Users/gjohnson/Downloads/6_book-recommender-rag-working-example/.venv/lib/python3.13/site-packages/tqdm/auto.py:21: TqdmWarning: IProgress not found. Please update jupyter and ipywidgets. See https://ipywidgets.readthedocs.io/en/

Go to terminal in vs code and run: 
pip install jupyter and ipywidgets

# Change Terminal font size
🛠️ Method 1: Change Terminal Font Size via Settings
Open Command Palette: Press Ctrl + Shift + P (or Cmd + Shift + P on macOS).
Type and select Preferences: Open Settings (UI).
In the search bar, type terminal font size.
Adjust the Terminal › Integrated: Font Size setting (default is usually 14). Increase it to your desired size (e.g., 16 or 18).

# VS Code Switch (Run from terminal)
source /Users/gjohnson/Downloads/6_book-recommender-rag-working-example/.venv/bin/activate

# 02 TEXT CLASSIFICATION - 1:15mins in video
Used for classifcation of books!

Use Hugging Face Model for text classification, but zero shot classifcation
https://huggingface.co/models
https://huggingface.co/models?pipeline_tag=zero-shot-image-classification&sort=trending

Going to use the Transformers Python package now too!

Course to learn more!
https://huggingface.co/learn/llm-course/en/chapter1/1
           
# Check if mps is available (I added)
import torch
print(torch.__version__)
print(torch.backends.mps.is_available())

# 03 SENTIMENT ANALYSIS SECTION - 1:35.20mins in video
Used for emotional tone of the books!

# Make sure this line looks like this for mps
from transformers import pipeline
classifier = pipeline("text-classification",
                      model="j-hartmann/emotion-english-distilroberta-base",
                      top_k = None,
                      device = "mps")
classifier("I love this!")

# 04 VECTOR SEARCH SECTION - 38mins in video
Textloader will be used for raw data for langchain.
Chroma will be used as the vector db
OpenAI is used for the embeddings

1. Create OpenAI key
Create an OpenAI account: 
https://platform.openai.com/welcome?step=try
https://platform.openai.com/docs/overview

2. Add some credit to your account
https://platform.openai.com/settings/organization/billing/overview

3. Create a new .env file
touch .env
vi .env
Add this line (update for your OpenAI key)
OPENAI_API_KEY = <INSERT YOUR OPENAI KEY HERE!!!>

4. Removed this because newline was cauing error
books["tagged_description"].to_csv("tagged_description.txt",
                                    sep = "\n",
                                    index = False,
                                    header = False)

5. This original code line failed for chunk size 0 ... might have been \n causing issue
raw_documents = TextLoader("tagged_description.txt").load()
text_splitter = CharacterTextSplitter(chunk_size=0, chunk_overlap=0, separator="\n")
documents = text_splitter.split_documents(raw_documents)

## So had to change it to be:
raw_documents = TextLoader("tagged_description.txt").load()

# Ensure chunk_size is set to a valid positive integer
safe_chunk_size = max(1, 0)  # Replace 0 with a minimum valid size
text_splitter = CharacterTextSplitter(chunk_size=safe_chunk_size, chunk_overlap=0, separator="\n")

documents = text_splitter.split_documents(raw_documents)

6. Remember: Chroma will create a Vector DB ... OpenAI is used for the embeddings.

7. Changed this line (but should be .env file):
db_books = Chroma.from_documents(
    documents,
    embedding=OpenAIEmbeddings())

to:

import os
db_books = Chroma.from_documents(
    documents,
    embedding=OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
)

8. Update this line:
books[books["isbn13"] == int(docs[0].page_content.split()[0].strip())]

to be:
isbn_str = docs[0].page_content.split()[0].strip().strip('"')
books[books["isbn13"] == int(isbn_str)]

🔍 Explanation
strip() removes leading/trailing whitespace.
strip('"') removes any leading/trailing double quotes.
Then int() safely converts the cleaned string to an integer.

# 05 GRADIO DASHBOARD SECTION - 1:54.25

1. To run the dashboard from the terminal
gradio 5-gradio-dashboard.py

2. Open the browser
http://localhost:7860/