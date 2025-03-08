import requests
import json

try: 
	URLclear = "http://127.0.0.1:5000/clear"
	r_clear = requests.get(url = URLclear)

	URL = "http://127.0.0.1:5000/create_user"
	PARAMS = {'first_name': 'James', 'last_name': 'Mariani', 'username': 'james.mariani', 'email_address': 'james@mariani.com', 'password': 'examplepassword1', 'salt': '4ErH1inwG6dJW0cu'}

	r = requests.post(url = URL, data = PARAMS)
	data = r.json()

	solution = {"status": 4, "pass_hash": "NULL"}

	for key in solution:
		if solution[key] != data[key]:
			print('Test Failed')
			quit()
			
	print('Test Passed')
except:
	print('Test Failed')