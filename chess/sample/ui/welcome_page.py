import tkinter as tk
from tkinter import *
from tkinter import ttk

class WelcomePage():

	def __init__(self):
		self.root = tk.Tk()

	def buildWelcomePage(self, game):
		root = self.root
		self.game = game
		root.title("Chess")
		root.configure(background='gray60')
		root.minsize(300, 300)
		root.geometry("700x500")
		root.rowconfigure(0, weight = 1)
		root.columnconfigure(0, weight = 1)
		root.columnconfigure(2, weight = 1)
		root.rowconfigure (6, weight = 1)
		self.createNameEntry()
		root.mainloop()

	def createNameEntry(self):
		root = self.root
		Label(text='Welcome to the game!\n May the odds be ever in your favor. ', fg = "blue", background="gray60", font = "Verdana 20 bold italic").grid(row=1, column = 1)

		labelText=StringVar()
		labelText.set("Enter player 1 name: ")
		labelDir=Label(root, textvariable=labelText, height=4, background='gray60', font = "Verdana 16 bold").grid(row = 2, column = 1)

		p1NameVar=StringVar(None)
		p1Entry=Entry(root, textvariable=p1NameVar,width=25)
		p1Entry.grid(row = 3, column = 1)

		labelText=StringVar()
		labelText.set("Enter player 2 name: ")
		labelDir=Label(root, textvariable=labelText, height=4, background='gray60', font = "Verdana 16 bold").grid(row = 4, column = 1)

		p2NameVar=StringVar(None)
		p2Entry=Entry(root, textvariable=p2NameVar,width=25)
		p2Entry.grid(row = 5, column = 1)

		def onok():
			name1 = p1Entry.get()
			name2 = p2Entry.get()
			print("Player 1 is :" + name1)
			print("Player 2 is :" + name2)
			for widget in root.winfo_children():
				widget.destroy()
			Label(text='Looking for the game? Rook no further, its in the terminal window! ', fg = "blue", background="gray60", font = "Verdana 16 bold italic").grid(row=1, column = 1)
			Button(root, text='Goodbye', command = close_window, background = 'gray60').grid(row=2, column = 1)
			self.game.start(name1, name2)

		def close_window():
			root.destroy()

		Button(root, text='Let\'s Do This', command=onok, background='gray60').grid(row=6, column=1)

