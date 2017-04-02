import discord
from discord.ext import commands
import random
from textblob import TextBlob
import os

description = 'Bot'
bot_prefix = '?'

bot = commands.Bot(description=description, command_prefix=bot_prefix)

tts_lines = []

class Navy(object):
    def read_lines(self, fname):
        with open(fname, 'r', encoding='utf8') as f:
            return f.readlines()

    def __init__(self):
        self.navy = self.read_lines('navy.txt')
        self.iter_navy = iter(self.navy)

    def get_next(self):
        try:
            next_line = next(self.iter_navy)
            return next_line
        except StopIteration:
            self.iter_navy = iter(self.navy)
            return next(self.iter_navy)

def list_files(mypath):
    f = []
    for (dirpath, dirnames, filenames) in os.walk(mypath):
        f.extend(filenames)
        break
    return f

IMGS_PATH = './img/'
imgs = list_files(IMGS_PATH)

navy = Navy()

def evaluate_msg(msg):
    analysis = TextBlob(msg)
    to_ret = 'Message Positivity [SCALE -1 TO 1]: '
    to_ret += str(analysis.sentiment.polarity)
    return to_ret

def get_everything_after_first_space(s):
    return s.split(' ', 1)[1]

@bot.event
async def on_ready():
    print('Logged in')
    print('Name : %s' % bot.user.name)
    print('ID : %s' % bot.user.id)
    print(discord.__version__)

@bot.command()
async def roll(dice : str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await bot.say('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await bot.say(result)

@bot.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == bot.user:
        return

    if message.content.startswith('!eval'):
        arg = message.content.split()[1]
        msg = await bot.get_message(message.channel, int(arg))
        polarity = evaluate_msg(msg.content)
        # await bot.send_message(message.channel, str(message.channel))
        await bot.send_message(message.channel, polarity)

    if message.content.startswith('!roll'):
        arg = message.content.split()[1]
        try:
            rolls, limit = map(int, arg.split('d'))
            if rolls>=200:
                rolls=200
        except Exception:
            await bot.send_message(message.channel, 'Format has to be in NdN!')
            return

        result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        await bot.send_message(message.channel, result)

    if message.content.startswith('!read'):
        arg = get_everything_after_first_space(message.content)
        await bot.send_message(message.channel, arg, tts=True)

    if message.content.startswith('!tts_add'):
        arg = get_everything_after_first_space(message.content)
        tts_lines.append(arg)
        await bot.send_message(message.channel, 'tts_add successful')

    if message.content.startswith('!tts_rand'):
        await bot.send_message(message.channel, random.choice(tts_lines), tts=True)

    if message.content.startswith('!next_navy'):
        await bot.send_message(message.channel, navy.get_next(), tts=True)

    if message.content.startswith('!nice_person'):
        with open(IMGS_PATH + random.choice(imgs), 'rb') as f:
            await bot.send_file(message.channel, f)

    if message.content.startswith('!guess'):
        await bot.send_message(message.channel, 'Guess a number between 1 to 10')

        def guess_check(m):
            return m.content.isdigit()

        guess = await bot.wait_for_message(timeout=5.0, author=message.author, check=guess_check)
        answer = random.randint(1, 10)
        if guess is None:
            fmt = 'Sorry, you took too long. It was {}.'
            await bot.send_message(message.channel, fmt.format(answer))
            return
        if int(guess.content) == answer:
            await bot.send_message(message.channel, 'You are right!')
        else:
            await bot.send_message(message.channel, 'Sorry. It is actually {}.'.format(answer))

bot.run('Mjk3ODMxMzM1MjExMzAyOTEy.C8GixA.mC1sCrokOgiq-ell-N8r45pg6Bg')