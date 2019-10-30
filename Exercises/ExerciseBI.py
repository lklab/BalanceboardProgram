import time
import json

from BalanceModules.BalanceInputs import *

import pygame

RESULT_TYPE_PERFECT = 0
RESULT_TYPE_FAST    = 1
RESULT_TYPE_LATE    = 2

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

	MOTION_STATE_FRONT_HIDING = 0
	MOTION_STATE_SHOWING      = 1
	MOTION_STATE_REAR_HIDING  = 2

	MOTION_DURATION_SECOND = 30

	# status
	isRunning = False
	state = STATE_NONE
	nextStateTime = 0.0

	# motion status
	motionState = MOTION_STATE_FRONT_HIDING
	nextMotionStateTime = 0.0
	stimulationTotalCount = 0
	currentStimulationCount = 0
	signalPeriodSecond = 0.0
	signalDurationSecond = 0.0
	hidingDurationSecondHalf = 0.0

	# judgment
	signalBaseTime = 0.0
	perfectDeviationMax = 0.0
	judgmentSet = False

	# parameters
	level = 0
	motion = 0
	signalPeriod = 0
	changeTime = 0

	# motion setting
	motionSetting = None

	# UI
	currentStimulation = None

	# instructions
	exerciseStartInstructionSequence = [
		"BI 운동을 시작합니다.",
		"각 동작에 따라 시각/청각 신호가\n주기적으로 주어집니다.",
		"주어진 신호에 맞게\n양 손 또는 양 발을\n사용하여 입력하세요."
	]

	stimulationInstructionDictionary = {
		STIMULATION_MODE_BOTH    : "신호는 시/청각이\n동시에 주어집니다.",
		STIMULATION_MODE_HEARING : "신호는 청각으로 주어집니다.",
		STIMULATION_MODE_VISION  : "신호는 시각으로 주어집니다.",
	}

	inputInstructionDictionary = {
		STIMULATION_MODE_BOTH : {
			INPUT_TYPE_LEFT_HAND  : "왼쪽에서 소리가 들리고,\n화면에 파란색 원이 출력되면\n왼 손을 입력하세요",
			INPUT_TYPE_RIGHT_HAND : "오른쪽에서 소리가 들리고,\n화면에 빨간색 원이 출력되면\n오른 손을 입력하세요",
			INPUT_TYPE_LEFT_FOOT  : "왼쪽에서 소리가 들리고,\n화면에 초록색 원이 출력되면\n왼 발을 입력하세요",
			INPUT_TYPE_RIGHT_FOOT : "오른쪽에서 소리가 들리고,\n화면에 노란색 원이 출력되면\n오른 발을 입력하세요",
		},
		STIMULATION_MODE_HEARING : {
			INPUT_TYPE_LEFT_HAND  : "왼쪽에서 소리가 들리면\n왼 손을 입력하세요",
			INPUT_TYPE_RIGHT_HAND : "오른쪽에서 소리가 들리면\n오른 손을 입력하세요",
			INPUT_TYPE_LEFT_FOOT  : "왼쪽에서 소리가 들리면\n왼 발을 입력하세요",
			INPUT_TYPE_RIGHT_FOOT : "오른쪽에서 소리가 들리면\n오른 발을 입력하세요",
		},
		STIMULATION_MODE_VISION : {
			INPUT_TYPE_LEFT_HAND  : "화면에 파란색 원이 출력되면\n왼 손을 입력하세요",
			INPUT_TYPE_RIGHT_HAND : "화면에 빨간색 원이 출력되면\n오른 손을 입력하세요",
			INPUT_TYPE_LEFT_FOOT  : "화면에 초록색 원이 출력되면\n왼 발을 입력하세요",
			INPUT_TYPE_RIGHT_FOOT : "화면에 노란색 원이 출력되면\n오른 발을 입력하세요",
		},
	}

	# stimulation dictionary
	visionStumulationDictionary = {
		INPUT_TYPE_LEFT_HAND  : "blue",
		INPUT_TYPE_RIGHT_HAND : "red",
		INPUT_TYPE_LEFT_FOOT  : "green",
		INPUT_TYPE_RIGHT_FOOT : "yellow",
	}

	def __init__(self, outfit, balanceUI) :
		self.outfit = outfit
		self.balanceUI = balanceUI

		pygame.mixer.init()
		self.effect_left = pygame.mixer.Sound("test/audio_test/effect_left.wav")
		self.effect_right = pygame.mixer.Sound("test/audio_test/effect_right.wav")

		file = open("Resources/exercise_bi_setting.json", "r")
		self.motionSetting = json.loads(file.read())
		file.close()

	def start(self) :
		self.isRunning = True

		self.level = self.outfit.status["level"]
		self.motion = 1
		self.signalPeriod = self.outfit.status["signalPeriod"]
		self.changeTime = self.outfit.status["changeTime"]

		self.state = self.STATE_INSTRUCTION
		self.nextStateTime = time.time() + len(self.exerciseStartInstructionSequence) * 5.0

		self.balanceUI.setMessageSequence(self.exerciseStartInstructionSequence, 5.0)
		self.balanceUI.appendUpdateEventListener(self.update)

		print("Exercise BI is started")

	def stop(self) :
		self.isRunning = False
		self.balanceUI.removeUpdateEventListener(self.update)
		self.balanceUI.clearHelpText()
		self.balanceUI.clearCanvas()
		closeKeyboardEvent()
		print("Exercise BI is stopped")

	def update(self) :
		if not self.isRunning :
			return

		if   self.state == self.STATE_NONE :
			return

		elif self.state == self.STATE_INSTRUCTION :
			if time.time() >= self.nextStateTime :
				self.startMotionInstruction(self.motion)

		elif self.state == self.STATE_MOTION_INSTRUCTION :
			if time.time() >= self.nextStateTime :
				self.balanceUI.setCountdown(self.changeTime)

				self.state = self.STATE_COUNTDOWN
				self.nextStateTime = self.nextStateTime + self.changeTime

		elif self.state == self.STATE_COUNTDOWN :
			if time.time() >= self.nextStateTime :
				# initialize motion variables
				# timing variables
				self.signalPeriodSecond = self.signalPeriod / 1000.0
				self.signalDurationSecond = self.signalPeriodSecond * \
						self.motionSetting[str(self.level)]["perfectDuration"] / 1000.0
				self.hidingDurationSecondHalf = (self.signalPeriodSecond - self.signalDurationSecond) / 2.0

				# stimulation count variables
				self.stimulationTotalCount = int(self.MOTION_DURATION_SECOND / self.signalPeriodSecond)
				self.currentStimulationCount = 0

				# motion state variables
				self.motionState = self.MOTION_STATE_FRONT_HIDING
				self.nextMotionStateTime = time.time() + self.hidingDurationSecondHalf

				# judgment variables
				self.perfectDeviationMax = self.signalDurationSecond / 2.0
				self.signalBaseTime = self.nextMotionStateTime + self.perfectDeviationMax
				self.judgmentSet = False

				# normal state variables
				self.state = self.STATE_MOTION

				# open keyboard event
				openKeyboardEvent()
				flushKeyboardEvent()

		elif self.state == self.STATE_MOTION :
			# judgment
			if not self.judgmentSet :
				key = getKeyboardEvent()
				if key != -1 :
					deviation = time.time() - self.signalBaseTime
					if abs(deviation) < self.perfectDeviationMax :
						self.balanceUI.showResponseResult(RESULT_TYPE_PERFECT)
					elif deviation < 0 :
						self.balanceUI.showResponseResult(RESULT_TYPE_FAST)
					else :
						self.balanceUI.showResponseResult(RESULT_TYPE_LATE)
					self.judgmentSet = True

			# state check
			if time.time() >= self.nextMotionStateTime :
				if self.motionState == self.MOTION_STATE_FRONT_HIDING :
					self.showStimulation(self.motion, self.currentStimulationCount)
					self.motionState = self.MOTION_STATE_SHOWING
					self.nextMotionStateTime = self.nextMotionStateTime + self.signalDurationSecond
					self.effect_left.play()

				elif self.motionState == self.MOTION_STATE_SHOWING :
					self.hideStumulation()
					self.currentStimulationCount = self.currentStimulationCount + 1
					self.motionState = self.MOTION_STATE_REAR_HIDING
					self.nextMotionStateTime = self.nextMotionStateTime + self.hidingDurationSecondHalf

				elif self.motionState == self.MOTION_STATE_REAR_HIDING :
					self.balanceUI.clearCanvas()

					# motion end check
					if self.currentStimulationCount < self.stimulationTotalCount :
						# prepare next stimulus
						self.motionState = self.MOTION_STATE_FRONT_HIDING
						self.nextMotionStateTime = self.nextMotionStateTime + self.hidingDurationSecondHalf
						self.signalBaseTime = self.signalBaseTime + self.signalPeriodSecond
						self.judgmentSet = False
						flushKeyboardEvent()
					else :
						# level end check
						if self.motion < len(self.motionSetting[str(self.level)]["stimulations"]) :
							# prepare next motion
							self.motion = self.motion + 1
							self.startMotionInstruction(self.motion)

							self.outfit.status["motion"] = self.motion
							self.balanceUI.setMotionText("동작 " + str(self.outfit.status["motion"]))
						else :
							# end of level
							self.state = self.STATE_END
							self.outfit.status["motion"] = 0
							self.balanceUI.setMotionText("완료")
							self.balanceUI.setHelpText("모든 동작을 마쳤습니다.")
							closeKeyboardEvent()

		elif self.state == self.STATE_END :
			return

	def startMotionInstruction(self, motion) :
		instruction = self.getMotionInstruction(motion)
		self.balanceUI.setMessageSequence(instruction, 5.0)

		self.state = self.STATE_MOTION_INSTRUCTION
		self.nextStateTime = time.time() + len(instruction) * 5.0

		# close keyboard event
		closeKeyboardEvent()

	def getMotionInstruction(self, motion) :
		instruction = []
		stimulation = self.motionSetting[str(self.level)]["stimulations"][motion-1]
		inputs = self.motionSetting[str(self.level)]["inputs"][motion-1]

		instruction.append(str(motion) + "번 동작을 준비합니다.")
		instruction.append(self.stimulationInstructionDictionary[stimulation])

		for inputType in inputs :
			instruction.append(self.inputInstructionDictionary[stimulation][inputType])

		instruction.append("그럼 시작하겠습니다.")

		return instruction

	def showStimulation(self, motion, index) :
		stimulation = self.motionSetting[str(self.level)]["stimulations"][motion-1]
		inputs = self.motionSetting[str(self.level)]["inputs"][motion-1]
		inputType = inputs[index % len(inputs)]

		# TODO check hearing stimulation

		self.currentStimulation = self.balanceUI.showStimulation(self.visionStumulationDictionary[inputType])

	def hideStumulation(self) :
		if self.currentStimulation :
			self.balanceUI.deleteObject(self.currentStimulation)
			self.currentStimulation = None
