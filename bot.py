from email import message
import discord
import command_functions as functions
from discord.ext import commands
import os 
import youtube_dl
from random import randrange

# events are found here: https://discordpy.readthedocs.io/en/stable/api.html#event-reference

client = commands.Bot(command_prefix='$')
# remove the default help command 
client.remove_command('help')


@client.event
async def on_ready():
    print("logged in as {0.user}".format(client))


# @client.event
# async def on_message(message):
#     # if the bot sent the message, then return directly to avoid bot answering to itself all the time
#     if message.author == client.user:
#         return
#     if message.content == 'hello':
#         await message.channel.send('hello')
    
#     # have the bot react to certain messages
#     if message.content == 'hi':
#         await message.add_reaction("\U0001F601")
    
#     await client.process_commands(message)

# # have the bot to do something when someone reacted 
# @client.event
# async def on_reaction_add(reaction, user):
#     await reaction.message.channel.send(str(user) + " reacted with " + reaction.emoji)

# # have the bot do something when a message is edited
# @client.event
# async def on_message_edit(before, after):
#     await before.channel.send(str(before.author) + " editted a message\n " + "Before: " + before.content + "\nAfter: " + after.content)

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


# let the bot join the voice channel I am currently in
@client.command()
async def join(ctx):
    # return the voice channel that the command issuer is currently in 
    channel = ctx.author.voice.channel        
    # connect the bot to the voice channel
    await channel.connect()


# disconnect the bot from the channel
@client.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()


# command to download a song 
@client.command()
# making sure the url is a string
async def download(ctx, url : str, song_name=''):
    
    await ctx.send("url is " + url + " song name will be " + song_name + "\n Now Downloading...")
    functions.download_yt(url, song_name)
    await ctx.send("Download Completed!")

# command that plays a song
@client.command()
async def music(ctx, song):
    voice_client = ctx.voice_client
    voice_client.play(discord.FFmpegPCMAudio("song/" + song + ".mp3"))
    ctx.send("Now playing: " + song)

# play a random song 
@client.command()
async def music_r(ctx):
    song_list = os.listdir('song/')
    voice_client = ctx.voice_client
    if voice_client.is_playing():
        voice_client.pause()

    index = randrange(len(song_list))
    voice_client.play(discord.FFmpegPCMAudio("song/" + song_list[index]))


# command to pause the song
@client.command()
async def pause(ctx):
    voice_client = ctx.voice_client
    if voice_client.is_playing():
        voice_client.pause()
    else:
        ctx.send("there is nothing playing")


# command to list all songs
@client.command()
async def song_list(ctx):
    await ctx.send(embed=functions.get_song_list())


# command to rename a song
@client.command()
async def rename(ctx, old, new):
    os.rename("song/" + old + ".mp3", "song/" + new + ".mp3")




###########################
#                         #
#  ERROR HANDLERS         #
#                         #
###########################

# handle the case where user uses $join when the user isn't in a voice channel
# the exeception returned is commands.CommandInvokeError
@join.error
async def join_error(ctx, error):
    if isinstance(error, commands.errors.CommandInvokeError):
        await ctx.send("you must be in a voice channel to use this command")

@leave.error
async def leave_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandInvokeError):
        await ctx.send("how can I leave the voice channel when I am not even there??")

@download.error
async def download_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandInvokeError):
        await ctx.send("error, maybe make sure you provided a good url?")

@music.error
async def music_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send("give me a song's name at least, I can't read your mind.")
    if isinstance(error, discord.ext.commands.errors.CommandInvokeError):
        await ctx.send("go to voice channel first, then summon me to the voice channel using $join and select type in a song name that exists, use $song_list to check")
    
@music.error
async def music_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandInvokeError):
        await ctx.send("go to voice channel first, then summon me to the voice channel using $join")




client.run("")