#########################################################################
#   File:        bot.py
#
#   Description: This file contains the definition of all commands 
#                as well as error handlers
# 
#   Run the bot: A token must be passed to the client.run() function 
#                at the bottom of this file. 
#                Then run python bot.py and the bot should be running.
#
#
#   MAKE SURE TO REMOVE THE TOKEN WHEN PUSHING THE CODE! OTHERWISE 
#   DISCORD WILL THINK THAT THE TOKEN IS COMPROMISED, SO A NEW ONE 
#   MUST BE GENERATED
#
#########################################################################



from email import message
import discord
from discord.ext import commands
import os 
import random
from datetime import datetime
import pymongo
import discord
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio


# file imports
import command_functions as functions
import pokedex 
import ai_chatbot as chatbot


# events are found here: https://discordpy.readthedocs.io/en/stable/api.html#event-reference
intents = discord.Intents.default()  # Create an instance of the default intents
# intents.typing = False  # Disable typing events to reduce unnecessary data
# intents.presences = False  # Disable presence updates to reduce unnecessary data
intents.message_content = True
client = commands.Bot(command_prefix='$', intents=intents)
# remove the default help command 
client.remove_command('help')

my_client = pymongo.MongoClient("")
mydb = my_client["discorddb"]

mycollection = mydb["userbirthdays"]


async def check_if_birthday():
    channel = client.get_channel(1124105493225414664)

    #while True:
    today = datetime.today()
    todaydate = today.strftime("%d/%m/%Y")

    query = {
        'day': today.day,
        'month': today.month
    }

    result = mycollection.count_documents(query)
    cursor = mycollection.find(query)
    

    if result != 0:
        if result == 1:
            reply = f"Happy Birthday <@{cursor[0]['user_id']}>!\nHope you have an amazing day 🥳"
            embedVal = discord.Embed(color=0x00ff00)
            embedVal.add_field(name="Birthday", value=reply, inline=False)
            await channel.send(embed=embedVal)
        else:
            for document in cursor:
                reply = f"Happy Birthday <@{document['user_id']}>!\nHope you have an amazing day 🥳"
                embedVal = discord.Embed(color=0x00ff00)
                embedVal.add_field(name="Birthday", value=reply, inline=False)
                await channel.send(embed=embedVal)
        

# game state variables for TicTacToe
player1 = ""
player2 = ""
turn = ""
game_over = True
board = []

# async def send_message():
#     channel_id = 1123713406743105689
#     channel = client.get_channel(channel_id)
#     await channel.send("test")

@client.event
async def on_ready():
    print("logged in as {0.user}".format(client))
    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_if_birthday, 'interval', minutes=1440)  # Schedule at 12 AM (midnight)
    scheduler.start()

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


#################################
#                               #
#   Command lists begin here    #
#                               #
#################################

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
    if ctx.author.voice and ctx.author.voice.channel:
        channel = ctx.author.voice.channel
        if not ctx.voice_client:
            await channel.connect()
        else:
            await ctx.voice_client.move_to(channel)


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

    index = random.randrange(len(song_list))
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

#command to add birthdays
@client.command()
async def add_birthday(ctx, dateString):
    format = "%d/%m/%Y"
    birth_date = datetime.strptime(dateString, format)
    user_id = ctx.author.id
    username = ctx.author.name

    #data being stored: user_id, username and birth date
    birthday_data = {
        'user_id': user_id,
        'username': username,
        'birth_date': birth_date,
        'day': birth_date.day,
        'month': birth_date.month
    }

    #creating mongodb db and storing data
    x = mycollection.insert_one(birthday_data)

    response = "Your birthday is on: " + dateString
    embedVal = discord.Embed(color=0x00ff00)
    embedVal.add_field(name="Birthday Added", value=response, inline=False)
    await ctx.send(embed = embedVal)

    #Note: add error exception handling



############################
#                          #
# AI chatbot commands      #
#                          #
############################

@client.command()
async def ai_chat(ctx):
    response_str = ""
    print("talk to the bot type quit to stop")
    while True:
        inp = await client.wait_for('message')
        if inp.content.lower() == "quit":
            await ctx.send("quitting")
            break
        results = chatbot.model.predict([chatbot.bag_of_words(inp.content,chatbot.words)])
        result_index = chatbot.np.argmax(results)
        tag = chatbot.labels[result_index]
        for tg in chatbot.data["intents"]:
            if tg["tag"] == tag:
                respones = tg["responses"]
        response_str += random.choice(respones)
        await ctx.send(random.choice(respones))

