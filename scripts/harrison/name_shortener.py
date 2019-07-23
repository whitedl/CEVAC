"""Very simple cevac table name shortener for lasr."""

from sys import argv


table = argv[-1]

name_to_shortened = {
    "CEVAC": "C",
}

words = table.split("_")
for i, word in enumerate(words):
    if word.upper() in name_to_shortened:
        words[i] = name_to_shortened[word.upper()]
    elif i > 1:
        words[i] = words[i][:3]

print("_".join(words))
