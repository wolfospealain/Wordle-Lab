"""Wordle Lab
A Wordle solver, dictionary utility, and strategy tester.
"""
__author__ = "wolfospealain"
__date__ = "11/04/2022"
__credits__ = "https://github.com/wolfospealain/Wordle-Lab"
__version__ = "0.1.0"

from collections import Counter
from random import choice
from datetime import datetime
import requests

BEST = "Gek6f2.2a.1 slate"
CHANCES = 6
DEBUG = False
LATIN = "'abcdefghijklmnopqrstuvwxyz"


def debug(message, variable=None):
    """Simple debug printing of messages and variables. Turned on and off with DEBUG."""
    if not DEBUG:
        return False
    print("\nDEBUG:", str(datetime.now()))
    if variable:
        print(message.upper(), ": ", variable, sep="")
    else:
        print(message)


def latin(word):
    """Check word for non-Latin characters."""
    for letter in word:
        if not letter in LATIN:
            return False
    return True


class Dictionary:
    """Dictionary file management."""

    def __init__(self, files="https://www.nytimes.com/games/wordle/main.3d28ac0c.js", save_wordle_filename="",
                 save_played_filename="", yesterday_filename="", save_allowed_filename="", directory="",
                 remove_apostrophe=True, latin_only=True):
        self.words = set()
        if "://" in files:
            self.words = self.wordle(yesterday_filename=yesterday_filename, save_filename=save_wordle_filename,
                                     save_played_filename=save_played_filename,
                                     save_allowed_filename=save_allowed_filename)
        else:
            self.files = files
            self.directory = directory
            self._load(remove_apostrophe, latin_only)

    def _load(self, remove_apostrophe=True, latin_only=True):
        """Load and combine words from files into dictionary. Designed for use with the Scowl files.
        https://launchpad.net/ubuntu/+source/scowl/2020.12.07-2 """
        words = set()
        for filename in self.files:
            file = open(self.directory + filename, "r")
            for word in file:
                word = word.strip()
                if remove_apostrophe:
                    word = word.replace("'s", "")
                if latin_only and not latin(word):
                    continue
                words.add(word)
            file.close()
        self.words = sorted(words)

    def extract(self, length=None):
        """Save extract of dictionary words by word length."""
        words = set()
        for word in self.words:
            word = word.strip()
            if length is None or len(word) == length:
                words.add(word)
        self.words = sorted(words)
        output_file = open("dictionary" + (str(length) + ".lst") if length is not None else "" + ".lst", "w")
        for word in self.words:
            print(word, file=output_file)
        output_file.close()

    def _wordle_source_parse(self, url="https://www.nytimes.com/games/wordle/main.3d28ac0c.js", start_text="var Ma=",
                             end_text=",Oa="):
        """Parse Wordle sourcecode for word lists."""
        code = requests.get(url, allow_redirects=True).text.split(start_text)[1].split(end_text)[0]
        words = []
        for word in code.split(","):
            words.append(word.split("\"")[1])
        return words

    def wordle(self, save_filename="", yesterday_filename="", save_played_filename="wordle_played.txt",
               save_allowed_filename=""):
        """Get, and optionally save, the Wordle solution word list from source code. Words are always sorted to hide
        the play order. To remove previously played words include the yesterday_filename with the last known
        solution. """
        # parse source code allow words
        if save_allowed_filename:
            words = self._wordle_source_parse(start_text="Oa=", end_text=",Ra=")
            with open(save_allowed_filename, "w") as f:
                for word in words:
                    print(word, file=f)
        # parse source code solution words
        words = self._wordle_source_parse(start_text="var Ma=", end_text=",Oa=")  # Wordle solution words
        # maybe list already played words
        if yesterday_filename:
            yesterdays_word = ""
            try:
                with open(yesterday_filename, "r") as f:
                    for line in f:
                        yesterdays_word = line
                already_played = []
                for word in words:
                    already_played.append(word)
                    if word == yesterdays_word:
                        break
                if save_played_filename:
                    with open(save_played_filename, "w") as f:
                        for word in already_played:
                            print(word, file=f)
                words = set(words) - set(already_played)
            except:
                print(yesterday_filename + " file not found (latest solution).")
        sorted_words = sorted(words)  # ensure that the Wordle game sequence is not revealed
        if save_filename:
            with open(save_filename, "w") as f:
                for word in sorted_words:
                    print(word, file=f)
        return sorted_words


