from tkinter import *

canvas_width = 300
canvas_height =300

master = Tk()

canvas = Canvas(master)
canvas.pack(side=TOP, expand=True, fill=BOTH)

img = PhotoImage(file="perfect.png")
canvas.create_image(20,20, anchor=NW, image=img)

mainloop()
