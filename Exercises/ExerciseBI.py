import time
import json

class ExerciseBI() :
	# constants
	STATE_NONE               = 0
	STATE_INSTRUCTION        = 1
	STATE_MOTION_INSTRUCTION = 2
	STATE_COUNTDOWN          = 3
	STATE_MOTION             = 4
	STATE_END                = 5

	STIMULATION_MODE_VISION = "v"
	STIMULATION_MODE_HEARING = "h"
	STIMULATION_MODE_BOTH = "b"

	INPUT_TYPE_LEFT_HAND = "lh"
	INPUT_TYPE_RIGHT_HAND = "rh"
	INPUT_TYPE_LEFT_FOOT = "lf"
	INPUT_TYPE_RIGHT_FOOT = "rf"

	# status
	isRunning = False
	state = STATE_NONE
	nexetStateTime = 0.0

	# parameters
	level = 0
	motion = 0
	signalPeriod = 0
	changeTime = 0

	# motion setting
	motionSetting = None

	# instructions
	exerciseStartMessageSequence = [
		"BI 운동을 시작합니다.",
		"각 동작에 따라 시각/청각 자극이\n주기적으로 주어집니다.",
		"주어진 자극에 맞게\n양 손 또는 양 발을\n사용하여 입력하세요."
	]

	def __init__(self, outfit, balanceUI) :
		self.outfit = outfit
		self.balanceUI = balanceUI

		file = open("Resources/exercise_bi_setting.json", "r")
		self.motionSetting = json.loads(file.read())
		file.close()
		print(self.motionSetting)

	def start(self) :
		self.isRunning = True

		self.level = self.outfit.status["level"]
		self.motion = 0
		self.signalPeriod = self.outfit.status["signalPeriod"]
		self.changeTime = self.outfit.status["changeTime"]

		self.state = self.STATE_INSTRUCTION
		self.nexetStateTime = time.time() + len(self.exerciseStartMessageSequence) * 5.0

		self.balanceUI.setMessageSequenceWithCanvas(self.exerciseStartMessageSequence, 5.0)
		self.balanceUI.appendUpdateEventListener(self.update)

		print("Exercise BI is started")

	def stop(self) :
		self.isRunning = False
		self.balanceUI.removeUpdateEventListener(self.update)
		self.balanceUI.clearHelpText()
		self.balanceUI.clearCanvas()
		print("Exercise BI is stopped")

	def startMotion(self, motion) :
		pass

	def update(self) :
		if not self.isRunning :
			return

		if   self.state == self.STATE_NONE :
			return

		elif self.state == self.STATE_INSTRUCTION :
			pass

		elif self.state == self.STATE_MOTION_INSTRUCTION :
			pass

		elif self.state == self.STATE_COUNTDOWN :
			pass

		elif self.state == self.STATE_MOTION :
			pass

		elif self.state == self.STATE_END :
			return
