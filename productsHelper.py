import csv
from datetime import datetime


def getNewProductId():
    csv_filepath='output.csv'
    max_id = 0
    with open(csv_filepath, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            product_id = int(row['id'])
            if product_id > max_id:
                max_id = product_id
    return str(max_id + 1)


def addUpdateProduct(merchantId, productId, name, price, source_video_path, is_deleted=False):
    csv_filepath='output.csv'
    current_time = datetime.now().isoformat()
    product_exists = False
    updated_rows = []

    # Read the CSV file and update if the product already exists
    with open(csv_filepath, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['merchantId'] == merchantId and row['id'] == productId:
                row['name'] = name
                row['source_video_path'] = source_video_path
                row['is_deleted'] = str(is_deleted).lower()
                row['lastUpdatedTime'] = current_time
                row['price'] = price
                product_exists = True
            updated_rows.append(row)

    # If the product does not exist, add it to the list
    if not product_exists:
        new_product = {
            'merchantId': merchantId,
            'id': productId,
            'name': name,
            'price': price, 
            'source_video_path': source_video_path,
            'is_deleted': str(is_deleted).lower(),
            'createdTime': current_time,
            'lastUpdatedTime': current_time
        }
        updated_rows.append(new_product)

    # Write the updated data back to the CSV file
    with open(csv_filepath, mode='w', newline='') as file:
        fieldnames = ['merchantId', 'id', 'name', 'price', 'source_video_path', 'is_deleted', 'createdTime', 'lastUpdatedTime']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_rows)


def deleteProduct(merchantId, productId):
    csv_filepath='output.csv'
    current_time = datetime.now().isoformat()
    updated_rows = []

    # Read the CSV file and mark the product as deleted
    with open(csv_filepath, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['merchantId'] == merchantId and row['id'] == productId:
                row['is_deleted'] = 'true'
                row['lastUpdatedTime'] = current_time
            updated_rows.append(row)

    # Write the updated data back to the CSV file
    with open(csv_filepath, mode='w', newline='') as file:
        fieldnames = ['merchantId', 'id', 'name', 'price', 'source_video_path', 'is_deleted', 'createdTime', 'lastUpdatedTime']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_rows)

def getProducts(merchantId, csv_filepath='output.csv'):
    products = []

    # Read the CSV file and filter products based on merchantId and is_deleted
    with open(csv_filepath, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['merchantId'] == merchantId and row['is_deleted'] == 'false':
                product = {
                    'id': row['id'],
                    'name': row['name'],
                    'price': row['price']
                }
                products.append(product)

    return products

# Example usage
if __name__ == '__main__':
    deleteProduct('1', '100001')




