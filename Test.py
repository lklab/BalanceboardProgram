#!/usr/bin/env python3

# from BalanceModules.Outfit import *
# from BalanceModules.ServerInterface import *

# outfit = Outfit()
# requestId(outfit)
# updateStatus(outfit)
# fetchCommand(outfit)
# print("command: " + str(outfit.command))

from BalanceModules.BalanceInputs import *
import time

openKeyboardEvent()

print("start to sleeping...")
time.sleep(5)
print("wake up!! let's get work!")
flushKeyboardEvent()

try :
	while True :
		key = getKeyboardEvent()
		if key != -1 :
			print("key pushed: " + str(key))
except KeyboardInterrupt :
	closeKeyboardEvent()
