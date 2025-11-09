# Project 13: Langchain Python Script Runner
# ------------------------------------------
# ------------------------------------------
# Folder:
13_langchain-ai-agent-python-script-runner

# Setup virtual env in local folder
python3.12 -m venv .venv
source .venv/bin/activate

# Installations
pip install --upgrade pip setuptools wheel
pip install python-dotenv openai langchain langchain-openai langchain-experimental streamlit

# To run:
streamlit run run_streamlit_python.py
streamlit run run_streamlit_agnostic.py

# NOTES:
In this script, the LLM (like GPT-5) is not actually executing the Python code itself. The code is executed by the PythonREPLTool.

The LLM's role is to act as the "brain" or the "reasoning engine" of the agent. Here's the breakdown of its job:

- Understanding Your Request: It reads your prompt, which is in natural language: "Please execute this python script and tell me the output...". It understands the intent behind your words.

- Choosing the Right Tool: The agent has a list of available tools. In this case, it only has one: the python_repl. The LLM looks at your request and decides, "To fulfill this request, I need to use the python_repl tool."

- Preparing the Input: The LLM then extracts the actual Python code from your prompt and formats it as the correct input for the python_repl tool.

- Interpreting the Result: After the PythonREPLTool runs the code and produces an output, that output is sent back to the LLM. The LLM then formulates the final, user-friendly answer.

Think of it like a smart assistant. You don't need to know the specific command to run a program. You just tell the assistant what you want in plain English, and it figures out which program to run and how to run it for you. This makes the system much more flexible and powerful.