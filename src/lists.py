import nltk

#Error Reply
defaultReply = 'Im sorry, I did not get that, please tell me a single command'

#Confirmation
areYouSure= 'Are you sure you want me to'
confirmList= ['confirm', 'confirmed', 'yup', 'yes', 'ok', 'go', 'sure']

#Command List
greetList = ['hello','hi', 'hey']
greetBack = "Hello Buddy, Please tell me a single command"

#Command List
cmdList = ['take','off', 'takeoff', 'land', 'fly', 'land', 'return', 'down', 'stop', 'go', 'head', 'hello', 'hi', 'hey']

#Take off Commands
takeoffList = ['take','off', 'takeoff', 'fly']
checkTakeOffSafely = 'Checking if its safe to take off'
areYouSureTakeOff = "are you sure you want me to take off"
cantTakeOff=('I can not take off, please ensure that I am sitting on a flat surface')
takingOff = 'I will take off now'

#Land Commands
landList = ['land','return', 'down', 'stop']
landingNow = 'Landing now to the nearest safe area'

# Go to Location
goToList = ['go', 'head']
locationPosition = [("station", 0, 0), ("kitchen" , -5.0, 6.2), ("living" , 15.3,11.2), ("washroom" , 6.3,3.2),("office" , -3.5,-3.9), ("bedroom" , 7,2.9)]
goingTo = "I am going to the"
eta = "Estimated time of arrival is about"

#for x in locationPosition:
  #if(x[0] is "kitchen"):
    #print(x[1], x[2])