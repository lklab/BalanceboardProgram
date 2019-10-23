#!/usr/bin/env python3

from tkinter import *
import tkinter.font as font

import time

PHOTO_IMAGE_TYPE_PERFECT = "perfect"
PHOTO_IMAGE_TYPE_FAST    = "fast"
PHOTO_IMAGE_TYPE_LATE    = "late"

class BalanceUI :
	# frame rate variables
	FRAME_PERIOD = 15
	isShowFrameRate = False

	# state variables
	isMainloop = False

	# countdown variables
	countdownCount = 0
	countdownStartTime = 0.0
	isCountdown = False

	# test variables

	def __init__(self) :
		self.root = Tk()
		self.app = BalanceBoardDisplay(self.root)

		self.updateEventListeners = []
		self.updateEventAppendListenerList = []
		self.updateEventRemoveListenerList = []

	def mainloop(self) :
		if self.isShowFrameRate :
			self.initializeFrameRateCounter()
			self.periodicTaskMethod = self.periodicTaskWithFrameRate
		else :
			self.periodicTaskMethod = self.periodicTask

		self.isMainloop = True
		self.root.after(self.FRAME_PERIOD, self.periodicTaskMethod)
		self.root.mainloop()

	def periodicTask(self) :
		for listener in self.updateEventListeners :
			listener()

		for listener in self.updateEventAppendListenerList :
			self.updateEventListeners.append(listener)
		self.updateEventAppendListenerList = []

		for listener in self.updateEventRemoveListenerList :
			try :
				self.updateEventListeners.remove(listener)
			except ValueError as e :
				pass
		self.updateEventRemoveListenerList = []

		self.root.after(self.FRAME_PERIOD, self.periodicTaskMethod)

	################################################################################
	#                                 update event                                 #
	################################################################################
	# These methods should Only be called on Update listeners when isMainloop is True.
	def appendUpdateEventListener(self, listener) :
		if self.isMainloop :
			self.updateEventAppendListenerList.append(listener)
		else :
			self.updateEventListeners.append(listener)

	def removeUpdateEventListener(self, listener) :
		if self.isMainloop :
			self.updateEventRemoveListenerList.append(listener)
		else :
			try :
				self.updateEventListeners.remove(listener)
			except ValueError as e :
				pass

	################################################################################
	#                                    UI API                                    #
	################################################################################
	# These methods should Only be called on Update listeners.
	def setOutfitID(self, id) :
		if id is -1 :
			self.app.setOutfitNameText("연결 중..")
		else :
			self.app.setOutfitNameText("교구 " + str(id) + "번")

	def setStateText(self, exercise, level, motion) :
		self.app.setExerciseText(exercise)
		self.app.setLevelText(level)
		self.app.setMotionText(motion)

	def showCanvasOrHelpText(self, isCanvas) :
		self.app.showCanvasOrHelpText(isCanvas)

	def setHelpMessage(self, message) :
		if self.isCountdown :
			self.isCountdown = False
			self.removeUpdateEventListener(self.countdownCoroutine)

		self.app.setHelpText(message)

	def setCountdown(self, count) :
		self.countdownStartTime = time.time()
		self.countdownCount = count
		self.isCountdown = True

		self.app.setHelpText("카운트다운 " + str(self.countdownCount))
		self.appendUpdateEventListener(self.countdownCoroutine)

	def showStimulation(self, color) :
		self.app.drawCircleCenter(color, 500)

	def showResponseResult(self, resultType) :
		self.app.showPhotoImage(resultType)

	def setHelpMessageWithCanvas(self, message) :
		self.app.showCanvasOrHelpText(False)
		self.setHelpMessage(message)

	def setCountdownWithCanvas(self, count) :
		self.app.showCanvasOrHelpText(False)
		self.setCountdown(count)

	def showStimulationWithCanvas(self, color) :
		self.app.showCanvasOrHelpText(True)
		self.showStimulation(color)

	def showResponseResultWithCanvas(self, resultType) :
		self.app.showCanvasOrHelpText(True)
		self.showResponseResult(resultType)

	def clearCanvas(self) :
		self.app.clearCanvas()

	################################################################################
	#                                frame rate API                                #
	################################################################################
	def showFrameRate(self, isShow) :
		self.isShowFrameRate = isShow

	def initializeFrameRateCounter(self) :
		self.timestemp = time.time()
		self.frameCount = 0

	def periodicTaskWithFrameRate(self) :
		self.frameCount = self.frameCount + 1

		if time.time() - self.timestemp > 1.0 :
			print("frameCount : " + str(self.frameCount))
			self.timestemp = self.timestemp + 1.0
			self.frameCount = 0

		self.periodicTask()

	################################################################################
	#                               private methods                                #
	################################################################################
	def countdownCoroutine(self) :
		if self.isCountdown :
			if time.time() - self.countdownStartTime >= 1.0 :
				self.countdownCount = self.countdownCount - 1

				if self.countdownCount <= 0 :
					self.isCountdown = False
					self.removeUpdateEventListener(self.countdownCoroutine)
					self.app.setHelpText("")
				else :
					self.countdownStartTime = self.countdownStartTime + 1.0
					self.app.setHelpText("카운트다운 " + str(self.countdownCount))
		else :
			self.removeUpdateEventListener(self.countdownCoroutine)



