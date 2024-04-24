# encoding=utf-8
import json
from models.chatbot_model import ChatbotModel
from utils.helpers import load_all_scene_configs
from flask import Flask, request, jsonify, send_file
from utils import logger

app = Flask(__name__)




@app.route('/function', methods=['POST'])
def function():
    json_data = request.get_data()
    data = json.loads(json_data)

    chatId = data.get('chatId')

    data = data["data"]
    question = data.get('question')
    AI_history = data.get('history')
    

    # 实例化ChatbotModel
    chatbot_model = ChatbotModel(load_all_scene_configs(chatId))

    if not question:
        return jsonify({"error": "No question provided"}), 400

    response = chatbot_model.process_multi_question(question,AI_history[-1]['value'] if AI_history else "",chatId)

    if response == question:
        return jsonify({"no_function":True, "question":question})
    else: 
        return jsonify({"use_function":True,"answer": response})



if __name__ == '__main__':
    app.run(host='127.0.0.1',port=7000)
