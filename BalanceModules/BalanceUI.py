#!/usr/bin/env python3

from tkinter import *
import tkinter.font as font

import time

RESULT_TYPE_PERFECT = 0
RESULT_TYPE_FAST    = 1
RESULT_TYPE_LATE    = 2

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

	# message sequence variables
	messageSequence = None
	messageSequencePeriod = 0.0
	nextMessageTime = 0.0
	isMessageSequence = False
	currentMessageIndex = 0
	currentHelpTextObject = None

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

	def setMotionText(self, motion) :
		self.app.setMotionText(motion)

	def deleteObject(self, obj) :
		self.app.deleteObject(obj)

	def clearCanvas(self) :
		self.app.clearCanvas()
		self.currentHelpTextObject = None

	def setHelpText(self, text) :
		self.clearHelpTextCoroutine()
		self.setHelpTextInternal(text)

	def clearHelpText(self) :
		if self.currentHelpTextObject :
			self.app.deleteObject(self.currentHelpTextObject)
			self.currentHelpTextObject = None

	# def showCanvasOrHelpText(self, isCanvas) :
	# 	self.app.showCanvasOrHelpText(isCanvas)

	# def setHelpMessage(self, message) :
	# 	self.clearHelpTextCoroutine()
	# 	self.app.setHelpText(message)

	def setCountdown(self, count) :
		self.clearHelpTextCoroutine()
		self.clearHelpText()

		if count <= 0 :
			return

		self.countdownStartTime = time.time()
		self.countdownCount = count
		self.isCountdown = True

		self.setHelpTextInternal("카운트다운 " + str(self.countdownCount))
		self.appendUpdateEventListener(self.countdownCoroutine)

	def setMessageSequence(self, messageSequence, messageSequencePeriod) :
		self.clearHelpTextCoroutine()
		self.clearHelpText()

		self.messageSequence = messageSequence
		if len(self.messageSequence) <= 0 :
			return

		self.messageSequencePeriod = messageSequencePeriod
		self.nextMessageTime = time.time() + self.messageSequencePeriod
		self.isMessageSequence = True
		self.currentMessageIndex = 0

		self.setHelpTextInternal(messageSequence[0])
		self.appendUpdateEventListener(self.messageSequenceCoroutine)

	def showStimulation(self, color) :
		return self.app.drawCircleCenter(color, 500)

	def showResponseResult(self, resultType) :
		(x, y) = self.app.getCanvasSize()

		if resultType is RESULT_TYPE_PERFECT :
			resultText = "정확"
			resultColor = "#00B050"
		elif resultType is RESULT_TYPE_FAST :
			resultText = "빠름"
			resultColor = "#0000FF"
		elif resultType is RESULT_TYPE_LATE :
			resultText = "느림"
			resultColor = "#FF0000"
		else :
			return None

		return self.app.drawText(
			resultText,
			x * 0.75, y * 0.5,
			resultColor,
			100,
			CENTER)

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
	def setHelpTextInternal(self, text) :
		self.clearHelpText()
		(x, y) = self.app.getCanvasSize()
		
		self.currentHelpTextObject = self.app.drawText(
			text,
			x / 2, y / 2,
			"black",
			100,
			CENTER)

	def clearHelpTextCoroutine(self) :
		if self.isCountdown :
			self.isCountdown = False
			self.removeUpdateEventListener(self.countdownCoroutine)

		if self.isMessageSequence :
			self.isMessageSequence = False
			self.removeUpdateEventListener(self.messageSequenceCoroutine)

	def countdownCoroutine(self) :
		if self.isCountdown :
			if time.time() - self.countdownStartTime >= 1.0 :
				self.countdownCount = self.countdownCount - 1

				if self.countdownCount <= 0 :
					self.isCountdown = False
					self.removeUpdateEventListener(self.countdownCoroutine)
					self.clearHelpText()
				else :
					self.countdownStartTime = self.countdownStartTime + 1.0
					self.setHelpTextInternal("카운트다운 " + str(self.countdownCount))
		else :
			self.removeUpdateEventListener(self.countdownCoroutine)

	def messageSequenceCoroutine(self) :
		if self.isMessageSequence :
			if time.time() >= self.nextMessageTime :
				self.currentMessageIndex = self.currentMessageIndex + 1

				if len(self.messageSequence) > self.currentMessageIndex :
					self.setHelpTextInternal(self.messageSequence[self.currentMessageIndex])
					self.nextMessageTime = time.time() + self.messageSequencePeriod
				else :
					self.isMessageSequence = False
					self.removeUpdateEventListener(self.messageSequenceCoroutine)
					self.clearHelpText()
		else :
			self.removeUpdateEventListener(self.messageSequenceCoroutine)



