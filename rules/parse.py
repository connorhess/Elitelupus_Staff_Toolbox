import pprint
import json

RULES = {}
LETTER_TO_NUMBER = {'a':1, 'b':2, 'c':3, 'd':4, 'e':5}

with open("General_Server_Rules.txt", 'r') as f:
	text = f.read()

lines = text.split('\n')

def get_number_letter(text):

	index = text.find("(")
	substring = text[index + 1:index + 2]
	if len(substring) == 1 and text[index + 2] == ")":
	    return substring
	else:
	    # print("There is more than one character between the parentheses.")
	    return None

current_topic = None
new_data = []
for line in lines:
	number, rule = line.split('-;-')
	number_og = number
	if '.0' in number:
		current_topic = rule
		RULES[current_topic] = []
	else:
			# print(rule)
		number_text = f"{number_og}"
		if get_number_letter(rule) != None:
			letter = get_number_letter(rule)
			number = f"{number}.{LETTER_TO_NUMBER[letter]}"
			number_text = f"{number_og} ({letter})"
			rule = rule.replace(f"({letter}) ", '')



		RULES[current_topic].append({"Number": number,
								"Number Text": number_text,
								"Text": rule,
								"Notes": [],
								"Punishments": []
								})
		# print(rule)

			

	# new_data.append(line.split('-;-'))


# pprint.pprint(RULES)
# print(RULES)
print(json.dumps(RULES))