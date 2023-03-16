from pygoogletranslation import Translator, LANGUAGES
from dotenv import load_dotenv
import os
import discord
import emoji
import re
import random

VERSION = '1.8'

DEBUG_MODE = False

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
    'sip', 'si', 'bueno', 'gracias', 'seas', 'sea', 'vale',
    'juan', 'lo', 'ok', 'ok.', 'okay', 'okey'
]

ingored_contained_words = [
    'gracias', 'bueno', 'seas', 'sea', 'los ', 'lo ', 'noo ', 'no ', 'nooo', 'juan ',
    'vale ', 'ok '
]

apologies = [
    "Lo siento, mi cerebro es un burrito sin frijoles.",
    "Perdóneme, a veces mi cabeza está en las nubes.",
    "Disculpa, estoy más perdido que un calcetín en la lavadora.",
    "Lo siento, soy más lento que un caracol con resaca.",
    "Perdóneme, mi inteligencia a veces es más baja que un caracol sin concha.",
    "Disculpa, mi cabeza es como un agujero negro, atrae toda la tontería.",
    "Lo siento, soy tan tonto que necesito un GPS para encontrar mi cerebro.",
    "Perdóneme, mi cerebro es como un plato de espagueti, todo revuelto.",
    "Disculpa, a veces soy más despistado que un pez en la montaña.",
    "Lo siento, mi capacidad intelectual a veces es inferior a la de un pato de goma.",
    "Perdóneme q soy medio pendejo"
]


def random_apology():
    return random.choice(apologies)


async def send_reply(message, response):
    if not DEBUG_MODE:
        await message.reply(response)
    else:
        print("REPLY (DEBUG): " + response)


@client.event
async def on_message(message):
    global DEBUG_MODE
    print(f'{message.author}: {message.content}')
    if message.author == client.user:
        return

    if message.reference is not None:
        if message.reference.resolved.author.id == client.user.id:
            await send_reply(message, random_apology())
            return

    msgLower = message.content.lower()
    if '@1083650431156232313' in msgLower or 'pelón' in msgLower or 'calvo' in msgLower \
            or 'pelon' in msgLower or 'señor traductor' in msgLower:
        await message.reply(random_apology())
        return
    elif '<@' in message.content:
        print("ignored because message tags another user")
        return

    if message.content.lower() == "$leave":
        exit()
    elif message.content.lower() == "$toggledebug":
        DEBUG_MODE = not DEBUG_MODE
        print('DEBUG_MODE set to ' + str(DEBUG_MODE))
        return
    elif message.content.lower() == "cállate pelón" or message.content.lower() == 'callate pelon':
        DEBUG_MODE = True
    elif msgLower == "habla pelon" or msgLower == "habla pelón" or "pelon donde estas" in msgLower \
            or "pelón dónde estás" in msgLower:
        DEBUG_MODE = False

    text = emoji.replace_emoji(message.content, " ")
    for word in ignored_words:
        if text.lower() == word:
            print("message is a word in the ignored words list, ignoring", end="\n\n")
            return

    for word in ingored_contained_words:
        if word in text.lower():
            print(f"message contains ignored word '{word}', ignoring", end="\n\n")
            return

    if text.startswith("+") or message.author.id == 228537642583588864:
        print("message is a bot command, ignoring", end="\n\n")
        return

    data = translator._translate(text, 'auto', 'es')
    print(f"detected language: {LANGUAGES[data[0][0][1]]}")
    if contains_vowels(text) and not text.isnumeric() and data[0][0][1] == 'en':
        await send_reply(message, f"**{message.author.name} dijo:** {data[0][0][0]}")
    else:
        print("did not translate because message is either only numbers or is not English")

    print("")


client.run(token)