class BalanceBoardDisplay(Frame) :
	root = None
	# photoImageDictionary = {}

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
		# helpTextLabelFont = font.Font(size=100)
		# self.helpTextLabel = Label(self.mainFrame, text="", font=helpTextLabelFont)
		# self.helpTextLabel.configure(background='white')

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
		# self.isCanvasShowing = True
		self.frameSeparator.pack(side=TOP, fill=X)
		# self.helpTextLabel.pack(side=TOP, expand=True, fill=BOTH)
		self.canvas.pack(side=TOP, expand=True, fill=BOTH)

		# self.photoImageDictionary[PHOTO_IMAGE_TYPE_PERFECT] = PhotoImage(file="Resources/perfect.png")
		# self.photoImageDictionary[PHOTO_IMAGE_TYPE_FAST   ] = PhotoImage(file="Resources/fast.png")
		# self.photoImageDictionary[PHOTO_IMAGE_TYPE_LATE   ] = PhotoImage(file="Resources/late.png")

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

	################################################################################
	#                            canvas control methods                            #
	################################################################################
	def getCanvasSize(self) :
		return (self.canvas.winfo_width(), self.canvas.winfo_height())

	def deleteObject(self, obj) :
		self.canvas.delete(obj)

	def clearCanvas(self) :
		self.canvas.delete("all")

	def drawText(self, text, x, y, color, fontSize, anchor) :
		return self.canvas.create_text(
			x, y,
			fill=color,
			font=font.Font(size=fontSize),
			text=text,
			anchor=anchor)

	def drawCircle(self, x1, y1, x2, y2, color) :
		return self.canvas.create_oval(
			x1, y1,
			x2, y2,
			fill=color,
			outline="#FFFFFF")

	def drawCirclePosition(self, x, y, color, size) :
		return self.canvas.create_oval(
			x - size / 2, # x1
			y - size / 2, # y1
			x + size / 2, # x2
			y + size / 2, # y2
			fill=color,
			outline="#FFFFFF")

	def drawCircleCenter(self, color, size) :
		canvasWidth = self.canvas.winfo_width()
		canvasHeight = self.canvas.winfo_height()

		return self.canvas.create_oval(
			(canvasWidth  - size) / 2, # x1
			(canvasHeight - size) / 2, # y1
			(canvasWidth  + size) / 2, # x2
			(canvasHeight + size) / 2, # y2
			fill=color,
			outline="#FFFFFF")

	def setHelpText(self, text) :
		pass
		# self.helpTextLabel["text"] = text

	def showCanvasOrHelpText(self, isCanvas) :
		pass
		# if isCanvas and not self.isCanvasShowing :
		# 	self.helpTextLabel.pack_forget()
		# 	self.canvas.pack(side=TOP, expand=True, fill=BOTH)
		# 	self.isCanvasShowing = True

		# elif not isCanvas and self.isCanvasShowing :
		# 	self.canvas.pack_forget()
		# 	self.helpTextLabel.pack(side=TOP, expand=True, fill=BOTH)
		# 	self.isCanvasShowing = False

	# def showPhotoImage(self, photoImage) :
	# 	canvasWidth = self.canvas.winfo_width()
	# 	canvasHeight = self.canvas.winfo_height()

	# 	self.canvas.create_image(
	# 		canvasWidth * 0.75, canvasHeight / 2,
	# 		anchor=CENTER,
	# 		image=self.photoImageDictionary[photoImage])

if __name__ == '__main__' :
	root = Tk()
	app = BalanceBoardDisplay(root)
	root.mainloop()
