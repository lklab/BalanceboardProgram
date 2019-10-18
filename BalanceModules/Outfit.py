import BalanceModules.Globals as Globals

class Outfit :
	status = {}
	command = {}
	newCommand = False

	def __init__(self) :
		# TODO initialize parameters from file

		self.status["id"] = -1
		self.status["exercise"] = Globals.EXERCISE_NONE
		self.status["level"] = 0
		self.status["motion"] = 0
		self.status["signalPeriod"] = 1000
		self.status["changeTime"] = 5

		self.command["type"] = Globals.COMMAND_NONE
		self.command["exercise"] = Globals.EXERCISE_NONE
		self.command["level"] = 0
		self.command["signalPeriod"] = 0
		self.command["changeTime"] = 0
