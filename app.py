from flask import Flask, request, jsonify
from initload import load_embeddings, load_products
from PIL import Image
from search import searchProduct

app = Flask(__name__)

@app.route('/ping', methods=['GET'])
def ping():
    print('Pong')
    return 'pong', 200

@app.route('/search', methods=['POST'])
def search():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image_file = request.files['image']
    image = Image.open(image_file)

    try:
        product = searchProduct(image)
        return jsonify(product), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    load_embeddings()
    load_products()
    app.run(host='0.0.0.0', port=3000)