import openai
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Access the OpenAI API key from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_completion(prompt):
    try:
        response = openai.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=100,  # Reduced max_tokens to encourage brevity
        temperature=0.5  # Adjusting temperature for more predictable outputs
    )
        return response.choices[0].text.strip()

    except Exception as e:
        print(f"Error generating completion: {e}")


# Example usage
if __name__ == "__main__":
    prompt = "Once upon a time,"
    completion = generate_completion(prompt)
    print("Generated completion:", completion)
