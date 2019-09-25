import requests
import json
import pandas as pd 
import sys 
import os
import string

print('Number of arguments: {}'.format(len(sys.argv)))
print('Argument(s) passed: {}'.format(str(sys.argv)))
keywords = sys.argv[1:]
print("Keywords are :- 	",keywords)

output = {}
for key in keywords:
	url = "https://inf551-ed1c3.firebaseio.com/restaurants/inverted_index/{}.json".format(key)
	response = requests.get(url)
	if response.json() == None:
		print("No such keyword found")
	else:
		serial_data = list(response.json())
		for arr in serial_data:
			chunk_no = arr[0] 
			serial_number = arr[1]
			output[serial_number] = {}
			retrieve_url = "https://inf551-ed1c3.firebaseio.com/restaurants/key_{}/{}/.json".format(str(chunk_no).zfill(4),serial_number)
			response = requests.get(retrieve_url)
			output[serial_number] = response.json()
print(output)