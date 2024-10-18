import json
from flask import Flask, render_template, request
import ApiCalls

client = ApiCalls.initializeApiClients()

app = Flask(__name__,) 

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    apiCallArgs = json.loads(request.form['apiCallArgs'])
    platform = apiCallArgs["model"].split(": ")[0]
    if platform in ["Groq", "OpenAI", "Mistral"]:
        response = ApiCalls.openAiSpecCall(apiCallArgs, file, client)
    elif platform == "Anthropic":
        print("ApiCalls.AnthropicSpecCall(apiCallArgs, file)")
    else:
        print("Invalid platform")
    return response

if __name__ == '__main__':
    app.run(debug=True)
