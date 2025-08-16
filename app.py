from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def bee_quote():
    return jsonify({
        "quote": "Be like a bee. Work hard, stay focused, and make something sweet."
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)
