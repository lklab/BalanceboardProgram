#!/usr/bin/env python3

from tkinter import *
import tkinter.font as font

class BalanceBoardDisplay(Frame) :
	root = None

	def __init__(self, root) :
		super().__init__()
		self.root = root
		self.initGeometry()
		self.initUI()
		self.bindEvent()

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
		playthingNameLabelFont = font.Font(size=80)
		self.playthingNameLabel = Label(self.titleFrame, text="교구 1번", font=playthingNameLabelFont)
		self.playthingNameLabel.configure(background='white')

		stateLabelFont = font.Font(size=40)
		self.exerciseLabel = Entry(self.titleFrame, width=12, font=stateLabelFont)
		self.levelLabel = Entry(self.titleFrame, width=15, font=stateLabelFont)
		self.motionLabel = Entry(self.titleFrame, width=8, font=stateLabelFont)

		self.exerciseLabel.insert(0, "밸런스 운동")
		self.exerciseLabel.configure(background='#DDDDDD', state='readonly')
		self.levelLabel.insert(0, "level 5-1(응용)")
		self.levelLabel.configure(background='#DDDDDD', state='readonly')
		self.motionLabel.insert(0, "동작 1")
		self.motionLabel.configure(background='#DDDDDD', state='readonly')

		# setup main widgets
		frameSeparatorFont = font.Font(size=2)
		self.frameSeparator = Label(self.mainFrame, font=frameSeparatorFont)
		self.frameSeparator.configure(background='#000000')
		helpTextLabelFont = font.Font(size=100)
		self.helpTextLabel = Label(self.mainFrame, text="카운트다운 5", font=helpTextLabelFont)
		self.helpTextLabel.configure(background='white')

		# setup frame layout
		self.titleFrame.pack(side=TOP, fill=X)
		self.mainFrame.pack(side=TOP, expand=True, fill=BOTH)

		# setup title widget layout
		self.playthingNameLabel.pack(side=LEFT, pady=25, padx=150)
		self.exerciseLabel.pack(side=LEFT, padx=20)
		self.levelLabel.pack(side=LEFT, padx=20)
		self.motionLabel.pack(side=LEFT, padx=20)

		# setup main widget layout
		self.frameSeparator.pack(side=TOP, fill=X)
		self.helpTextLabel.pack(side=TOP, expand=True, fill=BOTH)

	def bindEvent(self) :
		self.root.bind("<Escape>", self.onEscape)

	def onEscape(self, event) :
		self.root.destroy()

if __name__ == '__main__' :
	root = Tk()
	app = BalanceBoardDisplay(root)
	root.mainloop()
