from flask import Flask, jsonify, abort, request

# GLOBALS
MAX_KINDROID_MES = 750
LIMIT_MES_VIDEOCALLS = int(MAX_KINDROID_MES/2)

app = Flask(__name__)

@app.route("/", methods=["GET"])
def get_ping():
    return jsonify({"success": True}), 200

@app.route("/ping", methods=["GET"])
def get_neutral_ping():
    return get_ping()


# Desc: We are expecting as input something like this:
# {
#     "imageurl": "image",
#     "message": "A sample message to the AI"
# }
@app.route("/videocall", methods=["POST"])
def post_active_videocall():
    request_json = jsonify(request.json)
    img_url = request_json["imageurl"]
    mes = request_json["message"]
    if len(mes)>LIMIT_MES_VIDEOCALLS:
        return "Error: Message Too Long!"
    else:
        # Here call the chatgpt api to describe the image, then send that description to Maya. "\n(Attached image: "+description+")" where LIMIT_MES_VIDEOCALLS - len("(Attached image: )")
        # then we get the answer from Maya, and then just return that right away



if __name__ == "__main__":
    app.run(debug=True)
