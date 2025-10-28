# Project 8: RAG Pipeline (Vector DB & LLM)
# ------------------------------------------------------
# ------------------------------------------------------
# Folder (Create on Raspberry Pi):
8_1_local-RAG-pipeline-with-Ollama-on-Pi-bonus

# Copilot:
# To expose your local Streamlit app running at http://localhost:8501 to the internet 
# using ngrok, follow these steps:

# ✅ Step-by-Step Guide
1. Install ngrok on Raspberry Pi
If you haven’t installed ngrok yet, 
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-arm.zip
unzip ngrok-v3-stable-linux-arm.zip
sudo mv ngrok /usr/local/bin
ngrok version

My ngrok version 3.32.0 ...
🧠 Why this matters
v2 vs v3: ngrok v2 used ngrok authtoken <token> instead of config add-authtoken.
v3 adds config file support, persistent tunnels, and better CLI structure.
Let me know if you want to script this for your viewers or wrap it into a Docker container—I can help scaffold that for your Raspberry Pi series.

2. Authenticate ngrok (first-time setup)
Sign up at ngrok.com and get your authtoken from the dashboard.
https://ngrok.com/

Then run:
ngrok config add-authtoken <YOUR_AUTHTOKEN>

3. Expose your local port
Run the following command in your terminal:
ngrok http 8501

This tells ngrok to create a secure tunnel to your local Streamlit app running on port 8501.

4. Get the public URL
After running the command, ngrok will display a public URL like:
Forwarding                    https://abcd1234.ngrok.io -> http://localhost:8501
You can now share this URL (https://abcd1234.ngrok.io) with others to access your app online.

🔒 Optional: Custom Subdomain (Pro feature)
If you have a paid ngrok plan, you can use a custom subdomain:
ngrok http -subdomain=myapp 8501

This will give you a URL like https://myapp.ngrok.io.
Would you like help automating this with a script or integrating it into your development 
workflow?
You said:

Reconnecting (failed to send authentication request: tls: failed to verify certificate: 
              x509: certificate
Copilot said:
The error you're seeing:
reconnecting (failed to send authentication request: tls: failed to verify certificate: x509: certificate ...)
usually indicates a TLS/SSL certificate verification issue, which can happen when ngrok is trying to establish a secure tunnel but fails to verify the certificate of the local server (in this case, your Streamlit app on localhost:8501).

🔍 Common Causes & Fixes
✅ 1. Use http instead of https for localhost
Make sure your local app is running on plain HTTP, not HTTPS. Streamlit by default uses HTTP, so this should be fine unless you've manually configured SSL.

✅ 2. Correct ngrok command
Use this command to start ngrok:
ngrok http 8501
Avoid using https://localhost:8501 in the command — just specify the port.

✅ 3. Update ngrok
Make sure you're using the latest version of ngrok. Run:
Shell
ngrok version
If it's outdated, download the latest from https://ngrok.com/download.'

✅ 4. Check your firewall or proxy
If you're behind a corporate VPN, proxy, or firewall, it might interfere with TLS verification. Try running ngrok outside of that environment or check proxy settings.

✅ 5. Try disabling TLS verification (not recommended for production)
If you're testing locally and want to bypass TLS verification (again, not secure for public use), you can try:
ngrok http --host-header=localhost 8501
This tells ngrok to forward requests with the correct host header, 
which can help avoid certificate mismatches.