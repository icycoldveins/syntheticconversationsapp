from flask import Flask, jsonify, request, abort, render_template
import logging
import openai
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Load environment variables from .env
load_dotenv()

# Access the OpenAI API key from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set the logging level to DEBUG

# Create a file handler and set the logging level to DEBUG
file_handler = logging.FileHandler('flask.log')
file_handler.setLevel(logging.DEBUG)

# Create a formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Set the formatter for the file handler
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)


@app.route('/')
def home():
    return render_template('home.html')


# Define a dictionary to store previous dialogues
previousDialogues = {"Teacher": "", "Student": ""}


@app.route('/generate-dialogue', methods=['POST'])
def generate_dialogue():
    # Get the content from the request
    title = request.json.get('title', '')
    content = request.json.get('content', '')

    # Check if content exists
    if not content:
        abort(400, description="Content is required in the request")

    try:
        # Set up a prompt that explicitly asks for one question and one answer
        prompt = (f"Let's have a Discussion about '{title}'. The main points are: '{content}'.\n"
                  "WE WANT TO ONLY HAVE ONE EXCHANGE BETWEEN THE TEACHER AND STUDENT MEANING ONLY ONE QUESTION AND ONE ANSWER"
                  "Imagine we're in a classroom setting. I'll be the teacher asking one question to deepen our understanding, and you'll respond as a student with your single insight.\n"
                  "Here's how our conversation will go:\n"
                  "Teacher: [asks a question]\n"
                  "Student: [provides an answer]\n"
                  f"Teacher: {previousDialogues['Teacher']}\n"
                  f"Student: {previousDialogues['Student']}")
        app.logger.info(f"Prompt: {prompt}")

        response = openai.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=100,  # Reduced max_tokens to encourage brevity
            temperature=0.5  # Adjusting temperature for more predictable outputs
        )
        dialogue = response.choices[0].text.strip()

        # Store the new dialogue, considering how to handle previous dialogues


        # Return the generated dialogue as JSON response
        return jsonify({'dialogue': dialogue})

    except Exception as e:
        # Log error if dialogue generation fails
        logger.error(f"Failed to generate dialogue: {e}")
        return jsonify({'error': 'Failed to generate dialogue, please check server logs for more details'}), 500


if __name__ == '__main__':
    app.run(debug=True)
