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
## Instructions for Deploying the Microservice on Azure

To deploy the microservice to Azure Web App, follow these steps:

### 1. Create an Azure App Service Plan

Create a new App Service Plan with a Linux-based hosting environment:

```bash
az appservice plan create --name NimbusAppServicePlan --resource-group Nimbus-Ass --sku B1 --is-linux
```

### 2. Create an Azure Web App

Create a new Web App under the App Service Plan:

```bash
az webapp create --resource-group Nimbus-Ass --plan NimbusAppServicePlan --name UploadShapefile --runtime "PYTHON|3.9"
```

### 3. Configure Application Settings

Set up the application settings for your Azure Web App. This includes the connection string for Azure Blob Storage and PostgreSQL database credentials:

```bash
az webapp config appsettings set --resource-group Nimbus-Ass --name UploadShapefile --settings AZURE_STORAGE_CONNECTION_STRING="DefaultEndpointsProtocol=https;AccountName=nimbusuk;AccountKey=xYsPV/pxUu4bhReVpFn4idHxI5LkKYWvHvKpcbg4AlSuHw4rYw2NPagnC8Imr5fPwBQcCgY42ZS4+AStIxpLyA==;EndpointSuffix=core.windows.net" DB_HOST="nimbusuk.postgres.database.azure.com" DB_NAME="postgres" DB_USER="nimbususer" DB_PASSWORD="Chanaka@9633"
```

### 4. Deploy the Application

Deploy the application using Visual Studio Code:

1. Open Visual Studio Code.
2. Install the [Azure App Service extension] if not already installed.
3. Sign in to your Azure account within Visual Studio Code.
4. Open your project folder in Visual Studio Code (nimbus-ass/microservice/web-app).
5. In the Azure App Service extension panel, click on the "Deploy to Web App" button.
6. Select the target Web App (e.g., `UploadShapefile`) from the list.
7. Follow the prompts to deploy your application.

### 5. Access the Deployed Web App

Your Flask microservice will be available at `https://<your-web-app-name>.azurewebsites.net`. For this repository, the web app is hosted at:

```
https://uploadshapefile.azurewebsites.net
```

### 6. Verify Deployment

To verify that the deployment was successful, navigate to the URL provided by Azure and test the `/status` endpoint to ensure the microservice is running:

```bash
curl https://uploadshapefile.azurewebsites.net/status
```

You should receive a response indicating that the service is running:

```json
{
  "status": "Service is running"
}
```

## Creating and Uploading the Python Wheel

1. **Navigate to the Wheel Directory:**

    Ensure you're in the `microservice/python-wheel` directory:

    ```bash
    cd nimbus-ass/microservice/python-wheel
    ```

2. **Install Required Tools:**

    Ensure `setuptools` and `wheel` are installed:

    ```bash
    pip install setuptools wheel
    ```

3. **Create the Wheel File:**

    Run the following command to build the wheel file:

    ```bash
    python setup.py sdist bdist_wheel
    ```

    This will generate a `.whl` file in the `dist` directory.

4. **Upload the Wheel File to PyPI:**

    First, install `twine` if it's not already installed:

    ```bash
    pip install twine
    ```

    Then, upload the wheel file to PyPI:

    ```bash
    twine upload dist/*
    ```

    You'll be prompted to enter your PyPI credentials. After successful upload, your package will be available on PyPI.
5. **Installing the Package:**

   you can install the package from PyPI using pip:

    ```bash
    pip install uploadshapefile==1.0.0
    ```

6. **Verify the Package:**

    You can verify the package details on the [PyPI project page](https://pypi.org/project/uploadshapefile/1.0.0/).
# Steps for Creating and Configuring the Databricks Notebook

- Open the Azure Portal
- Navigate to the [Azure Portal](https://portal.azure.com).
- Create a Databricks Workspace
- Create a Databricks Compute Cluster
- Create a Databricks Notebook or upload the [given file](https://github.com/chanakaprabath/nimbus-ass/blob/main/pipeline/load_data.ipynb)  

### How to configure the Notebook to Install the Wheel Package and Perform Tasks

- In the first cell of the notebook, use `%pip` to install the `uploadshapefile` package:

  ```python
  %pip install uploadshapefile==1.0.0
- Then import libraries from `uploadshapefile` package:
  ```python
  from uploadshapefile import functions
  spark = SparkSession.builder.appName("Shapefile_load").getOrCreate()
  upload_result = functions.upload(container,blob)#load data
  
# Setting Up and Configuring an Azure Data Factory Pipeline

This guide will walk you through the steps to set up an Azure Data Factory (ADF) pipeline that uses a Databricks notebook to process data. The pipeline includes creating a linked service, adding activities, and setting up triggers and schedules.

## Steps to Set Up the Pipeline

- Create a New Linked Service
- Create a Pipeline
- Add Databricks Activity
- Add an If Condition Activity
     - **Expression:** Set the condition to check the output of the Databricks notebook:
       ```json
       @endsWith(substring(activity('load_data').output.runOutput, sub(lastIndexOf(activity('load_data').output.runOutput, ')'), 8), 7), 'success')
       ```
     - **If False Activities:** Add a `Fail` activity to handle failures.
- Configure the Fail Activity
     - **Message:** Use the output of the `load_data` activity to describe the failure:
       ```json
       @activity('load_data').output.runOutput
       ```
     - **Error Code:** Set an error code (e.g., `error`).

- Create a Trigger
- Add Trigger and Schedule
- Publish All Changes

## Explanation of the Pipeline

The pipeline is designed to process data using a Databricks notebook and handle errors effectively:

Below is a screenshot of the Azure Data Factory pipeline:

![Pipeline Diagram](images/pipeline.png)
1. **Databricks Notebook Activity:**
   - Executes a Databricks notebook that processes the data.
   - The notebook takes parameters for the container and blob to process.

2. **If Condition Activity:**
   - Checks the status of the notebook execution.
   - Uses the output from the notebook activity to determine if it was successful.

3. **Fail Activity:**
   - Executes if the notebook fails.
   - Logs the error message and stops the pipeline.
