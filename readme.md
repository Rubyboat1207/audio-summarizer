# Build Instructions

I used "auto py to exe" to build but it can be done just as easily using command line

Here is the command line version:
```
pyinstaller main.spec
```
or if that doesn't work use:
```
pyinstaller --noconfirm --onedir --windowed --add-data "./venv/Lib/site-packages/customtkinter;customtkinter/" --add-data "./venv/Lib/site-packages/pvrecorder;pvrecorder/"  "./main.py"
```

to do in the gui, you'll need to add customtkinter and pvrecorder directories as additional folders