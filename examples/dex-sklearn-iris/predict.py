from kserve import KServeClient

import json
import requests

HOST = "http://localhost:8080"

USERNAME = "user@example.com"
PASSWORD = "12341234"

NAMESPACE = "admin"

with requests.Session() as session:
	# Auth
	response = session.get(HOST)
	headers = {
		"Content-Type": "application/x-www-form-urlencoded",
	}

	data = {"login": USERNAME, "password": PASSWORD}
	session.post(response.url, headers=headers, data=data)
	session_cookie = session.cookies.get_dict()["authservice_session"]

	# Prepare model info and data 
	namespace = NAMESPACE
	name = "sklearn-iris"

	KServe = KServeClient()
	model = KServe.get(name, namespace=namespace)
	model_url = model['status']['url']

	inputs = json.load(open('./iris-input.json', 'r'))
	print(inputs)

	# request prediction
	# url = f"{HOST}/v1/models/{name}:predict"
	url = f"{HOST}/v2/models/{name}/infer"
	headers = {
		"Host": model_url.split("/")[-1],
	}
	cookies = {
		'authservice_session': session_cookie,
	}
	response = session.post(url, headers=headers, cookies=cookies, json=inputs)
	print(response.status_code, response.text)
