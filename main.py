#!/usr/bin/python
# Requires PyAudio and PySpeech.
# Requires a contacts.txt file with each line containing a name and phone number seperated by a space
import speech_recognition as sr
import time
import os
import numpy as np
import cv2
from gtts import gTTS
import webbrowser
from llama_cpp import Llama
import asyncio
import moviepy.editor as mpe
import pygame
from moviepy.editor import VideoFileClip
model="/tmp/ggml-vicuna-13b-4bit-rev1.bin"
audiofile="audio.mp3"

def readtxt(name):
	content = []
	with open(name+".txt", 'r') as file:
		for i in file.readlines():
			content.append(str(i).replace("\n",""))	
	return content	
def writetxt(name,content):
	with open(name+".txt", 'w') as file:
		for i in content:
			file.write(i+"\n")
		file.close()
def loadvideo(video_path):
    pygame.init()
    clip = VideoFileClip(video_path)
    clip.preview()

    pygame.quit()
    
def combine_audio(vidname, audname, outname, fps=25):
    my_clip = mpe.VideoFileClip(vidname)
    audio_background = mpe.AudioFileClip(audname)
    final_clip = my_clip.set_audio(audio_background)
    final_clip.write_videofile(outname,fps=fps)

def vicuniaanswer(text,promp="Act as my girlfriend and just answer this message '{text}' be kind and lovely ",model="models/ggml-vicuna-13b-4bit-rev1.bin"):
	llm=Llama(model_path=model)
	msg=promp.replace("{text}",text)
	ans=llm(msg)
	return ans["choices"][0]["text"]
	
def loadConfigurations():
	filename = "config"
	fristconfigurations= ["tim","jane"]
	try:
		configurations = readtxt(filename)
		vale = configurations
	except:	
		writetxt(filename,fristconfigurations)
		vale = fristconfigurations
	return vale
def speakold(audioString):
    print(audioString)
    tts = gTTS(text=audioString, lang='en')
    tts.save(audiofile)
    os.system("mpg123 audio.mp3")
def speak(audioString,vid="1"):
    print(audioString)
    tts = gTTS(text=audioString, lang='en')
    tts.save(audiofile)
    combine_audio("videos/voice/"+vid+".mp4",audiofile,"newvid.mp4")
    loadvideo("newvid.mp4")
    #os.system("mpg123 audio.mp3")

def recordAudio():
    # Record Audio
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
    
        # Speech recognition using Google Speech Recognition
        data = ""
        try:
            # Uses the default API key
            # To use another API key: `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            data = r.recognize_google(audio)
            print("You said: " + data)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            speak("I couldn't understand you")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
        data = data.lower()
        return data
    
def sendSMS():
    numbers = []
    names = []
    my_file = "contacts.txt"
        # open file in read mode
    with open(my_file, 'r') as file_handle:
            # convert file contents into a list
        lines = file_handle.read().splitlines()
        for i, val in enumerate(lines): 
            #split each line and appends name and number to respective list                
            person = val.split(" ", 1)
            names.append(person[0])
            numbers.append(person[1])
            print(i, names[i], numbers[i])
            if(i + 1 >= len(lines)):
                break
    speak("Select acontact by number: ")
    data = recordAudio()        
    i = data
    i = int(i)
    dest = numbers[i]
    speak("Record your message")
    data = recordAudio()
    message = data
    speak("Would you like to send " + message + " to " + names[i] + "?")
    data = recordAudio()
    if "yes" in data:
        os.system("kdeconnect-cli --send-sms '%s' -n s20 --destination %s"  % (message, dest))
        speak("Message sent to " + names[i])

def jane(name,data):
    name = str(name)+" "
    if name+"how are you" in data:
        speak("I am fine, thanks")

    elif name+"see you later" in data or "bye "+name in data or name+"bye" in data:
        exit()

    elif name+"what time is it" in data:
        print(time.ctime())
        speak(time.ctime())

    elif name+"where is" in data:
        data = data.split(" ", 2)
        location = data[2]
        speak("Hold on Tim, I will show you where " + location + " is.")
        webbrowser.open_new_tab("https://www.google.com/maps/place/" + location + "/&amp;")
        
    elif name+"search for" in data:
        data = data.split(" ", 2)
        search = data[2]
        speak("Hold on Tim, I will search for " + search)
        webbrowser.open_new_tab('http://www.google.com/search?btnG=1&q=' + search)
        
    elif name+"start" in data:
        data = data.split(" ", 1)
        start = data[1]
        start = start.lower()
        speak("Starting " + start)
        os.system(start + "&")
        
        
    elif "hey "+name in data:
        speak("Hey Tim, what's up?")
        
    elif name+"send text" in data:
        sendSMS()
        
    elif name+"open Instagram" in data:
        instagram = 'istekram'
        os.system(istekram + "&")
    elif name+"configuration" in data:
        configMenu()
    else:
        ans=vicuniaanswer(data)
        print(ans)
        speak(ans)
def configMenu():
	i = 0
	optionsAvibles= """
	1) change your username
	2) what do you want to call me
	3) going back
	"""
	filename = "config"
	attempts = 3
	speak(optionsAvibles)
	configurations = loadConfigurations()
	tmpConfigurations = configurations	
	while i < attempts:
		option = recordAudio()
		if option == "change your username" or "1":
			speak("how is you new username?")
			configurations[0] = recordAudio()
			speak("ok ,"+configurations[0]+" is right?"+"""
			1) yes			
			""")
			verification = recordAudio()
			if verification == "yes" or verification == "1":
				speak("ok ,"+configurations[0]+" Nice to meet you again ")
				break
			else:
				pass
		elif option == "what do you want to call me" or "2":
			speak("how you want to call me?")
			speak("ok ,"+configurations[1]+" is right?"+"""
			1) yes

			""")
			configurations[1] = recordAudio()
			if verification == "yes" or verification == "1":
				speak(configurations[1]+" ? i like that name ")
				break
		elif option == "going back" or "3":
			speak("as you wish it could be another time")
			configurations = tmpConfigurations 
			break
		else:
			pass
	writetxt(filename,configurations)
def banner():
	print("""
     _                                 Virtual
    | | __ _ _ __   ___   _ __  _   _  Assistant
 _  | |/ _` | '_ \ / _ \ | '_ \| | | |
| |_| | (_| | | | |  __/_| |_) | |_| |
 \___/ \__,_|_| |_|\___(_) .__/ \__, |
                         |_|    |___/ 
	""")
# initialization
def main():
	banner()
	configurations = loadConfigurations()
	speak("Hi "+configurations[0]+",I am "+configurations[1]+", how can I help?")

	while True:
    		time.sleep(0.5)
    		#data = recordAudio()
    		data = input()
    		jane(configurations[1],data)
if __name__ == "__main__":
	main()
