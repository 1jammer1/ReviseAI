# please forgive our horrible code
import os
import ollama

ollama.pull('codellama:7b-instruct')
os.system("ollama serve")
print("ollama process ended")


## undefined