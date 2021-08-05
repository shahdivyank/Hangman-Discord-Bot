from random_word import RandomWords
from PyDictionary import PyDictionary
from discord.ext import commands
import os

client = commands.Bot(command_prefix="!")

random = RandomWords()
dictionary = PyDictionary()

letters = []
guesses = []
lives = 0
word = ""
inGame = False


def generateWord():
    return random.get_random_word(hasDictionaryDef="true")

def ending():
    global inGame
    if inGame:
        inGame = False
        partsOfSpeechs = ["Verb", "Noun", "Adjective"]
        meaning_dict = dictionary.meaning(word)
        meaning_list = []
        meaning_str = ""
        for partsOfSpeech in partsOfSpeechs:
            try:
                meaning_list.append(meaning_dict[partsOfSpeech])
            except:
                pass

        count = 1
        for meaning in meaning_list:
            for sub_meaning in meaning:
                if "(" in sub_meaning and ")" not in sub_meaning:
                    sub_meaning = sub_meaning.replace("(", "")
                if ")" in sub_meaning and "(" not in sub_meaning:
                    sub_meaning = sub_meaning.replace(")", "")
                meaning_str += " " + str(count) + ". " + sub_meaning
                count += 1
        msg = str("Your word was " + word + ". It means" + meaning_str)
        return msg

@client.command()
async def playHangman(ctx):
    global letters
    global guesses
    global lives
    global word
    global display
    global inGame

    lives = 10

    if inGame == False:
        inGame = True
        await ctx.send("Welcome to Hangman Adventures! Once prompted enter a letter using '!guess letter' you think is in the mystery word! Type '!guessWord your_guess' to guess the entire word!")

        letters = []
        guesses = []
        display = ""

        while True:
            word = generateWord()
            try:
                if "-" not in word and dictionary.meaning(word, disable_errors=True) != None:
                    break
            except:
                pass

        for letter in word:
            letters.append("-")

        await ctx.send(display.join(letters) + "\nEnter a letter:")
    else:
        await ctx.send("A game is already in progress. Enter !end to stop the game!")

@client.command()
async def guess(ctx, guess_letter:str):
    global lives
    global word
    global display
    print(word)
    if len(guess_letter) > 1:
        await ctx.send("Enter single letters!")
    elif not guess_letter.isalpha():
        await ctx.send("Enter letters only")
    elif guess_letter in guesses:
        await ctx.send("You Have Already Guessed the letter " + guess_letter)
    elif guess_letter.strip().lower() in word:
        index = 0
        for letter in word:
            if letter == guess_letter:
                letters[index] = guess_letter
            index += 1
        guesses.append(guess_letter)
        await ctx.send("Great Guesing!\n" + display.join(letters) + "\nEnter a letter:")
    elif "-" not in letters:
        msg = ending()
        inGame = False
        await ctx.send("Congratulations you got it! " + msg)
    elif lives == 0:
        await ctx.send("Better luck next time!")
    else:
        await ctx.send("Incorrect Guess.\n" + display.join(letters) + "\nYou have " + str(lives) + "lives left. " + "Enter a letter:")
        guesses.append(guess_letter)
        lives -= 1

@client.command()
async def endgame(ctx):
    msg = ending()
    await ctx.send(msg)

@client.command()
async def guessWord(ctx, guess_word:str):
    global lives
    if guess_word == word:
        msg = ending()
        inGame = False
        await ctx.send("Congratulations you guessed the word right! " + msg)
    else:
        await ctx.send("Incorrect Guess.\n" + display.join(letters) + "\nYou have " + str(lives) + " lives left. " + "Enter a letter:")
        lives -= 1

client.run(os.environ["TOKEN"])
