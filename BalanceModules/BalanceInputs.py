from ctypes import *

keyboardEvent = None

def openKeyboardEvent() :
	global keyboardEvent
	
	keyboardEvent = CDLL("./BalanceModules/BalanceInputsLibrary/keyboard_input.so")
	keyboardEvent.open_keyboard_event()

def getKeyboardEvent() :
	global keyboardEvent

	if keyboardEvent :
		return keyboardEvent.get_keyboard_event()
	else :
		return -1

def closeKeyboardEvent() :
	global keyboardEvent

	if keyboardEvent :
		keyboardEvent.close_keyboard_event()
		close_keyboard_event = None
