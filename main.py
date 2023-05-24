"""Main Module for speech to summary"""

import os
import struct
import threading
import time
import tkinter
import wave

import customtkinter
from pvrecorder import PvRecorder

from summarize import SummarizeController
from voice import TranscriptionController

# global SUMMARY_MANAGER
# global TRANSCRIPT_MANAGER

SUMMARY_MANAGER = SummarizeController('')
TRANSCRIPT_MANAGER = TranscriptionController('')

customtkinter.set_appearance_mode('System')
customtkinter.set_default_color_theme('blue')

devices = PvRecorder.get_audio_devices()
# global DEVICE_INDEX
DEVICE_INDEX = 0
# global RECORDER
RECORDER = PvRecorder(device_index=0, frame_length=512)
# global SUMMARY_FUNCTION
SUMMARY_FUNCTION = SUMMARY_MANAGER.summarizeLecture


for index, device in enumerate(devices):
    print(f"[{index}] {device}")

def select_device(choice):
    """used by the dropdown to select a recording device"""
    global RECORDER
    global DEVICE_INDEX
    DEVICE_INDEX = devices.index(choice)
    RECORDER = PvRecorder(device_index=DEVICE_INDEX, frame_length=512)


summarizeTypes = [
    'Lecture',
    'Conversation',
    'Story',
    'Instructions'
]


def set_summary_type(choice):
    """used by the dropdown to select a summary type"""
    global SUMMARY_FUNCTION

    if choice == 'Lecture':
        SUMMARY_FUNCTION = SUMMARY_MANAGER.summarizeLecture
    elif choice == 'Conversation':
        SUMMARY_FUNCTION = SUMMARY_MANAGER.summarizeConversation
    elif choice == 'Story':
        SUMMARY_FUNCTION = SUMMARY_MANAGER.summarizeStory
    elif choice == 'Instructions':
        SUMMARY_FUNCTION = SUMMARY_MANAGER.summarizeInstructions
    else:
        SUMMARY_FUNCTION = SUMMARY_MANAGER.summarizeLecture


app = customtkinter.CTk()
app.geometry("800x500")
app.title('Summarize This')

everythingbuttonText = customtkinter.StringVar(app, "Record")

outputbox = customtkinter.CTkTextbox(master=app, width=400)
deviceDropdown = customtkinter.CTkComboBox(
    master=app, values=devices, command=select_device, width=450)
audioTypeDropdown = customtkinter.CTkComboBox(
    master=app, values=summarizeTypes, command=set_summary_type)
keybox = customtkinter.CTkTextbox(
    master=app, border_color='#444444', border_width=4, height=30, width=450)


def set_token_from_textbox():
    """used to update summary & transcript api tokens"""
    tex = keybox.get('1.0', tkinter.END).rstrip()

    SUMMARY_MANAGER.key = tex
    TRANSCRIPT_MANAGER.key = tex


keySet = customtkinter.CTkButton(
    master=app, command=set_token_from_textbox, text="set token")


setTokenFrom = set_token_from_textbox

outputbox.configure(state=tkinter.DISABLED)
outputbox.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)
deviceDropdown.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)
audioTypeDropdown.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)
keybox.place(relx=0.4, rely=0.1, anchor=tkinter.CENTER)
keySet.place(relx=0.8, rely=0.1, anchor=tkinter.CENTER)

# global IS_RECORDING
IS_RECORDING = False
# global RECORD_PATH
RECORD_PATH = 'recording.mp3'
outputpath = './out/'
# global AUDIO_CACHE
AUDIO_CACHE = []
# global RECORDING_COMPLETE
RECORDING_COMPLETE = False


def while_recording():
    """ran async in other thread to record to file"""
    global RECORDING_COMPLETE
    global RECORDER

    if RECORDER is None:
        RECORDER = PvRecorder(device_index=-1, frame_length=512)

    RECORDING_COMPLETE = False
    print('beginning recording')
    RECORDER.start()
    while IS_RECORDING:
        frame = RECORDER.read()
        AUDIO_CACHE.extend(frame)

    RECORDER.stop()
    with wave.open(RECORD_PATH, 'w') as wave_write:
        wave_write.setparams((1, 2, 16000, 512, "NONE", "NONE"))
        wave_write.writeframes(struct.pack("h" * len(AUDIO_CACHE), *AUDIO_CACHE))

    RECORDER.delete()
    RECORDER = PvRecorder(device_index=DEVICE_INDEX, frame_length=512)

    RECORDING_COMPLETE = True
    print('completed recording')


def record():
    """ran on button click"""
    global IS_RECORDING
    global AUDIO_CACHE

    IS_RECORDING = not IS_RECORDING
    everythingbuttonText.set('Stop' if IS_RECORDING else 'Record')
    if IS_RECORDING:
        AUDIO_CACHE = []
        recordthread = threading.Thread(target=while_recording)

        recordthread.start()

        print('starting')
    else:
        while not RECORDING_COMPLETE:
            print('waiting')
            time.sleep(0.1)
        # Allow Editing:
        outputbox.configure(state=tkinter.NORMAL)

        # Edit:
        outputbox.delete('0.0', 'end')
        transcript = TRANSCRIPT_MANAGER.transcribe(RECORD_PATH)
        summary = SUMMARY_FUNCTION(transcript)
        print(summary)
        outputbox.insert('0.0', summary)

        # Complete Editing:
        outputbox.configure(state=tkinter.DISABLED)

        if not os.path.exists(outputpath):
            os.mkdir(outputpath)

        files = os.listdir(outputpath)

        with open(outputpath + str(len(files)) + '.txt', 'w', encoding='UTF-8') as thing:
            thing.write(f'Summary:\n{summary}\nRaw Transcript:\n{transcript}')


everythingButton = customtkinter.CTkButton(
    master=app, textvariable=everythingbuttonText, command=record)
everythingButton.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

app.mainloop()
IS_RECORDING = False
RECORDER.delete()
if os.path.exists(RECORD_PATH):
    os.remove(RECORD_PATH)
