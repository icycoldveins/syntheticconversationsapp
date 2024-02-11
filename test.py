import os
from openai import OpenAI
from dotenv import load_dotenv

# Load variables from .env into environment
load_dotenv()


def test_api_key(api_key):
    try:
        # Instantiate the OpenAI client with your API key
        client = OpenAI(api_key=api_key)

        # Test the API key by making a simple request
        response = client.chat.completions.create(
            model="text-davinci-003",
            messages=[{"role": "user", "content": "Hello, world!"}]
        )

        # Check if the response is successful
        if response.status == 200:
            print("API key test successful!")
        else:
            print(f"API key test failed with status code: {response.status}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    # Get the API key from environment variables
    api_key = os.environ.get("OPENAI_API_KEY")

    if api_key is None:
        print("API key not found in environment variables.")
    else:
        # Test the API key
        test_api_key(api_key)
