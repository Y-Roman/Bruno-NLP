# Importing all the necessary modules
import os
import time
import math
import gtts
from tkinter import *
from tkinter.messagebox import showinfo
import speech_recognition as sr
from playsound import playsound
from lists import *
from droneData import *

Query = "Nothing"
Reply = "Nothing"
vel = 1.0 #m/s

def speak(text):
    tts = gtts.gTTS(text)
    tts.save(text+'.mp3')
    playsound(text+'.mp3')
    os.remove(text+'.mp3')

def record():
    text.delete(1.0,END)
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        audio = r.listen(source)
        try:
            global Query
            Query = r.recognize_google(audio, language="en-IN")
            print(Query)
            process()
        except Exception as e:
            showinfo(title='Error!', message=e)
            return "Nothing"
        return Query

def reply():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        audio = r.listen(source)
        try:
            global Reply
            Reply = r.recognize_google(audio, language="en-IN")
            print(Reply)
        except Exception as e:
            showinfo(title='Error!', message=e)
            return "Nothing"
        return Reply

def process():
    if Query == "Nothing":
        return
    queryList = list(Query.split(' '))
    print(queryList)
    setList = set(queryList) & set(cmdList)
    print(setList)
    keywords = sorted(setList, key = lambda k: queryList.index(k))
    print(keywords)
    if not keywords:
        speak(defaultReply)
    else:
        ################  Take OFF   #####################
        if any(item in keywords for item in takeoffList):
            speak(areYouSureTakeOff)
            replyText = reply()
            replyList = list(replyText.split(' '))
            print(replyList)
            if not any(item in replyList for item in confirmList):
                return
            speak(checkTakeOffSafely)
            if(isReadyToTakeOff()):
                speak(takingOff)
            else:
                speak(cantTakeOff)
        ################    Land     #####################
        elif any(item in keywords for item in landList):
            speak(landingNow)
        ################  Go To Location   #####################
        elif any(item in keywords for item in goToList):
            for x in locationPosition:
                if(x[0] in queryList):
                    print(x[1], x[2])
                    speak(goingTo + x[0])
                    duration = round((math.sqrt(x[1]*x[1]+x[2]*x[2]))/vel,2)
                    print(duration)
                    duration = str(duration)
                    speak(eta + duration + "seconds")
        elif any(item in queryList for item in greetList):
            speak(greetBack)
                   
        else:
            return
    text.delete(1.0,END)
    return
   
# Creating the main GUI window
root = Tk()
root.title('SOTI AEROSPACE Voice Command Proof of Concept')
root.geometry('500x425')
root.resizable(0, 0)
img = PhotoImage(file="drone4.PNG")
label = Label(
    root,
    image=img
)
label.place(x=-100, y=-10)


# Placing all the components
Label(root, text='SOTI AEROSPACE Voice Control PoC',
      font=('Comic Sans MS', 16), bg='Salmon', wrap=True, wraplength=500).place(x=50, y=10)
text = Text(root, font=12, height=3, width=37)
text.place(x=80, y=350)

record_btn = Button(root, text='Record', bg='Sienna', command=lambda:text.insert(END, record()))
record_btn.place(x=250, y=300)

# Updating main window
root.update()
root.mainloop()