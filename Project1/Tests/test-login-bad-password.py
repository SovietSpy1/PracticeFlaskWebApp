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

	PARAMS = {'first_name': 'James', 'last_name': 'Mariani', 'username': 'jmm', 'email_address': 'jmm@mariani.com', 'password': 'Examplepassword2', 'salt': '4ErH1inwG6dJW0cu'}

	r = requests.post(url = URL, data = PARAMS)
	data = r.json()

	URLLogin = "http://127.0.0.1:5000/login"
	LOGINPARAMS = {'username': 'jmm', 'password': 'Examplepassword2'}

	r_login = requests.post(url = URLLogin, data = LOGINPARAMS)
	login_data = r_login.json()
	print(login_data)
	URL = "http://127.0.0.1:5000/update"
	PARAMS = {"password": 'Examplepassword2', "new_password": "Examplepassword3", "jwt": login_data['jwt']}
	r = requests.post(url = URL, data = PARAMS)
	data = r.json()
	print(data)
	PARAMS = {"password": 'Examplepassword3', "new_password": "Examplepassword2", "jwt": login_data['jwt']}
	r = requests.post(url = URL, data = PARAMS)
	data = r.json()
	print(data)

	#solution = {"status": 2, "jwt": "NULL"}
		
	#for key in solution:
		#if solution[key] != login_data[key]:
			#print('Test Failed')
			#quit()
	#print('Test Passed')
except:
	print('Test Failed')
