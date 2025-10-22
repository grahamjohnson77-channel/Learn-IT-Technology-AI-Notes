# NOTE: I had to use this one for work laptop to work
import os
import httpx
import openai
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def main():
    # Print OpenAI SDK version
    print(f"OpenAI version: {openai.__version__}")
    print("-" * 20)

    # Load API key from environment
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        print("OPENAI_API_KEY is not set in environment variables.")
        return
    else:
        print("OPENAI_API_KEY successfully set in environment variables.")
        #print("OPENAI_API_KEY: " + openai_api_key)

    # Create a custom httpx client that does NOT verify SSL certificates
    # This is the insecure part.
    unverified_client = httpx.Client(verify=False)

    # Initialize OpenAI client
    client = OpenAI(api_key=openai_api_key, http_client=unverified_client)

    # Send a simple "Hello" message to OpenAI
    chat_response = client.chat.completions.create(
        model="gpt-4",  # or "gpt-3.5-turbo"
        messages=[
            {"role": "system", "content": "What is an AI prompt?"}
        ]
    )

    # Print the response
    print("OpenAI Response: " + chat_response.choices[0].message.content)

if __name__ == '__main__':
    main()