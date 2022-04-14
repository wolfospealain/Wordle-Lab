# Wordle Lab

A *Wordle* solver, dictionary utility, and strategy tester.

## Wordle Strategy

For those who don't need, nor want, to read the code documentation below, here is the 12-point summary of the best<sup>a</sup> *Wordle* strategy:

1. The best start word is: **SLATE**.<sup>b</sup>

2. If the first line produces just <u>1 yellow</u>, or nothing, ignore, and play the best of the rest: **CRONY**.<sup>b</sup>

3. Otherwise, always play with known **yellows** in a <u>new</u> place.

4. Always play with known **greens** in place.

5. Never replay a **grey** letter.

6. Do not play words with **repeated letters** until <u>line 3</u>, or until at least <u>4 letters, including at least 2 green</u>, are found.

7. Do not play **plurals**. There are no plurals in the game solutions.

8. Spellings are **American**.

9. Play the **most likely**, familiar, letter combinations, word starts and endings.

10. When there are more possible guesses from the grey letters remaining than plays available, play a word solely to **eliminate** as many of the letter options as possible (except on the last play).

11. Always **check** your next letters against the board and colours on the keyboard before you press enter.

12. Don't cheat.

<sup>a</sup> The average score for the computer is 3.59 with an unbroken streak.

<sup>b</sup> Still, as of 14th April 2022.

## About Wordle

*Wordle* came to life on the 19th of June 2021 with the word CIGAR. It is a simple, gentle game, which has captured the imagination of hundreds of thousands of people worldwide daily players.

A large part of its charm is that there is just one word per day and everyone plays the same word.

It lives now at the *New York Times* at https://www.nytimes.com/games/wordle/

According to the game itself it is simply:

"Guess the WORDLE in six tries. Each guess must be a valid five-letter word. Hit the enter button to submit. After each guess, the color of the tiles will change to show how close your guess was to the word."

- A green indicates that the letter is in the word and in the correct spot.

- A yellow indicates that the letter is in the word but in the wrong spot.

- And a grey indicates that the letter is not in the word in any spot.

### Words

The *Wordle* solutions are a pre-programmed list of 2,309 words. It starts CIGAR, REBUT, SISSY, HUMPH, AWAKE, BLUSH, FOCAL, EVADE, NAVAL, SERVE ...

Importantly:

- There are no plurals. There are some words that end in S, such as BASIS and GLASS, but these are not plurals. 

- And, the spellings are American. You will find words like COLOR, FAVOR, and METER.

A secondary list of 10,663 extra words which are allowed but will never be solutions is also used. This list includes plurals and non-American spellings. You'll find TYRES () English spelling and also a plural) and TIRES (which is plural), and METRE and LITRE (which are English spelling), and LITER (which although American spelling, must just not make sense to the non-metric Americans). METER on the other hand has more meanings and is a solution.

"A new WORDLE will be available each day!" https://www.nytimes.com/games/wordle/

You must play everyday on the same device in order to maintain your streak.

As of the 14th of April 2022, at the time of writing this, since it began with CIGAR on the 19th of June 2021, 300 words have been played. The game will end on the 14th of September 2027 once all 2,309 words have been played.

### New York Times

It has never been particularly easy or difficult. The word list is made up of all normal five-letter words in the American-English language. And the move to the *New York Times* on the 10th of February 2022 did not change the game source code, word order, or make it more difficult despite what everyone believed and complained about.

The word list and order of words had already been programmed into the source code of the game.

The *New York Times* did however remove 6 words from the original 2,315 word list: AGORA, PUPAL, LYNCH, FIBRE, SLAVE and WENCH.

AGORA was due on the 15th of February, PUPAL on the 19th, LYNCH on March 20th, FIBRE on April 10th, SLAVE on the 20th, and WENCH would have been on July 20th.

For the record these were not difficult words to solve, albeit PUPAL was definitely not in everyone's vocabulary.

In this best algorithm (without word-counting) AGORA is solved in 3 ['slate', 'crony', 'agora'], PUPAL in 4 ['slate', 'coral', 'papal', 'pupal'], LYNCH in 3 ['slate', 'crony', 'lynch'], FIBRE  in 4 ['slate', 'price', 'dirge', 'fibre'], SLAVE in 2 ['slate', 'slave'], and WENCH in 4 ['slate', 'crony', 'bench', 'wench'].

One can imagine that AGORA and PUPAL were pulled for obscurity, LYNCH and SLAVE for reasons on American black history, and WENCH for notions of respectability, perhaps.

