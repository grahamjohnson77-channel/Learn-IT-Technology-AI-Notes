# Install docker compose on MAC
brew install docker docker-compose

# Docker commands:
docker image ls						        # list docker images currently available!
docker container ls 				      # list docker containers currently available
docker stop <container name>		  # stop container name
docker rm $(docker ps -a -q)		  # Remove all stopped containers
docker image rm -f <image name>		# To remove an image (forcefully)
docker rmi $(docker images -a -q)	# delete ALL images in one command!

# List of ollama models here:
https://ollama.com/library

# Project 3: 3_hello-genai-docker-model
# --------------------------------------
# --------------------------------------
# Folder: 3_hello-genai-docker-model

# Start the Docker Model (1.32 GB)
docker model pull ai/llama3.2:1B-Q8_0

# Docker Model list
docker model list

# Testing from CLI
docker model run ai/llama3.2:1B-Q8_0
Interactive chat mode started. Type '/bye' to exit.
> test
It looks like you're testing to see if I'm working properly. I'm happy to report that I'm functioning as expected. How can I assist you today?

# Testing Models from curl (this didnt work!)
curl http://localhost:1234/v1/models

curl http://localhost:1234/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "ai/llama3.2:3B-Q4_0",
    "messages": [
      { "role": "system", "content": "You are a helpful assistant." },
      { "role": "user", "content": "What is the capital of Italy?" }
    ]
  }'

# Get MAC IP
ipconfig getifaddr en0
This shows your Wi-Fi IP.
# If you're using Ethernet, try:
ipconfig getifaddr en1

# Get Public IP
curl ifconfig.me

# Docker Model delete (Only if required)
docker model rm ai/llama3.2:1B-Q8_0

Then ... for the application:

# GitHub Repo:
https://github.com/docker/hello-genai

# Clone the repo
cd Downloads/3_hello-genai-docker-model/
git clone https://github.com/docker/hello-genai
cd hello-genai

# Make sure you have a .env file like this!!!
# ---

# Configuration for the LLM service
LLM_BASE_URL=http://model-runner.docker.internal/engines/llama.cpp/v1

# Configuration for the model to use
LLM_MODEL_NAME=ai/llama3.2:1B-Q8_0

# -----

# To Create the containers 
docker compose up -d

# To attach the model to the UI and run the app
./run.sh

# Go to Docker Desktop now to find the URL of the app for node ...
http://localhost:8082/