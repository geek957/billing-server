import os
import pandas as pd

def generate_csv_from_filenames(folder_path='./sourceDataVideos', output_csv='temp.csv'):
    # List all files in the folder
    file_names = os.listdir(folder_path)

    # Prepare data for the CSV
    data = []
    for file_name in file_names:
        # Split the file name by '_'
        parts = file_name.split('_')
        if len(parts) >= 3:
            file_id = parts[0]
            name = parts[1]
            price = parts[2].split('.')[0]  # Remove the file extension
            data.append({'id': file_id, 'name': name, 'price': price})

    # Create a DataFrame and save it as a CSV file
    df = pd.DataFrame(data)
    df.to_csv(output_csv, index=False)

def process_csv(input_csv='temp.csv', output_csv='output.csv'):
    # Read the CSV file
    df = pd.read_csv(input_csv)

    # Replace '-' with space in the 'name' column
    df['name'] = df['name'].str.replace('-', ' ')

    # Order the data by 'id'
    df = df.sort_values(by='id')

    # Save the updated DataFrame to a new CSV file
    df.to_csv(output_csv, index=False)

# Example usage
if __name__ == '__main__':
    generate_csv_from_filenames()
    process_csv(input_csv='temp.csv', output_csv='output.csv')