FIBRE is non-American spelling. *Wordle* is American spelling (added difficulty for those of us on this side of the Atlantic). The word FIBER remains - solvable in 5 ['slate', 'crony', 'rider', 'viper', 'fiber'].

These words have been added instead to list of allowed words that are not solutions.

These minor changes have not caused any significant change. There were however some few issues with two different words in play on the same day depending on whether one had switched to the new website or not, or whether the page was downloaded and cached already on the device.

"We are updating the word list over time to remove obscure words to keep the puzzle accessible to more people, as well as insensitive or offensive words. To ensure your game is in sync with the updated version, you should refresh the website where you play Wordle. We have not made any changes to the basic functionality or rules of the game. We are committed to continuing what makes the game great." https://help.nytimes.com/hc/en-us/articles/360029050872-Word-Games-and-Logic-Puzzles

#### More Reading

- https://www.nytimes.com/2022/01/03/technology/wordle-word-game-creator.html

- https://www.bbc.com/news/technology-60416057

### Game Play

*Wordle* is interesting as a game and in developing game strategy.

*Wordle* isn't always solvable with an ordinary approach. Some words provoke outrage because the number of possibilities for the final letter that will break everyone's streaks, e.g., SHAPE, SHAKE, SHADE, SHAVE, SHAME, SHARE, SHALE.

Many people attempt to play an anagram variation, first collecting as many of the word letters as possible without reusing the hint yellow and green letters. The problem being that there can't always be enough plays for this to work. Technically it could take 6 plays to arrive at the 5 letters needed and it is already too late.

The solution space is 2,309 words which is very big and needs to be whittled down to 1 in under 6 plays.

Worse, brute force random guessing is highly unlikely to succeed.

