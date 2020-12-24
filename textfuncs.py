import re
import sys

def tolower_onlyletters(text):
    text = text.lower()
    reg = re.compile('[^a-z]')

    return reg.sub('', text)


def input_text(file):
    if file is None:
        text = sys.stdin.read()
    else:
        with open(file, 'r') as file:
            text = file.read()

    return text	


def print_text(text, file):
    if text is None:
        return

    if file is None:
        print(text)
    else:
        with open(file, 'w') as file:
            file.write(text)
