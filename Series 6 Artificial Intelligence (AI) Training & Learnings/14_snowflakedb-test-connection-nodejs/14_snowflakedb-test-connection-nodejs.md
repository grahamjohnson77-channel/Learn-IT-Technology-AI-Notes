# Project 14: Snowflake DB Test Connection NodeJs
# -----------------------------------------------
# -----------------------------------------------
# Folder:
14_snowflakedb-test-connection-nodejs

# Setup virtual env in local folder
python3.12 -m venv .venv
source .venv/bin/activate

# Installations
pip install --upgrade pip setuptools wheel

# Notes from inside of the snowflake_nodejs_v4.js File
// Install latest version of nvm
// curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
// Install latest version of snowflake
// rm -rf node_modules package-lock.json
// npm init -y
// npm install snowflake-sdk
// npm install snowflake-sdk@1.6.21 https-proxy-agent@5.0.0
// https://docs.snowflake.com/en/developer-guide/node-js/nodejs-driver-install
// Convert the pem file to p8
// openssl pkcs8 -topk8 -inform PEM -outform PEM -in keypair_stg.pem -out rsa_key.p8 -nocrypt
// Mani's repo >>>
// https://github.corp.ebay.com/CS-Data-Reporting/genesys_a3s_tool/tree/main
// To Run:
// node snowflake_nodejs_v4.js