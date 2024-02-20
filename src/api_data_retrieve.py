import requests

url = "https://moviesdatabase.p.rapidapi.com/actors"

headers = {
	"X-RapidAPI-Key": "9e79a62e4dmsh5081d5b2b325cccp10440fjsn88c2207f5d7d",
	"X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params={})


if response.status_code == 200:
    data = response.json()
    # Process the data returned from the API
else:
    print("Error connecting to the API:", response.status_code)
    
print(data)
