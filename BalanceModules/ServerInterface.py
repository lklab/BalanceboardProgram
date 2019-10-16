import requests, json

URL = "http://192.168.0.12:8000/plaything/"

def getRequestTest() :
	response = requests.get(URL + "fetchCommand")
	print(response.text)

def postRequestTest() :
	# setup data dictionary
	data = {}
	data["outer"] = {}
	data["outer"]["inner"] = [1, 2, 3, 4]
	data["outer"]["value"] = "broccoli"

	# request POST
	response = requests.post(URL + "updateStatus", data=json.dumps(data))

