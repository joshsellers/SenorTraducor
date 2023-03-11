from pygoogletranslation import Translator
from dotenv import load_dotenv
import os
import discord
import emoji
from pygoogletranslation import LANGUAGES

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

translator = Translator()

client = discord.Client(intents=discord.Intents.all())


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord')


@client.event
async def on_disconnect():
    print('disconnecting')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.reference is not None:
        if message.reference.resolved.author.id == client.user.id:
            await message.reply(f'Perdóneme q soy medio pendejo')
            return

    if '@1083650431156232313' in message.content:
        await message.reply(f'Perdóneme q soy medio pendejo')
        return
    elif '<@' in message.content:
        return

    if message.content.lower() == "$leave":
        exit()

    text = emoji.replace_emoji(message.content, " ")
    print(f'{message.author}: {message.content}')

    if text.startswith("+") or message.author.id == 228537642583588864:
        print("message is a bot command, ignoring", end="\n\n")
        return

    data = translator._translate(text, 'auto', 'es')
    print(f"detected language: {LANGUAGES[data[0][0][1]]}")
    if not text.isnumeric() and data[0][0][1] == 'en':
        await message.reply(f"{message.author.name} dijo: {data[0][0][0]}")
    else:
        print("did not translate because message is either only emoji, only numbers, or is not English")

    print("")

client.run(token)
