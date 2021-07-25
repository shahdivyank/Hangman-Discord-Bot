from random_word import RandomWords
from PyDictionary import PyDictionary
import discord
import os

TOKEN = os.environ["TOKEN"]

random = RandomWords()
dictionary = PyDictionary()
client = discord.Client()

letters = []
guesses = []

def generateWord():
    return random.get_random_word(hasDictionaryDef = "true")

@client.event
async def on_ready():
   print("Active")

@client.event
async def on_message(message):
    channel = ""

    if message.content.lower() == "$play":
        await message.channel.send("Welcome to Hangman")
        global letters = []
        global guesses = []
        global display = ""
        channel = message.channel
        word = generateWord()
        while True:
            try:
                if "-" not in word and dictionary.meaning(word, disable_errors=True) != None:
                    break
            except:
                pass
            word = generateWord()
        for letter in word:
            letters.append("-")
        print(word)

        def check(m):
            return len(m.content) >= 1 and m.channel == channel

        lives = 10

        while True:
            display = ""
            for letter in letters:
                display += letter + " "
            await channel.send(display)
            await message.channel.send("Enter Your Guess. Enter 0 to Give Up:")
            msg = await client.wait_for('message', check=check)
            guess = str(msg.content.lower())
            if guess == "0":
                break
            if lives == 0:
                await message.channel.send("Better luck next time!")
                break
            if guess in guesses:
                await message.channel.send("You Have Already Guessed the letter " + guess)
                continue
            if not guess.isalpha() or len(guess) > 1:
                await message.channel.send("Please only enter single letters.")
                continue
            guesses.append(guess)
            if guess in word:
                i = 0
                for letter in word:
                    if guess == word[i]:
                        letters[i] = guess
                    i += 1
                await message.channel.send("Great Guessing!")
            else:
                lives -= 1
                msg = str("Try Again. You have " + str(lives) + " wrong guesses before GAME OVER!")
                await message.channel.send(msg)
            if "-" not in letters:
                await message.channel.send("Congratulations you guessed the word right!")
                break

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
        await message.channel.send(msg)

client.run(TOKEN)
