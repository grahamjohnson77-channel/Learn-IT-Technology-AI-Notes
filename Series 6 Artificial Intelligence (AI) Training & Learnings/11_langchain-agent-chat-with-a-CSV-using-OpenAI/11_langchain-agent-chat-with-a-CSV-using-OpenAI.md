# Project 11: 11_Chat-with-a-CSV
# ------------------------------------------------------
# ------------------------------------------------------
# Background to Application
Do you want a ChatGPT for your CSV? Welcome to this LangChain Agents tutorial on building a chatbot to interact with CSV files using OpenAI's LLMs. In this project-based tutorial, we will be using LangChain's framework for developing applications powered by language models.

With LangChain, we can create data-aware and agentic applications that can interact with their environment using language models. In this tutorial, we will be focusing on building a chatbot agent that can answer questions about a CSV file using ChatGPT's LLM.

We will begin by introducing the concepts of LangChain tools, LLMs, and agents. Then, we will dive into the code and show you how to load and use the agent with the OpenAI API. Now you can use OpenAI's LLMs to chat with your CSV or Excel files. 

If you're interested in machine learning, natural language processing, or want to learn how to build a chatbot using OpenAI's LLM, then this tutorial is perfect for you. Join us and let's build a powerful LangChain CSV chatbot together!

# Youtube
https://www.youtube.com/watch?v=tjeti5vXWOU

# Code
https://github.com/alejandro-ao/langchain-ask-csv

# Setup virtual env in local folder
python3.12 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip setuptools wheel
pip install langchain openai pandas numpy streamlit python-dotenv tabulate pandas

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

# Download a sample file from this for testing
https://sample-files.com/documents/

# Run streamlit app
streamlit run main.py

# LangChain Agents
https://python.langchain.com/v0.2/api_reference/experimental/agents.html

# Sample questions
What is the mean radius of the malignant tumors?

# Add gitigore from here
https://github.com/github/gitignore/blob/main/Python.gitignore