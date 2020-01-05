import re
import os
import unicodedata
import json
import sys
import difflib

spoken_dict_file_path = "spoken_dist.txt"
input_file_path = "res.txt"
output_file_path = "modified_res.txt"
end_character = "。"
queue_length = 200
remove_spoken_text = True


def isBrokenSentence(sentence):
    #    return isOnlySpaceSentence(sentence) or existContinualSpace(sentence) or isOnlyEnglishSentence(sentence)
    return isOnlySpaceSentence(sentence) or isOnlyEnglishSentence(sentence)

# def existContinualSpace(sentence):
#    if "  " in sentence:
#        return True
#    return False


def isOnlySpaceSentence(sentence):
    result = True
    for one_character in list(sentence):
        if not one_character == " ":
            result = False
            break
    return result


def isOnlyEnglishSentence(sentence):
    for ch in sentence:
        name = unicodedata.name(ch)
        if "CJK UNIFIED" in name \
                or "HIRAGANA" in name \
                or "KATAKANA" in name:
            return False
    return True


def removeSpokenLine(draft_each_lines):
    try:
        spoken_queue = []
        if os.path.exists(spoken_dict_file_path):
            with open(spoken_dict_file_path, 'r', encoding="utf-8") as spoken_dict_file:
                for spoken_line in spoken_dict_file.readlines():
                    spoken_queue.append(spoken_line.replace("\n", ""))

            for key in spoken_queue:
                for draft_line in draft_each_lines:
                    if difflib.SequenceMatcher(None, draft_line, key).ratio() >= 0.6:
                        draft_each_lines.remove(draft_line)

        for draft_line in draft_each_lines:
            if len(spoken_queue) >= queue_length:
                spoken_queue.pop(0)
            spoken_queue.append(draft_line)
        with open(spoken_dict_file_path, 'w', encoding="utf-8") as spoken_dict_file:
            spoken_dict_file.write('\n'.join(spoken_queue))
    except Exception as e:
        print(e)

    return draft_each_lines


def modify():
    draft_each_lines = []
    with open(input_file_path, encoding="utf-8") as input_file:
        txt = input_file.read()
        txt = txt.replace("  ", "\n")
        for line in txt.split("\n"):
            if len(line) > 2 and not isBrokenSentence(line) and not line in draft_each_lines:
                draft_each_lines.append(line)

    if remove_spoken_text:
        draft_each_lines = removeSpokenLine(draft_each_lines)

    modified_text = ""
    for line in draft_each_lines:
        modified_text += line + end_character

    print(modified_text)

    with open(output_file_path, 'w') as output:
        output.write(modified_text)


if __name__ == "__main__":
    args = sys.argv
    try:
        for arg in args:
            if arg == "not_remove":
                remove_spoken_text = False
    except:
        print("no input")
    modify()
