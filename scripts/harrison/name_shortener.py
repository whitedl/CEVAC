"""Very simple cevac table name shortener for lasr."""

from sys import argv


table = argv[-1]

name_to_shortened = {
    "CEVAC" : "C",
    "LASR" : "",
}

words = table.split("_")
for i, word in enumerate(words):
    if word.upper() in name_to_shortened:
        words[i] = name_to_shortened[word.upper()]
    elif i > 1:
        words[i] = words[i][:3]


output = "_".join(words)
if output.endswith("_"):
    output = output[:-1]

print(output)