class Wordlist:
    """Game play word lists."""

    def __init__(self, words):
        self.original = words.copy()
        self.words = self.original.copy()
        self.word_size = len(max(self.words, key=len))
        self.count = len(words)
        self.equal_choices = []

    def _reset(self):
        """Reset the word list."""
        self.words = self.original.copy()
        self.count = len(self.words)
        self.equal_choices = []

    def get_frequencies(self, position=None):
        """Get the frequencies of letters in the word list. Optionally for individual positions in the words."""
        text = ""
        for word in self.words:
            if position is None:
                text += word
            else:
                text += word[position]
        return Counter(text)

    def sort_words(self, priority="G", score_duplicates=False):
        """Sort word list by either general letter frequency priority ('Y' for Yellow) or frequency in place ('G' for
        Green). The same letter in multiple places can be scored as a duplicate or not. """
        sorted_words = {}
        self.equal_choices = []
        frequencies = [self.get_frequencies()]
        for position in range(self.word_size):
            frequencies.append(self.get_frequencies(position))

        # main sort by greens
        for word in self.words:
            sort_score = 0
            letter_scores = dict(zip(word, [0] * len(word)))
            for position in range(self.word_size):  # score by green probability
                letter = word[position]
                score = frequencies[position + 1][letter] / (1 if priority == "G" else self.count)
                if score_duplicates:
                    letter_scores[letter] += score
                elif letter_scores[letter] < score:
                    letter_scores[letter] = score
            for score in letter_scores.values():
                sort_score += score
            sorted_words[word] = sort_score

        # find top equal choices
        top_score = max(list(sorted_words.values()))
        for word, score in sorted_words.items():
            if score == top_score:
                self.equal_choices.append(word)

        # subsort by yellows for best guess
        for word in self.words:
            sort_score = 0
            for letter in set(word):  # score yellows, never duplicates
                sort_score += frequencies[0][letter] / (1 if priority == "Y" else self.count)
            sorted_words[word] += sort_score

        self.words = sorted(sorted_words, key=sorted_words.get, reverse=True)

        return self.words.copy()

    def filter_words(self, guess, result):
        """Filter the remaining game space based on the result from the last guess."""
        filtered = set()
        for word in self.words:
            unknown_space = []
            for word_place in range(len(word)):
                if result[word_place] != "G":
                    unknown_space.append(word[word_place])
            for guess_place in range(len(result)):
                letter = guess[guess_place]
                if result[guess_place] == "G":  # must include in place
                    if not letter == word[guess_place]:
                        filtered.add(word)
                elif result[guess_place] == "g":  # can't include
                    if letter in unknown_space:
                        filtered.add(word)
                elif result[guess_place] == "Y":  # must include
                    if letter == word[guess_place]:  # but first not in this place
                        filtered.add(word)
                    else:
                        if letter not in unknown_space:
                            filtered.add(word)
        for word in filtered:
            self.words.remove(word)
        self.count = len(self.words)

    def test_human(self, score_duplicates=True):
        """Test for the best start word for human players - priority score for consonants."""
        vowels = "aeiouy"
        best_words = {}
        frequencies = [self.get_frequencies()]
        for position in range(self.word_size):
            frequencies.append(self.get_frequencies(position))
        for word in self.words:
            word_score = 0
            letter_scores = dict(zip(word, [0] * len(word)))
            for position in range(self.word_size):  # score by green probability
                letter = word[position]
                score = frequencies[position + 1][letter] / (1 if letter not in vowels else self.count)
                if score_duplicates:
                    letter_scores[letter] += score
                elif letter_scores[letter] < score:
                    letter_scores[letter] = score
            for score in letter_scores.values():
                word_score += score
            best_words[word] = word_score
        # print(sorted(best_words.values(),reverse=True))
        return sorted(best_words, key=best_words.get, reverse=True)

    def test_binarysort_by_letter(self):
        """An unsuccessful test sort to score by the median letters in each location."""
        data = {}
        frequencies = [self.get_frequencies()]
        for position in range(self.word_size):
            frequencies.append(self.get_frequencies(position))
        for word in self.words:
            word_score = 0
            for position in range(self.word_size):
                letter = word[position]
                word_score += abs(.5 - (frequencies[position + 1][letter] / self.count))
            data[word] = word_score
        # extract top scoring words
        best_word = sorted(data, key=data.get)[0]
        top_score = data[best_word]
        best_words = []
        for word, score in data.items():
            if score == top_score:
                best_words.append(word)
        return best_words

    def test_binarysort_by_word(self):
        """An unsuccessful test sort to find the word with potential to equally divide the game space."""
        data = {}
        for test in self.words:
            included = set()
            excluded = set()
            for word in self.words:
                exclude = False
                for letter in set(test):
                    if not letter in word:
                        excluded.add(word)
                        exclude = True
                        break
                if exclude:
                    continue
                else:
                    included.add(word)
            score = abs(.5 - (len(included) / len(self.words)))
            data[test] = score
        # extract top scoring words
        best_word = sorted(data, key=data.get)[0]
        top_score = data[best_word]
        best_words = []
        for word, score in data.items():
            if score == top_score:
                best_words.append(word)
        return best_words

    def test_maximum_subset(self):
        """An unsuccessful test sort to score by the maximum disruptive potential of word."""
        data = {}
        for test in self.words:
            included = set()
            excluded = set()
            for word in self.words:
                exclude = False
                for letter in set(test):
                    if not letter in word:
                        excluded.add(word)
                        exclude = True
                        break
                if exclude:
                    continue
                else:
                    included.add(word)
            score = len(excluded)
            data[test] = score
        # extract top scoring words
        best_word = sorted(data, key=data.get, reverse=True)[0]
        top_score = data[best_word]
        best_words = []
        for word, score in data.items():
            if score == top_score:
                best_words.append(word)
        return best_words

    def test_random(self):
        """A test to choose only random correct words from the game space."""
        return choice(self.words)


