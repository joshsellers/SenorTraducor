from pygoogletranslation import Translator
from dotenv import load_dotenv
import os
import discord
import emoji

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

translator = Translator()

client = discord.Client(intents=discord.Intents.all())


def check_only_emoji(content):
    if content.endswith("️j"):
        return True

    for char in content:
        if not emoji.is_emoji(char) and not content.isspace():
            return False
    return True



@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord')


@client.event
async def on_disconnect():
    print('disconnecting')


@client.event
async def on_message(message):
    if message.content.lower() == "$leave":
        exit()

    text = emoji.replace_emoji(message.content, " ")
    print(f'{message.author}: {message.content}')
    if message.author == client.user:
        return

    if text.startswith("+") or message.author.id == 228537642583588864:
        print("message is a bot command, ignoring", end="\n\n")
        return

    data = translator._translate(text, 'auto', 'es')
    print(f"detected language: {data[0][0][1]}")
    if not text.isnumeric() and data[0][0][1] == 'en':
        await message.reply(f"{message.author} dijo: {data[0][0][0]}")
    else:
        print("did not translate because message is either only emoji, only numbers, or is not English")

    print("")

client.run(token)
