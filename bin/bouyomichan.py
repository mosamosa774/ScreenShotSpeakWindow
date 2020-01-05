import os
import subprocess


def checkBouyomiChanIsAlive():
    proc = subprocess.Popen("tasklist", shell=True, stdout=subprocess.PIPE)

    for line in proc.stdout:
        if "BouyomiChan.exe" in str(line):
            print("found")
            return True
    return False


def launchBouyomiChan(bouyomi_chan_exe_file):
    subprocess.Popen(bouyomi_chan_exe_file)


if __name__ == "__main__":
    import json
    if not checkBouyomiChanIsAlive():
        settings_path = "settings.json"
        settings = open(settings_path)
        settings_dict = json.load(settings)
        launchBouyomiChan(settings_dict["bouyomi_exe"])
