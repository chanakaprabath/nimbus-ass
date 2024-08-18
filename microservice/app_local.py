from flask import Flask, request, jsonify
import geopandas as gpd
from azure.storage.blob import BlobServiceClient
import psycopg2
import io
import os

app = Flask(__name__)# Initialize Flask app

# Azure Blob Storage connection details
connect_str = 'DefaultEndpointsProtocol=https;AccountName=nimbusuk;AccountKey=xYsPV/pxUu4bhReVpFn4idHxI5LkKYWvHvKpcbg4AlSuHw4rYw2NPagnC8Imr5fPwBQcCgY42ZS4+AStIxpLyA==;EndpointSuffix=core.windows.net'
#################################################
db_params = {
    "host": "nimbusuk.postgres.database.azure.com",
    "dbname": "postgres",
    "user": "nimbususer",
    "password": "Chanaka@9633",
    "port": "5432",
    "sslmode": "require"
}

### Function to download the shapefile from Azure Blob Storage
def download_shapefile(container_name: str, blob_name: str):
    service_client = BlobServiceClient.from_connection_string(connect_str)# Create BlobServiceClient
    blob_client = service_client.get_blob_client(container=container_name, blob=blob_name) 
    blob_data = blob_client.download_blob() # Download the blob
    return io.BytesIO(blob_data.readall())

### Function to process the shapefile
def process_shapefile(data: io.BytesIO):
    gdf = gpd.read_file(data)# Read the shapefile
    gdf['geometry_wkt'] = gdf['geometry'].apply(lambda geom: geom.wkt) # Convert the geometry to WKT format
    gdf = gdf.drop(columns='geometry')# Drop the original geometry column

    # Connect to the PostgreSQL database using psycopg2
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    # SQL query for inserting shapefile data into the  PostgreSQL table
    insert_query = """
        INSERT INTO he_regions (name, geometry_wkt)
        VALUES (%s, %s)
    """

    # insert the data into the database
    for idx, row in gdf.iterrows():
        cursor.execute(insert_query, (row['NAME'], row['geometry_wkt']))

    conn.commit()
    cursor.close()
    conn.close()

# Flask route to handle the shapefile processing request
@app.route('/process', methods=['POST'])
def process_shapefile_endpoint():
    data = request.json# Get the request data 
    container_name = data.get('container_name')
    blob_name = data.get('blob_name')

    if not container_name or not blob_name:
        return jsonify({"error": "container_name and blob_name are required"}), 400

    try:
        shapefile_data = download_shapefile(container_name, blob_name)# Download the shapefile from Azure Blob Storage
        process_shapefile(shapefile_data)#insert its data into the PostgreSQL database
        return jsonify({"status": "success"}), 200
    except Exception as e:
        # If an error occurs, return the error message
        return jsonify({"error": str(e)}), 500

# Flask route to check the status of the service
@app.route('/status', methods=['GET'])
def status():
    # Return a simple status message indicating that the service is running
    return jsonify({"status": "Service is running"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 
