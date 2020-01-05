
import subprocess
import socket

speech_file_path = "modified_res.txt"
bouyomi_path = ".\BouyomiChan %d %d %d %d \"%s\""

max_speed = 200

akari = "k)"


def loadDraft():
    with open(speech_file_path, encoding="utf-8") as speech_file:
        return speech_file.read()


def speak(draft, speaker, speed=100, tone=-1, volume=-1, voice=0):
    try:
        if(len(draft) > 0):
            print(bouyomi_path % (
                min([max_speed, max([len(draft*2), speed])]), tone, volume, voice, speaker + draft))
            subprocess.run(bouyomi_path %
                           (min([max_speed, max([len(draft*2), speed])]), tone, volume, voice, speaker + draft), shell=True)
        else:
            print("No Speak")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    speak(loadDraft(), akari)
    speak("マイクテスト、マイクテスト　マイクテスト。マイクテスト！マイクテスト？",akari)
