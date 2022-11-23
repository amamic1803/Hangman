import os
import random
import sys
from tkinter import *
from tkinter.messagebox import askyesno


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
		selected_language_temp = selected_language
		selected_language = language
		if start_game():
			if language == "en":
				en_lbl.config(highlightthickness=2)
				hr_lbl.config(highlightthickness=0)
			else:
				en_lbl.config(highlightthickness=0)
				hr_lbl.config(highlightthickness=2)
			change_gui_language(selected_language)
		else:
			selected_language = selected_language_temp
			if language == "en":
				en_lbl.config(highlightthickness=0)
			else:
				hr_lbl.config(highlightthickness=0)

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
		missed_guesses_title.config(text=" Missed:")
	else:
		root.title("Vješala")
		title.config(text="Vješala")
		guess_btn.config(text="Probaj")
		missed_guesses_title.config(text=" Promašaji:")

def change_thickness(event, widget, typ):
	if typ:
		widget.config(highlightthickness=3)
	else:
		widget.config(highlightthickness=5)

def restart_change(event, typ):
	if typ:
		restart_lbl.config(image=restart_image_smaller)
	else:
		restart_lbl.config(image=restart_image_bigger)

def start_game(event=None):
	global selected_language, en_words, hr_words, letter_coords, word, word_letters, guessed_letters, missed_letters, ended
	restart_lbl.config(image=restart_image_smaller)
	if not ended and (len(guessed_letters) > 0 or len(missed_letters) > 0):
		if selected_language == "en":
			end_game = askyesno("Game in progress!", "Are you sure you want to start a new game?")
		else:
			end_game = askyesno("Igra u tijeku!", "Jeste li sigurni da želite pokrenuti novu igru?")
		if not end_game:
			return False
	word_canvas.delete("all")
	missed_guesses.config(text="")
	end_status_lbl.config(text="")
	drawing_lbl.config(image="")
	letter_coords = []
	word_letters = []
	guessed_letters = []
	missed_letters = []
	ended = False
	if selected_language == "en":
		word = random.choice(en_words)
		word_letters = [x for x in word]
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
		word_temp = word
		while len(word_temp) > 0:
			if len(word_temp) == 1:
				word_letters.append(word_temp)
				word_temp = ""
			elif word_temp[0:2] in ["DŽ", "NJ", "LJ"]:
				word_letters.append(word_temp[0:2])
				word_temp = word_temp[2:]
			else:
				word_letters.append(word_temp[0])
				word_temp = word_temp[1:]
		len_word = len(word_letters)
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
	return True

def validate_input(full_text):
	global word
	if full_text == "":
		return True
	elif full_text.isalpha() and len(full_text) <= 11:
		return True
	else:
		return False

def guess_click(event):
	global word, word_letters, letter_coords, guessed_letters, missed_letters, ended, hangman_images, selected_language
	inpt = guess_ent.get().upper()
	guess_ent.delete(0, END)
	if len(inpt) != 0:
		if inpt in word_letters and inpt not in guessed_letters:
			guessed_letters.append(inpt)
			to_end = True
			for i in range(len(word_letters)):
				if word_letters[i] == inpt:
					word_canvas.create_text(letter_coords[i], 40, text=inpt, font=("Helvetica", 21, "bold"), fill="black", activefill="black", anchor="s")
				if word_letters[i] not in guessed_letters:
					to_end = False
			if to_end:
				ended = True
				if selected_language == "en":
					end_status_lbl.config(text="Victory!", foreground="green", activeforeground="green")
				else:
					end_status_lbl.config(text="Pobjeda!", foreground="green", activeforeground="green")
		elif inpt == word and not ended:
			for i in range(len(word_letters)):
				if word_letters[i] not in guessed_letters:
					word_canvas.create_text(letter_coords[i], 40, text=word_letters[i], font=("Helvetica", 21, "bold"), fill="black", activefill="black", anchor="s")
			ended = True
			if selected_language == "en":
				end_status_lbl.config(text="Victory!", foreground="green", activeforeground="green")
			else:
				end_status_lbl.config(text="Pobjeda!", foreground="green", activeforeground="green")
		elif not ended:
			missed_letters.append(inpt)
			missed_guesses.config(text="\n".join(missed_letters))
			drawing_lbl.config(image=hangman_images[len(missed_letters) - 1])
			if len(missed_letters) == 9:
				ended = True
				if selected_language == "en":
					end_status_lbl.config(text="Fail!", foreground="red", activeforeground="red")
				else:
					end_status_lbl.config(text="Poraz!", foreground="red", activeforeground="red")
				for i in range(len(word_letters)):
					if word_letters[i] not in guessed_letters:
						word_canvas.create_text(letter_coords[i], 40, text=word_letters[i], font=("Helvetica", 21, "bold"), fill="black", activefill="black", anchor="s")

