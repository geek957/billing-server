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
    embedding_path = "./run_1/embeddings.pt"
    global embeddings 
    embeddings = torch.load(embedding_path)
    # print(len(embeddings))

def load_products():
    # Read the CSV file
    df = pd.read_csv('output.csv')

    # Create the dictionary
    for _, row in df.iterrows():
        product_id = str(row['id'])
        products[product_id] = {
            'id': product_id,
            'nickname': row['nickname'],
            'price': row['price']
        }

load_precomputed_embeddings()
print(len(embeddings))
load_products()