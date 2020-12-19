import re


def tolower_onlyletters(text):
    text = text.lower()
    reg = re.compile('[^a-z]')

    return reg.sub('', text)


def get_text():
    text = ""
    while True:
        try:
            x = input()
            if x:
                text += x
        except:
            break

    return text

def input_text(file):
    if file is None:
        text = get_text()
    else:
        file = open(file, 'r')
        text = file.read()

    return text	

def print_text(text, file):
    if text is None:
        return

    if file is None:
        print(text)
    else:
        file = open(file, 'w')
        file.write(text)
