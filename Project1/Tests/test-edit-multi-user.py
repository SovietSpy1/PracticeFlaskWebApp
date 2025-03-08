import requests
import json
import os

try:
	URLclear = "http://127.0.0.1:5000/clear"
	r_clear = requests.get(url = URLclear)
	URL = "http://127.0.0.1:5000/create_user"
	PARAMS = {'first_name': 'James', 'last_name': 'Mariani', 'username': 'james.mariani', 'email_address': 'james@mariani.com', 'password': 'Examplepassword1', 'salt': '4ErH1inwG6dJW0cu'}

	r = requests.post(url = URL, data = PARAMS)
	data = r.json()
	print(data)
	if data['status'] != 1:
		print('Test Failed')
		quit()

	PARAMS = {'first_name': 'Jame', 'last_name': 'Marian', 'username': 'jmm', 'email_address': 'jmm', 'password': 'Examplepassword1', 'salt': '4ErH1inwG6dJW0cu'}

	r = requests.post(url = URL, data = PARAMS)
	data = r.json()
	print(data)
	if data['status'] != 1:
		print('Test Failed')
		quit()

	URL = "http://127.0.0.1:5000/login"
	PARAMS = {'username': 'james.mariani', 'password': 'Examplepassword1'}

	r = requests.post(url = URL, data = PARAMS)
	data = r.json()
	print(data)
	if data['status'] != 1:
		print('Test Failed')
		quit()

	URLEdit = "http://127.0.0.1:5000/update"
	EDITPARAMS = {'username': 'james.mariani', 'new_username': 'jmm', 'jwt': "eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJ1c2VybmFtZSI6ICJqYW1lcy5tYXJpYW5pIiwgImFjY2VzcyI6ICJUcnVlIn0=.e4d6e529e675f2bdd363da4c50219317375b7cc7d49da91083d1f0f09044ff89"}

	r_edit = requests.post(url = URLEdit, data = EDITPARAMS)
	edit_data = r_edit.json()
	print(edit_data)
	solution = {"status": 2}
	for key in solution:
		if solution[key] != edit_data[key]:
			print('Test Failed')
			quit()
			
	print('Test Passed')
except:
	print('Test Failed')
