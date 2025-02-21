from flask import Flask,jsonify,request
import json
import re

app =Flask(__name__)





@app.route("/api", methods=["POST"])
def detect_mentions():
    """Detect @mentions in a message"""
    data = request.json
    content = data.get("content")

    if not content:
        return jsonify({"error": "Message content required"}), 400

    # Use regex to find words starting with @
    mentions = re.findall(r"@(\w+)", content)


    return jsonify({
        "message": "Mentions detected",
        "content": content,
        "mentions": mentions
    }), 200






def load_json():
    with open("integration.json", "r") as file:
        data = json.load(file)
    return data

@app.route("/jsonsetting",methods=['GET'])
def jsonsetting():
    return jsonify(load_json())












if __name__ == '__main__':
    app.run(debug=True)



