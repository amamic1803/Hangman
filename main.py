from tkinter import *
from tkinter.messagebox import showwarning
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
		guess_btn.config(text="Try")
	else:
		root.title("Vješala")
		title.config(text="Vješala")
		guess_btn.config(text="Probaj")

def change_thickness(event, widget, typ):
	if typ:
		widget.config(highlightthickness=3)
	else:
		widget.config(highlightthickness=5)

def start_game():
	global selected_language, en_words, hr_words, letter_coords, word
	word_canvas.delete("all")
	letter_coords = []
	if selected_language == "en":
		word = random.choice(en_words)
		len_word = len(word)
		start_coord = (500 - (len_word * 30 + (len_word - 1) * 11)) // 2
		line_or_space = True
		for i in range(2 * len_word - 1):
			if line_or_space:
				word_canvas.create_line(start_coord, 40, start_coord + 30, 40, fill="black", width=4)
				letter_coords.append(start_coord + 14)
				line_or_space = False
				start_coord += 30
			else:
				start_coord += 11
				line_or_space = True
	else:
		word = random.choice(hr_words)

def validate_input(full_text):
	global word
	if full_text == "":
		return True
	elif full_text.isalpha() and len(full_text) <= len(word):
		return True
	else:
		return False

def guess_click(event):
	pass


if __name__ == '__main__':
	selected_language = "en"
	letter_coords = []
	word = ""

	with open("data/en_words.txt", "r", encoding="utf-8") as file1, open("data/hr_words.txt", "r", encoding="utf-8") as file2:
		en_words = [i.rstrip("\n") for i in file1.readlines()]
		hr_words = [i.rstrip("\n") for i in file2.readlines()]

	root = Tk()
	root.title("Hangman")
	root.resizable(False, False)
	root.geometry(f"500x425+{root.winfo_screenwidth() // 2 - 250}+{root.winfo_screenheight() // 2 - 212}")
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
	word_canvas.place(x=0, y=100, width=500, height=50)

	start_game()

	word_canvas.create_text(64, 40, text="DŽ", font=("Helvetica", 21, "bold"), fill="black", activefill="black", anchor="s")

	drawing_lbl = Label(root, image=hangman_images[8], justify=CENTER, borderwidth=0, background="green", activebackground="#fffae6", highlightthickness=0)
	drawing_lbl.place(x=0, y=175, width=200, height=250)

	reg = root.register(validate_input)
	guess_ent = Entry(root, justify=CENTER, validate="key", validatecommand=(reg, "%P"), background="#ffffff", foreground="#000000", highlightthickness=3, highlightcolor="black", highlightbackground="black", borderwidth=0, font=("Helvetica", 15))
	guess_ent.place(x=250, y=200, width=173, height=35)

	guess_btn = Label(root, text="Try", font=("Helvetica", 15, "bold"), justify=CENTER, borderwidth=0, background="#fffae6", activebackground="#fffae6", highlightthickness=3, highlightcolor="black", highlightbackground="black")
	guess_btn.place(x=420, y=200, width=80, height=35)
	guess_btn.bind("<Enter>", lambda event: change_thickness(event, guess_btn, False))
	guess_btn.bind("<Leave>", lambda event: change_thickness(event, guess_btn, True))
	guess_btn.bind("<ButtonRelease-1>", lambda event: guess_click(event))

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