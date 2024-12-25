from initload import model, processor, embeddings, products, object_detector
from PIL import Image
import torch
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from utils import get_device_type

def searchProduct(image, merchant_id):
    # Process the input image
    #resultsMasked = object_detector.predict(image, "hand, no background, no object")
    #masked_image = object_detector.hide_mask(image, resultsMasked)
    #cropped_image = object_detector.predict_and_crop_image(masked_image, "object, no hand, no background")
    inputs = processor(images=image, return_tensors="pt", padding=True).to(get_device_type())
    with torch.no_grad():
        features = model(**inputs)

    
    if(get_device_type() == 'cuda'):
        features.image_embeds = features.image_embeds.to(torch.float32)
    query_embedding = features.image_embeds.detach().cpu().numpy()


    # Calculate cosine similarities
    similarities = []
    for id, embedding in embeddings[merchant_id].items():
        if(get_device_type() == 'cuda'):
            embedding.image_embeds = embedding.image_embeds.to(torch.float32)
        embedding = embedding.image_embeds.detach().cpu().numpy()
        similarity = cosine_similarity(query_embedding, embedding)
        similarities.append((id, similarity))

    closest_id, _ = max(similarities, key=lambda item: item[1])
    closest_id = closest_id.split("_")[0]

    product_details = products[merchant_id][closest_id]
    print(product_details)
    if product_details is None:
        raise Exception("No product found")
    return product_details

# Example usage
if __name__ == '__main__':
    image_path = 'sourceDataImages/1001/PXL_20241204_030823951.jpg'
    image = Image.open(image_path)
    product_details = searchProduct(image)
    print(product_details)
