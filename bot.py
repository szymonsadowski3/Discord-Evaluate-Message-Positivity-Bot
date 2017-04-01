import discord
from discord.ext import commands
import random
from textblob import TextBlob

description = 'Bot'
bot_prefix = '?'

bot = commands.Bot(description=description, command_prefix=bot_prefix)

def evaluate_msg(msg):
    analysis = TextBlob(msg)
    to_ret = 'Message Positivity [SCALE -1 TO 1]: '
    to_ret += str(analysis.sentiment.polarity)
    return to_ret

@bot.event
async def on_ready():
    print('Logged in')
    print('Name : %s' % bot.user.name)
    print('ID : %s' % bot.user.id)
    print(discord.__version__)

@bot.command(pass_context=True)
async def choose(*choices : str):
    """Chooses between multiple choices."""
    await bot.say(random.choice(choices))

@bot.event
async def on_message(message):
    if message.content.startswith('!whereami'):
        msg = await bot.send_message(message.author, '10')
        await bot.sleep(3)
        await bot.edit_message(msg, '40')

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

bot.run('Mjk3ODMxMzM1MjExMzAyOTEy.C8GixA.mC1sCrokOgiq-ell-N8r45pg6Bg')