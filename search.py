from initload import model, processor, embeddings, products
from PIL import Image
import torch
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def searchProduct(image):
    # Process the input image
    inputs = processor(images=image, return_tensors="pt", padding=True)
    with torch.no_grad():
        query_embedding = model(**inputs).image_embeds.detach().cpu().numpy()


    # Calculate cosine similarities
    similarities = []
    for id, embedding in embeddings.items():
        embedding = embedding.image_embeds.detach().cpu().numpy()
        similarity = cosine_similarity(query_embedding, embedding)
        similarities.append((id, similarity))

    closest_id, _ = max(similarities, key=lambda item: item[1])
    print(products)
    closest_id = closest_id.split("_")[0]

    product_details = products[closest_id]
    print(product_details)
    return product_details

# Example usage
if __name__ == '__main__':
    image_path = './sourceData/test.jpg'
    image = Image.open(image_path)
    product_details = searchProduct(image)
    print(product_details)