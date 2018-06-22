import requests
import json

# Create Bank
data = {'name': 'simulated_bank'}
bank = requests.post("http://localhost:8000/bank/", data=data)


# Create Loans
# ! Assuming bank id will be 1 !
data = {'title': 'loans'}
while(True):
	loan = requests.post("http://localhost:8000/bank/1/loans/", data=data)
