
import requests
from contextlib import suppress
import wave
from gradio_client import Client
import unicodedata


client = Client("http://127.0.0.1:7860/")

def api_call(line):
	print("line: " + line + "...")
	result = client.predict(
		"EN-Default",	# Literal['EN-Default", 'EN-US', 'EN-BR', 'EN_INDIA', 'EN-AU']  in 'Speaker' Dropdown component
		line,	# str  in 'Text to speak' Textbox component
		1,	# float (numeric value between 0.1 and 10.0) in 'Speed' Slider component
		api_name="/synthesize")
	return result

def concatenate_wavs(*files):
	with wave.open(r'f:\temp\tts\chosenone.wav', 'wb') as out:
		data=[]
		for file in files:
			print ("appending " + file + "...")
			w = wave.open (file, 'rb')
			data.append([w.getparams(), w.readframes(w.getnframes())] )
			w.close()

		out.setparams(data[0][0])
		for i in range (len(data)):
			out.writeframes(data [i][1])
		out.close()

def prep(line):
	#line=''.join(c for c in line if c.isprintable())
	#line.encode().decode('unicode-escape')
	#line.decode("utf-8")
	#line = line.encode('unicode_escape').decode('utf-8')
	line.replace("\u2026","...").replace(":","...").replace(";","...").replace("â€”","...").replace(u"\u2014","...")
	line = line.replace("\u2019","'").replace("\u201c","\u0022").replace("\u201d","\u0022")
	return line.strip()

# replace smart quotes, also colons, semicolons, dashes, …
with open(r'F:\temp\tts\chosenone.txt', 'r') as f:
	lines = [prep(line) for line in f]
concatenate_wavs(*[api_call(line) for line in lines if line])



