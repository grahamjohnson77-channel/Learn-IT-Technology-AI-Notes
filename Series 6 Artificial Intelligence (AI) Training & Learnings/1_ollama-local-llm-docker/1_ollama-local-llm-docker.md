# Install docker compose on MAC
brew install docker docker-compose

# Docker commands:
docker image ls						# list docker images currently available!
docker container ls 				# list docker containers currently available
docker stop <container name>		# stop container name
docker rm $(docker ps -a -q)		# Remove all stopped containers
docker image rm -f <image name>		# To remove an image (forcefully)
docker rmi $(docker images -a -q)	# delete ALL images in one command!

# List of ollama models here:
https://ollama.com/library

# Project 1: Ollama Setup Notes
# -----------------------------
# -----------------------------
# GitHub:
https://github.com/grahamjohnson77-channel/Learn-IT-Technology-AI-Notes

# Create Folder on Pi
1_ollama-local-llm-docker

# To Run: 
docker-compose up -d

# Check if ollama container is running:
docker ps | grep ollama

# If you want to list models inside the container:
# NOTE: run a command inside a container named 1_ollama_container (returns no models)
docker exec -it 1_ollama_container ollama list
OR
docker exec -it 1_ollama_container ollama ls

# Check browser is running for ollama model!
http://localhost:11434

# Use postman to call post requests on the model!
http://localhost:11434/api/generate

# Send model a direct message for testing! Tries to run model 'ollama'
docker exec -it 1_ollama_container ollama run tinyllama
docker exec -it 1_ollama_container ollama run llama2

# Execute to pull model: 
docker exec -it 1_ollama_container ollama pull tinyllama
docker exec -it 1_ollama_container ollama pull llama2

# To remove a model
docker exec -it 1_ollama_container ollama rm tinyllama:latest
docker exec -it 1_ollama_container ollama rm gemini:latest
docker exec -it 1_ollama_container ollama rm llama3.2:latest

# To switch the model
docker exec -it 1_ollama_container ollama pull tinyllama:latest
docker exec -it 1_ollama_container ollama pull gemini:latest
docker exec -it 1_ollama_container ollama pull llama3.2:latest