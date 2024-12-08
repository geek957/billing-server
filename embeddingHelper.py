from PIL import Image
import requests
import torch
from transformers import CLIPProcessor, CLIPModel
if __name__ == '__main__':
    model_name = "openai/clip-vit-base-patch16"
    processor = CLIPProcessor.from_pretrained(model_name)
    model = CLIPModel.from_pretrained(model_name)

    image = Image.open('./sourceData/test.jpg')

    inputs = processor(text=["a photo of a cat", "a photo of a dog"], images=image, return_tensors="pt", padding=True)
    outputs = model(**inputs)
    print(outputs)
    print("Done")