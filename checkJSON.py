# libraries
import json

with open('combinedData.json') as f:
    cJSON = json.load(f)

# counter variable
i = 0

for key in cJSON:
    length = len(cJSON[key])
    if length != 3:
        i += 1

print('-~- THERE ARE {} INCORRECT FORMATS -~-'.format(i))
