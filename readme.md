# Prerequisites
The program will ask for a token each time it's reopened, to get a token you can get it from https://platform.openai.com/account/api-keys. You should store it somewhere easy to copy, as it does not save right now.

# How to download

Go to the [(win) builds page](https://github.com/Rubyboat1207/audio-summarizer/actions/workflows/pyinstaller.yml) or [(linux) builds page](https://github.com/Rubyboat1207/audio-summarizer/actions/workflows/pyinstaller-linux.yml) and click on the latest ran workflow. Then scroll down to artifacts to grab the latest windows build.

# Run from source

install requirements:
```
pip install -r requirements.txt
```

then to use normally, just type the following into the console:
```
py main.py
```

# Build from source

I used "auto py to exe" to build but it can be done just as easily using command line

Here is the command line version:
```
pyinstaller main.spec
```
or if that doesn't work use:
```
pyinstaller --noconfirm --onedir --windowed --add-data "<python dir>/Lib/site-packages/customtkinter;customtkinter/" --add-data "<python dir>/Lib/site-packages/pvrecorder;pvrecorder/"  "./main.py"
```

to do in the gui, you'll need to add customtkinter and pvrecorder directories as additional folders