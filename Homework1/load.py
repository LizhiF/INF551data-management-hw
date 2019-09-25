import requests
import json
import pandas as pd 
import sys 
import os
import string

avoidable = list(string.printable[62:])

df_name = sys.argv[1]

if not os.path.exists("./"+df_name):
	print("CSV File doesn't exist")
else:
	# Read data into a dataframe
	resto = pd.read_csv("./"+df_name,chunksize = 1000)
	
inverted_index = {}
for idx,chunk in enumerate(resto):
	chunk = chunk[["serial_number","facility_name","score"]]
	serial_url = 'https://inf551-ed1c3.firebaseio.com/restaurants/key_{}.json'.format(str(idx).zfill(4))
	resp = requests.put(serial_url,chunk.set_index('serial_number').to_json(orient='index'))
	print(idx," hit ",resp.reason)

	for df in chunk.itertuples():
		word = "".join((char if char.isalpha() else " ") for char in df.facility_name).split()
		#word = df.facility_name.split(" ") 
		for w in word: 
			w = w.lower()
			for i in avoidable:
				if i in w:
					w = w.replace(i,"")
				else:
					w = w
			if w not in inverted_index.keys():
				inverted_index[w] = [] 
			inverted_index[w].append([idx,df.serial_number])
#del inverted_index[""]

inverted_url = "https://inf551-ed1c3.firebaseio.com/restaurants/inverted_index.json"
response = requests.put(inverted_url,json.dumps(inverted_index))
print("Second hit",response.reason)

response = requests.get("https://inf551-ed1c3.firebaseio.com/restaurants/inverted_index.json?print=pretty")
print(response.json())