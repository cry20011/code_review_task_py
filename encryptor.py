#!/usr/bin/env python3

from string import ascii_lowercase
from argparse import ArgumentParser
from collections import Counter
from yaml import dump, safe_load
import textfuncs



class caesar:

    def encode(text, key):
        encoded_text = []
        for c in text:
            encoded_text.append(ascii_lowercase[
                (ascii_lowercase.index(c) + key)
                % len(ascii_lowercase)])

            # encoded_text.append((char + key) % len(alph))

        return ''.join(encoded_text)


    def decode(encoded_text, key, length = -1):
        if length == -1:
            length = len(encoded_text)
        decoded_text = []
        for i in range(length):
            decoded_text.append(ascii_lowercase[
                (ascii_lowercase.index(encoded_text[i]) - key)
                % len(ascii_lowercase)])

            # decoded_text.append((char - key) % len(alph))

        return ''.join(decoded_text)




class vigenere:

    def encode(text, key):
        encoded_text = []
        for i in range(len(text)):
            key_pos = i % len(key)
            encoded_text.append(ascii_lowercase[
                (ascii_lowercase.index(text[i])
                 + ascii_lowercase.index(key[key_pos]))
                % len(ascii_lowercase)])

            # encoded_text.append((text[i] + key[i % len(key)]) % len(alph))

        return ''.join(encoded_text)

    def decode(encoded_text, key):
        decoded_text = []
        for i in range(len(encoded_text)):
            key_pos = i % len(key)
            decoded_text.append(ascii_lowercase[
                (ascii_lowercase.index(encoded_text[i])
                 - ascii_lowercase.index(key[key_pos]))
                % len(ascii_lowercase)])

            # decoded_text.append((text[i] - key[i % len(key)]) % len(alph))

        return ''.join(decoded_text)




class hack_caesar:


    def get_freqs(text):
        counted = Counter(text)
        freqs = []

        for c in ascii_lowercase:
            freqs.append(counted[c] / len(text))

            '''
            считаем количество вхождений каждого символа в текст
            и делим на общее количество символов,
            то есть находим частоты каждого символа,
            а потом записыаем частоты каждого символа
            в список по порядку (то есть по алфавиту)
            '''

        return freqs


    def build_shifts(model_freqs, text_freqs):
        alph_len = len(ascii_lowercase)
        shifts = []
        for i in range(alph_len):
            diff = 0
            for j in range(alph_len):
                diff += abs(model_freqs[j] - text_freqs[(j + i)
                            % alph_len])
            shifts.append((diff, i))

            # для каждого смещения вычисляется суммарное отклонение от частоты модели


        return sorted(shifts)


    def hack(text, shifts, trial_len = 20):
        
        decoded_text = caesar.decode(text, shifts[0][1], trial_len)
        # shifts - пары (частота, смещение), отсортированные по частоте
        # пытаемся расшифровать несколько первых символов текста, 
        # и показываем пользователю, что получилось

        print(decoded_text)
        print('NICE? [y/n]')
        ans = input()

        if ans == 'y':
            return caesar.decode(text, shifts[0][1])
            # если получилось что-то адекватное,
            # то расшифровываем весь текст с правильным ключом

        elif ans == 'n':
            for i in range(1, len(shifts)):
                decoded_text = caesar.decode(text,
                                             shifts[i][1], 
                                             trial_len)

                print(decoded_text)
                print('NICE? [y/n]')
                ans = input()

                if ans == 'y':
                    return caesar.decode(text, shifts[i][1])
                elif ans == 'n': continue

        raise Exception









parser = ArgumentParser()


parser.add_argument("task")

parser.add_argument("--chiper")
parser.add_argument("--key")

parser.add_argument("--input-file")
parser.add_argument("--output-file")

parser.add_argument("--text-file")
parser.add_argument("--model-file")


args = parser.parse_args()


if args.task == 'encode':

    text = textfuncs.input_text(args.input_file)
    text = textfuncs.tolower_onlyletters(text)

    if args.chiper == 'caesar':
        encoded_text = caesar.encode(text, int(args.key))
    elif args.chiper == 'vigenere':
        encoded_text = vigenere.encode(text, args.key)

    textfuncs.print_text(encoded_text, args.output_file)

elif args.task == 'decode':

    encoded_text = textfuncs.input_text(args.input_file)
    encoded_text = textfuncs.tolower_onlyletters(encoded_text)

    if args.chiper == 'caesar':
        decoded_text = caesar.decode(encoded_text, int(args.key))
    elif args.chiper == 'vigenere':
        decoded_text = vigenere.decode(encoded_text, args.key)

    textfuncs.print_text(decoded_text, args.output_file)

elif args.task == 'train':

    text = textfuncs.input_text(args.text_file)
    text = textfuncs.tolower_onlyletters(text)

    freqs = hack_caesar.get_freqs(text);

    with open(args.model_file, 'w') as model:
        dump(freqs, model, default_flow_style=False)

elif args.task == 'hack':

    encoded_text = textfuncs.input_text(args.input_file)
    encoded_text = textfuncs.tolower_onlyletters(encoded_text)

    with open(args.model_file, 'r') as model:
        model_freqs = safe_load(model)
    text_freqs = hack_caesar.get_freqs(encoded_text)

    shifts = hack_caesar.build_shifts(model_freqs, text_freqs)
    decoded_text = hack_caesar.hack(encoded_text, shifts)

    textfuncs.print_text(decoded_text, args.output_file)























