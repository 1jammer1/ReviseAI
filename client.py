# please forgive my horrible code
import ollama
from ollama import Client
import os
import re

server = input("whats the servers ip: ")
foldy = input("where is the codes folder: ")

server = "http://" + server + ":11434"

client = Client(host=server)

code = []




def prompt(jeff):
	response = client.chat(model='codellama:7b-instruct', messages=[
	  {
	    'role': 'user',
	    'content': jeff,
	  },
	])



def index_code():
	# fix and implement multiple directorys
	for item in os.listdir(foldy):
		match = re.search(".py", item)
		if match:
			print("HEY")
			code.append(item)
		# makes code valid for some reason


index_code()
print(code)