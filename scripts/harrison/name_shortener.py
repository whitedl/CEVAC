"""Very simple cevac table name shortener for lasr."""

from sys import argv


table = argv[-1]

name_to_shortened = {
    "CEVAC": "C",
    "POWER": "PO",
    "SUMS": "SU",
    "COMPARE": "CO",
    "LATEST": "LA",
    "BROKEN": "BR",
    "LASR": "LASR",
}

words = table.split("_")
for i, word in enumerate(words):
    if word.upper() in name_to_shortened:
        words[i] = name_to_shortened[word.upper()]
print("_".join(words))
