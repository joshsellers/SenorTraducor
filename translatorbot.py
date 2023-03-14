from pygoogletranslation import Translator
from dotenv import load_dotenv
import os
import discord
import emoji
from pygoogletranslation import LANGUAGES
import re

VERSION = '1.0'

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

translator = Translator()

client = discord.Client(intents=discord.Intents.all())


def contains_vowels(content):
    text = content.lower()
    return len(re.findall("a|e|i|o|u", text)) > 0


@client.event
async def on_ready():
    print(f'{client.user} v{VERSION} has connected to Discord')


@client.event
async def on_disconnect():
    print('disconnecting')


ignored_words = [
    'yo', 'holi', 'holis', 'mmm', 'mm', 'mmmm',
    'anto', 'zay', 'karol', '...', 'josh', 'siri', '…',
    'sip', 'si', 'bueno', 'gracias'
]

ingored_contained_words = [
    'gracias', 'bueno'
]


@client.event
async def on_message(message):
    print(f'{message.author}: {message.content}')
    if message.author == client.user:
        return

    if message.reference is not None:
        if message.reference.resolved.author.id == client.user.id:
            await message.reply(f'Perdóneme q soy medio pendejo')
            return

    msgLower = message.content.lower()
    if '@1083650431156232313' in msgLower or 'pelón' in msgLower or 'calvo' in msgLower \
            or 'pelon' in msgLower or 'señor traductor' in msgLower:
        await message.reply(f'Perdóneme q soy medio pendejo')
        return
    elif '<@' in message.content:
        return

    if message.content.lower() == "$leave":
        exit()

    text = emoji.replace_emoji(message.content, " ")
    for word in ignored_words:
        if text.lower() == word:
            print("message is a word in the ignored words list, ignoring", end="\n\n")
            return

    for word in ingored_contained_words:
        if word in text.lower():
            print("message contains a ignored word, ignoring", end="\n\n")
            return

    if text.startswith("+") or message.author.id == 228537642583588864:
        print("message is a bot command, ignoring", end="\n\n")
        return

    data = translator._translate(text, 'auto', 'es')
    print(f"detected language: {LANGUAGES[data[0][0][1]]}")
    if contains_vowels(text) and not text.isnumeric() and data[0][0][1] == 'en':
        await message.reply(f"**{message.author.name} dijo:** {data[0][0][0]}")
    else:
        print("did not translate because message is either only numbers or is not English")

    print("")

client.run(token)
