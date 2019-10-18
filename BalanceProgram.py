#!/usr/bin/env python3

import time
import threading
try :
    import queue
except ImportError :
    import Queue as queue

from BalanceModules.BalanceUI import *

state = 0
nextTime = 0.0

def update() :
	global balanceUI
	global state
	global nextTime

	if state is 0 :
		balanceUI.setOutfitID(20)
		balanceUI.setStateText("밸런스 운동", "level 1-1(응용)", "동작 12")
		# balanceUI.setHelpMessage("준비하세요.")
		# balanceUI.removeUpdateEventListener(update)

		state = 3
		nextTime = time.time() + 1.0

	elif state is 1 :
		if time.time() >= nextTime :
			balanceUI.showStimulationWithCanvas("blue")
			balanceUI.showResponseResult(PHOTO_IMAGE_TYPE_LATE)
			state = 2
			nextTime = time.time() + 1.0

	elif state is 2 :
		if time.time() >= nextTime :
			balanceUI.clearCanvas()
			state = 3
			nextTime = time.time() + 1.0

	elif state is 3 :
		if time.time() >= nextTime :
			balanceUI.setCountdownWithCanvas(2)
			state = 1
			nextTime = time.time() + 2.0

balanceUI = BalanceUI()
balanceUI.showFrameRate(True)
balanceUI.appendUpdateEventListener(update)
balanceUI.mainloop()
