import os
from PIL import Image
import cv2
from transformers import CLIPImageProcessor, CLIPVisionModelWithProjection
import pandas as pd
import torch

# Load the model and processor
model = CLIPVisionModelWithProjection.from_pretrained("openai/clip-vit-base-patch16")
processor = CLIPImageProcessor.from_pretrained("openai/clip-vit-base-patch16")

embeddings = {}
products = {}

def extract_frames(video_path, frame_rate=2):
    video_capture = cv2.VideoCapture(video_path)
    total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = video_capture.get(cv2.CAP_PROP_FPS)
    interval = int(fps / frame_rate)
    frame_number = 0
    frames = []
    while True:
        success, frame = video_capture.read()
        if not success:
            break
        if frame_number % interval == 0:
            frames.append(frame)

        frame_number += 1
    video_capture.release()
    return frames

def load_embeddings():
    path_to_videos = "./sourceDataVideos/"
    videos = os.listdir(path_to_videos)
    print(videos)
    count = 0
    for video in videos:
        print("--------------------- Processing video: ", count, video)
        count += 1
        video_path = os.path.join(path_to_videos, video)
        frames = extract_frames(video_path)
        id = video.split("_")[0]
        frame_number = 0
        for frame in frames:
            image = Image.fromarray(frame)
            inputs = processor(images=image, return_tensors="pt", padding=True)
            with torch.no_grad():
                features = model(**inputs)
            embeddings[id + "_"+str(frame_number)] = features
            frame_number += 1


def load_products():
    # Read the CSV file
    df = pd.read_csv('dataMap.CSV')

    # Create the dictionary
    for _, row in df.iterrows():
        product_id = str(row['id'])
        products[product_id] = {
            'id': product_id,
            'nickname': row['nickname'],
            'price': row['price']
        }

# load_products()
# print(products)    
# load_embeddings()
# print(len(encodings))