#############################
#                           #
# TicTacToe Commands Here   # 
#                           #
#############################

# command to quit a the game 
@client.command()
async def quit(ctx):
    global game_over
    game_over = True
    await ctx.send("quitted the game")


@client.command()
async def tictactoe(ctx, p1 : discord.Member, p2 : discord.Member):
    global player1
    global player2
    global turn
    global game_over

    # draw the board if there is no game in progress
    if game_over:
        global board
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                ":white_large_square:", ":white_large_square:", ":white_large_square:",
                ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        turn = ""
        # game starts after the board is created, hence setting game_over to false
        game_over = False
        player1 = p1
        player2 = p2

        # three lines in total as shown in board above
        line = ""

        # printing the board on discord
        for x in range(len(board)):
            # send a new line every three white squares
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]
        
        # determine who goes first 
        num = random.randint(1, 2)
        if num == 1:
            turn = player1
            await ctx.send("<@" + str(player1.id) + ">'s turn")
            return 
        else:
            turn = player2
            await ctx.send("<@" + str(player2.id) + ">'s turn")
            return
    else:
        await ctx.send("No new game when a game is in progress!!")
        return


@client.command()
async def mark(ctx, position: int):
    global board
    global player1
    global player2
    global turn
    global count 
    global game_over
    line = ""
    mark = ""

    if not game_over:
        # make sure to only take correct player's command 
        if turn == ctx.author:
            # player1 will have an 'x' mark and player2 will have 'o' mark
            if turn == player1:
                # make sure the position entered by user is between 1 to 9 and selected position is not marked
                if 0 < position < 10 and board[position - 1] == ":white_large_square:":
                    mark = ":regional_indicator_x:"
                    board[position - 1] = mark
                    turn = player2

                    # print the updated board
                    for x in range(len(board)):
                        if x == 2 or x == 5 or x == 8:
                            line += " " + board[x]
                            await ctx.send(line)
                            line = ""
                        else:
                            line += " " + board[x]
                    
                    if functions.check_win(board):
                        game_over = True
                        await ctx.send("<@" + str(player1.id) + "> win!")
                        return 

                    await ctx.send("<@" + str(player2.id) + ">'s turn")
                    return 
                else: 
                    await ctx.send("<@" + str(ctx.author.id) + ">you cannot place a mark here") 
            
            # check if it is player2's turn
            if turn == player2:
                if 0 < position < 10 and board[position - 1] == ":white_large_square:":
                    mark = ":regional_indicator_o:"
                    board[position - 1] = mark
                    turn = player1

                    for x in range(len(board)):
                        if x == 2 or x == 5 or x == 8:
                            line += " " + board[x]
                            await ctx.send(line)
                            line = ""
                        else:
                            line += " " + board[x]
                    
                    if functions.check_win(board):
                        game_over = True
                        await ctx.send("<@" + str(player2.id) + "> win!")
                        return
                    
                    await ctx.send("<@" + str(player1.id) + ">'s turn")
                    return
                else: 
                    await ctx.send("<@" + str(ctx.author.id) + ">you cannot place a mark here")
        else:
            await ctx.send("<@" + str(ctx.author.id) + "> it's not your turn!")
    else:
        await ctx.send("no game in progress, start a game to use this command")


###########################
#                         #
#  Pokedex Commands       #
#                         #
###########################

@client.command()
async def pokemon(ctx, poke_name : str):
    await ctx.send(embed=pokedex.pokemon_basic_info(poke_name))

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

@tictactoe.error
async def tictactoe_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandInvokeError):
        await ctx.send("error, try the command again")
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send("make sure to @ both players")

@mark.error
async def mark_error(ctx, error):
    if isinstance(error, error, discord.ext.commands.errors.CommandInvokeError):
        await ctx.send("enter a position, from 1 to 9")

# @pokemon.error
# async def pokemon_error(ctx, error):
#     if isinstance(error, discord.ext.commands.errors.CommandInvokeError):
#         await ctx.send("this pokemon doesn't exist")
#     if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
#         await ctx.send("enter a pokemon name")

client.run("")