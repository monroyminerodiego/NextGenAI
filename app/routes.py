from flask import Blueprint, render_template, request, jsonify

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    # TODO: integrar aquí la lógica de tu chatbot
    response_message = f"User echo: {user_message}"
    return jsonify({'message': response_message})