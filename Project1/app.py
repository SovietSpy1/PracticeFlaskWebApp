import sqlite3
import os

from flask import Flask, request
import hashlib
import hmac
import json
import base64
app = Flask(__name__)
db_name = "project1.db"
sql_file = "project1.sql"
db_flag = False
def create_db():
	conn = sqlite3.connect(db_name)
	try:
		with open(sql_file, 'r') as sql_startup:
			init_db = sql_startup.read()
		cursor = conn.cursor()
		cursor.executescript(init_db)
		conn.commit()
		conn.close()
		global db_flag
		db_flag = True
		return conn
	except:
		conn.close()

def get_db():
	if not db_flag:
		create_db()
	conn = sqlite3.connect(db_name)
	return conn

@app.route('/', methods=(['GET']))
def index():
	conn = get_db()
	try:
		cursor = conn.cursor()
		cursor.execute("SELECT * FROM accounts;")
		result = cursor.fetchall()
		conn.close()
		return result
	except:
		conn.close()
@app.route('/view', methods = (['POST']))
def view():
	conn = get_db()
	try:
		cursor = conn.cursor()
		result = request.form
		jwt = result['jwt']
		jsonObj = {
			"status": 1,
			"data": {}
		}
		payload = decode_jwt(jwt)
		username = payload.get('username')
		if(createJWT(username) != jwt or payload.get('access') != 'True'):
			conn.close()
			jsonObj['status'] = 2
			jsonObj['data'] = "NULL"
			return json.dumps(jsonObj)
		cursor.execute("SELECT username, email_address, first_name, last_name FROM accounts WHERE username = ?;", (username,))
		list = cursor.fetchone()
		username, email_address, first_name, last_name = list
		jsonObj['data']['username'] = username
		jsonObj['data']['email_address'] = email_address
		jsonObj['data']['first_name'] = first_name
		jsonObj['data']['last_name'] = last_name
		return json.dumps(jsonObj)
	except:
		conn.close()
		jsonObj['status'] = 2
		jsonObj['data'] = "NULL"
		return json.dumps(jsonObj)


@app.route('/clear', methods=(['GET']))
def clear():
	conn = get_db()
	try:
		cursor = conn.cursor()
		cursor.execute("DROP TABLE IF EXISTS accounts;")
		global db_flag
		db_flag = False
	except:
		conn.close()
def decode_jwt(jwt):
	payload = jwt.split('.')
	payload = payload[1]
	padding = len(payload) % 4
	if (padding != 0):
		payload += '=' * (4 - padding)
	payload = base64.urlsafe_b64decode(payload)
	payload = payload.decode('utf-8')
	payload = json.loads(payload)
	return payload
@app.route('/create_user', methods=(['POST']))
def create():
	global prev_passwords
	jsonObj = {'status': 1, 'pass_hash': 'NULL'}
	conn = get_db()
	try:
		cursor = conn.cursor()
		result = request.form
		first_name = result['first_name']
		last_name = result['last_name']
		username = result['username']
		email_address = result['email_address']
		password = result['password']
		salt = result['salt']
		cursor.execute("SELECT * FROM accounts WHERE username = ?;", (username, ))
		if (cursor.fetchone() != None):
			conn.close()
			jsonObj['status'] = 2
			return json.dumps(jsonObj)
		cursor.execute("SELECT * FROM accounts WHERE email_address = ?;", (email_address,))
		if (cursor.fetchone() != None):
			conn.close()
			jsonObj['status'] = 3
			return json.dumps(jsonObj)
		if (~(len(password) >= 8 &
			  any(char.islower() for char in password) and
			  any(char.isupper() for char in password) and
			  any(char.isdigit() for char in password) and
			  ~password.__contains__(username) and
			  ~password.__contains__(first_name) and
			  ~password.__contains__(last_name))):
			conn.close()
			jsonObj['status'] = 4
			return json.dumps(jsonObj)
		password = str(password) + str(salt)
		password = hashlib.sha256(password.encode()).hexdigest()
		jsonObj['pass_hash'] = password
		cursor.execute("INSERT INTO prevPasswords VALUES(?,?);", (username, password))
		params = (first_name, last_name, username, email_address, password, salt)
		cursor.execute("INSERT INTO accounts VALUES(?, ?, ?, ?, ?, ?);", params)
		conn.commit()
		conn.close()
		return json.dumps(jsonObj)
	except:
		jsonObj['status'] = 2
		jsonObj['pass_has'] = "NULL"
		conn.close()
		return json.dumps(jsonObj)


