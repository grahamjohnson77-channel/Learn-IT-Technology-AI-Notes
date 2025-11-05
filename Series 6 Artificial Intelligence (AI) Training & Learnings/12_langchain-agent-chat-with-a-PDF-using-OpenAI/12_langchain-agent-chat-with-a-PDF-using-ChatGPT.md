# Project 12: 12_langchain-agent-chat-with-a-PDF-using-ChatGPT
# ------------------------------------------------------
# ------------------------------------------------------
# Youtube
https://www.youtube.com/watch?v=wUAUdEw5oxM

# Code
https://github.com/alejandro-ao/langchain-ask-pdf/tree/main

# Setup virtual env in local folder
python3.12 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip setuptools wheel
pip install langchain openai pandas numpy streamlit python-dotenv tabulate pandas
pip install PyPDF2
python3.12 pip install PyPDF2

Restart the virtual env just to be sure!

# Since LangChain 1.0.3’s agent API is unstable and missing the new helper functions, the simplest and most reliable fix is to use the officially stable “LangChain Community” split — i.e., the langchain-community package — which keeps the old-style tools and agents working:
pip install langchain==0.3.7 langchain-community==0.3.7 langchain-openai==0.3.0
pip show langchain langchain-community

(The 0.3.x line is the stable LangChain Community release as of late 2025.)

✅ Why this works
Uses langchain-community for tools (that’s now the correct home for older APIs).
Keeps your original code structure.
Restores initialize_agent and AgentType compatibility.
Works smoothly with OpenAI models via langchain-openai.

# Import faiss python package
pip install faiss-cpu

# Install altair for streamlit
pip install altair==4.2.2
python -c "import altair; print(altair.__version__)"

# Download a sample file from this for testing
https://sample-files.com/documents/

# Run streamlit app
streamlit run main.py

# REALLY IMPORTANT !!!
The current code is adjusted to work with the langchain and openai versions
in the requirements file only!! Any upgrades could break it!!