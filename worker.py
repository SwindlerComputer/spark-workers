from flask import Flask, request
import requests
import json
from google.cloud import secretmanager

app = Flask(__name__)

# Function to retrieve the API key from Cloud Secret Manager
def get_api_key():
    project_id = "resolute-mote-408120"
    secret_id = "compute-api-key"

    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    
    try:
        response = client.access_secret_version(name=name)
        return response.payload.data.decode("UTF-8")
    except Exception as e:
        # Handle exceptions (e.g., Secret version not found)
        print(f"Error retrieving secret: {e}")
        return None

@app.route("/")
def hello():
    return "Add workers to the Spark cluster with a POST request to add"

@app.route("/test")
def test():
    return get_api_key()

@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        return "Use post to add"  # replace with form template
    else:
        token = get_api_key()
        if token is None:
            return "Error: Unable to retrieve API key"
            
        num = request.form.get('num')
        if num is None:
            return "Error: 'num' parameter missing in form data"
            
        ret = add_worker(token, num)
        return ret

def add_worker(token, num):
    tdata = request.json
    tdata['name'] = 'slave' + str(num)
    data = json.dumps(tdata)
    url = 'https://www.googleapis.com/compute/v1/projects/resolute-mote-408120/zones/europe-west1-b/instances'
    
    headers = {"Authorization": "Bearer " + token, "Content-Type": "application/json"}
    resp = requests.post(url, headers=headers, json=tdata)
    
    if resp.status_code == 200:
        return "Done"
    else:
        print(resp.content)
        return f"Error\n{resp.content.decode('utf-8')}\n\n\n{data}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080')