class BalanceBoardDisplay(Frame) :
	root = None
	photoImageDictionary = {}

	def __init__(self, root) :
		super().__init__()
		self.root = root
		self.initGeometry()
		self.initUI()
		self.bindEvent()

	################################################################################
	#                              initialize methods                              #
	################################################################################
	def initGeometry(self) :
		# self.root.geometry("500x500+1000+0")
		self.root.attributes("-fullscreen", True)

	def initUI(self) :
		# setup main frame
		self.master.title("Balance board")
		self.pack(expand=True, fill=BOTH)
		self.configure(background='white')

		# setup sub frames
		self.titleFrame = Frame(self)
		self.mainFrame = Frame(self)
		self.titleFrame.configure(background='white')
		self.mainFrame.configure(background='white')

		# setup title widgets
		outfitNameLabelFont = font.Font(size=80)
		self.outfitNameLabel = Label(self.titleFrame, text="        ", font=outfitNameLabelFont)
		self.outfitNameLabel.configure(background='white')

		stateLabelFont = font.Font(size=40)
		self.exerciseLabel = Entry(self.titleFrame, width=12, font=stateLabelFont)
		self.levelLabel = Entry(self.titleFrame, width=15, font=stateLabelFont)
		self.motionLabel = Entry(self.titleFrame, width=8, font=stateLabelFont)

		# self.exerciseLabel.insert(0, "")
		self.exerciseLabel.configure(background='#DDDDDD')#, state='readonly')
		# self.levelLabel.insert(0, "")
		self.levelLabel.configure(background='#DDDDDD')#, state='readonly')
		# self.motionLabel.insert(0, "")
		self.motionLabel.configure(background='#DDDDDD')#, state='readonly')

		# setup main widgets
		frameSeparatorFont = font.Font(size=2)
		self.frameSeparator = Label(self.mainFrame, font=frameSeparatorFont)
		self.frameSeparator.configure(background='#000000')
		helpTextLabelFont = font.Font(size=100)
		self.helpTextLabel = Label(self.mainFrame, text="", font=helpTextLabelFont)
		self.helpTextLabel.configure(background='white')

		# setup canvas
		self.canvas = Canvas(self.mainFrame)
		self.canvas.configure(background='white')

		# setup frame layout
		self.titleFrame.pack(side=TOP, fill=X)
		self.mainFrame.pack(side=TOP, expand=True, fill=BOTH)

		# setup title widget layout
		self.outfitNameLabel.pack(side=LEFT, pady=25, padx=150)
		self.exerciseLabel.pack(side=LEFT, padx=20)
		self.levelLabel.pack(side=LEFT, padx=20)
		self.motionLabel.pack(side=LEFT, padx=20)

		# setup main widget layout
		self.isCanvasShowing = True
		self.frameSeparator.pack(side=TOP, fill=X)
		# self.helpTextLabel.pack(side=TOP, expand=True, fill=BOTH)
		self.canvas.pack(side=TOP, expand=True, fill=BOTH)

		self.photoImageDictionary[PHOTO_IMAGE_TYPE_PERFECT] = PhotoImage(file="Resources/perfect.png")
		self.photoImageDictionary[PHOTO_IMAGE_TYPE_FAST   ] = PhotoImage(file="Resources/fast.png")
		self.photoImageDictionary[PHOTO_IMAGE_TYPE_LATE   ] = PhotoImage(file="Resources/late.png")

	def bindEvent(self) :
		self.root.bind("<Escape>", self.onEscape)

	################################################################################
	#                                event methods                                 #
	################################################################################
	def onEscape(self, event) :
		self.root.destroy()

	################################################################################
	#                              UI control methods                              #
	################################################################################
	def setOutfitNameText(self, text) :
		self.outfitNameLabel["text"] = text

	def setExerciseText(self, text) :
		self.exerciseLabel.delete(0, END)
		self.exerciseLabel.insert(0, text)

	def setLevelText(self, text) :
		self.levelLabel.delete(0, END)
		self.levelLabel.insert(0, text)

	def setMotionText(self, text) :
		self.motionLabel.delete(0, END)
		self.motionLabel.insert(0, text)

	def setHelpText(self, text) :
		self.helpTextLabel["text"] = text

	def showCanvasOrHelpText(self, isCanvas) :
		if isCanvas and not self.isCanvasShowing :
			self.helpTextLabel.pack_forget()
			self.canvas.pack(side=TOP, expand=True, fill=BOTH)
			self.isCanvasShowing = True

		elif not isCanvas and self.isCanvasShowing :
			self.canvas.pack_forget()
			self.helpTextLabel.pack(side=TOP, expand=True, fill=BOTH)
			self.isCanvasShowing = False

	def drawCircleCenter(self, color, size) :
		canvasWidth = self.canvas.winfo_width()
		canvasHeight = self.canvas.winfo_height()

		self.canvas.create_oval((canvasWidth  - size) / 2, # x1
								(canvasHeight - size) / 2, # y1
								(canvasWidth  + size) / 2, # x2
								(canvasHeight + size) / 2, # y2
								fill=color,
								outline="#FFFFFF")

	def showPhotoImage(self, photoImage) :
		canvasWidth = self.canvas.winfo_width()
		canvasHeight = self.canvas.winfo_height()

		self.canvas.create_image(
			canvasWidth * 0.75, canvasHeight / 2,
			anchor=CENTER,
			image=self.photoImageDictionary[photoImage])

	def clearCanvas(self) :
		self.canvas.delete("all")

if __name__ == '__main__' :
	root = Tk()
	app = BalanceBoardDisplay(root)
	root.mainloop()
