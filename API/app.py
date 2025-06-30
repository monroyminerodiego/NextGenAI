import sys
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_restful import Api
from flask_cors import CORS
import traceback

load_dotenv()
sys.stdout = sys.stderr

app = Flask(__name__)
# 1) Activa debug y propagación de errores
app.config["DEBUG"] = True
app.config["PROPAGATE_EXCEPTIONS"] = True

CORS(app)
api = Api(app, prefix='/api')

# 2) Handler global para que devuelva siempre el stack trace
@app.errorhandler(Exception)
def handle_all_exceptions(e):
    tb = traceback.format_exc().splitlines()
    app.logger.error("\n".join(tb))
    return jsonify({
        "status": "error",
        "message": str(e),
        "trace": tb
    }), 500

# Enpoints del chat
from Scripts.chatbot.chat      import ChatbotResponse


api.add_resource(ChatbotResponse, "/a/chat")

if __name__ == '__main__':
    app.run(debug=True)