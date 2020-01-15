"""Very simple cevac table name shortener for lasr."""

from sys import argv


table = argv[-1].replace("\n","")

name_to_shortened = {
    "CEVAC" : "C",
    "LASR" : "",
    "LIVE" : "LAT"
}

words = table.split("_")
for i, word in enumerate(words):
    if word.upper() in name_to_shortened:
        words[i] = name_to_shortened[word.upper()]
    elif i > 1:
        words[i] = words[i][:3]

words = [word for word in words if word != ""]

print("_".join(words),end="")
