import requests

API_URL = "https://api-inference.huggingface.co/models/yanekyuk/bert-keyword-extractor"
headers = {"Authorization": "Bearer xxxxxxxxxxxxxxxxxxxxx"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()
	
output = query({
	"inputs": "My name is Sarah Jessica Parker but you can call me Jessica",
})

print(output)
