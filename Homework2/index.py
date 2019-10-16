import sys
from lxml import etree
import string
import time


def printf(elements):
	for element in elements:
		print(etree.tostring(element, pretty_print = True))

avoidable = string.punctuation
avoidable = avoidable.replace("'","")
f_in = open(sys.argv[1])
tree = etree.parse(f_in)
root = tree.getroot()
all_keywords = {}

# author
for element in root.iter("book"):
	split_words = element.getchildren()[0].text.lower().split(", ")
	for keyword in split_words: 
		if keyword != '\n' and keyword not in all_keywords:
			all_keywords[keyword] = {}
		all_keywords[keyword][element.get("id")] = [] 
		all_keywords[keyword][element.get("id")].append(element.getchildren()[0].tag)

# title
for element in root.iter("book"):
	word = element.getchildren()[1].text.lower()
	for ch in avoidable:
		word = word.replace(ch,"")
	split_words = word.split(" ")
	for keyword in split_words:
		if keyword != '\n' and keyword not in all_keywords:
			all_keywords[keyword] = {}
		all_keywords[keyword][element.get("id")] = [] 
		all_keywords[keyword][element.get("id")].append(element.getchildren()[1].tag)


# genre
for element in root.iter("book"):
	split_words = element.getchildren()[2].text.lower() 
	if split_words != '\n' and split_words not in all_keywords:
		all_keywords[keyword] = {}
	all_keywords[keyword][element.get("id")] = [] 
	all_keywords[keyword][element.get("id")].append(element.getchildren()[2].tag)

# description
for element in root.iter("book"):
	sentence = element.getchildren()[5].text.lower().replace("\n","").replace("  ","")
	for ch in avoidable:
		sentence = sentence.replace(ch," ")
	split_words = sentence.split(" ")
	for keyword in split_words:
		if keyword != '' and keyword != '\n':
			if keyword not in all_keywords:
				all_keywords[keyword] = {}
			all_keywords[keyword][element.get("id")] = [] 
			all_keywords[keyword][element.get("id")].append(element.getchildren()[5].tag)

new_root = etree.Element("keywords_catalog") 
for key, val in all_keywords.items(): 
	keyword = etree.SubElement(new_root,"keyword") 
	keyword.text = key 
	for k,v in val.items(): 
		ids = etree.SubElement(keyword,"id") 
		ids.text = k 
		for att in v: 
			attr = etree.SubElement(ids,"attribute") 
			attr.text = att 


et = etree.ElementTree(new_root)
et.write(sys.argv[2],pretty_print=True)