def main():
	global guessed_letters, missed_letters
	global root
	global title
	global guess_btn, missed_guesses_title
	global en_lbl, hr_lbl
	global restart_lbl, restart_image_smaller, restart_image_bigger
	global word_canvas
	global missed_guesses
	global end_status_lbl
	global drawing_lbl
	global guess_ent
	global selected_language
	global en_words, hr_words
	global letter_coords, word, word_letters
	global ended
	global hangman_images

	selected_language = "en"
	ended = True
	guessed_letters = []
	missed_letters = []

	with open(resource_path("run_data/words/en_words.txt"), "r", encoding="utf-8") as file1, open(resource_path("run_data/words/hr_words.txt"), "r", encoding="utf-8") as file2:
		en_words = [i.rstrip("\n").upper() for i in file1.readlines()]
		hr_words = [i.rstrip("\n").upper() for i in file2.readlines()]

	root = Tk()
	root.title("Hangman")
	root.resizable(False, False)
	root.geometry(f"500x425+{root.winfo_screenwidth() // 2 - 250}+{root.winfo_screenheight() // 2 - 212}")
	root.iconbitmap(resource_path("data/hangman-icon.ico"))
	root.config(background="#fffae6")

	hangman_images = []
	for i in range(1, 10):
		hangman_images.append(PhotoImage(file=resource_path(f"run_data/images//hangman_{i}.png")))

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

	restart_image_smaller = PhotoImage(file=resource_path("run_data/images/hangman-restart_smaller.png"))
	restart_image_bigger = PhotoImage(file=resource_path("run_data/images/hangman-restart_bigger.png"))
	restart_lbl = Label(root, image=restart_image_smaller, anchor=CENTER, justify=CENTER, borderwidth=0, background="#fffae6", activebackground="#fffae6", highlightbackground="#fffae6", highlightthickness=0)
	restart_lbl.place(x=0, y=0, width=45, height=45)
	restart_lbl.bind("<ButtonRelease-1>", start_game)
	restart_lbl.bind("<Enter>", lambda event: restart_change(event, False))
	restart_lbl.bind("<Leave>", lambda event: restart_change(event, True))

	word_canvas = Canvas(root, borderwidth=0, highlightthickness=0, background="#fffae6")
	word_canvas.place(x=0, y=100, width=500, height=50)

	drawing_lbl = Label(root, image="", justify=CENTER, borderwidth=0, background="#fffae6", activebackground="#fffae6", highlightthickness=0)
	drawing_lbl.place(x=0, y=175, width=200, height=250)

	reg = root.register(validate_input)
	guess_ent = Entry(root, justify=CENTER, validate="key", validatecommand=(reg, "%P"), background="#ffffff", foreground="#000000", highlightthickness=3, highlightcolor="black", highlightbackground="black", borderwidth=0, font=("Helvetica", 15))
	guess_ent.place(x=250, y=195, width=173, height=35)

	guess_btn = Label(root, text="Try", font=("Helvetica", 15, "bold"), justify=CENTER, borderwidth=0, background="#fffae6", activebackground="#fffae6", highlightthickness=3, highlightcolor="black", highlightbackground="black")
	guess_btn.place(x=420, y=195, width=80, height=35)
	guess_btn.bind("<Enter>", lambda event: change_thickness(event, guess_btn, False))
	guess_btn.bind("<Leave>", lambda event: change_thickness(event, guess_btn, True))
	guess_btn.bind("<ButtonRelease-1>", lambda event: guess_click(event))
	root.bind("<KeyRelease-Return>", lambda event: guess_click(event))

	missed_guesses_title = Label(root, text=" Misses:", font=("Helvetica", 12, "bold"), anchor="w", justify=CENTER, borderwidth=0, background="#fffae6", activebackground="#fffae6", highlightthickness=0, highlightcolor="black", highlightbackground="black")
	missed_guesses_title.place(x=250, y=230, width=250, height=25)

	missed_guesses = Label(root, text="", font=("Helvetica", 12, "bold"), anchor="n", justify=CENTER, borderwidth=0, background="#fffae6", activebackground="#fffae6", highlightthickness=0, highlightcolor="black", highlightbackground="black")
	missed_guesses.place(x=250, y=255, width=250, height=170)

	end_status_lbl = Label(root, text="", font=("Helvetica", 20, "bold"), anchor=CENTER, justify=CENTER, borderwidth=0, foreground="green", activeforeground="green", background="#fffae6", activebackground="#fffae6", highlightthickness=0, highlightcolor="black", highlightbackground="black")
	end_status_lbl.place(x=0, y=143, width=500, height=51)

	start_game()

	root.mainloop()


if __name__ == '__main__':
	main()
