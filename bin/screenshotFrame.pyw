import sys
import tkinter as tk
from tkinter import ttk, Button, filedialog, messagebox
import threading
import subprocess
import json
import modifyCapture as modify
import imageDiff as diff
import speak
import bouyomichan
import shutil
import os
import time

settings_path = "settings.json"
error_x = 8
error_y = 30
tool_window_height = 30
init_x = 20
init_y = 20
init_width = 500
init_height = 400
volume = 100
be_caputuring = False


def resize(event):
    capture_frame.config(height=root.winfo_height()
                         - tool_window_height - 15, width=root.winfo_width())
    tool_frame.config(width=root.winfo_width())


def speakTextInImage():
    if not be_caputuring:
        print(os.getcwd())
        typ = [('画像ファイル', '*.png')]
        image_file = filedialog.askopenfilenames(
            filetypes=typ, initialdir=os.getcwd())
        print(image_file)
        for img in image_file:
            print(img)
            shutil.copy(img, "screen.png")
            capture_thread = defineCaptureThread(modify.not_remove_key)
            capture_thread.start()
            root.after(1000, checkCapture)


def capture(x, y, width, height, option=""):
    print("start speech")
    subprocess.run(getCommand(x, y, width, height
                              ), shell=True)
    if diff.isImageDifferent():
        diff.copyCurrentImageAsPrevOne()
        print("different")
        modify.modifyCapture(option=option)
        speak.setTalkable(True)
        speak.speak(speak.loadDraft(), speak.akari)
        print("end speech")
    root.after(1000, checkCapture)


def checkCapture():
    global capture_thread
    entityChangesApply()
    if be_caputuring and not capture_thread.is_alive():
        print("reraise", be_caputuring, capture_thread.is_alive())
        capture_thread = defineCaptureThread()
        capture_thread.start()
        root.after(1000, checkCapture)
    elif be_caputuring and capture_thread.is_alive():
        root.after(1000, checkCapture)


def startCapture():
    global be_caputuring, capture_thread
    try:
        if capture_thread.isAlive():
            print("Alive")
            return
    except:
        print("First Time?")
    be_caputuring = True
    cap_btn.configure(text="Stop", command=stopCapture)
    root.title(u"Screenshot Speak (Speaking)")
    entityChangesApply()
    capture_thread = defineCaptureThread()
    capture_thread.start()


def defineCaptureThread(option=""):
    thread = threading.Thread(target=lambda: capture(root.winfo_x(), root.winfo_y(),
                                                     root.winfo_width(), root.winfo_height(), option))
    thread.daemon = True
    return thread


def stopCapture():
    global be_caputuring
    be_caputuring = False
    speak.setTalkable(False)
    cap_btn.configure(text="Capture", command=startCapture)
    root.title(u"Screenshot Speak")


def getCommand(x, y, width, height):
    return "python captureScreen.py %d %d %d %d" % ((x+error_x), (y+error_y), (x+width+error_x), (y+height))


def initializeCaptureFrame():
    global capture_frame
    tk.ttk.Style().configure("TP.TFrame", bd=4,
                             background="yellow", highlightbackground="blue", highlightthickness=0)
    capture_frame = ttk.Frame(master=root, style="TP.TFrame",
                              width=init_width, height=init_height-tool_window_height, relief="solid")
    capture_frame.pack(side="top")


def initializeToolFrame():
    global tool_frame, cap_btn, volume_txt
    tool_frame = ttk.Frame(master=root, width=init_width,
                           height=tool_window_height)
    tool_frame.pack(side="bottom", fill="both")
    sizegrip = ttk.Sizegrip(master=tool_frame)
    sizegrip.pack(anchor="se", side="right")
    image_btn = Button(tool_frame, text="Image", command=speakTextInImage)
    image_btn.pack(side="left")
    cap_btn = Button(tool_frame, text="Capture", command=startCapture)
    cap_btn.pack(side="left")
    input_frame = ttk.Frame(master=tool_frame)
    input_frame.pack(side="left")

    volume_lbl = ttk.Label(master=input_frame, text='Volume')
    volume_lbl.pack(side="left")
    volume_txt = ttk.Entry(master=input_frame, width=5)
    volume_txt.insert(0, str(volume))
    volume_txt.pack(side="left")


def initializeRoot():
    global root
    root = tk.Tk()
    root.title(u"Screenshot Speak")
    root.wm_attributes("-transparentcolor", "yellow")
    root.geometry('%dx%d+%d+%d' % (init_width, init_height, init_x, init_y))
    root.attributes("-topmost", True)
    root.bind("<Configure>", resize)
    root.resizable(True, True)
    root.protocol("WM_DELETE_WINDOW", onClosing)


def readSettings():
    global init_width, init_height, init_x, init_y, volume, bouyomi_exe
    print("open")
    settings = open(settings_path)
    settings_dict = json.load(settings)
    init_x = int(settings_dict["x"])
    init_y = int(settings_dict["y"])
    init_width = int(settings_dict["width"])
    init_height = int(settings_dict["height"])
    volume = int(settings_dict["volume"])
    bouyomi_exe = settings_dict["bouyomi_exe"]


def onClosing():
    print("close")
    entityChangesApply()
    save_dict = {"x": root.winfo_x(), "y": root.winfo_y(), "width": root.winfo_width(),
                 "height": root.winfo_height(), "volume": volume, "bouyomi_exe": bouyomi_exe}
    settings = open(settings_path, 'w')
    json.dump(save_dict, settings, sort_keys=True, indent=4)
    root.destroy()


def entityChangesApply():
    global volume
    try:
        volume = max([min([int(volume_txt.get()), 100]), 1])
    except:
        volume_txt.delete(0, len(volume_txt.get()))
        volume_txt.insert(0, str(volume))


if __name__ == '__main__':
    readSettings()
    initializeRoot()
    initializeToolFrame()
    initializeCaptureFrame()
    if not bouyomichan.checkBouyomiChanIsAlive():
        bouyomichan.launchBouyomiChan(bouyomi_exe)
        res = messagebox.showinfo(
            "Confirmation", "棒読みちゃんを起動しました\n準備が完了したらOKを押してください")
    root.mainloop()
