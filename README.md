# Shapefile Processing Microservice

This microservice downloads shapefiles from Azure Blob Storage, processes them using GeoPandas, and stores the processed data into a PostgreSQL database. It is built with Flask and can be run locally.

## Prerequisites

Before running the microservice, make sure you have the following installed:

- Python 3.8 or higher
- pip (Python package installer)

You will also need:

- Access to an Azure Blob Storage account.
- Access to a PostgreSQL database which has the he_regions table.
```
  CREATE TABLE he_regions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    geometry_wkt TEXT 
);
```

## Setup Instructions

### 1. Clone the Repository

Clone this repository to your local machine:

```
git clone https://github.com/chanakaprabath/nimbus-ass.git
cd nimbus-ass/microservice
```

### 2. Set Up Virtual Environment


```
python3 -m venv venv
```

Activate the virtual environment:

- On Windows:

```
venv\Scripts\activate
```

- On Mac/Linux:

```
source venv/bin/activate
```

### 3. Install Dependencies

Install the required Python packages using pip:

```
pip install -r requirements.txt
```

### 4. Run the Microservice

Start the Flask microservice:

```
python app_local.py
```

The service will be available at `http://127.0.0.1:5000`.

## API Endpoints

### 1. Process Shapefile

- **Endpoint:** `/process`
- **Method:** `POST`
- **Description:** Downloads and processes a shapefile from Azure Blob Storage, then stores the processed data in PostgreSQL.

- **Request Body Example:**

```json
{
  "container_name": "data",
  "blob_name": "HE_Regions.zip"
}
```

- **Response Example:**

```json
{
  "status": "success"
}
```

### 2. Service Status

- **Endpoint:** `/status`
- **Method:** `GET`
- **Description:** Returns a status message indicating that the service is running.

- **Response Example:**

```json
{
  "status": "Service is running"
}
```
