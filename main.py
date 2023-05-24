import customtkinter
import tkinter
import wave
from pvrecorder import PvRecorder
import threading
import struct
import time
import os

from voice import transcribe
import summarize as summi

customtkinter.set_appearance_mode('System')
customtkinter.set_default_color_theme('blue')

devices = PvRecorder.get_audio_devices()
global deviceIndex
deviceIndex = 0
global recorder
recorder = PvRecorder(device_index=0, frame_length=512)
global sumfunc
sumfunc = summi.summarizeLecture


for index, device in enumerate(devices):
    print(f"[{index}] {device}")

def selectDevice(choice):
    global recorder
    deviceIndex = devices.index(choice)
    recorder = PvRecorder(device_index=deviceIndex, frame_length=512)

summarizeTypes = [
    'Lecture',
    'Conversation',
    'Story',
    'Instructions'
]

def setSummaryType(choice):
    global sumfunc
    if choice == 'Lecture':
        sumfunc = summi.summarizeLecture
    elif choice == 'Conversation':
        sumfunc = summi.summarizeConversation
    elif choice == 'Story':
        sumfunc = summi.summarizeStory
    elif choice == 'Instructions':
        sumfunc = summi.summarizeInstructions
    else:
        sumfunc = summi.summarizeLecture


app = customtkinter.CTk()
app.geometry("800x400")
app.title('Summarize This')

everythingbuttonText = customtkinter.StringVar(app, "Record")

outputbox = customtkinter.CTkTextbox(master=app, width=400)
deviceDropdown = customtkinter.CTkComboBox(master=app, values=devices, command=selectDevice, width=450)
audioTypeDropdown = customtkinter.CTkComboBox(master=app, values=summarizeTypes, command=setSummaryType)


outputbox.configure(state = tkinter.DISABLED)
outputbox.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)
deviceDropdown.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)
audioTypeDropdown.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

global isRecording
isRecording = False
global recordPath
recordPath = 'recording.mp3'
global audio
audio = []
global recordthread
global recordingDone
recordingDone = False

def whileRecording():
    global recordingDone
    global isRecording
    global recorder
    global audio
    
    if recorder is None:
        recorder = PvRecorder(device_index=-1, frame_length=512)
    
    recordingDone = False
    print('beginning recording')
    recorder.start()
    while isRecording:
        frame = recorder.read()
        audio.extend(frame)

    recorder.stop()
    with wave.open(recordPath, 'w') as f:
        f.setparams((1, 2, 16000, 512, "NONE", "NONE"))
        f.writeframes(struct.pack("h" * len(audio), *audio))

    recorder.delete()
    recorder = PvRecorder(device_index=deviceIndex, frame_length=512)

    recordingDone = True
    print('completed recording')

def record():
    global sumfunc
    global recordingDone
    global recordthread
    global isRecording
    global deviceIndex
    global audio

    isRecording = not isRecording
    everythingbuttonText.set( 'Stop' if isRecording else 'Record')
    if isRecording:
        audio = []
        recordthread = threading.Thread(target=whileRecording)
        
        recordthread.start()

        print('starting')
    else:
        while not recordingDone:
            print('waiting')
            time.sleep(0.1)
        # Allow Editing:
        outputbox.configure(state = tkinter.NORMAL)

        # Edit:
        outputbox.delete('0.0', 'end')
        summary = sumfunc(transcribe(recordPath))
        print(summary)
        outputbox.insert('0.0', summary)

        # Complete Editing:
        outputbox.configure(state = tkinter.DISABLED)

        if os.path.exists(recordPath):
            os.remove(recordPath)

everythingButton = customtkinter.CTkButton(master=app, textvariable=everythingbuttonText, command=record)
everythingButton.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

app.mainloop()
isRecording = False
recorder.delete()
