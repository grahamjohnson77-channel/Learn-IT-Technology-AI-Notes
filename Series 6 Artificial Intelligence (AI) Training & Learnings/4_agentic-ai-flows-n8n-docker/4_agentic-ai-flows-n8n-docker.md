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

# Project 4: agentic-ai-flows-n8n-docker
# --------------------------------------
# --------------------------------------
# Folder:
4_agentic-ai-flows-n8n-docker

# To Build the docker image
docker build -t agentic-ai-flows-n8n-docker .

# To Run the n8n App from the Cmd Line (INTERACTIVELY!)
docker run -it --rm -p 5678:5678 -v ~/.n8n:/home/node/.n8n agentic-ai-flows-n8n-docker

# ChatGPT - Let’s break this Dockerfile down line by line and explain what each part does:

# Use the official n8n image as the base
FROM n8nio/n8n

✅ Explanation:
This tells Docker to start from the official n8n image provided by the n8n team.
n8n is an open-source workflow automation tool (like Zapier or Node-RED).
The base image already contains Node.js, n8n, and all its dependencies installed and configured.
So, your Docker image starts from a ready-to-use n8n environment.

# Optional: Set environment variables directly here (or use docker-compose/env file)
ENV N8N_BASIC_AUTH_ACTIVE=true
ENV N8N_BASIC_AUTH_USER=admin
ENV N8N_BASIC_AUTH_PASSWORD=securepassword

✅ Explanation:
These ENV instructions define environment variables inside the container.

They configure basic authentication for your n8n instance:
N8N_BASIC_AUTH_ACTIVE=true → Turns on basic authentication (so not everyone can access your n8n UI).
N8N_BASIC_AUTH_USER=admin → Username to log in.
N8N_BASIC_AUTH_PASSWORD=securepassword → Password to log in.

⚠️ Security note:
You shouldn’t hardcode real credentials in a Dockerfile.
Instead, it’s safer to use:

a .env file, or
environment variables set in your docker-compose.yml.

# Optional: Copy custom workflows or credentials
# COPY ./workflows /home/node/.n8n
✅ Explanation:
This line (currently commented out) would copy local files into the container.
The local ./workflows folder → /home/node/.n8n inside the container.
That’s where n8n stores workflows, credentials, and data.
If you uncomment this line, you can pre-load workflows into the container image.

# Expose the default port
EXPOSE 5678

✅ Explanation:
This tells Docker that the container will listen on port 5678 — the default port for the n8n web UI and API.

It doesn’t open the port itself; it’s just metadata so Docker (and humans) know which port the application uses.
You’d still need to publish the port using -p 5678:5678 when running the container or in your docker-compose.yml.