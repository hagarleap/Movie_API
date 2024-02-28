# import requests

# url = "https://moviesdatabase.p.rapidapi.com/actors"

# headers = {
# 	"X-RapidAPI-Key": ,
# 	"X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com"
# }

# response = requests.get(url, headers=headers, params={})


# if response.status_code == 200:
#     data = response.json()
#     # Process the data returned from the API
# else:
#     print("Error connecting to the API:", response.status_code)
    
# print(data)

import csv

movies_csv = "imdb_top_1000.csv"

with open(movies_csv, "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    



