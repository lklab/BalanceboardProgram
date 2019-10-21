import BalanceModules.Globals as Globals

class Outfit :
	status = {}
	command = {}
	newCommand = False

	def __init__(self) :
		# TODO initialize parameters from file

		self.status["id"] = -1							# integer
		self.status["exercise"] = Globals.EXERCISE_NONE # string
		self.status["level"] = 0						# integer
		self.status["motion"] = 0						# integer
		self.status["signalPeriod"] = 1000				# integer
		self.status["changeTime"] = 5					# integer

		self.command["type"] = Globals.COMMAND_NONE		 # integer
		self.command["exercise"] = Globals.EXERCISE_NONE # string
		self.command["level"] = 0						 # integer
		self.command["signalPeriod"] = 0				 # integer
		self.command["changeTime"] = 0					 # integer
