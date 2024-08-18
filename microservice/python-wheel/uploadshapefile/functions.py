import requests

def upload(container, shapefile):
    try:
        response = requests.post('https://uploadshapefile.azurewebsites.net/process', json={
            'container_name': container,
            'blob_name': shapefile
        })
        response.raise_for_status()  
        return response.json()
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return {"error": str(e)}

def check_status():
    try:
        response = requests.get('https://uploadshapefile.azurewebsites.net/status')
        response.raise_for_status()  
        return response.json()
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return {"error": str(e)}
