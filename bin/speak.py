
import subprocess
import time


speech_file_path = "modified_res.txt"
seikasay_path = ".\SeikaSay -cid %s -volume %f -speed %f -t \"%s\""

max_speed = 2
draft_length = 30

speaker = {"akari": "2000"}
talkable = True


def loadSpeakerSettings():
    print("not implementing")


def loadDraft():
    with open(speech_file_path, encoding="utf-8") as speech_file:
        return speech_file.read()


def setTalkable(flag=True):
    global talkable
    talkable = flag


def speak(draft, speaker, speed=1, volume=1):
    try:
        if(len(draft) > 0):
            for talk in draft.split("。"):
                if not talkable:
                    break
                if len(talk) > 0:
                    print(seikasay_path % (speaker,
                                           volume, min([max_speed, max([len(talk)/draft_length, speed])]), talk))
                    subprocess.run(seikasay_path % (speaker,
                                                    volume, min([max_speed, max([len(talk)/draft_length, speed])]), talk), shell=True)
        else:
            print("No Speak")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    loadSpeakerSettings()
    speak("マイクテスト、マイクテスト　マイクテスト。マイクテスト！マイクテスト？", speaker["akari"])
