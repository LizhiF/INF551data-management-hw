import sys
from lxml import etree
import string
import time


avoidable = string.punctuation
avoidable = avoidable.replace("'","")
stop_words = ['a','an','the','of','to','as','only','he','she','it','they','his','her','and','are','into']

def printf(elements):
	for element in elements:
		print(etree.tostring(element, pretty_print = True))

# def make_elements(new_root,split_words,child_no):
# 	if child_no == 2:

# 	for keyword in split_words: 
# 		child = etree.SubElement(new_root,"keyword") 
# 		child.text = keyword
# 		sub_child = etree.SubElement(child, "id")
# 		sub_child.text = element.get("id")
# 		another_child = etree.SubElement(child,str(element.getchildren()[child_no].tag))
# 		another_child.text = element.getchildren()[child_no].text
# 		return new_root

f_in = open(sys.argv[1])
#f_out = open(sys.argv[2])

tree = etree.parse(f_in)
#print(etree.tostring(tree, pretty_print = True))

root = tree.getroot()
new_root = etree.Element("keywords_catalog")

# author
for element in root.iter("book"):
	#print(element.tag, element.attrib)
	#print(element.getchildren()[0].text)
	split_words = element.getchildren()[0].text.lower().split(", ")
	#print(split_words)
	for keyword in split_words: 
		child = etree.SubElement(new_root,"keyword") 
		child.text = keyword
		child.set("id",element.get("id"))
		child.set(str(element.getchildren()[1].tag),element.getchildren()[1].text)
		# sub_child = etree.SubElement(child, "id")
		# sub_child.text = element.get("id")
		# another_child = etree.SubElement(child,str(element.getchildren()[0].tag))
		# another_child.text = element.getchildren()[0].text
	#new_root = make_elements(new_root,split_words,0)

# title
for element in root.iter("book"):
	#print(element.getchildren()[1].text)
	word = element.getchildren()[1].text.lower()
	for ch in avoidable:
		word = word.replace(ch,"")
	split_words = word.split(" ")
	#print(split_words)	
	for keyword in split_words:
		child = etree.SubElement(new_root,"keyword")
		child.text = keyword
		child.set("id",element.get("id"))
		child.set(str(element.getchildren()[1].tag),element.getchildren()[1].text)
		#sub_child = etree.SubElement(child, "id")
		#sub_child.text = element.get("id")
		#another_child = etree.SubElement(child,str(element.getchildren()[1].tag))
		#another_child.text = element.getchildren()[1].text
	#new_root = make_elements(new_root,split_words,1)


# genre
for element in root.iter("book"):
	split_words = element.getchildren()[2].text.lower() 
	#print(split_words)	
	#new_root = make_elements(new_root,split_words,2)
	child = etree.SubElement(new_root,"keyword")
	child.text = split_words
	child.set("id",element.get("id"))
	child.set(str(element.getchildren()[1].tag),element.getchildren()[1].text)
	# sub_child = etree.SubElement(child, "id")
	# sub_child.text = element.get("id")
	# another_child = etree.SubElement(child,str(element.getchildren()[2].tag))
	# another_child.text = element.getchildren()[2].text

# description
for element in root.iter("book"):
	#print(element.getchildren()[5].text)
	sentence = element.getchildren()[5].text.lower().replace("\n","").replace("  ","")
	#print(sentence)
	for ch in avoidable:
		sentence = sentence.replace(ch," ")
	split_words = sentence.split(" ")
	#print(split_words)	
	#new_root = make_elements(new_root,split_words,5)
	for keyword in split_words:
		if keyword != '':
			child = etree.SubElement(new_root,"keyword")
			child.text = keyword
			# sub_child = etree.SubElement(child, "id")
			# sub_child.text = element.get("id")
			# another_child = etree.SubElement(child,str(element.getchildren()[5].tag))
			# another_child.text = element.getchildren()[5].text
			child.set("id",element.get("id"))
			child.set(str(element.getchildren()[1].tag),element.getchildren()[1].text)		
et = etree.ElementTree(new_root)
et.write(sys.argv[2],pretty_print=True)
