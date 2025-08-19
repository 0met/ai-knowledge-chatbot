# app.py (Flask example)
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from models import AIModel
from database import KnowledgeBase

app = Flask(__name__)
CORS(app)

# Initialize components
ai_model = AIModel()
knowledge_base = KnowledgeBase('knowledge_base/')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    response = ai_model.generate_response(user_input, knowledge_base)
    return jsonify({'response': response})

@app.route('/teach', methods=['POST'])
def teach():
    topic = request.json.get('topic')
    information = request.json.get('information')
    knowledge_base.add_knowledge(topic, information)
    return jsonify({'status': 'success'})

@app.route('/import', methods=['POST'])
def import_knowledge():
    file = request.files.get('file')
    if file:
        knowledge_base.import_from_file(file)
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error', 'message': 'No file provided'})

if __name__ == '__main__':
    app.run(debug=True)