class Game:
    """Wordle interactive game play, autoplay, and testing."""

    def __init__(self, words, lines=CHANCES):
        self.words_in_play = Wordlist(words)
        self.anagram_words_in_play = Wordlist(words)  # for anagram play algorithm
        self.lines = lines
        self.line = 1
        self.history = []
        self._reset_known()

    def _reset_known(self):
        """Reset game play."""
        self.known_yellows = {place: set() for place in range(self.words_in_play.word_size)}
        self.known_greens = {place: set() for place in range(self.words_in_play.word_size)}
        self.known_greys = {place: set() for place in range(self.words_in_play.word_size)}

    def get_guess_word(self, algorithm, result=""):
        """Calculate the best guess word according to the algorithm (default = BEST)."""
        yellows = set()
        greens = set()
        greys = set()
        for place in self.known_yellows:
            yellows = yellows.union(self.known_yellows[place])
            greens = greens.union(self.known_greens[place])
            greys = greys.union(self.known_greys[place])
        known = len(set.union(yellows, greens, greys))
        matches = len(greens)
        for letter in yellows:
            if letter not in greens:
                matches += .5 / self.words_in_play.word_size
        start_word = None
        if " " in algorithm:
            start_word = algorithm.split(" ")[1]
            algorithm = algorithm.split(" ")[0]
        if self.words_in_play.count > 0:
            if start_word and self.line == 1:
                guess = start_word
                self.words_in_play.sort_words() # avoid problems with randomised sorts differing in tests
            elif "BL" in algorithm:
                if "s" in algorithm:
                    guess = Wordlist(self.words_in_play.test_binarysort_by_letter()).sort_words(priority="Y")[0]
                else:
                    guess = self.words_in_play.test_binarysort_by_letter()[0]
            elif "BW" in algorithm:
                if "s" in algorithm:
                    if "Y" in algorithm:
                        guess = Wordlist(self.words_in_play.test_binarysort_by_word()).sort_words(priority="Y")[0]
                    else:
                        guess = Wordlist(self.words_in_play.test_binarysort_by_word()).sort_words()[0]
                else:
                    guess = self.words_in_play.test_binarysort_by_word()[0]
            elif "M" in algorithm:
                if "s" in algorithm:
                    guess = Wordlist(self.words_in_play.test_maximum_subset()).sort_words()[0]
                else:
                    guess = self.words_in_play.test_maximum_subset()[0]
            elif "y" in algorithm and self.line == 1:
                guess = self.words_in_play.sort_words("Y")[0]
            elif "g" in algorithm and self.line == 1:
                guess = self.words_in_play.sort_words("G")[0]
            elif "Y" in algorithm:
                guess = self.words_in_play.sort_words("Y")[0]
            elif "R" in algorithm:
                guess = self.words_in_play.test_random()
            elif "G" in algorithm:
                if "n" in algorithm or self.line == 1:
                    guess = self.words_in_play.sort_words()[0]
                elif "a" in algorithm and self.line == 2 and float(
                        algorithm.split("a")[1].split("f")[0].split("k")[0]) >= matches:
                    guess = self.anagram_words_in_play.sort_words()[0]
                elif ("k" in algorithm) and (int(algorithm.split("k")[1].split("f")[0].split("a")[0]) <= known):
                    guess = self.words_in_play.sort_words(score_duplicates=True)[0]
                elif ("f" in algorithm) and (float(algorithm.split("f")[1].split("k")[0].split("a")[0]) <= matches):
                    guess = self.words_in_play.sort_words(score_duplicates=True)[0]
                else:
                    guess = self.words_in_play.sort_words()[0]
                elimination_word = ""
                if "e" in algorithm and len(self.words_in_play.words) > 2 and len(self.words_in_play.equal_choices) > (
                        1 + self.lines - self.line) and self.line > 1 and self.line < self.lines:
                    elimination_word = self.get_elimination_words(result)
                if elimination_word:
                    guess = elimination_word
                    # print(self.history, self.debug_word)
                    # print(self.debug_last_words)
                    # print(self.debug_remaining)
                    # print(self.debug_elimination_words)
                    # print("Elimination: Line",self.line, elimination_word, self.history)
            else:
                print("Unknown:", algorithm)
                exit()
            self.line += 1
            return guess
        else:
            return False

    def get_elimination_words(self, result):
        """Calculate the best words to eliminate the most remaining options."""
        debug("Equal", self.words_in_play.equal_choices)
        debug("Count", len(self.words_in_play.equal_choices))
        debug("Words", self.words_in_play.words)
        debug("Line", self.line)
        debug("History", self.history)

        # calculate known letters
        known = set()
        greys = set()
        greens = set()
        for place in self.known_yellows:
            known = known.union(self.known_yellows[place])
            known = known.union(self.known_greens[place])
            known = known.union(self.known_greys[place])
            greys = greys.union(self.known_greys[place])
            greens = greens.union(self.known_greens[place])
        blanks = set()
        for place in range(self.words_in_play.word_size):
            if result[place] != "-":
                blanks.add(place)
        yellows_played = []
        for place in blanks:
            for letter in self.known_yellows[place]:
                yellows_played.append(letter)
        possible_yellows = set()  # ignore played yellows
        for letter in yellows_played:
            if yellows_played.count(letter) < len(blanks):
                possible_yellows.add(letter)
        possible_repeating_greens = greens - greys  # greens which haven't shown up grey
        # print("known", known)
        # if possible_yellows:
        #    print("possible_yellows", possible_yellows)
        # if possible_repeating_greens:
        #    print("possible_repeating_greens", possible_repeating_greens)
        known -= set.union(possible_repeating_greens, possible_yellows)
        # print("known", known)
        # print(self.line, "out of", self.lines)
        # print(len(last_words), "greater than", (self.lines + 1 - self.line))
        # find remaining letters to eliminate
        remaining = set()
        for position in range(self.words_in_play.word_size):
            if result[position] != "G":
                for word in self.words_in_play.equal_choices:
                    if word[position] not in known:
                        remaining.add(word[position])
        # self.debug_remaining = remaining
        # print("Remaining:", remaining)
        debug("Remaining", remaining)
        best_elimination_words = {}
        for word in self.words_in_play.original:
            score = 0
            for letter in set(word):
                # print(letter, remaining)
                if letter in remaining:
                    score += 1
            if score > (len(self.words_in_play.words) - (
                    1 + self.lines - self.line)):  # only if the word eliminates enough choices
                for place in blanks:
                    if word[place] in remaining:
                        score += 1 / self.words_in_play.word_size  # small score increase for letters in a playable place - don't waste a play
                best_elimination_words[word] = score
                debug("Word", word)
                debug("Score", score)
                debug("len(self.words_in_play.equal_choices) - (1+self.lines - self.line)",
                      len(self.words_in_play.equal_choices) - (1 + self.lines - self.line))
        debug("Elimination", sorted(best_elimination_words, key=best_elimination_words.get, reverse=True))
        debug("Count", len(best_elimination_words))
        if len(best_elimination_words) > 0:  # only if word found
            # print(sorted(best_elimination_words, key=best_elimination_words.get, reverse=True)[0])
            # print(sorted(best_elimination_words, key=best_elimination_words.get, reverse=True))
            # self.debug_elimination_words = best_elimination_words
            return sorted(best_elimination_words, key=best_elimination_words.get, reverse=True)[0]
        return False

    def interactive_game(self, algorithm=BEST):
        """Play for a solution interactively."""
        self._reset_known()
        self.line = 1
        score = 0
        result = ""
        while 0 < self.line <= self.lines:
            guess = self.get_guess_word(algorithm, result)
            self.history.append(guess)
            if guess:
                print(guess.upper())
                result = ""
                while len(result) != self.words_in_play.word_size:
                    result = input("     Result ([G]reen [Y]ellow [g]rey): ").strip()
                    for character in result:
                        if character not in "GYg":
                            result = ""
                unknown_space = []
                for place in range(len(guess)):
                    if result[place] != "G":
                        unknown_space.append(guess[place])
                for place in range(len(guess)):
                    if result[place] == "G":
                        self.known_greens[place].add(guess[place])
                    elif guess[place] in unknown_space:
                        self.known_yellows[place].add(guess[place])
                    else:
                        self.known_greys[place].add(guess[place])
                if len(result.replace("G", "")) == 0:
                    score = self.line - 1
                    break
                self.words_in_play.filter_words(guess, result)
                self.anagram_words_in_play.filter_words(guess, "g" * self.words_in_play.word_size)
            else:
                break
        print("\nWORDLE", str(score) + "/" + str(self.lines))
        print(self.history)

    def auto_play(self, word, algorithm=BEST, test_limit=CHANCES):
        """Automatically generate the best solution for a word."""
        self.debug_word = word
        self.line = 1
        result = ""
        self.guess = ""
        self.history = []
        self._reset_known()
        while 0 < self.line <= test_limit:
            guess = self.get_guess_word(algorithm, result)
            self.history.append(guess)
            if guess:
                unknown_space = []
                for place in range(len(guess)):
                    if guess[place] != word[place]:
                        unknown_space.append(word[place])
                result = ""
                for place in range(len(guess)):
                    if guess[place] == word[place]:
                        result += "G"
                        self.known_greens[place].add(guess[place])
                    elif guess[place] in unknown_space:
                        result += "Y"
                        self.known_yellows[place].add(guess[place])
                    else:
                        result += "g"
                        self.known_greys[place].add(guess[place])
                if len(result.replace("G", "")) == 0:
                    break
                self.words_in_play.filter_words(guess, result)
                self.anagram_words_in_play.filter_words(guess, "g" * self.words_in_play.word_size)
            else:
                break
        self.words_in_play._reset()
        self.anagram_words_in_play._reset()
        if word in self.history:
            return self.history
        else:
            return []

    def run_tests(self, algorithms=[], words=[], filename="tests.log", bookmark="", word_counting=False):
        """Run and log a series of tests of different algorithms."""
        if not words:
            words = self.words_in_play.original
        for algorithm in algorithms:
            try:
                with open(filename) as f:
                    for line in f:
                        pass
                    last_log = line
                if last_log.split(" ")[0] == algorithm:
                    bookmark = last_log.split(" ")[1]
            except FileNotFoundError:
                pass
            for start_word in (
                    reversed(self.words_in_play.sort_words()) if "-" in algorithm else self.words_in_play.sort_words()):
                if start_word == bookmark:
                    bookmark = ""
                    continue
                elif len(bookmark) == 5:
                    continue
                log = open(filename, "a")
                scores = []
                for word in words.copy():
                    score = len(self.auto_play(word, algorithm + ((" " + start_word) if "c" in algorithm else ""), 12))
                    if word_counting:
                        self.words_in_play.original.remove(word)
                    if not score in [1, 2, 3, 4, 5, 6]:
                        debug("History", self.history)
                    scores.append(score)
                if len(words) > 1 or word_counting:
                    statistics = Counter(scores)
                    valid_scores = scores.copy()
                    count = len(scores)
                    valid_scores = [value for value in valid_scores if value != 0]
                    solved = valid_scores.copy()
                    for failed in range(7, 13):
                        solved = [value for value in solved if value != failed]
                    print(algorithm + ((" " + start_word) if "c" in algorithm else ""), "| Average |",
                          round(sum(valid_scores) / len(valid_scores), 4), "| Average (in Solved) |",
                          round(sum(solved) / len(solved), 4), "| Total |", count, "| Valid |", len(valid_scores),
                          "| Solved |",
                          len(solved), "| % |", round(len(solved) / count * 100, 2), "| Statistics |", statistics, "|",
                          str(datetime.now()))
                    print(algorithm + ((" " + start_word) if "c" in algorithm else ""), "| Average |",
                          round(sum(valid_scores) / len(valid_scores), 4), "| Average (in Solved) |",
                          round(sum(solved) / len(solved), 4), "| Total |", count, "| Valid |", len(valid_scores),
                          "| Solved |",
                          len(solved), "| % |", round(len(solved) / count * 100, 2), "| Statistics |", statistics, "|",
                          str(datetime.now()), file=log)
                else:
                    pass
                log.close()
                if "c" not in algorithm.split(" ")[0]:
                    break


