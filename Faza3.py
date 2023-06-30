import speech_recognition as sr
import random
from gtts import gTTS
import pygame
import os
import wikipedia
import pywhatkit as py
import datetime
import json
import cv2
import face_recognition
from time import sleep
wikipedia.set_lang("ar")




def Speak(text):
    pygame.mixer.init()
    playsa = pygame.mixer.music
    text = text
    myfile = 'speak.mp3'
    obj = gTTS(text=text, lang='ar')
    obj.save(myfile)
    playsa.load(myfile)
    playsa.play()
    while playsa.get_busy() == True:
        continue
    pygame.mixer.quit()
    if os.path.isfile(myfile):
        os.remove(myfile)
    else:
        pass

def Get_audio():
    r = sr.Recognizer()
    with sr.Microphone(device_index=0) as source:
        print("I am listening...")
        r.adjust_for_ambient_noise(source, duration=0.2)
        audio = r.listen(source, timeout=1, phrase_time_limit=5)
    try:
        datas = r.recognize_google(audio, language='ar-SA')
        print(datas)
    except Exception as e:
        print("Say that again please")
    return datas

def set_reminder():
    Speak('بماذا يجب ان اذكرك؟')
    reminder = Get_audio()
    Speak('حسنا!, الان اخبرني متى يجب ان اذكرك بذلك؟, ارجو ان تذكر الساعة ثم الدقيقة')
    reminder_time = Get_audio()
    try:
        hour, minute = map(int, reminder_time.split())
        now = datetime.datetime.now()
        reminder_datetime = now.replace(hour=hour, minute=minute)
        if now > reminder_datetime:
            reminder_datetime += datetime.timedelta(days=1)
        Speak(f"حسنا سوف اذكرك ب '{reminder}' في تمام الساعة {hour:02d}:{minute:02d}.")
        while True:
            if datetime.datetime.now() >= reminder_datetime:
                Speak(f"تذكر لديك موعد الان وهو : {reminder}")
                break
    except ValueError:
        Speak( "اسف لم افهم بالتوقيت الذي زودتني به")

def Create_todo_list():
    todo_list = []
    Speak("هيا بنا ننشئ قائمة المهام..., ارجو ان تذكر القائمة مهمة مهمة, قل تم عند الانتهاء من قائمة المهام")
    while True:
        task = Get_audio()
        if task == "تم":
            break
        todo_list.append(task)
        Speak(f"تم اضافة : {task}")
    Speak("هذه هي قائمة مهامك...:")
    for task in todo_list:
        Speak(task)

def Search():
    Speak('عن ماذا تريد مني ان ابحث لك')
    search = Get_audio()
    Speak(wikipedia.summary(search, sentences = 1))

def music():
    Speak('ما هو الفيديو الذي تريد ان اعرضه لك؟')
    video = Get_audio()
    py.playonyt(video)

def JSearch(tag):
    with open('intents.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    for intent in data['intents']:
        if intent['tag'] == tag:
            patterns = intent['patterns']
            responses = intent['responses']
            break
    responses = random.choice(responses)
    return responses

def CheckPerson():
    capture()
    for image in os.listdir():
        if(image.endswith(".jpg")):
            if image == 'capture.jpg':
                pass
            elif FaceDetect(image) == True:
                Speak('لقد تعرفت عليك.... انت')
                Speak(image)
        else:
            AddPerson)()

def AddPerson():
    Speak('سوف اقوم بإضاقة شخص جديد ليتم التعرف عليه لاحقا')
    Speak('اذكر لي اسمك')
    new_name = Get_audio()
    Speak('الان اريد ان التقط لك صورة حتى احتفظ بالشخص')
    capture()
    os.rename("capture.jpg", new_name)
    Speak('تم اضاقة الشخص الجديد')

def FaceDetect(images):
    #**************************************
   # load and open for two picture
   #**************************************
   imgSh = face_recognition.load_image_file("capture.jpg")
   imgSh = cv2.cvtColor(imgSh,cv2.COLOR_RGB2BGR)
   imgtest = face_recognition.load_image_file(images)
   imgtest = cv2.cvtColor(imgtest,cv2.COLOR_RGB2BGR)
   #**************************************
   #Select and pin the face for two picture
   #**************************************
   faceLoc = face_recognition.face_locations(imgSh)[0]
   encodeSh = face_recognition.face_encodings(imgSh)[0]
   cv2.rectangle(imgSh,(faceLoc[3],faceLoc[0]),(faceLoc[1],faceLoc[2]),(255,0,255),2)
   faceLocTest = face_recognition.face_locations(imgtest)[0]
   encodetest = face_recognition.face_encodings(imgtest)[0]
   cv2.rectangle(imgtest,(faceLocTest[3],faceLocTest[0]),(faceLocTest[1],faceLocTest[2]),(255,0,255),2)
   #**************************************
   #compare between two picture and get the resualt if it the same face that will print True
   #**************************************
   results = face_recognition.compare_faces([encodeSh],encodetest)
   x= results[0]
   print(x)
   images = images.replace(".jpg","")
   print(images)
   Speak(images)
   #**************************************
   return x

def capture():
   cap = cv2.VideoCapture(0)
   ret, frame = cap.read()
   rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
   out = cv2.imwrite('capture.jpg', frame)

def main():
    Speak('مرحبا, كيف يمكنني مساعدتك؟')
    while True:
        try:
            text = Get_audio()
            if 'فزاع' in text:
                Speak('ارحب')
                text = Get_audio()
                if text == 'توقف':
                    Speak('مع السلامة')
                    sleep(3600)
                else:
                    if text is not None:
                        response = JSearch(text)
                        if response is not None:
                            Speak(response)
        except:
            continue

main()