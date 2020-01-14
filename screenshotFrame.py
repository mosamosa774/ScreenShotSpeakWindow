import os
import sys
import tkinter as tk
from tkinter import ttk, Button, filedialog, messagebox
import threading
import subprocess
import json
import time
import shutil
import bin.modifyCapture as modify
import bin.imageDiff as diff
import bin.speak as speak
import bin.frameTrayIcon as tray
import bin.voiceroid as voiceroid


settings_path = "settings.json"
error_x = 9
error_y = 32
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


def hideFrame():
    root.withdraw()
    threading.Thread(target=lambda: tray.generateTrayIcon(
        lambda: releaseHide())).start()
    print("start hiding")


def releaseHide():
    print("end hiding")
    root.update()
    root.deiconify()


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


def capture(x, y, width, height, option=""):
    global capture_thread
    entityChangesApply()
    print("start speech")
    root.title(u"Speak Screenshot (Capturing)")
    subprocess.run(getCommand(x, y, width, height
                              ), shell=True)
    if diff.isImageDifferent():
        diff.copyCurrentImageAsPrevOne()
        print("different")
        modify.modifyCapture(option=option)
        speak.setTalkable(True)
        root.title(u"Speak Screenshot (Speaking)")
        speak.speak(speak.loadDraft(),
                    speak.speaker["akari"], volume=float(volume)/100)
        print("end speech")

    if be_caputuring:
        print("reraise", be_caputuring, capture_thread.is_alive())
        capture_thread = defineCaptureThread()
        capture_thread.start()


# def checkCapture():
#    if be_caputuring and not capture_thread.is_alive():
#        print("reraise", be_caputuring, capture_thread.is_alive())
#        capture_thread = defineCaptureThread()
#        capture_thread.start()
#        root.after(1000, checkCapture)
#    elif be_caputuring and capture_thread.is_alive():
#        root.after(1000, checkCapture)


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
    entityChangesApply()
    capture_thread = defineCaptureThread()
    capture_thread.start()


def defineCaptureThread(option=""):
    thread = threading.Thread(target=lambda: capture(root.winfo_x(), root.winfo_y(),
                                                     capture_frame.winfo_width(), capture_frame.winfo_height(), option))
    thread.daemon = True
    return thread


def stopCapture():
    global be_caputuring
    be_caputuring = False
    speak.setTalkable(False)
    cap_btn.configure(text="Capture", command=startCapture)
    root.title(u"Speak Screenshot")


def getCommand(x, y, width, height):
    return "python captureScreen.py %d %d %d %d" % ((x+error_x), (y+error_y), (x+width+6), (y+height+30))


def initializeCaptureFrame():
    global capture_frame
    tk.ttk.Style().configure("TP.TFrame", bd=4,
                             background="yellow", highlightbackground="blue", highlightthickness=0)
    capture_frame = ttk.Frame(master=root, style="TP.TFrame",
                              width=init_width, height=init_height-tool_window_height, relief="solid")
    capture_frame.pack(side="top")


def initializeToolFrame():
    global tool_frame, cap_btn, volume_txt, hide_btn
    tool_frame = ttk.Frame(master=root, width=init_width,
                           height=tool_window_height)
    tool_frame.pack(side="bottom", fill="both")
    sizegrip = ttk.Sizegrip(master=tool_frame)
    sizegrip.pack(anchor="se", side="right")
    cap_btn = Button(tool_frame, text="Capture", command=startCapture)
    cap_btn.pack(side="left")
    image_btn = Button(tool_frame, text="Image", command=speakTextInImage)
    image_btn.pack(side="left")
    hide_btn = Button(tool_frame, text="Hide", command=hideFrame)
    hide_btn.pack(side="left")
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
    root.title(u"Speak Screenshot")
    root.iconbitmap("../src/icon.ico")
    root.wm_attributes("-transparentcolor", "yellow")
    print('%dx%d+%d+%d' % (init_width, init_height, init_x, init_y))
    root.geometry('%dx%d+%d+%d' % (init_width, init_height, init_x, init_y))
    root.attributes("-topmost", True)
    root.bind("<Configure>", resize)
    root.resizable(True, True)
    root.protocol("WM_DELETE_WINDOW", onClosing)


def readSettings():
    global init_width, init_height, init_x, init_y, volume, voiceroid_exe, seika_center_exe
    print("open")
    settings = open(settings_path)
    settings_dict = json.load(settings)
    init_x = int(settings_dict["x"])
    init_y = int(settings_dict["y"])
    init_width = int(settings_dict["width"])
    init_height = int(settings_dict["height"])
    volume = int(settings_dict["volume"])
    voiceroid_exe = settings_dict["voiceroid_exe"]
    seika_center_exe = settings_dict["seika_center_exe"]
    print((init_width, init_height, init_x, init_y))


def onClosing():
    print("close")
    entityChangesApply()
    settings = open(settings_path)
    settings_dict = json.load(settings)
    settings.close()
    settings_dict["x"] = root.winfo_x()
    settings_dict["y"] = root.winfo_y()
    settings_dict["width"] = root.winfo_width()
    settings_dict["height"] = root.winfo_height()
    settings_dict["volume"] = volume
    settings = open(settings_path, 'w')
    json.dump(settings_dict, settings, sort_keys=True, indent=4)
    root.destroy()


def entityChangesApply():
    global volume
    try:
        volume = max([min([int(volume_txt.get()), 100]), 1])
    except:
        volume_txt.delete(0, len(volume_txt.get()))
        volume_txt.insert(0, str(volume))


if __name__ == '__main__':
    if not os.path.exists("bin"):
        tk.Tk().withdraw()
        res = messagebox.showinfo(
            "Confirmation", "適正なパスで実行されていません")
        sys.exit()
    os.chdir("bin")

    readSettings()
    initializeRoot()
    initializeToolFrame()
    initializeCaptureFrame()
    res = voiceroid.check(voiceroid_exe, seika_center_exe)
    if len(res) > 0:
        res = messagebox.showinfo(
            "Confirmation", res)
    root.mainloop()
