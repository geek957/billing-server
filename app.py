from flask import Flask, request, jsonify
from initload import  load_products, load_precomputed_embeddings
from PIL import Image
from search import searchProduct
import time

app = Flask(__name__)

@app.route('/ping', methods=['GET'])
def ping():
    client_ip = request.remote_addr
    print(f"Client IP: {client_ip}")
    print('Pong')
    return 'pong', 200

@app.route('/search', methods=['POST'])
def search():
    start_time = time.time()
    client_ip = request.remote_addr
    print(f"Client IP: {client_ip}")

    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image_file = request.files['image']
    image = Image.open(image_file)

    try:
        product = searchProduct(image)
        response = jsonify(product)
        responseCode = 200
    except Exception as e:
        response = jsonify({"error": str(e)})
        responseCode = 500
    end_time = time.time()
    elapsed_time_ms = (end_time - start_time) * 1000
    print(f"Request from {client_ip} took {elapsed_time_ms:.2f} ms")

    return response, responseCode


if __name__ == '__main__':
    load_precomputed_embeddings()
    load_products()

    app.run(host='0.0.0.0', port=5000, ssl_context=('cert.pem', 'key.pem'))
