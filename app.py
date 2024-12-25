from flask import Flask, request, jsonify
from initload import load_precomputed_embeddings, load_products
from PIL import Image
from search import searchProduct
import time
import os
import uuid
import csv
from functools import wraps

app = Flask(__name__)

# Define the encoded string for authentication (e.g., "Basic base64encodedstring")
AUTH_STRING = "Chitragupta-ai_d3ce3de3-4570-4ff1-a632-a489beaf3dfd"

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if auth_header != AUTH_STRING:
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/ping', methods=['GET'])
# @require_auth
def ping():
    client_ip = request.remote_addr
    merchant_id = request.args.get('merchantId')
    if merchant_id is None:
        return jsonify({'error': 'Merchant ID is required'}), 400
    print(f"Client IP: {client_ip}")
    print(f"Merchant ID: {merchant_id}")
    print('Pong')
    return jsonify({'message': 'pong', 'merchantId': merchant_id}), 200

@app.route('/search', methods=['POST'])
@require_auth
def search():
    start_time = time.time()
    client_ip = request.remote_addr
    print(f"Client IP: {client_ip}")

    merchant_id = request.args.get('merchantId')
    if merchant_id is None:
        merchant_id = "1"
        # return jsonify({'error': 'Merchant ID is required'}), 400

    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image_file = request.files['image']
    image = Image.open(image_file)

    try:
        product = searchProduct(image, merchant_id)
        response = jsonify(product)
        status_code = 200
    except Exception as e:
        response = jsonify({"error": str(e)})
        status_code = 500

    end_time = time.time()
    elapsed_time_ms = (end_time - start_time) * 1000
    print(f"Request from {client_ip} took {elapsed_time_ms:.2f} ms")

    return response, status_code

@app.route('/feedback', methods=['POST'])
@require_auth
def feedback():
    merchant_id = request.args.get('merchantId')
    correct = request.args.get('correct')
    product_id = request.args.get('productId')

    if not merchant_id or not correct or not product_id:
        return jsonify({"error": "Missing query parameters"}), 400

    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image_file = request.files['image']
    image = Image.open(image_file)

    # Create directory if it doesn't exist
    directory = f'queriedImages/{merchant_id}'
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Generate a random UUID for the filename
    filename = f'{uuid.uuid4()}.png'
    filepath = os.path.join(directory, filename)

    # Save the image
    image.save(filepath)

    # Append details to queries.csv
    csv_filepath = 'queriedImages/queries.csv'
    with open(csv_filepath, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([merchant_id, product_id, filename, correct])

    return jsonify({"message": "Feedback received"}), 200

if __name__ == '__main__':
    load_precomputed_embeddings()
    load_products()
    app.run(host='0.0.0.0', port=3000)