Amongst the [Twitter](https://twitter.com/search?q=wordle%20%2F6) outrages about unfair words it can be so easy to spot the mistakes and wasted plays.

Strategy, good knowledge of the English language, and hard thought are required at each move.

However, on the other hand, what is interesting is that there is also no way to become stunningly better than everyone else.

The average score for this code using an algorithm which obeys the strategy rules of never replaying a grey, always replaying a green, and always playing a yellow in a new place (basically "Hard Mode"), but selects any arbitrary acceptable word at random is 4 with a 98% success rate.

The best algorithm which selects words for their likelihood to whittle through the solution space, nets a 3.59 average.

As humans that skills is our knowledge of letter combinations in the English language and guessing what to us are the most likely words - which if they match letters it is a success and if they don't match it is also a success by eliminating so many alternatives.

And with word-counting, which may or may not be considered cheating, the program nets a 3.37 average.

As humans also we are playing on average within the bounds of a good 3 and an acceptable 4. A 1 is a fluke and we should all get one once if we keep playing the same word. A 2 is just great luck. At 5 we're in trouble. And at 6 we're doomed.

The world average, according to [analysis of Twitter](https://word.tips/wordle-wizards/), is 3.919 (calculated from tweets of successful games only). The very best country is Sweden at 3.72, the best city is Canberra, Australia, at 3.58; and the very worst is Arabic speaking Egypt but still not very far away at 4.43.

So if we don't also enjoy the perils of 5s and 6s, the mistakes and the words that seem impossible, the everyday 3s and 4s don't seem to prove much at all.

It's not about winning.

#### Strategy

In *Wordle* there are 2,309 possible solution words facing you to begin and every word has an equal chance of being the answer. Each of the 2,309 will one day be the answer. Your job is to whittle that down to 1 as fast as possible and within 6 plays.

You can only successfully do that by eliminating letters that are not in the word and finding letters that are: thus narrowing the possible solution space with each successive play.

The most successful play is to guess words with the most popular letters of the words in the solution space. Either more quickly confirming letters or eliminating larger amounts of words. The solution is tackled from both ends, in the letters found and in the letters eliminated.

#### Single American

The language of the solution list is American spelling only and there are no plurals.

#### Start Word

Everyone agrees that a good start word is important. But people don't agree on which.

With the best testing algorithm, the worst start words were in worsening order are AFFIX, CIVIC, JAZZY, NINJA, MAMMA, and QUEUE. Repeated and rare letters are clearly not a good idea. QUEUE, the worst, scores 4.32 (worryingly still better than Egyptian players!). It compares to a better score of 4 for randomised tests. AFFIX scored 4.27 but had the lowest success rate at 99.18%.

Note: The scores quoted here are more accurate as they include in the averages the failing scores beyond 6.

The most frequents letters in the *Wordle* solution list are: e, a, r, o and t. The least frequent are q, and j. E is over 45 times more likely than j. So we make sure to play e to quickly eliminate nearly half the words or confirm its existence.

The best start word based on probability of a yellow (a letter appearing anywhere in the word) is **AEROS**. It will also satisfy those who believe vowels are more important. It has a score of 3.83 and success rate of 99.7%.

So while, for instance, e may be the most frequent word in the English language and in *Wordle*, the most frequent letter in position 1 is s. The most frequent in positions 2 and 3 is a. E is the most frequent in positions 4 and 5. So instead of looking for probabilities of yellow, we look instead for probabilities of green - the correct letter in position.

The best start word from the complete set of allowable words in *Wordle* is **CARES**, scoring 3.7 with a success rate of 99.96%. It will not appear in the solutions as there are no plurals in the solution list.

But, assuming that we are playing with only the words in the *Wordle* solution list (also the more obvious words), the **best start word is SLATE**, the word with the highest ranking combination of letters in probability of appearing green, and scoring an average of 3.59 with 100% success.

This has the same letters as [Barry Smyth](https://towardsdatascience.com/what-i-learned-from-playing-more-than-a-million-games-of-wordle-7b69a40dbfdb)'s **TALES**, which scores 3.64, but with only 99.96% success, and remember that there are no plurals in *Wordle* solutions. Similarly, **LEAST**, **STALE** and **STEAL** score at 3.6, 3.62 and 3.65, with 99.96%, 100%, and 99.87% success, respectively. Position matters.

##### Vowels and Consonants

Many profess the importance of vowels: "aeiou" and "y". It's not unusual for people to play lines 1 and 2 solely as the way to cover as many letters, especially vowels, at the beginning.

The average number of vowels per word in the solution space is 1.77 out of 5. The word with the best amount of vowels is **AUDIO**, however it scores 3.81 with a success rate of 99.83%.

Vowels are an important part of the language, but probably not as important as you think for spelling. W cn rd wtht vwls. And we, as humans, are probably more likely to see emerging word structure via the scaffolding of consonants.

The best start word for humans is probably **SLANT** - which the most highly scoring consonants in place. However, for the computer it scores 3.68 but at least with a success rate of 100%.

#### Second Word

If the first line produces just 1 yellow, or nothing, ignore it, and play the best of the rest: **CRONY** (COVEY if you've played SLANT).

It can also be a helpful guide when trying to come up with a second play when you've found more than 1 yellow.

If CRONY fails to produce anything significant then a failsafe HUMID is the best third word.

#### Hard Mode

Other, than when a play has no better than 1 yellow, always play as though in "Hard Mode" where you must play with all known hints.

In tests, ignoring 1 yellow yielded scores of 3.62 compared to 3.63.

Known yellows must be played in a new place.

Known greens must be played in place.

Never replay a grey letter.

Always checked the played words and the keyboard colours before committing to a word.

Many people are tempted to play as though amount letters for an anagram puzzle, but with 26 letters in the alphabet it would take 6 plays just to assemble the letters. The solution space is 2,309 so the only winning strategy is to narrow the space as soon as possible.

#### Queen's English

Letters in the English language do not appear in random order - they appear according to familiar patterns. 1 in 14 words start with either "st", "sh", or "sp". 1 in 16 words end in "er". 1 in a 100 words end in "ing". 1 in 12 words have an "er" in them. Over 1 in 20 have "in" or "st". U always follows q.

As humans we don't have the power of a computer's instant sort and recall of a dictionary but we have a similar instinct for what makes a word.

Only by playing with all known hints do we successfully apply that language instinct to narrow down the solution space.

That time when you can't find a word with the known greens in place and the known yellows in new places, then that is the moment you are on the verge of the maybe the 1 and only word that fits. The solution is there in this pattern.

In tests, playing words for letters in place, green probability, yield 3.63 compared to 3.67 for yellow probability.

#### Repeated Letters

It's difficult to know when to play words with repeated letters.

32% of solution words have repeated letters. MAMMA is a word we will have to deal with.

To play a guess with repeated letters is to also forgo the chance to find new letters.

The best strategy is to not play repeated letter until either line 3 or you have at least 4 letters (2 of which are green) known to exist. This can also be recognised as a single grey remaining.

In tests waiting until line 3 yielded scores of 3.62 compared to 3.64. Having 4 known letters yielded 3.63 compared to 3.64. Combined the rules yielded 3.618.

#### Unwinnable

*Wordle* is not always automatically winnable. Too much is up to chance, even for a computer, and there are far too many words in 2,309.

The last letter for some solutions can be interminable: SHAPE, SHAKE, SHADE, SHAVE, SHAME, SHARE, SHALE.

In order not to lose your streak you have think proactively and when there are more possible guesses from the grey letters remaining than plays available, you have to play a word solely to eliminate as many of the letter options as possible. Except on the last play: then you must guess.

In tests, eliminating options when the number of possibilities are too great yields a score of 3.629 compared to 3.636. Every strategy helps.

#### Cheating

All the words to be played are already in the JavaScript source code of the page and downloaded to your device. So it is very easy to cheat. The list of words or today's answer are also widely available online.

It is also very easy to cheat by using a second device or incognito browser window: only to play the game again on your usual browser. 

But what would be the point.

*Wordle* is nice and simple and social. It is hardly competitive. Part of the fun has to be sharing your dramas and cursing at the solution.

The code here uses and saves the word list in only alphabetical order. It never uses or records the game order. So, the "computer" play only ever knows as much about the game as we do, albeit with far far better recall of words from the complete *Wordle* dictionary.

Cheating: don't.

##### Word-Counting

Card-counting in casinos is not illegal, but casinos don't like it. It's when a skilled player keeps track of the cards played so they can make plays with better odds with the better knowledge of cards in play. The use of electronic aides would be not permitted.

Similarly, with *Wordle* it is possible to remember the solution-words played. Solutions played will not be played again.

It's not cheating to remember. But would it be cheating to write them all down, or to look them up?

If the code here has yesterday's solution in a file *yesterday.txt* the computer player will eliminate all played solution-words and recalibrate its statistics accordingly.

This strategy ensure that the computer has every possible advantage and ensure that the its plays the most effective solution based on all knowledge known to this date; albeit of course with the processing power of a computer and the knowledge of the entire *Wordle* solutions vocabulary, that us ordinary humans most very likely lack.

It brings the average score of our friendly computer opponent using the best algorithm from 3.59 to 3.257.

##### Time Zones

An interesting side effect of the fact that *Wordle* is all pre-written and ready for everyday in JavaScript is that it plays today's date as given to it by your device and your device's time zone. So, one can tweak the time zone west in order to catch up late on today's *Wordle*.

This may or may be cheating: but since time has always been relative so you can surely be entitled to your own time zone at times. Legitimately you may have just travelled a long way east today.

## The Code

Written in Python, this *Wordle Lab* is a command-line set of tools designed to test *Wordle* strategies.

##### Menu

1. ###### Download *Wordle* Files:
   
   Download the 2309-word solutions dictionary (alphabetical order), plus the extra 10,663 allowed words dictionary.
   
   If the latest solution word is put in a file *yesterday.txt*, it will also generate a list of previously played words (date order), and a list of remaining words (alphabetical order).
   
   Useful for offline experimentation and other *Wordle* coding projects.

2. ###### Solution Generator:
   
   Enter the solution word and the code generates the game play.
   
   Interesting as a computer competitor for your *Wordle* play and an objective arbiter of difficulty.

3. ###### Solution Generator (offline):
   
   As above, but using the previously downloaded files.

4. ###### Interactive Play:
   
   The computer guesses and you let it know the results from *Wordle*. Enter the results as a 5 letter combination: G for Green, Y for Yellow, and g for grey.
   
   It was the original code to test game play.
   
   Useful for testing or (not recommended), for cheating on the next play.

5. ###### Interactive Play (offline):
   
   As above, but using the previously downloaded files.

6. ###### Run Tests:
   
   Ultimately the purpose of the *Wordle Lab* was to auto-play and test strategy theories and log the results.
   
   The code here has very many tests algorithm tests.
   
   Edit the code to move the break line or create your own tests using the algorithm syntax:
   
   **R**: random selection of words following the hints.
   
   **Y**: select the words based on Yellow probability (most frequent letters in dictionary).
   
   **g**: start word is selected on Green probability.
   
   **G**: select the words based on Green probability (most frequent letters in place).
   
   **y**: the start word is selected on Yellow probability.
   
   **n**: do not recalculate the dictionary probabilities after each play.
   
   **BW**: binary search by word score.
   
   **BL**: binary search by letter scores.
   
   **M**: word with maximum set size.
   
   **s**: adds sorting to BW, BL, M.
   
   **a*X.Y***: apply an "anagram" strategy, not following the hints, if the number of known greens is not more than *X* and the number of yellows not more than *Y*.
   
   **k*X***: play words with repeated letters if *X* number of letters known (played).
   
   **f*X*.*Y***: play words with repeated letters if found at least *X* greens and *Y* yellows.
   
   **c**: cycle through all possible start words.
   
   **-c**: as c but starting with the words with least green probability.
   
   e.g., the best algorithm is "Gek6f2.2a.1": select words based on <u>G</u>reen probability, use an <u>e</u>limination strategy if necessary, play repeated letters once 6 letters are <u>k</u>nown (played), or at least 2 greens and 2 yellows are <u>f</u>ound, play for <u>a</u>lgorithm is only 1 yellow or nothing is found.

7. ###### Dictionary Utility:
   
   The dictionary utility was designed to work with Scowl files to create word lists and extract only 5 letter Latin words.

##### Classes

**Dictionary**: the Dictionary object with basic file management, file loading and merging, extraction of words by word-length, *Wordle* word list download and parsing. A dictionary object can provide the word list to populate a Game and Wordlist.

**Wordlist**: a Wordlist object that can be sorted and filtered and reset to original. A Wordlist object is initialised with a list of words.

**Game**: the main Game object with methods for interactive play, auto-play, and testing. A Game object is initialised with a list of words and creates its required Wordlist objects.

###### See Also

- https://towardsdatascience.com/what-i-learned-from-playing-more-than-a-million-games-of-wordle-7b69a40dbfdb

## 5N2927 Programming and Design Principles

For learners of 5N2927 Programming and Design Principles, note that while the code uses Python basics, functions, and a command-line menu interface with which you are familiar, the code is also written in an object-oriented style with which you will not yet be familiar and is not part of our syllabus (these are the class definitions: Dictionary, Wordlist, Game). The code also relies heavily on more advanced data structures for storing and manipulating large lists of data, lists, sets, and dictionaries, instead of our usual individual variables.

## Bio

Eoin Ó Spealáin is a teacher of Python QQI Programming and Design Principles in the Cork College of FET (Further Education and Training), Mallow Campus, in Cork, Ireland.

*Wordle Lab* cracks the code for the best *Wordle* start word and game strategy for the best score and 100% success - as long as you have the vocabulary, that is.

A *Wordle* player, I'm fascinated by the various *Wordle* strategies found online and in discussion with friends and family. Many are very plausible, but very few are tested.

Even with so many best start words proposed, TEARS, STARE, CARES, AUDIO, etc., none are tested against game play. UCD's [Barry Smyth](https://towardsdatascience.com/what-i-learned-from-playing-more-than-a-million-games-of-wordle-7b69a40dbfdb)'s analysis yielded the start word TALES (which is not far off what I calculated, but Barry, there are no plurals in *Wordle*). Are vowels really as important as everyone thinks, or is that it is easier to imagine needing one of 5 or 6 vowels than panic about the other 20 letters? Should we start with the word AUDIO? Should we always reuse the known green and yellow hint letters ("Hard Mode") or is going for an entirely new set of letters in order to get more letters for an anagram a better strategy? When is it advisable to start guessing words with repeated letters when it could be a wasted opportunity to find more letters. And what is the solution for those deadly long lists of final letter options like SHAPE, SHAKE, SHADE, SHAVE, ... ?

The Python programming language is just the language for such experimentation.

*Wordle Lab* is a collection of utilities to test *Wordle* play strategies - playing itself through every possible solution-word in order to compare various techniques. This is no trivial task. An ordinary laptop took 3 days non-stop to test every possible start word through every possible *Wordle* solution - a total of 5,331,481 games. And given that the code had to be refined and corrected many times, there's no accounting for how many times this has been run.

The result is a clearly winning start word and strategy which can be successful 100% of the time with an average score of 3.59, or 3.33 with the computer's ability for word-counting ([Barry Smyth](https://towardsdatascience.com/what-i-learned-from-playing-more-than-a-million-games-of-wordle-7b69a40dbfdb) is on 3.66 for successful games with a 95% success rate). 

The world average, [as calculated via Twitter](https://word.tips/wordle-wizards/), is 3.919 - though this also is only on successful games, excluding 2% of tweeted failures. Ireland's is 3.89. 

But, as well as perfecting the best *Wordle* strategy, the code is a fun computer opponent to the my daily *Wordle* score - knowing I'm playing against the best possible score. My score average today is a rather average 3.907 - but it's going to get better.

The *Wordle Lab* project was also a nice way to practice programming and relax. As I often tell my class, I can just as easily relax away with endless hours of programming as they do playing computer games.

They don't believe me and insist I get a PlayStation instead.
