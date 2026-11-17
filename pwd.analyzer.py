#!/usr/bin/env python3
"""
FOR USER INPUT, DO:
1. Run the script with `-w` to generate a wordlist.
2. Provide your name, date of birth, and any other personal information.
3. The script will create a wordlist based on your inputs and save it to a file.
4. Run the script with `-a <password>` to analyze a password's strength.

Example INPUT FLOW for wordlist generation:
$ python pwd.analyzer.py -w
Name: Superman
DoB (YYYYMMDD or YYYY): 2001
Anything else that is personal to you: Krypton
Wordlist saved to: custom_wordlist.txt
Total entries: 27

Example INPUT FLOW for password analysis:
$ python pwd.analyzer.py -a 'Superman2001!'
# Password Analyzer and Wordlist Generator
Length: 15
zxcvbn Score: 3/4
Estimated crack time (slow offline attack): 1 day 2 hours 3 minutes
"""

from zxcvbn import zxcvbn
import argparse
import itertools # for generating combinations

class Analyzer:
    def analyze(self, p):
        result = zxcvbn(p)
        return {
            'length': len(p),
            'score': result['score'],
            'crack_times': result['crack_times_display']
        }

class Wordlist:
    def __init__(self):
        self.sub = {
            'a': ['@', '4'], 'e': ['3'], 'i': ['1', '!'], 'o': ['0'],
            's': ['5', '$'], 't': ['7'], 'l': ['1'], 'g': ['9']
        } # Character substitutions

        self.years = r'(19|20)\d{2}' # Regex for years 1900-2099
        self.suffixes = ['', '!', '123'] + self.years
        self.prefixes = ['', 'my', 'the']

    def replacer(self, word):

        x = set([word])
        for i, c in enumerate(word.lower()):
            if c in self.sub:

                for sub in self.sub[c]:
                    x.update(w[:i] + sub + w[i+1:] for w in list(x)) # Replace character at position i with sub
        return x

    def generate(self, words):

        result = set() # To store combinations

        for word in words:
            y = self.replacer(word)

            for v in y:
                for p, s in itertools.product(self.prefixes, self.suffixes):
                    result.add(f"{p}{v}{s}") # Add prefix and suffix to each variation

        return sorted(result)

def main():
    parser = argparse.ArgumentParser(description='Password Analyzer and Wordlist Generator')
    parser.add_argument('-a', '--analyze', help='Check password strength')
    parser.add_argument('-w', '--wordlist', action='store_true', help='Generate and export wordlist')
    args = parser.parse_args()

    if args.analyze:
        data = Analyzer().analyze(args.analyze)

        print(f"Length: {data['length']}")
        print(f"zxcvbn Score: {data['score']}/4")
        print("Estimated crack time (slow offline attack):",
        data['crack_times']['offline_slow_hashing_1e4_per_second'])



    elif args.wordlist:
        name = input("Name: ").strip()
        date = input("DoB (YYYYMMDD or YYYY): ").strip()
        misc  = input("Anything else that is personal to you: ").strip()
        inputs = [name, date, misc]

        wordlist = Wordlist().generate(inputs)

        filename = 'custom_wordlist.txt'
        with open(filename, 'w', encoding='utf-8') as f:
            f.writelines(w + '\n' for w in wordlist)

        print(f"\nWordlist saved to: {filename}")
        print(f"Total entries: {len(wordlist)}")

    else:
        parser.print_help()

if __name__ == '__main__':
    main()
