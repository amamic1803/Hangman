import os
import random
import sys
import tkinter as tk
from tkinter.messagebox import askyesno


def resource_path(relative_path):
	""" Get absolute path to resource, works for dev and for PyInstaller """
	try:
		# PyInstaller creates a temp folder and stores path in _MEIPASS
		base_path = sys._MEIPASS
	except AttributeError:
		base_path = os.path.abspath(".")
	return os.path.join(base_path, relative_path)

def validate_input(full_text):
	if full_text == "":
		return True
	elif full_text.isalpha() and len(full_text) <= 11:
		return True
	else:
		return False


class App:
	def __init__(self):
		self.selected_language = "en"
		self.ended = True
		self.guessed_letters = []
		self.missed_letters = []
		self.word_letters = []
		self.letter_coords = []
		self.word = ""

		with open(resource_path("resources/words/en_words.txt"), "r", encoding="utf-8") as file:
			self.en_words = [i.rstrip("\n").upper() for i in file.readlines()]
		with open(resource_path("resources/words/hr_words.txt"), "r", encoding="utf-8") as file:
			self.hr_words = [i.rstrip("\n").upper() for i in file.readlines()]

		self.root = tk.Tk()
		self.root.title("Hangman")
		self.root.resizable(False, False)
		self.root.geometry(f"500x425"
		                   f"+{self.root.winfo_screenwidth() // 2 - 250}"
		                   f"+{self.root.winfo_screenheight() // 2 - 212}")
		self.root.iconbitmap(resource_path("resources/hang-icon.ico"))
		self.root.config(background="#fffae6")

		self.hangman_images = [tk.PhotoImage(file=resource_path(f"resources/images//hangman_{i}.png")) for i in range(1, 10)]
		self.restart_img_small = tk.PhotoImage(file=resource_path("resources/images/hangman-restart_smaller.png"))
		self.restart_img_big = tk.PhotoImage(file=resource_path("resources/images/hangman-restart_bigger.png"))

		self.title = tk.Label(self.root, text="Hangman", font=("Gabriola", 40, "bold"),
		                      borderwidth=0, background="#fffae6", activebackground="#fffae6")
		self.title.place(x=0, y=0, width=500, height=75)

		self.en_lbl = tk.Label(self.root, text="EN", font=("Helvetica", 12, "bold"), justify=tk.CENTER, cursor="hand2",
		                       borderwidth=0, background="#fffae6", activebackground="#fffae6", highlightthickness=2,
		                       highlightcolor="black", highlightbackground="black")
		self.en_lbl.place(x=430, y=0, width=35, height=25)
		self.en_lbl.bind("<Enter>", lambda event: self.en_lbl.config(highlightthickness=4) if self.selected_language != "en" else None)
		self.en_lbl.bind("<Leave>", lambda event: self.en_lbl.config(highlightthickness=0) if self.selected_language != "en" else None)
		self.en_lbl.bind("<ButtonRelease-1>", lambda event: self.change_language("en"))

		self.hr_lbl = tk.Label(self.root, text="HR", font=("Helvetica", 12, "bold"), justify=tk.CENTER, cursor="hand2",
		                       borderwidth=0, background="#fffae6", activebackground="#fffae6", highlightthickness=0,
		                       highlightcolor="black", highlightbackground="black")
		self.hr_lbl.place(x=465, y=0, width=35, height=25)
		self.hr_lbl.bind("<Enter>", lambda event: self.hr_lbl.config(highlightthickness=4) if self.selected_language != "hr" else None)
		self.hr_lbl.bind("<Leave>", lambda event: self.hr_lbl.config(highlightthickness=0) if self.selected_language != "hr" else None)
		self.hr_lbl.bind("<ButtonRelease-1>", lambda event: self.change_language("hr"))

		self.restart_lbl = tk.Label(self.root, image=self.restart_img_small, cursor="hand2",
		                            anchor=tk.CENTER, justify=tk.CENTER,
		                            borderwidth=0, background="#fffae6", activebackground="#fffae6",
		                            highlightbackground="#fffae6", highlightthickness=0)
		self.restart_lbl.place(x=0, y=0, width=45, height=45)
		self.restart_lbl.bind("<ButtonRelease-1>", lambda event: self.start_game(restart=True))
		self.restart_lbl.bind("<Enter>", lambda event: self.restart_lbl.config(image=self.restart_img_big))
		self.restart_lbl.bind("<Leave>", lambda event: self.restart_lbl.config(image=self.restart_img_small))

		self.word_canvas = tk.Canvas(self.root, borderwidth=0, highlightthickness=0, background="#fffae6")
		self.word_canvas.place(x=0, y=100, width=500, height=50)

		self.drawing_lbl = tk.Label(self.root, image="", justify=tk.CENTER, borderwidth=0, background="#fffae6",
		                            activebackground="#fffae6", highlightthickness=0)
		self.drawing_lbl.place(x=0, y=175, width=200, height=250)

		self.reg = self.root.register(validate_input)
		self.guess_ent = tk.Entry(self.root, justify=tk.CENTER, validate="key", validatecommand=(self.reg, "%P"),
		                          background="#ffffff", foreground="#000000", highlightthickness=3,
		                          highlightcolor="black", highlightbackground="black", borderwidth=0,
		                          font=("Helvetica", 15))
		self.guess_ent.place(x=250, y=195, width=173, height=35)

		self.guess_btn = tk.Label(self.root, text="Try", font=("Helvetica", 15, "bold"), justify=tk.CENTER, cursor="hand2",
		                          borderwidth=0, background="#fffae6", activebackground="#fffae6", highlightthickness=3,
		                          highlightcolor="black", highlightbackground="black")
		self.guess_btn.place(x=420, y=195, width=80, height=35)
		self.guess_btn.bind("<Enter>", lambda event: self.guess_btn.config(highlightthickness=5))
		self.guess_btn.bind("<Leave>", lambda event: self.guess_btn.config(highlightthickness=3))
		self.guess_btn.bind("<ButtonRelease-1>", lambda event: self.guess_click())

		self.root.bind("<KeyRelease-Return>", lambda event: self.guess_click())

		self.missed_guesses_title = tk.Label(self.root, text=" Misses:", font=("Helvetica", 12, "bold"), anchor="w",
		                                     justify=tk.CENTER, borderwidth=0, background="#fffae6",
		                                     activebackground="#fffae6", highlightthickness=0, highlightcolor="black",
		                                     highlightbackground="black")
		self.missed_guesses_title.place(x=250, y=230, width=250, height=25)

		self.missed_guesses = tk.Label(self.root, text="", font=("Helvetica", 12, "bold"),
		                               anchor="n", justify=tk.CENTER, borderwidth=0,
		                               background="#fffae6", activebackground="#fffae6", highlightthickness=0,
		                               highlightcolor="black", highlightbackground="black")
		self.missed_guesses.place(x=250, y=255, width=250, height=170)

		self.end_status_lbl = tk.Label(self.root, text="", font=("Helvetica", 20, "bold"),
		                               anchor=tk.CENTER, justify=tk.CENTER, borderwidth=0, foreground="green",
		                               activeforeground="green", background="#fffae6", activebackground="#fffae6",
		                               highlightthickness=0, highlightcolor="black", highlightbackground="black")
		self.end_status_lbl.place(x=0, y=143, width=500, height=51)

		self.start_game()

		self.root.mainloop()

	def change_language(self, language):
		if self.selected_language != language:
			if not self.ended and (len(self.guessed_letters) > 0 or len(self.missed_letters) > 0):
				match self.selected_language:
					case "en":
						end_game = askyesno("Game in progress!", "Are you sure you want to start a new game?")
					case "hr":
						end_game = askyesno("Igra u tijeku!", "Jeste li sigurni da želite pokrenuti novu igru?")
					case _:
						end_game = None
			else:
				end_game = True
			if end_game:
				match language:
					case "en":
						self.en_lbl.config(highlightthickness=2)
						self.hr_lbl.config(highlightthickness=0)
						self.root.title("Hangman")
						self.title.config(text="Hangman")
						self.guess_btn.config(text="Try")
						self.missed_guesses_title.config(text=" Missed:")
					case "hr":
						self.en_lbl.config(highlightthickness=0)
						self.hr_lbl.config(highlightthickness=2)
						self.root.title("Vješala")
						self.title.config(text="Vješala")
						self.guess_btn.config(text="Probaj")
						self.missed_guesses_title.config(text=" Promašaji:")
				self.selected_language = language
				self.start_game()
			else:
				match language:
					case "en":
						self.en_lbl.config(highlightthickness=0)
					case "hr":
						self.hr_lbl.config(highlightthickness=0)

	def start_game(self, restart=False):
		self.restart_lbl.config(image=self.restart_img_small)

		if restart:
			if not self.ended and (len(self.guessed_letters) > 0 or len(self.missed_letters) > 0):
				match self.selected_language:
					case "en":
						end_game = askyesno("Game in progress!", "Are you sure you want to start a new game?")
					case "hr":
						end_game = askyesno("Igra u tijeku!", "Jeste li sigurni da želite pokrenuti novu igru?")
					case _:
						end_game = None
				if not end_game:
					return

		self.word_canvas.delete("all")
		self.missed_guesses.config(text="")
		self.end_status_lbl.config(text="")
		self.drawing_lbl.config(image="")

		self.letter_coords = []
		self.word_letters = []
		self.guessed_letters = []
		self.missed_letters = []
		self.ended = False

		match self.selected_language:
			case "en":
				self.word = random.choice(self.en_words)
				self.word_letters = [x for x in self.word]
				len_word = len(self.word)
				start_coord = (500 - (len_word * 30 + (len_word - 1) * 11)) // 2
				line_or_space = True
				for i in range(2 * len_word - 1):
					if line_or_space:
						self.word_canvas.create_line(start_coord, 40, start_coord + 30, 40, fill="black", width=4)
						self.letter_coords.append(start_coord + 14)
						line_or_space = False
						start_coord += 30
					else:
						start_coord += 11
						line_or_space = True
			case "hr":
				self.word = random.choice(self.hr_words)
				word_temp = self.word
				while len(word_temp) > 0:
					if len(word_temp) == 1:
						self.word_letters.append(word_temp)
						word_temp = ""
					elif word_temp[0:2] in ["DŽ", "NJ", "LJ"]:
						self.word_letters.append(word_temp[0:2])
						word_temp = word_temp[2:]
					else:
						self.word_letters.append(word_temp[0])
						word_temp = word_temp[1:]
				len_word = len(self.word_letters)
				start_coord = (500 - (len_word * 30 + (len_word - 1) * 11)) // 2
				line_or_space = True
				for i in range(2 * len_word - 1):
					if line_or_space:
						self.word_canvas.create_line(start_coord, 40, start_coord + 30, 40, fill="black", width=4)
						self.letter_coords.append(start_coord + 14)
						line_or_space = False
						start_coord += 30
					else:
						start_coord += 11
						line_or_space = True

		return True

	def guess_click(self):
		inpt = self.guess_ent.get().upper()
		self.guess_ent.delete(0, tk.END)

		if len(inpt) != 0:
			if inpt in self.word_letters and inpt not in self.guessed_letters:
				self.guessed_letters.append(inpt)
				to_end = True
				for i in range(len(self.word_letters)):
					if self.word_letters[i] == inpt:
						self.word_canvas.create_text(self.letter_coords[i], 40, text=inpt,
						                             font=("Helvetica", 21, "bold"),fill="black",
						                             activefill="black", anchor="s")
					if self.word_letters[i] not in self.guessed_letters:
						to_end = False
				if to_end:
					self.ended = True
					match self.selected_language:
						case "en":
							self.end_status_lbl.config(text="Victory!", foreground="green", activeforeground="green")
						case "hr":
							self.end_status_lbl.config(text="Pobjeda!", foreground="green", activeforeground="green")
			elif inpt == self.word and not self.ended:
				for i in range(len(self.word_letters)):
					if self.word_letters[i] not in self.guessed_letters:
						self.word_canvas.create_text(self.letter_coords[i], 40, text=self.word_letters[i],
						                             font=("Helvetica", 21, "bold"), fill="black", activefill="black",
						                             anchor="s")
				self.ended = True
				match self.selected_language:
					case "en":
						self.end_status_lbl.config(text="Victory!", foreground="green", activeforeground="green")
					case "hr":
						self.end_status_lbl.config(text="Pobjeda!", foreground="green", activeforeground="green")
			elif not self.ended:
				self.missed_letters.append(inpt)
				self.missed_guesses.config(text="\n".join(self.missed_letters))
				self.drawing_lbl.config(image=self.hangman_images[len(self.missed_letters) - 1])
				if len(self.missed_letters) == 9:
					self.ended = True
					match self.selected_language:
						case "en":
							self.end_status_lbl.config(text="Fail!", foreground="red", activeforeground="red")
						case "hr":
							self.end_status_lbl.config(text="Poraz!", foreground="red", activeforeground="red")
					for i in range(len(self.word_letters)):
						if self.word_letters[i] not in self.guessed_letters:
							self.word_canvas.create_text(self.letter_coords[i], 40, text=self.word_letters[i],
							                             font=("Helvetica", 21, "bold"), fill="black",
							                             activefill="black", anchor="s")


def main():
	App()


if __name__ == '__main__':
	main()
