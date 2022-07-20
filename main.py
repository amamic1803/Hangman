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
