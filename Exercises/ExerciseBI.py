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

	MOTION_STATE_HIDING  = 0
	MOTION_STATE_SHOWING = 1

	MOTION_DURATION_SECOND = 30

	# status
	isRunning = False
	state = STATE_NONE
	nextStateTime = 0.0

	# motion status
	motionState = MOTION_STATE_HIDING
	nextMotionStateTime = 0.0
	stimulationTotalCount = 0
	currentStimulationCount = 0
	signalPeriodSecond = 0.0
	signalDurationSecond = 0.0
	hidingDurationSecond = 0.0

	# parameters
	level = 0
	motion = 0
	signalPeriod = 0
	changeTime = 0

	# motion setting
	motionSetting = None

	# instructions
	exerciseStartInstructionSequence = [
		"BI 운동을 시작합니다.",
		"각 동작에 따라 시각/청각 자극이\n주기적으로 주어집니다.",
		"주어진 자극에 맞게\n양 손 또는 양 발을\n사용하여 입력하세요."
	]

	stimulationInstructionDictionary = {
		STIMULATION_MODE_BOTH    : "자극은 시/청각이\n동시에 주어집니다.",
		STIMULATION_MODE_HEARING : "자극은 청각으로 주어집니다.",
		STIMULATION_MODE_VISION  : "자극은 시각으로 주어집니다.",
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

		self.balanceUI.setMessageSequenceWithCanvas(self.exerciseStartInstructionSequence, 5.0)
		self.balanceUI.appendUpdateEventListener(self.update)

		print("Exercise BI is started")

	def stop(self) :
		self.isRunning = False
		self.balanceUI.removeUpdateEventListener(self.update)
		self.balanceUI.clearHelpText()
		self.balanceUI.clearCanvas()
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
				self.balanceUI.setCountdownWithCanvas(self.changeTime)

				self.state = self.STATE_COUNTDOWN
				self.nextStateTime = self.nextStateTime + self.changeTime

		elif self.state == self.STATE_COUNTDOWN :
			if time.time() >= self.nextStateTime :
				self.balanceUI.showCanvasOrHelpText(True)

				# initialize motion variables
				self.signalPeriodSecond = self.signalPeriod / 1000.0
				self.signalDurationSecond = self.signalPeriodSecond * \
						self.motionSetting[str(self.level)]["perfectDuration"] / 1000.0
				self.hidingDurationSecond = self.signalPeriodSecond - self.signalDurationSecond

				self.stimulationTotalCount = int(self.MOTION_DURATION_SECOND / self.signalPeriodSecond)
				self.currentStimulationCount = 0
				self.motionState = self.MOTION_STATE_HIDING
				self.nextMotionStateTime = time.time() + self.hidingDurationSecond

				self.state = self.STATE_MOTION

		elif self.state == self.STATE_MOTION :
			if time.time() >= self.nextMotionStateTime :
				if self.motionState == self.MOTION_STATE_HIDING :
					self.showStimulation(self.motion, self.currentStimulationCount)
					self.motionState = self.MOTION_STATE_SHOWING
					self.nextMotionStateTime = self.nextMotionStateTime + self.signalDurationSecond

				elif self.motionState == self.MOTION_STATE_SHOWING :
					self.hideStumulation()
					self.currentStimulationCount = self.currentStimulationCount + 1

					if self.currentStimulationCount < self.stimulationTotalCount :
						self.motionState = self.MOTION_STATE_HIDING
						self.nextMotionStateTime = self.nextMotionStateTime + self.hidingDurationSecond
					else :
						if self.motion < len(self.motionSetting[str(self.level)]["stimulations"]) :
							self.motion = self.motion + 1
							self.startMotionInstruction(self.motion)

							self.outfit.status["motion"] = self.motion
							self.balanceUI.setMotionText("동작 " + str(self.outfit.status["motion"]))
						else :
							self.state = self.STATE_END
							self.outfit.status["motion"] = 0
							self.balanceUI.clearCanvas()
							self.balanceUI.setMotionText("완료")
							self.balanceUI.setHelpMessageWithCanvas("모든 동작을 마쳤습니다.")

		elif self.state == self.STATE_END :
			return

	def startMotionInstruction(self, motion) :
		instruction = self.getMotionInstruction(motion)
		self.balanceUI.setMessageSequenceWithCanvas(instruction, 5.0)

		self.state = self.STATE_MOTION_INSTRUCTION
		self.nextStateTime = time.time() + len(instruction) * 5.0

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
		inputType = self.motionSetting[str(self.level)]["inputs"][motion-1][index % 2]

		# TODO check hearing stimulation

		self.balanceUI.showStimulation(self.visionStumulationDictionary[inputType])

	def hideStumulation(self) :
		self.balanceUI.clearCanvas()
