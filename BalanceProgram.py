#!/usr/bin/env python3

import time
import threading
try :
    import queue
except ImportError :
    import Queue as queue

from BalanceModules.BalanceUI import BalanceUI
from BalanceModules.Outfit import Outfit
import BalanceModules.ServerInterface as ServerInterface
import BalanceModules.Globals as Globals

from Exercises.ExerciseBI          import ExerciseBI
from Exercises.ExerciseDirectional import ExerciseDirectional
from Exercises.ExerciseBalance     import ExerciseBalance
from Exercises.ExerciseRotation    import ExerciseRotation

################################################################################
#                                   constants                                  #
################################################################################
SERVER_STATE_DISCONNECTED = 0
SERVER_STATE_CONNTECTED = 1

COMMAND_CODE_CONNECTION = 0
COMMAND_CODE_COMMAND = 1

EXERCISE_TO_STRING = {
	Globals.EXERCISE_NONE        : "대기 중",
	Globals.EXERCISE_BI          : "BI 운동",
	Globals.EXERCISE_DIRECTIONAL : "방향성 운동",
	Globals.EXERCISE_BALANCE     : "밸런스 운동",
	Globals.EXERCISE_ROTATION    : "회전 운동",
}

################################################################################
#                             server communication                             #
################################################################################
def serverCommunicationTask() : # running in communication thread
	global outfit
	global serverState, SERVER_STATE_DISCONNECTED, SERVER_STATE_CONNTECTED
	global commandQueue, COMMAND_CODE_CONNECTION, COMMAND_CODE_COMMAND
	global taskLock, taskEnabledFlag

	if serverState is SERVER_STATE_DISCONNECTED :
		if ServerInterface.requestId(outfit) :
			print("outfit ID received: " + str(outfit.status["id"]))
			serverState = SERVER_STATE_CONNTECTED
			commandQueue.put((COMMAND_CODE_CONNECTION, outfit.status["id"]))

	elif serverState is SERVER_STATE_CONNTECTED :
		with taskLock :
			if ServerInterface.updateStatus(outfit) :
				if outfit.newCommand and commandQueue.empty() :
					if ServerInterface.fetchCommand(outfit) :
						print("command received: " + str(outfit.command))
						if outfit.command["type"] != Globals.COMMAND_NONE :
							commandQueue.put((COMMAND_CODE_COMMAND, outfit.command.copy()))

			else : # updateStatus is failed
				print("server is disconnected")
				serverState = SERVER_STATE_DISCONNECTED
				commandQueue.put((COMMAND_CODE_CONNECTION, -1))
		# end of with taskLock

	if taskEnabledFlag :
		threading.Timer(1, serverCommunicationTask).start()

def serverResponseHandler() : # running in UI thread
	global balanceUI, outfit
	global EXERCISE_TO_STRING

	global commandQueue, COMMAND_CODE_CONNECTION, COMMAND_CODE_COMMAND
	global currentExercise, exerciseDictionary

	global taskLock

	with taskLock :
		try :
			code, data = commandQueue.get(False)

			if code is COMMAND_CODE_CONNECTION :
				balanceUI.setOutfitID(data)
				if data is -1 :
					balanceUI.setStateText("대기 중", "", "")

			elif code is COMMAND_CODE_COMMAND :
				if data["type"] is Globals.COMMAND_PARAMETER :
					outfit.status["signalPeriod"] = data["signalPeriod"]
					outfit.status["changeTime"]   = data["changeTime"]

				elif data["type"] is Globals.COMMAND_START :
					outfit.status["exercise"]     = data["exercise"]
					outfit.status["level"]        = data["level"]
					outfit.status["motion"]       = 1
					outfit.status["signalPeriod"] = data["signalPeriod"]
					outfit.status["changeTime"]   = data["changeTime"]

					balanceUI.setStateText(
						EXERCISE_TO_STRING[outfit.status["exercise"]],
						"레벨 " + str(outfit.status["level"]),
						"동작 " + str(outfit.status["motion"]))

					if currentExercise is not None :
						currentExercise.stop()
					currentExercise = exerciseDictionary[outfit.status["exercise"]]
					currentExercise.start()
					
				elif data["type"] is Globals.COMMAND_STOP :
					outfit.status["exercise"]     = Globals.EXERCISE_NONE
					outfit.status["level"]        = 0
					outfit.status["motion"]       = 0
					balanceUI.setStateText("대기 중", "", "")

					currentExercise.stop()
					currentExercise = None

		except queue.Empty :
			pass # there is no command

################################################################################
#                             initialization script                            #
################################################################################
print("initialize outfit variables.")
outfit = Outfit()

print("initialize server communication variables.")
serverState = SERVER_STATE_DISCONNECTED
commandQueue = queue.Queue()

print("starting server communication task.")
taskLock = threading.Lock()
taskEnabledFlag = True
threading.Timer(5, serverCommunicationTask).start()

print("setup UI.")
balanceUI = BalanceUI()
balanceUI.showFrameRate(False)
balanceUI.setOutfitID(-1)
balanceUI.setStateText("대기 중", "", "")
balanceUI.appendUpdateEventListener(serverResponseHandler)

print("setup exercises.")
currentExercise = None
exerciseDictionary = {
	Globals.EXERCISE_NONE        : None,
	Globals.EXERCISE_BI          : ExerciseBI(outfit, balanceUI),
	Globals.EXERCISE_DIRECTIONAL : ExerciseDirectional(outfit, balanceUI),
	Globals.EXERCISE_BALANCE     : ExerciseBalance(outfit, balanceUI),
	Globals.EXERCISE_ROTATION    : ExerciseRotation(outfit, balanceUI),
}

print("starting UI.")
balanceUI.mainloop()

print("terminating server communication task.")
taskEnabledFlag = False
