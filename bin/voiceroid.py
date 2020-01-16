import os
import subprocess
import re


def getPS():
    stdout = re.split(",", str(subprocess.check_output(['tasklist'])))
    return stdout


def checkVoiceroidIsAlive():
    stdout = subprocess.check_output(
        ["tasklist", "/FI", "WINDOWTITLE eq VOICEROID2"])
    stdout_aster = subprocess.check_output(
        ["tasklist", "/FI", "WINDOWTITLE eq VOICEROID2*"])
    lines = str(stdout).split("\n")
    lines.extend(str(stdout_aster).split("\n"))
    for line in lines:
        if "VoiceroidEditor.exe" in str(line):
            print("found")
            return True
    return False


def checkSeikaCenterIsAlive(stdout):
    for line in stdout:
        if "SeikaCenter.exe" in str(line):
            print("found")
            return True
    return False


def launchProcess(exe_file):
    subprocess.Popen(exe_file)


def check(voiceroid_exe, seika_center_exe):
    init_msg = "%s起動が完了したらOKを押してください"
    msg = ""
    stdout = getPS()
    if not checkVoiceroidIsAlive():
        launchProcess(voiceroid_exe)
        msg += "Voiceroidを起動しました\nアプリケーション使用前にSeikaCenterの起動ボタンを押してください\n"
    if not checkSeikaCenterIsAlive(stdout):
        launchProcess(seika_center_exe)
        msg += "SeikaCenterを起動しました\n" if len(
            msg) > 0 else "SeikaCenterを起動しました\nアプリケーション使用前に起動ボタンを押してください\n"
    return init_msg % msg if len(msg) > 0 else ""


if __name__ == "__main__":
    import json
    settings_path = "settings.json"
    settings = open(settings_path)
    settings_dict = json.load(settings)
    print(check(settings_dict["voiceroid_exe"],
                settings_dict["seika_center_exe"]))
