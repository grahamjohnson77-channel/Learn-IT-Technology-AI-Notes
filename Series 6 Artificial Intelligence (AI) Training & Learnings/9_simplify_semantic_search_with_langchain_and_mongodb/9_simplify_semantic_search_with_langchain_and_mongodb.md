# Project 9: Semantic Search (Vector DB & LLM)
# ------------------------------------------------------
# ------------------------------------------------------
# Folder:
9_simplify_semantic_search_with_langchain_and_mongodb

# Tutorial
https://www.mongodb.com/developer/languages/python/semantic-search-made-easy-langchain-mongodb/?utm_campaign=devrel&utm_source=youtube&utm_medium=organic_social&utm_content=ZvwUzcMvKiI&utm_term=jay.javed

# Youtube reference
https://www.youtube.com/watch?v=ZvwUzcMvKiI

# NOTE:
I used 3.11 for Python version for the project, same as video!

# Change to that new folder
cd /Users/gjohnson/Downloads/9_simplify_semantic_search_with_langchain_and_mongodb

# Setup virtual env in local folder
python3 -m venv .venv
source .venv/bin/activate

# Note: Pip was already installed in venv on MAC!

# Install the project requirements
pip3 install -r requirements.txt

# ------------------------------------------------------

# Login to OpenAI using email and standard home password!
https://auth.openai.com/log-in/password

# Get the Open API Key ...
https://platform.openai.com/settings/organization/api-keys

# Course code
git clone https://github.com/wbleonard/atlas-langchain.git

# Complete MongoDB Signup (uses email auth) ...

# Node or Python Installs
npm install mongodb
python3 -m pip install "pymongo[srv]"

# Get MONGODB_CONN_STRING = 
'mongodb+srv://<INSERT YOUR STRING HERE>'

# Update the params file
Update [params.py](https://github.com/wbleonard/atlas-langchain/blob/main/params.py) with your MongoDB connection string and Open AI [API key](https://platform.openai.com/account/api-keys).

# ############
# Ran this to remove the ssl cert issue
/Applications/Python\ 3.11/Install\ Certificates.command

# Above runs this anyway! 
pip install certifi

# I added this code to avoid ssl cert issues
client = MongoClient(MONGO_URI, tls=True, tlsCAFile=certifi.where(), serverSelectionTimeoutMS=5000)
# ###########

# BEFORE running, make sure to create the following collection:
DB_NAME = "langchain_search_db"
COLL_NAME = "search_col"

# NOTE:
I didnt need to create this beforehand:
INDEX_NAME = "langchain_vsearch_index"

# Run the following to test basic MongoDB connection:
python 1_test_mongodb_connection.py

# NOTE:
# When I first ran this, there was an error because the DB cluster 0 was not started
# in cloud.mongodb.com, so I had to 'resume' the cluster in DATABASE -> Clusters
# To resume the cluster, its needs to take about 3-5minutes.

  File "/Users/gjohnson/Downloads/9_simplify_semantic_search_with_langchain_and_mongodb/.venv/lib/python3.13/site-packages/pymongo/synchronous/srv_resolver.py", line 157, in get_hosts
    _, nodes = self._get_srv_response_and_hosts(True)
               ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "/Users/gjohnson/Downloads/9_simplify_semantic_search_with_langchain_and_mongodb/.venv/lib/python3.13/site-packages/pymongo/synchronous/srv_resolver.py", line 131, in _get_srv_response_and_hosts
    results = self._resolve_uri(encapsulate_errors)
  File "/Users/gjohnson/Downloads/9_simplify_semantic_search_with_langchain_and_mongodb/.venv/lib/python3.13/site-packages/pymongo/synchronous/srv_resolver.py", line 125, in _resolve_uri
    raise ConfigurationError(str(exc)) from None
pymongo.errors.ConfigurationError: The DNS query name does not exist: _mongodb._tcp.cluster0.i4rmgkr.mongodb.net.

# Once the cluster came backup online ...
(.venv) gjohnson@Graham 9_simplify_semantic_search_with_langchain_and_mongodb % python 1_test_mongodb_connection.py
✅ Connection successful!

# Run the following to test the database/collection is found and delete old documents
python 2_delete_mongodb_documents.py

(.venv) gjohnson@Graham 9_simplify_semantic_search_with_langchain_and_mongodb % python 2_delete_mongodb_documents.py
✅ Connected to MongoDB!
📚 Databases: ['langchain_search_db', 'admin', 'local']
📁 Collections in 'langchain_search_db': ['search_col']
🗑️ Deleted 324 documents from 'search_col'.
📦 Remaining documents in 'search_col': 0

# Install the required packages
pip3 install -U langchain langchain-core langchain-community langchain-chroma langchain-ollama langchain-huggingface langchain-openai langchain_mongodb sentence-transformers streamlit pathlib bs4

# Run the following to populate the database/collection:
python 3_vectorize_mongodb.py

If all worked, you should see this from the terminal window (it can take a few minutes!):

(.venv) gjohnson@Graham atlas-langchain % python 3_vectorize_mongodb.py
USER_AGENT environment variable not set, consider setting it to identify your requests.
Loaded 2 docs
Split into 324 docs

# Then check the Cluster() -> Collections and it should have 324 documents!
(.venv) gjohnson@Graham 9_simplify_semantic_search_with_langchain_and_mongodb % python 4_check_mongodb_documents.py
✅ Connected to MongoDB!
📚 Databases: ['langchain_search_db', 'admin', 'local']
📁 Collections in 'langchain_search_db': ['search_col']
📦 Remaining documents in 'search_col': 324

# Now we need to create a 'Vector Search Index' on Vector Embeddings Field
Go Back to MongoDB Atlas -> https://cloud.mongodb.com/
Choose 'DATABASE -> Search & Vector Search'
Ensure Project0 -> Cluster0 are selected
Select 'Create Vector Search Index'
Select 'Vector Search'
Search for the Database 'lang' ... the 'search_col' (in langchain_search_db) will show up!
Then 'JSON Editor'

This JSON should show up e.g
{
  "fields": [
    {
      "type": "vector",
      "path": "embedding",
      "numDimensions": 1536,
      "similarity": "cosine"
    }
  ]
}

# NOTE: Just use cosine here only! Remove other fields!
Then click 'Create Vector Index Search' button!

Status will be READY after a few minutes for the index!
e.g. 324 (100%) indexed of 324

# Run the following to query the data from the collection using the CLI:
python 5_query_vector_search.py -q "Who started AT&T?"

# NOTES:
Running this will create a new embedding so the original embeddings are compared against this new embedding for matching!

This query.py is also using a 'Contextual Compression' to use LLM so more directly tries to answer the question!

If your documents were indexed with a different embedding model (e.g., text-embedding-ada-002) than the one used here, the vector search will fail silently.
Ensure both sides use the same embeddings model.

# Semantic Search returns most relevant chunk of text:

Query Response:
---------------
AT&T - Wikipedia
AT&T was founded as Bell Telephone Company by Alexander Graham Bell, Thomas Watson and Gardiner Greene Hubbard after Bell's patenting of the telephone in 1875.[20] etc.....

# And passing it through the AI returns:

AI Response:
-----------
AT&T - Wikipedia
AT&T was founded as Bell Telephone Company by Alexander Graham Bell, Thomas Watson and Gardiner Greene Hubbard after Bell's patenting of the telephone in 1875.[20] One of its subsidiaries was the American Telephone and Telegraph Company (AT&T), established in 1885.[22] On December 30, 1899, AT&T acquired the assets of its parent American Bell Telephone, becoming the new parent company.[23]