from email import message
import discord
import requests
import io
import aiohttp
import random
import command_functions as functions
from discord.ext import commands

# events are found here: https://discordpy.readthedocs.io/en/stable/api.html#event-reference

client = commands.Bot(command_prefix='$')
# remove the default help command 
client.remove_command('help')



@client.event
async def on_ready():
    print("logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    # if the bot sent the message, then return directly to avoid bot answering to itself all the time
    if message.author == client.user:
        return
    if message.content == 'hello':
        await message.channel.send('hello')
    
    # have the bot react to certain messages
    if message.content == 'hi':
        await message.add_reaction("\U0001F601")
    
    await client.process_commands(message)

# have the bot to do something when someone reacted 
@client.event
async def on_reaction_add(reaction, user):
    await reaction.message.channel.send(str(user) + " reacted with " + reaction.emoji)

# have the bot do something when a message is edited
@client.event
async def on_message_edit(before, after):
    await before.channel.send(str(before.author) + " editted a message\n " + "Before: " + before.content + "\nAfter: " + after.content)


#################################
#                               #
#   Command lists begin here    #
#                               #
#################################

@client.command()
async def test_command(ctx):
    # return the name of the person that issued the command
    await ctx.send(ctx.author)
    # return the command itself
    await ctx.send(ctx.message.content)
    # return the server in which the command was issued 
    await ctx.send(ctx.guild)

# test commands with multiple args
@client.command()
async def test_command1(ctx, arg1, arg2):
    await ctx.send("arg1 = " + arg1 + " arg2 = " + arg2)

@client.command()
async def test_command2(ctx, *args):
    for arg in args:
        await ctx.send(arg)
    
    await ctx.send("*args is " + str(type(args)))

# test command from a different file
@client.command()
async def test(ctx):
    await ctx.send(embed=functions.test_function())

# sending custom help menu
@client.command()
async def help(ctx):
    await ctx.send(embed=functions.get_help())


# sending dad jokes
@client.command()
async def dad_joke(ctx):
    await ctx.send(embed=functions.get_dad_joke())


# sending the weather info -> city is the argument that follows the command, it is possible to have multiple args
# example: $weather montreal ---> montreal is the argument, which will be stored in city
@client.command()
async def weather(ctx, city):
    try:
        await ctx.send(embed=functions.get_whether(city))
    except:
        await ctx.send("what the heck is that city???")


# sending a meme
@client.command()
async def meme(ctx):
    await ctx.send(embed=functions.get_meme())


# sending a cat picture
@client.command()
async def kitty(ctx):
    await ctx.send(embed=functions.get_kitty())


# sending a picture of a waifu
@client.command()
async def waifu(ctx):
    await ctx.send(embed=functions.get_waifu())


client.run("")