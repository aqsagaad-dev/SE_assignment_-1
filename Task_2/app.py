
from flask import Flask, request, jsonify
import secrets

app = Flask(__name__)

api_keys = {
    secrets.token_hex(16): "Consumer 1",
    secrets.token_hex(16): "Consumer 2",
    secrets.token_hex(16): "Consumer 3"
}

print("RootSoftware API Keys:")
for key, consumer in api_keys.items():
    print(f"{consumer}: {key}")

@app.route("/process", methods=["POST"])
def process_text():
    api_key = request.headers.get("X-API-Key")

    if not api_key or api_key not in api_keys:
        return jsonify({"error": "Invalid or missing API key"}), 401

    data = request.get_json(silent=True)

    if not data or not data.get("text"):
        return jsonify({"error": "Text is required"}), 400

    result = data["text"].upper()

    return jsonify({
        "consumer": api_keys[api_key],
        "result": result
    }), 200

if __name__ == "__main__":
    app.run(debug=True, port=5001)
