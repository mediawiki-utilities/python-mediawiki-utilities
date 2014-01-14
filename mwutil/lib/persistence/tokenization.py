import re

def simple_split(text):
	return re.findall(
		r"[\w]+|\[\[|\]\]|\{\{|\}\}|\n+| +|&\w+;|'''|''|=+|\{\||\|\}|\|\-|.",
		text
	)
