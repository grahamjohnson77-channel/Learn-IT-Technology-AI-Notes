# Project 18: AI Vulnerabilities Scanning
# ---------------------------------------
# ---------------------------------------
# Folder:
18_ai-vulnerabilities-scanning

Trivy (by Aqua Security) is an open-source vulnerability and security scanner for containers, filesystems, and code repositories. It’s one of the most popular tools in the DevSecOps ecosystem because it’s simple, fast, and comprehensive.

Quick Summary: 
Trivy is a traditional vulnerability scanner for containers, images, and code.
DockSec is an AI‑powered Docker security analyzer that uses tools like Trivy under the hood but adds intelligent remediation, prioritization, and developer‑friendly reporting.

🔍 Key Differences Between Trivy and DockSec	
Trivy	
Type:                   Open‑source vulnerability scanner	
Focus:                  Finds CVEs, misconfigurations, secrets, SBOMs
Scope:                  Containers, images, Kubernetes, IaC, code repos, cloud
Output:	                Raw vulnerability lists (JSON, table, etc.)
User Experience:        CLI‑based, technical
Integration:	          CI/CD pipelines, Kubernetes security
Remediation             Guidance:	Limited (severity levels, CVE links)

DockSec
Type:                   AI‑powered Docker security analyzer
Focus:                  Enriches findings with AI explanations, remediation, compliance
Scope:                  Dockerfiles, images, containers; integrates Trivy, Hadolint, Docker Bench
Output:	                Actionable reports (JSON, CSV, HTML, PDF) with context and priorities
User Experience:        Developer‑friendly, explains risks in plain language
Integration:            CI/CD + IDEs (VS Code), DevSecOps workflows
Remediation Guidance:	  AI‑generated suggestions, compliance enforcement, best practices

🧩 Key Features:
🧱 Vulnerability Scanning
Detects CVEs (Common Vulnerabilities and Exposures) in OS and app dependencies.
Supports many package managers (apt, yum, apk, npm, pip, go modules, etc.).

🔐 Secrets Detection
Finds hardcoded passwords, tokens, or API keys in your code.

⚙️ Misconfiguration Scanning
Checks for insecure settings in Dockerfiles, Terraform, Kubernetes, etc.

🧾 SBOM Generation
Generates and verifies Software Bills of Materials in SPDX or CycloneDX format.

🚀 CI/CD Integration
Works seamlessly in Jenkins, GitHub Actions, GitLab CI, CircleCI, etc.

📦 Offline & Air-Gapped Mode
Can run without internet after downloading the vulnerability DB.

🧰 How It Works
Trivy downloads a local vulnerability database (from Aqua Security’s servers).
Scans your target (image, filesystem, repo, etc.) for installed software and dependencies.
Compares them against the database to find known vulnerabilities.
Outputs results in table, JSON, or SARIF format (for CI tools).

🔍 Why Developers Use It
Simple CLI — no complex setup needed.
Works out-of-the-box with Docker.
Fast incremental scans (caches the DB).
Open source and widely trusted (by GitHub, AWS, etc.).

# Install venv
python3 -m venv .venv
source .venv/bin/activate

# Part 1: Running trivy on Docker Directly
docker run --rm aquasec/trivy:latest image python:3.10

--rm → removes the container after it finishes.
aquasec/trivy:latest → the Trivy container image.
image python:3.10 → tells Trivy to scan the python:3.10 Docker image for vulnerabilities.

# OR 
# 🐳 Running trivy on Docker for Scanning
docker pull aquasec/trivy:latest

# 📁 Scan files or directories on your host
If you want to scan files in your local directory, you must mount it into the Trivy container:
docker run --rm -v $(pwd):/root/project aquasec/trivy:latest fs /root/project
-v $(pwd):/root/project → mounts your current directory to /root/project in the container.
fs /root/project → scans the mounted directory as a file system.

# ✅ Common Use Cases
Scan a local Docker image:
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy:latest image myapp:latest
Scan a directory:
docker run --rm -v $(pwd):/root/project aquasec/trivy:latest fs /root/project
Output results in JSON:
docker run --rm aquasec/trivy:latest image --format json nginx:latest

# ✅ Quick summary
Create persistent cache:
mkdir -p $HOME/.cache/trivy
Scan Docker image with cache:	
docker run --rm -v $HOME/.cache/trivy:/root/.cache/ -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy:latest image nginx:latest
Update DB only:
docker run --rm -v $HOME/.cache/trivy:/root/.cache/ aquasec/trivy:latest --download-db-only
Add shell alias:	
alias trivy='docker run --rm \
  -v $HOME/.cache/trivy:/root/.cache/ \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v $(pwd):/root/project \
  aquasec/trivy:latest'
