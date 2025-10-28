# Project 8: RAG Pipeline (Vector DB & LLM)
# ------------------------------------------------------
# ------------------------------------------------------
# Folder (Create on Raspberry Pi):
8_local-RAG-pipeline-with-Ollama-on-Pi

## NOTES BELOW FOR RASPBERRY PI ##
sudo apt install vim -y
vim --version

# NOTE: App requires a BRIGHTDATA_API_KEY so didn't really use ... but keep it for references purposes anyway ... e.g. chunking and streamlit samples
It also provided that streamlit could run on the raspberry pi

# Youtube reference base
https://www.youtube.com/watch?v=c5jHhMXmXyo

# NOTE:
I used 3.11 for Python version for the project, same as video!

# Course code
https://github.com/ThomasJanssen-tech/Local-RAG-with-Ollama

# Install Ollama
https://ollama.com/download

# Open the code in Pycharm to run!
# Needs the Ollama running locally

# NOTE:
Ollama requires an ARM64 (aarch64) operating system. If your Raspberry Pi model supports it (like Pi 3 or Pi 4), consider installing a 64-bit version of Raspberry Pi OS or Ubuntu.

# ####### Retrieve the latest version of GitHub CLI
GITHUB_CLI_VERSION=$(curl -s "https://api.github.com/repos/cli/cli/releases/latest" | grep -Po '"tag_name": "v\K[0-9.]+')

# Navigate to home directory and download the .deb package
cd ~
curl -Lo gh.deb "https://github.com/cli/cli/releases/latest/download/gh_${GITHUB_CLI_VERSION}_linux_armv6.deb"

# Install the package
sudo dpkg -i gh.deb

# Verify installation
gh --version
# ########

# ######## Install Ollama on Raspberry Pi
curl -fsSL https://ollama.com/install.sh | sh

You should see:
Created symlink /etc/systemd/system/default.target.wants/ollama.service → /etc/systemd/system/ollama.service.
>>> The Ollama API is now available at 127.0.0.1:11434.
>>> Install complete. Run "ollama" from the command line.
WARNING: No NVIDIA/AMD GPU detected. Ollama will run in CPU-only mode.
# ########

# ######## Download Ollama models for the Application onto the Pi
Check if Ollama is running:
ollama serve

Or check if it’s already running:
ps aux | grep ollama

If it’s not running, start it:
sudo systemctl start ollama

Then confirm:
curl http://localhost:11434/api/tags

# List & Pull models
ollama list
ollama pull llama3.2:3b

# Try smaller Text Embedding models for Pi!!
# These below will NOT work for Pi ...
# But left for testing anyway!

# NOTE: Larger embedding models will not work on Pi
ollama pull mxbai-embed-large
ollama pull nomic-embed-text

# Test Ollama manually
ollama embed --model mxbai-embed-large "test"

# If needed to delete older model
ollama rm mxbai-embed-large:latest
ollama rm nomic-embed-text:latest

# ########
# On MAC - Copy the github folder for quick testing
scp /Users/gjohnson/Downloads/8_Local-RAG-with-Ollama-on-Pi.zip admin@192.168.1.102:/home/admin/ai_learnings

# On Pi - Extract files for Pi project
cd ai_learnings/
filename="8_Local-RAG-with-Ollama-on-Pi"
foldername="${filename%.zip}"
mkdir "$foldername" && unzip "$filename" -d "$foldername"

# Change to that new folder
cd /home/admin/ai_learnings/8_Local-RAG-with-Ollama-on-Pi

# Install venv
sudo apt update
sudo apt install python3-venv
sudo apt install python3-wheel
sudo apt install python3-setuptools
sudo apt install python3-pip

# Setup virtual env in local folder
python3 -m venv .venv
source .venv/bin/activate

# Install pip
sudo apt install python3-pip
pip3 --version

# Alternative option for pip install
wget https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py

# Install the project requirements
chmod 777 requirements.txt
pip3 install -r requirements.txt

# Some early versions of langchain_ollama and ollama clients had HTTPX compatibility issues. Install AI packages using:
pip3 install --upgrade ollama langchain_ollama httpx
pip install -U langchain langchain-core langchain-community langchain-chroma langchain-ollama langchain-huggingface sentence-transformers streamlit pathlib

# Both should show 0.2.x or newer.
pip show langchain | grep Version
pip show langchain-core | grep Version

# Application was working with these versions:
Version: 1.0.2
Version: 1.0.1

# Note
LangChain modularized its codebase in v1.0+, moving core types like Document into langchain_core. This change improves clarity and separation between core logic and integrations.

# Update the .env file to be just that!
touch .env
vi .env
chmod 777 .env
Copy the contents over!

# Testing of the chunking, embeddings and retrievers
vi test_chunking.py
chmod 777 test_chunking.py
python3 test_chunking.py

Total chunks: 53
First chunk: LangChain is a framework for developing applications powered by large language models (LLMs).

