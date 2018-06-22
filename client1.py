import requests
import json

# Retrieving all loans
all_loans = requests.get("http://localhost:8000/loans/")
loans = json.loads(all_loans.text)

# for item in loans:
# 	id = item['id']
# 	url = "http://localhost:8000/loans/" + str(id) + "/recalculate/"
# 	requests.get(url)

for item in loans:
	if item['saleable'] == 1:
		if item['pd_mean'] < 1:
			if item['el_mean'] < 15000:
				requests.post("http://localhost:8000/loans/" + str(item['id']) + "/buy/", data = {'owner': 'geri'})