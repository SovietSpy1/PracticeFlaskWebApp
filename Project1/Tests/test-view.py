import requests
import json

try:
	URLclear = "http://127.0.0.1:5000/clear"
	r_clear = requests.get(url = URLclear)

	URL = "http://127.0.0.1:5000/create_user"
	PARAMS = {'first_name': 'James', 'last_name': 'Mariani', 'username': 'james.mariani', 'email_address': 'james@mariani.com', 'password': 'Examplepassword1', 'salt': 'FE8x1gO+7z0B'}

	r = requests.post(url = URL, data = PARAMS)
	data = r.json()

	URLLogin = "http://127.0.0.1:5000/login"
	LOGINPARAMS = {'username': 'james.mariani', 'password': 'Examplepassword1'}

	r_login = requests.post(url = URLLogin, data = LOGINPARAMS)
	login_data = r_login.json()
	print(login_data)

	URLView = "http://127.0.0.1:5000/view"
	VIEWPARAMS = {'jwt': login_data['jwt']}
	print(login_data['jwt'])
	r_view = requests.post(url = URLView, data = VIEWPARAMS)
	view_data = r_view.json()
	print(view_data)
	solution = {"status": 1, "data": {"username": "james.mariani", "email_address": "james@mariani.com", "first_name": "James", "last_name": "Mariani"}}
		
	for key in solution:
		if solution[key] != view_data[key]:
			print('Test Failed')
			quit()

	print('Test Passed')
except:
	print('Test Failed')