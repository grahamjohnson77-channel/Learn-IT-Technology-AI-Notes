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

# Project 5: 5_self-hosted-ai-starter-n8n-kit
# --------------------------------------
# --------------------------------------
# Folder:
5_self-hosted-ai-starter-n8n-kit

# To build the n8n interface
docker compose --profile cpu up

# If all worked, you should be able to open
http://localhost:5678/

Log in and see that it looks like the same as mine!