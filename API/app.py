from flask import Flask, jsonify, abort

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def get_ping():
    return jsonify({"success": True}), 200

@app.route("/neutral/ping", methods=["GET"])
def get_neutral_ping():
    return get_ping()

if __name__ == "__main__":
    app.run(debug=True)
