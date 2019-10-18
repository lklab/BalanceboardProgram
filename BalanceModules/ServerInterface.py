#!/usr/bin/env python3

import requests, json
import os
import traceback

import BalanceModules.Globals as Globals

URL = "http://192.168.0.12:8000/outfit/"

def requestId(outfit) :
	try :
		parameter = {}
		parameter["uuid"] = getUUID()
		parameter["signalPeriod"] = str(outfit.status["signalPeriod"])
		parameter["changeTime"] = str(outfit.status["changeTime"])

		response = requests.get(URL + "requestId", params=parameter)

		if response.status_code is 200 :
			responseData = json.loads(response.text)
			outfit.status["id"] = int(responseData["id"])
			return True

		else :
			outfit.status["id"] = -1
			print("HTTP error occurred in requestId(): " + str(response.status_code) + "\n" + str(parameter))
			return False

	except :
		outfit.status["id"] = -1
		print("requestId is failed. traceback:")
		traceback.print_exc()
		return False

def updateStatus(outfit) :
	try :
		response = requests.post(URL + "updateStatus", data=json.dumps(outfit.status))

		if response.status_code is 200 :
			responseData = json.loads(response.text)
			if responseData["newCommand"] is "0" :
				outfit.newCommand = False
			else :
				outfit.newCommand = True
			return True

		else :
			outfit.newCommand = False
			print("HTTP error occurred in updateStatus(): " + str(response.status_code) + "\n" + str(outfit.status))
			return False

	except :
		outfit.newCommand = False
		print("updateStatus is failed. traceback:")
		traceback.print_exc()
		return False

def fetchCommand(outfit) :
	try :
		parameter = {}
		parameter["id"] = str(outfit.status["id"])

		response = requests.get(URL + "fetchCommand", params=parameter)

		if response.status_code is 200 :
			responseData = json.loads(response.text)
			outfit.command = responseData
			return True

		else :
			outfit.command["type"] = Globals.COMMAND_NONE
			print("HTTP error occurred in fetchCommand(): " + str(response.status_code) + "\n" + str(parameter))
			return False

	except :
		outfit.command["type"] = Globals.COMMAND_NONE
		print("fetchCommand is failed. traceback:")
		traceback.print_exc()
		return False

def submitResult(outfit, resultCsv) :
	try :
		resultData = {}
		resultData["id"] = str(outfit.status["id"])
		resultData["exercise"] = outfit.status["exercise"]
		resultData["level"] = outfit.status["level"]
		resultData["result"] = resultCsv
		response = requests.post(URL + "submitResult", data=json.dumps(resultData))

		if response.status_code is 200 :
			return True
		else :
			print("HTTP error occurred in submitResult(): " + str(response.status_code) + "\n" + str(resultData))
			return False

	except :
		print("submitResult is failed. traceback:")
		traceback.print_exc()
		return False

def getUUID() :
	if os.path.exists("device_uuid.data") :
		file = open("device_uuid.data", "r")
		uuidStr = file.read()
		file.close()
		return uuidStr
		
	else :
		import uuid
		uuidStr = str(uuid.uuid4())
		del uuid

		file = open("device_uuid.data", "w")
		file.write(uuidStr)
		file.close()

		return uuidStr

if __name__ == '__main__' :
	from Data.Outfit import *
	outfit = Outfit()
	requestId(outfit)
