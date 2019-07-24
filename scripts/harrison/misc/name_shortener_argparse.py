"""Very simple cevac table name shortener for lasr."""

from sys import argv
import argparse

# Argument Parsing
parser = argparse.ArgumentParser()
parser.add_argument('-r', '-raw', '-R', help='Raw, disable', default="True", type=bool, dest="dog")
parser.add_argument('-foo', help='Raw, disable', default="True", type=bool)
args = parser.parse_known_args()[0]
dog = args.dog
print(dog, type(dog))
print(args)



table = argv[-1].replace("\n","")

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

words = [word for word in words if word != ""]

print("_".join(words),end="")
