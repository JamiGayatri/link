from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    # Pass user_input to your chatbot logic and get a response
    bot_response = get_chatbot_response(user_input)
    return jsonify({'response': bot_response})

def get_chatbot_response(user_input):
    # Here you would integrate with your existing chatbot logic
    # For example, you might pass the user_input to Rasa or OpenAI API
    # and return the response
    response = "This is a dummy response"
    return response

if __name__ == '__main__':
    app.run(debug=True)
