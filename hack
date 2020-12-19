import argparse
import textfuncs


alph = "abcdefghijklmnopqrstuvwxyz"


def read_model(model_file):
    model = open(model_file, 'r')
    freqs = model.read().split('\n')
    for i in range(len(freqs) - 1):
        freqs[i] = float(freqs[i])
    freqs.pop()

    return freqs


def get_freqs_from_text(text):
    freqs = []
    for letter in alph:
        freqs.append(text.count(letter)/len(text))

    return freqs


def build_dict_shifts(model_freq, text_freq):
    dict_similarity = {}
    for i in range(len(model_freq)):
        diff = 0
        for j in range(len(model_freq)):
            diff += abs(model_freq[j] - text_freq[(j + i) % len(text_freq)])
        dict_similarity[diff] = i 

    return dict_similarity


def decode_caesar(text, key, length = -1):
    if length == -1:
        length = len(text)
    key = int(key)
    chiper = ""
    for i in range(length):
        chiper += alph[(alph.index(text[i]) - key) % len(alph)]

    return chiper


def hack(text, dict_shifts):
    decoded_text = decode_caesar(text, dict_shifts[min(dict_shifts)], 20)

    print(decoded_text[:20])
    print('NICE? [y/n]')
    ans = input()

    if ans == 'y':
        return decode_caesar(text, dict_shifts[min(dict_shifts)])
    elif ans == 'n':
        for i in range(len(dict_shifts) - 1):
            dict_shifts.pop(min(dict_shifts))
            decoded_text = decode_caesar(text,
                                         dict_shifts[min(dict_shifts)], 
                                         20)

            print(decoded_text[:20])
            print('NICE? [y/n]')
            ans = input()

            if ans == 'y':
                return decode_caesar(text, dict_shifts[min(dict_shifts)])
            elif ans == 'n': continue

    print('((((')





parser = argparse.ArgumentParser()

parser.add_argument("--input-file")
parser.add_argument("--output-file")
parser.add_argument("--model-file")
args = parser.parse_args()

text = textfuncs.input_text(args.input_file)
text = textfuncs.tolower_onlyletters(text)  

model_freq = read_model(args.model_file)
text_freq = get_freqs_from_text(text)

dict_shifts = build_dict_shifts(model_freq, text_freq)
hacked_text = hack(text, dict_shifts)

textfuncs.print_text(hacked_text, args.output_file)