# Testing embedding using the small model
vi test_embedding.py
chmod 777 test_embedding.py
python3 test_embedding.py

Should see something like:
-0.06689118593931198, -0.06350499391555786, 0.08124810457229614, -0.03388379514217377, 0.04588960483670235, 0.024952365085482597, -0.016521651297807693, 0.03934253752231598, -0.026782402768731117, -0.053943004459142685, -0.021042238920927048, -0.061427000910043716, 0.055464498698711395, 8.663527114549652e-05, -0.055299315601587296, 0.019222790375351906, -0.034269221127033234, -0.035487234592437744, -0.020091326907277107, 0.028644626960158348, -0.008767243474721909, -0.01538928784430027, 0.04792075231671333, -0.03411838412284851, 0.06182337924838066, 0.013315950520336628, 0.1024472638964653, 0.008530953899025917]

# Testing the document retriever
vi test_retriever.py
chmod 777 test_retriever.py
python3 test_retriever.py

✅ Found 7 existing documents.
🔍 Searching for: 'what is langchain'
* LangChain is a framework for building applications powered by language models. [{}]
* It offers residential, mobile, and datacenter proxies. [{}]
* Use cases include market research, SEO monitoring, and ad verification. [{}]
* SentenceTransformers provide lightweight text embeddings for semantic search. [{}]
* Bright Data is a proxy and web scraping platform. [{}]

# Copy excel file (if changed)
scp /Users/gjohnson/Downloads/8_Local-RAG-with-Ollama-on-Pi/find_keywords.xlsx admin@192.168.1.102:/home/admin/ai_learnings/8_Local-RAG-with-Ollama-on-Pi

# BrightData
Setup using my personal email

# Pipeline 1: Run the following:
vi 1_scraping_wikipedia_using_brightdata.py
chmod 777 1_scraping_wikipedia_using_brightdata.py
python3 1_scraping_wikipedia_using_brightdata.py

✅ How to confirm progress directly
You can verify the job’s status in Bright Data’s dashboard:
Go to your Bright Data Datasets Console
Open your dataset with ID
Check the “Snapshots” tab — you should see the same snapshot ID written in your snapshot_id.txt.

It will show:
Running = still scraping
Ready = data available
Error = something failed

This took a few minutes to run, maybe 7-8mins ... finally:

🔍 Checking snapshot status (attempt 15/15)...
➡️ Current status: ready
✅ Snapshot is ready! Fetching scraped data...
✅ Data saved successfully to: datasets/data_20251028_082822.json

# Check the new dataset file created (11m for a Pi is big!)
ls -lhr ./datasets/
total 11M
-rw-rw-r-- 1 admin admin 11M Oct 28 08:28 data_20251028_082822.json

# ⚡ Tips if it stays “running” too long
If it’s been over 30–45 minutes and still says "running", try these:
Reduce scope in find_keywords.xlsx
Fewer keywords or smaller “Pages” count (e.g. Pages = 1).

# Pipeline 2: Use the new version of chunking
chmod 777 2_chunking_embedding_ingestion.py
python3 2_chunking_embedding_ingestion.py

This took a few minutes to run, maybe 4-5mins ... finally:

🗂️ Using latest dataset file: datasets/data_20251028_082822.json
🧠 Using embedding model: all-MiniLM-L6-v2
Found existing JSONL file: datasets/data_20251028_082822.jsonl
📚 Loaded 0 documents from scraped data.
🧩 Split into 0 chunks.

Embedding & adding chunks: 0it [00:00, ?it/s]

✅ Ingestion complete! Data saved to: chroma_db

# Pipeline 3: Testing the Vector DB
vi 3_retrieve_and_query.py
chmod 777 3_retrieve_and_query.py
python3 3_retrieve_and_query.py

# Summary of pipeline
| Step    | Script                                               | Purpose                                           |
| ------- | ---------------------------------------------------- | ------------------------------------------------- |
| 1️⃣ | BrightData scraper                     | Fetches web content (`data<DATE>.txt`)                  |
| 2️⃣ | `2_chunking_embedding_ingestion.py` | Converts + embeds scraped data into Chroma        |
| 3️⃣ | `3_retrieve_and_query.py`        | Searches and optionally answers questions locally |

# Run the Streamlit website
vi 4_streamlit_rag_chatbot.py
chmod 777 4_streamlit_rag_chatbot.py
streamlit run 4_streamlit_rag_chatbot.py --server.address 0.0.0.0 --server.port 8501

# Run the Streamlit website
vi 4_streamlit_rag_chatbot_no_vectordb_regen.py
chmod 777 4_streamlit_rag_chatbot_no_vectordb_regen.py
streamlit run 4_streamlit_rag_chatbot_no_vectordb_regen.py --server.address 0.0.0.0 --server.port 8501

# Sample questions
What is langchain used for?
How does Bright Data collect proxy information?

http://192.168.1.102:8501/