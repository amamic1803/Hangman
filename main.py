from tkinter import *
import os
import sys
import random


def resource_path(relative_path):
	""" Get absolute path to resource, works for dev and for PyInstaller """
	try:
		# PyInstaller creates a temp folder and stores path in _MEIPASS
		base_path = sys._MEIPASS
	except AttributeError:
		base_path = os.path.abspath(".")
	return os.path.join(base_path, relative_path)

def change_language(event, language):
	global selected_language
	if selected_language != language:
		if language == "en":
			en_lbl.config(highlightthickness=2)
			hr_lbl.config(highlightthickness=0)
		else:
			en_lbl.config(highlightthickness=0)
			hr_lbl.config(highlightthickness=2)
		selected_language = language
		change_gui_language(selected_language)

def change_language_thickness(event, widget, typ, language, selected_language):
	if language != selected_language:
		if typ:
			widget.config(highlightthickness=0)
		else:
			widget.config(highlightthickness=4)

def change_gui_language(language):
	if language == "en":
		root.title("Hangman")
		title.config(text="Hangman")
	else:
		root.title("Vješala")
		title.config(text="Vješala")


if __name__ == '__main__':
	selected_language = "en"

	with open("data/en_words.txt", "r", encoding="utf-8") as file1, open("data/hr_words.txt", "r", encoding="utf-8") as file2:
		en_words = [i.rstrip("\n") for i in file1.readlines()]
		hr_words = [i.rstrip("\n") for i in file2.readlines()]

	root = Tk()
	root.title("Hangman")
	root.resizable(False, False)
	root.geometry(f"500x500+{root.winfo_screenwidth() // 2 - 250}+{root.winfo_screenheight() // 2 - 250}")
	root.iconbitmap(resource_path("images/hangman-icon.ico"))
	root.config(background="#fffae6")

	hangman_images = []
	for i in range(1, 10):
		hangman_images.append(PhotoImage(file=f"images//hangman_{i}.png"))

	title = Label(root, text="Hangman", font=("Gabriola", 40, "bold"), borderwidth=0, background="#fffae6", activebackground="#fffae6")
	title.place(x=0, y=0, width=500, height=75)

	en_lbl = Label(root, text="EN", font=("Helvetica", 12, "bold"), justify=CENTER, borderwidth=0, background="#fffae6", activebackground="#fffae6", highlightthickness=2, highlightcolor="black", highlightbackground="black")
	en_lbl.place(x=430, y=0, width=35, height=25)
	en_lbl.bind("<Enter>", lambda event: change_language_thickness(event, en_lbl, False, "en", selected_language))
	en_lbl.bind("<Leave>", lambda event: change_language_thickness(event, en_lbl, True, "en", selected_language))
	en_lbl.bind("<ButtonRelease-1>", lambda event: change_language(event, "en"))

	hr_lbl = Label(root, text="HR", font=("Helvetica", 12, "bold"), justify=CENTER, borderwidth=0, background="#fffae6", activebackground="#fffae6", highlightthickness=0, highlightcolor="black", highlightbackground="black")
	hr_lbl.place(x=465, y=0, width=35, height=25)
	hr_lbl.bind("<Enter>", lambda event: change_language_thickness(event, hr_lbl, False, "hr", selected_language))
	hr_lbl.bind("<Leave>", lambda event: change_language_thickness(event, hr_lbl, True, "hr", selected_language))
	hr_lbl.bind("<ButtonRelease-1>", lambda event: change_language(event, "hr"))

	restart_image = PhotoImage(file="images/hangman-restart_image.png")
	restart_lbl = Label(root, image=restart_image, justify=CENTER, borderwidth=0, background="#fffae6", activebackground="#fffae6", highlightthickness=0)
	restart_lbl.place(x=0, y=0, width=40, height=40)

	word_canvas = Canvas(root, borderwidth=0, highlightthickness=0, background="#fffae6")
	word_canvas.place(x=0, y=100, width=500, height=100)

	len_word = 10
	start_coord = (500 - (len_word * 30 + (len_word - 1) * 11)) // 2
	line_or_space = True
	for i in range(2 * len_word - 1):
		if line_or_space:
			word_canvas.create_line(start_coord, 50, start_coord + 30, 50, fill="black", width=3)
			line_or_space = False
			start_coord += 30
		else:
			start_coord += 11
			line_or_space = True

	drawing_lbl = Label(root, image=hangman_images[8], justify=CENTER, borderwidth=0, background="#fffae6", activebackground="#fffae6", highlightthickness=0)
	drawing_lbl.place(x=0, y=250, width=200, height=250)

	root.mainloop()

"""
def upisivanje(x):
	file = open("ploca.txt", "w", encoding="utf-8")
	file.write("".join(x))
	file.close()


file1 = open("rjesenje.txt", "r", encoding="utf-8")
rjesenje_str = file1.read()
rjesenje_str = rjesenje_str.lower()
rjesenje = []
for i in range(len(rjesenje_str)):
	manje_slovo = rjesenje_str[i - 1] + rjesenje_str[i]
	if i < len(rjesenje_str) - 1:
		vece_slovo = rjesenje_str[i] + rjesenje_str[i + 1]
	if manje_slovo == "nj" or manje_slovo == "lj" or manje_slovo == "dž":
		pass
	elif vece_slovo == "lj":
		rjesenje.append("lj")
	elif vece_slovo == "nj":
		rjesenje.append("nj")
	elif vece_slovo == "dž":
		rjesenje.append("dž")
	else:
		rjesenje.append(rjesenje_str[i])
file1.close()

x = []
for i in rjesenje:
	if i == " ":
		x.append(i)
	else:
		x.append("_")
upisivanje(x)

broj_gresaka = 0
while "_" in x and broj_gresaka != 10:
	print("Broj grešaka {}/10".format(broj_gresaka))
	upis = input("Unesi slovo ili pojam: ")
	if len(upis) > 1 and upis != "lj" and upis != "nj" and upis != "dž":
		if upis == rjesenje_str:
			x = rjesenje
			upisivanje(x)
		else:
			broj_gresaka = broj_gresaka + 1
	else:
		greska = True
		for i in range(len(rjesenje)):
			if rjesenje[i] == upis:
				x[i] = upis
				upisivanje(x)
				greska = False

		if greska:
			broj_gresaka = broj_gresaka + 1
		else:
			print("Slovo pogođeno!")

if broj_gresaka == 10:
	print("Broj grešaka 10/10")
	print("Izgubili ste!")
else:
	print("Bravo, svaka čast!")
"""