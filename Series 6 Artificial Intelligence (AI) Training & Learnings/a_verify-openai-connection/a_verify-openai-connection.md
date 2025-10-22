# To test the OpenAI Key
python3 -m venv .venv
source .venv/bin/activate

# Installation openai (latest or version required?)
pip install --upgrade pip

pip install python-dotenv openai
OR
pip install python-dotenv openai==0.27.8
OR
pip install python-dotenv openai==1.1.1

# To run the app to test the connection
python3 test_connection.py