if __name__ == "__main__":
    print("WORDLE LAB")
    print(
        "\n1. Download Wordle Files\n2. Solution Generator\n3. Solution Generator (offline)\n4. Interactive Play\n5. "
        "Interactive Play (offline)\n6. Run Tests\n7. Dictionary Utility\n")
    while True:
        wordle = "wordle_dictionary.txt"
        allowed = "wordle_allowed.txt"
        yesterday = "yesterday.txt"
        played = "wordle_played_dictionary.txt"
        remaining = "wordle_remaining_dictionary.txt"
        option = input(": ").strip()
        if option == "1":
            print("\nDownloading files from Wordle ...")
            Game(Dictionary(save_wordle_filename=wordle, save_allowed_filename=allowed).words)
            try:
                f = open(yesterday, "r")
                f.close
                Game(Dictionary(save_wordle_filename=remaining,
                                save_played_filename=played,
                                save_allowed_filename=allowed,
                                yesterday_filename=yesterday).words)
            except FileNotFoundError:
                print(yesterday + " file not found (latest solution).")
            print("Done.")
            break
        if option in ["2", "3"]:
            print("\nSolution Generator.")
            if option == "2":
                game = Game(Dictionary(yesterday_filename=yesterday).words)
            else:
                game = Game(Dictionary(files=[wordle], yesterday_filename=yesterday).words)
                try:
                    pass
                except FileNotFoundError:
                    print(wordle + " file not downloaded or found.")
                    break
            word = ""
            while len(word) != game.words_in_play.word_size:
                word = input("Enter word: ").strip().lower()
                for character in word:
                    if not latin(word):
                        word = ""
            print(game.auto_play(word, algorithm=BEST))
            break
        if option in ["4", "5"]:
            print("\nInteractive Play.\nEnter Wordle result as a 5 letter combination of G, Y, and g.")
            if option == "4":
                game = Game(Dictionary(yesterday_filename=yesterday).words)
            else:
                game = Game(Dictionary(files=[wordle], yesterday_filename=yesterday).words)
                try:
                    pass
                except FileNotFoundError:
                    print(wordle + " file not downloaded or found.")
                    break
            game.interactive_game()
            break
        if option == "6":
            print("\nRunning tests (see code for samples) ...")
            game = Game(Dictionary().words)
            print("Best original start word:", game.words_in_play.sort_words()[0])
            print("Best 'human' start word?", game.words_in_play.test_human()[0])
            game = Game(Dictionary(["wordle_remaining_dictionary.txt"]).words)
            print("Best start word from now:", game.words_in_play.sort_words()[0])
            game = Game(Dictionary().words)
            print("Testing 1st, 2nd, 3rd words:", game.auto_play("vivid"))
            print("Testing 1st, 2nd, 3rd words:", game.auto_play("vivid",BEST.split(" ")[0]+" slant"))
            game = Game(Dictionary(["wordle_dictionary.txt", "wordle_allowed.txt"]).words)
            print("Best start word from complete dictionary:", game.words_in_play.sort_words()[0])
            print("Best start word using yellow probability:", game.words_in_play.sort_words("Y")[0])
            game = Game(Dictionary().words)
            print("Testing best algorithm ("+BEST+"):")
            game.run_tests([BEST])
            print("Testing best algorithm with word-counting:")
            game.run_tests([BEST], word_counting=True)
            game = Game(Dictionary().words)
            # Sort tests for debugging.
            print("Frequencies:", game.words_in_play.get_frequencies())
            debug("Sort by Green Probability", game.words_in_play.sort_words())
            debug("Sort by Yellow Probability", game.words_in_play.sort_words(priority="Y"))
            debug("Binary by Word", game.words_in_play.test_binarysort_by_word())
            debug("Binary by Letter", game.words_in_play.test_binarysort_by_letter())
            game = Game(Dictionary().words)
            # test various algorithms
            game.run_tests(["R", "Y", "gY", "G", "yG"])
            break  # more sample tests below
            # test no resorting
            game.run_tests(["Gn"])
            # test binary searches
            game.run_tests(["BW", "BL"])
            game.run_tests(["BWs", "BLs"])
            game.run_tests(["M", "Ms"])
            # test second line anagram strategy
            game.run_tests(["Ga.1", "Ga.2", "Ga.3", "Ga.4", "Ga.5", "Ga1", "Ga1.1", "Ga1.2", "Ga1.3", "Ga1.4", "Ga2", "Ga2.1", "Ga2.2", "Ga2.3"])
            # test duplicates for known
            game.run_tests(["Gk5", "Gk6", "Gk7", "Gk8", "Gk9", "Gk10", "Gk11"])
            # test duplicates for found
            game.run_tests(["Gf.1", "Gf.2", "Gf.3", "Gf.4", "Gf.5", "Gf1", "Gf1.1", "Gf1.2", "Gf1.3", "Gf1.4","Gf2", "Gf2.1", "Gf2.2", "Gf2.3","Gf3", "Gf3.1", "Gf3.2","Gf4", "Gf4.1"])
            # test elimination strategy
            game.run_tests(["Ge"])
            # test duplicates for known with elimination
            game.run_tests(["Gek5", "Gek6", "Gek7", "Gek8", "Gek9", "Gek10", "Gek11"])
            # test duplicates for found with elimination
            game.run_tests(["Gef.1", "Gef.2", "Gef.3", "Gef.4", "Gef.5", "Gef1", "Gef1.1", "Gef1.2", "Gef1.3", "Gef1.4","Gef2", "Gef2.1", "Gef2.2", "Gef2.3","Gef3", "Gef3.1", "Gef3.2","Gef4", "Gef4.1"])
            # test combinaton
            game.run_tests(["Gek6f.1", "Gek6f.2", "Gek6f.3", "Gek6f.4", "Gek6f.5", "Gek6f1", "Gek6f1.1", "Gek6f1.2", "Gek6f1.3", "Gek6f1.4","Gek6f2", "Gek6f2.1", "Gek6f2.2", "Gek6f2.3","Gek6f3", "Gek6f3.1", "Gek6f3.2","Gek6f4", "Gek6f4.1"])
            # test best algorithm
            print("Testing best algorithm ("+BEST+"):")
            game.run_tests(["Gek6f2.2a.1"])
            # test for best start words with best algorithm
            game.run_tests(["Geck6f2.2a.1"], filename="Geck6f2.2a.1.log")
            # test for worst start words with best algorithm
            game.run_tests(["Ge-ck6f2.2a.1"],filename="Ge-ck6f2.2a.1.log")
            # test for worst start words with sorted lists
            game.run_tests(["Gc"],filename="Gc.log")
            # test for worst start words with sorted lists
            game.run_tests(["G-c"],filename="G-c.log")
            # test for best start words with random
            game.run_tests(["Rc"],filename="Rc.log",bookmark="abort")
            # test for worst start words with random
            game.run_tests(["R-c"], filename="R-c.log")
            break
        if option == "7":
            print("\nCreating sample dictionary of 5 letter words from files in scowl\ folder (if exists) ...")
            try:
                dictionary = Dictionary(
                    ["english-words.10", "english-words.20", "english-words.35", "english-words.40", "english-words.50",
                     "english-words.55", "english-words.60", "english-words.70", "english-words.80",
                     "american-words.10",
                     "american-words.20", "american-words.35", "american-words.40", "american-words.50",
                     "american-words.55", "american-words.60", "american-words.70", "american-words.80"],
                    directory="scowl\\")  # Sample: Create dictionary with Scowl files. Source: http://wordlist.aspell.net/
            except FileNotFoundError:
                print("Source file(s) not found. See http://wordlist.aspell.net/ for Scowl files.")
                break
            dictionary.extract(5)  # Extract only 5 letter words.
            dictionary = Dictionary(["dictionary5.lst"])  # Sample: Load dictionary.
            print("Done.")
            break
