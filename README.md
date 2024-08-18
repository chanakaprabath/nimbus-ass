# Shapefile Processing Microservice

This microservice downloads shapefiles from Azure Blob Storage, processes them using GeoPandas, and stores the processed data into a PostgreSQL database. It is built with Flask and can be run locally.

## Prerequisites

Before running the microservice, make sure you have the following installed:

- Python 3.8 or higher
- pip (Python package installer)

You will also need:

- Access to an Azure Blob Storage account.
- Access to a PostgreSQL database (e.g., Azure Database for PostgreSQL).

## Setup Instructions

### 1. Clone the Repository

Clone this repository to your local machine:

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
