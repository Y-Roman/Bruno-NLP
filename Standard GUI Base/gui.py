# Importing all the necessary modules
import os
import gtts
from tkinter import *
from tkinter.messagebox import showinfo
import speech_recognition as sr
from playsound import playsound

cmdList = ['take','off', 'takeoff', 'land']
defaultReply = 'Im sorry, I did not get that, please tell me a single command'
Query = "Nothing"

def speak(text):
    tts = gtts.gTTS(text)
    tts.save(text+'.mp3')
    print('speaking')
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
            #set_text()
            process()
        except Exception as e:
            showinfo(title='Error!', message=e)
            return "Nothing"
        return Query

def process():
    print(Query)
    if Query == "Nothing":
        return
    queryList = list(Query.split(' '))
    setList = set(queryList) & set(cmdList)
    print(setList)
    keywords = sorted(setList, key = lambda k: queryList.index(k))
    print(keywords)
    if not keywords:
        speak(defaultReply)
    text.delete(1.0,END)
    return
    
def set_text():
    print('This is T')
    #print(t)
    text.insert(END, Query)
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
text.place(x=100, y=350)

record_btn = Button(root, text='Record', bg='Sienna', command=lambda:text.insert(END, record()))
#record_btn = Button(root, text='Record', bg='Sienna', command=lambda: [process(), record()])
#record_btn = Button(root, text='Record', bg='Sienna', command=lambda:[set_text(record()), process()])

record_btn.place(x=250, y=300)

# Updating main window
root.update()
root.mainloop()