import os
from PIL import Image
import cv2
from transformers import CLIPImageProcessor, CLIPVisionModelWithProjection
import pandas as pd
import torch
from utils import get_device_type
from objectDetector import ObjectDetector

# Load the model and processor
model = CLIPVisionModelWithProjection.from_pretrained("openai/clip-vit-base-patch16").to(get_device_type())
processor = CLIPImageProcessor.from_pretrained("openai/clip-vit-base-patch16")
object_detector = ObjectDetector()

embeddings = {}
products = {}

def load_precomputed_embeddings():
    embeddings_folder = "./run_1"
    allFiles = os.listdir(embeddings_folder)
    print(allFiles)
    global embeddings 
    for file_ in allFiles:
        if file_.endswith(".pt"):
            merchant_id = file_.split(".")[0].split("_")[-1]
            embedding_path = os.path.join(embeddings_folder, file_)
            embeddings[merchant_id] = torch.load(embedding_path,  map_location=get_device_type())
        print(merchant_id, len(embeddings[merchant_id]))
    print("total merchants loaded: ", len(embeddings))

def load_products():
    # Read the CSV file
    df = pd.read_csv('output.csv')

    # Create the dictionary
    for _, row in df.iterrows():
        merchant_id = str(row['merchantId'])
        if merchant_id not in products:
            products[merchant_id] = {}
        product_id = str(row['id'])
        products[merchant_id][product_id] = {
            'id': product_id,
            'nickname': row['nickname'],
            'price': row['price']
        }

load_precomputed_embeddings()
print(len(embeddings))
print(len(embeddings['1']))
load_products()
print(len(products))
print(len(products['1']))