Now you can run:
trivy image ubuntu:latest
trivy fs /root/project

# #########################

# Part 2: DockSec

# 📌 DockSec Notes
DockSec is an AI-powered Docker security analyzer.
If you plan to use DockSec with Docker images, ensure Docker is installed and running on your system.

# DockSec will analyze the image for:
Vulnerabilities (CVEs)
Misconfigurations
Security best practices

# To download DockSec
pip install docksec
docksec --help

Docker Security Analysis Tool:

positional arguments:
  dockerfile           Path to the Dockerfile to analyze (optional when using --image-only)

options:
  -h, --help           show this help message and exit
  -i, --image IMAGE    Docker image name to scan
  -o, --output OUTPUT  Output file for the report (default: security_report.txt)
  --ai-only            Run only AI-based recommendations (requires Dockerfile)
  --scan-only          Run only Dockerfile/image scanning (requires --image)
  --image-only         Scan only the Docker image without Dockerfile analysis

Usage examples:
  docksec Dockerfile -i myapp:latest          # Analyze both Dockerfile and image
  docksec --image-only -i myapp:latest        # Scan only the image
  docksec --ai-only Dockerfile                # AI analysis only

Run DockSec against the container:
Use the --container (or -c) flag with the container ID or name:
docksec -c my-python-app

Optional: Save the report
docksec -c my-python-app -o container-report.json

If you have a container running from python:3.12-slim:
docker run -d --name test-python python:3.12-slim sleep infinity
docksec -c test-python

OR

Have a docker-compose.yml file ready ...

version: "3.9"
services:
  web:
    image: python:3.12-slim
    container_name: web-service
  db:
    image: postgres:16
    container_name: db-service

docker compose up -d
docksec -c web-service
docksec -c db-service
docksec -c web-service -o web-report.json
docksec -c db-service -o db-report.json

Optional: Automate scanning
You can write a small script to loop through all containers in your Compose project:

bash
for c in $(docker ps --format '{{.Names}}'); do
  docksec -c $c -o ${c}-report.json
done

# ⚡ Benefits
Full-stack coverage: Scan every service in your Compose project.
Centralized reports: Store JSON outputs for CI/CD pipelines.
AI + vulnerability checks: DockSec combines traditional CVE scanning with AI insights.

# Examples ... To scan an image
docksec --image-only -i python:3.12-slim

👉 Now you can scan both images and running containers with DockSec.

# How to combine Trivy (With mounted volume to get the report in current dir) and DockSec
docker run --rm \
  -v $(pwd):/root/trivy \
  aquasec/trivy image python:3.12-slim \
  --format json -o /root/trivy/trivy-report.json

docksec trivy-report.json -o docksec-report.html

DockSec will enrich the Trivy findings with AI‑based remediation suggestions.

# #########################

# 🚀 Steps to Integrate DockSec with GitHub Actions
Create a GitHub Actions workflow file

In your repo, add:
.github/workflows/docksec.yml

Define the workflow Example workflow to scan a Docker image after build:
name: DockSec Scan

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

jobs:
  docksec-scan:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install DockSec
        run: |
          python -m pip install --upgrade pip
          pip install docksec

      - name: Build Docker image
        run: |
          docker build -t my-app:latest .

      - name: Run DockSec scan
        run: |
          docksec -i my-app:latest -o docksec-report.json

      - name: Upload DockSec report
        uses: actions/upload-artifact@v4
        with:
          name: docksec-report
          path: docksec-report.json

What this does:
Builds your Docker image from the repo.
Runs DockSec against the image.
Saves the results into docksec-report.json.
Uploads the report as a downloadable artifact in the GitHub Actions run.

Optional Enhancements
Fail the pipeline on critical vulnerabilities (Do not included the yaml)
yaml
- name: Run DockSec scan
  run: |
    docksec -i my-app:latest --scan-only --output docksec-report.json || exit 1
Scan multiple services (if using Docker Compose):

yaml
- name: Run DockSec on Compose
  run: |
    docker compose up -d
    for c in $(docker ps --format '{{.Names}}'); do
      docksec -c $c -o ${c}-report.json
    done

⚡ Benefits
Every PR or push gets an automatic security check.
Reports are stored as artifacts for auditing.
You can enforce security gates (block merges if vulnerabilities are found).