@app.route('/login', methods=(['POST']))
def login():
	JWT = {'status': 1, 'jwt': 'NULL'}
	result = request.form
	username = result['username']
	login_password = result['password']
	conn = get_db()
	cursor = conn.cursor()
	cursor.execute("SELECT salt FROM accounts WHERE username = ?;", (username,))
	user_check = cursor.fetchone()
	if (user_check is None):
		JWT['status'] = 2
		return json.dumps(JWT)
	salt = user_check[0]
	login_password= str(login_password) + str(salt)
	login_password_hash = hashlib.sha256(login_password.encode()).hexdigest()
	cursor.execute("SELECT * FROM accounts WHERE password = ? AND username = ?;", (login_password_hash, username))
	pass_check = cursor.fetchone()
	if (pass_check is None):
		JWT['status']=2
		return json.dumps(JWT)
	conn.close()
	JWT['jwt'] = createJWT(username)
	return json.dumps(JWT)
def createJWT(username):
	JWTHeader = {
		"alg": "HS256",
		"typ": "JWT"
	}
	json_header = json.dumps(JWTHeader).encode()
	header_encoded = base64.urlsafe_b64encode(json_header)
	JWTPayload = {
		"username": username,
		"access": "True"
	}
	json_payload = json.dumps(JWTPayload).encode()
	payload_encoded = base64.urlsafe_b64encode(json_payload)
	secret = b"QZkRdigqi2iRe0DcfUnYYML7eZx2yKbC"
	message = header_encoded + b'.' + payload_encoded
	signature = hmac.new(secret, message, hashlib.sha256).hexdigest()
	token = (header_encoded + b'.' + payload_encoded + b'.').decode() + signature
	return token
@app.route('/update', methods = (['POST']))
def update():
	status = {'status': 1}
	conn = get_db()
	cursor = conn.cursor()
	result = request.form
	username = result.get('username')
	new_username = result.get('new_username')
	password = result.get('password')
	new_password = result.get('new_password')
	jwt = result.get('jwt')
	payload = ""
	payusername = ""
	access = ""
	try:
		payload = decode_jwt(jwt)
		payusername = payload.get('username')
		access = payload.get('access')
	except:
		conn.close()
		status['status'] = 3
		return json.dumps(status)
	cursor.execute("SELECT * FROM accounts WHERE username = ?;", (payusername,))
	user_check = cursor.fetchone()
	if (jwt != createJWT(payusername)):
		status['status']=3
		return json.dumps(status)
	if ((access != "True") or (user_check is None)):
		status['status'] = 3
		return json.dumps(status)

	if (new_username is not None):
		cursor.execute("SELECT username FROM accounts WHERE username = ?;", (new_username,))
		if (cursor.fetchone() is not None):
			status['status'] = 2
			return json.dumps(status)
		if (username != payusername):
			status['status'] = 2
			return json.dumps(status)
		cursor.execute("SELECT username FROM accounts WHERE username = ?;", (username,))
		user_check = cursor.fetchone()
		if (user_check is None):
			conn.close()
			status['status'] = 2
			return json.dumps(status)
		cursor.execute("UPDATE accounts SET username = ? WHERE username = ?;", (new_username, username))
		conn.commit()
		conn.close()
		return json.dumps(status)

	if (new_password is None):
		conn.close()
		status['status'] = 2
		return json.dumps(status)
	cursor.execute('SELECT salt FROM accounts WHERE username = ?;', (payusername,))
	salt = cursor.fetchone()
	if (salt is None):
		status['status'] = 2
		conn.close()
		return json.dumps(status)
	salt = salt[0]
	password = str(password) + str(salt)
	password_hash = hashlib.sha256(password.encode()).hexdigest()
	cursor.execute("SELECT * FROM accounts WHERE password = ? AND username = ?;", (password_hash,payusername))
	pass_check = cursor.fetchone()
	if (pass_check is None):
		conn.close()
		status['status'] = 2
		return json.dumps(status)
	new_password = str(new_password) + str(salt)
	new_password_hash = hashlib.sha256(new_password.encode()).hexdigest()
	try:
		cursor.execute("INSERT INTO prevPasswords VALUES(?, ?);", (payusername, new_password_hash))
	except:
		conn.close()
		status['status'] = 2
		return json.dumps(status)
	cursor.execute("UPDATE accounts SET password = ? WHERE password = ?;", (new_password_hash, password_hash))
	conn.commit()
	conn.close()
	return json.dumps(status)