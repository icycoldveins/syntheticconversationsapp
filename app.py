from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Route for serving the home page


@app.route('/')
def home():
    # You can pass any initial data to the template here
    return render_template('home.html')

# Route for handling Ajax request for conversation data


@app.route('/get_conversation', methods=['GET'])
def get_conversation():
    # Extract topic or any other parameter sent by the client
    topic = request.args.get('topic', None)

    # Based on the topic, retrieve the corresponding conversation
    # For the sake of the example, we're returning a static conversation
    conversation_data = {
        'topic': topic,
        'conversation_html': '<div class="chat-bubble">This is a chat bubble for topic: {}</div>'.format(topic)
    }

    # Return the conversation data as a JSON object
    return jsonify(conversation_data)


if __name__ == '__main__':
    app.run(debug=True)
