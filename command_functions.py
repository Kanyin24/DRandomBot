from email import message
import discord
import requests
import os 
import youtube_dl

def test_function():
    embed_quote = discord.Embed(color=0x00ff00)
    embed_quote.add_field(name="test", value="test_string", inline=False)
    return embed_quote


# getting a random dad joke from https://icanhazdadjoke.com/
def get_dad_joke():
    url = "https://icanhazdadjoke.com/"
    response = requests.get(url, headers={"Accept": "application/json"}).json()
    joke = response["joke"]
    embedVal = discord.Embed(color=0x00ff00)
    embedVal.add_field(name="dad joke", value=joke, inline=False)
    return embedVal


# getting from https://waifu.pics/docs
def get_waifu():
    url = "https://api.waifu.pics/sfw/waifu"
    response = requests.get(url).json()
    image = response["url"]
    embed_waifu = discord.Embed(title="waifu", color=0x00ff00)
    embed_waifu.set_image(url=image)
    return embed_waifu


def get_kitty():
    url = "https://api.thecatapi.com/v1/images/search"
    response = requests.get(url).json()
    cat_url = response[0]["url"]
    embed_cat = discord.Embed(title="kitty cat", color=0x00ff00)
    embed_cat.set_image(url=cat_url)
    return embed_cat


# getting meme using a meme API, https://github.com/D3vd/Meme_Api
def get_meme():
    url = "https://meme-api.herokuapp.com/gimme"
    response = requests.get(url).json()
    response_url = response['url']
    print(response_url)
    embed_meme = discord.Embed(title="meme", color=0x00ff00)
    embed_meme.set_image(url=response_url)
    return embed_meme


# getting weather info from openweathermap API
def get_whether(city_name):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid=f2f245b1ba7153ca1ecd2e6ff52a563a"
    response = requests.get(url).json()
    weather = f"city: {response['name']}\ntemperature: {round(response['main']['temp'] - 273.15)} C\nfeels like: " \
              f"{round(response['main']['feels_like'] - 273.15)} C\nmax temperature: {round(response['main']['temp_max'] - 273.15)} C" \
              f"\nmin temperature: {round(response['main']['temp_min'] - 273.15)} C\npressure: {response['main']['pressure']}" \
              f"hPa\nhumidity: {response['main']['humidity']} %\nweather: {response['weather'][0]['main']}\n" \
              f"condition: {response['weather'][0]['description']}"
    embed_val = discord.Embed(color=0x00ff00)
    embed_val.add_field(name='Weather', value=weather, inline=False)
    return embed_val

# preparing an embed for help menu
def get_help():
    embed = discord.Embed(
        title="Help Menu",
        description="All commands and their descriptions",
        color=discord.Color.blurple()
    )
    embed.set_thumbnail(url="https://c.tenor.com/cs3SeyyeR_cAAAAC/spy-x-family-anya-forger.gif")
    embed.add_field(name="$help", value="Display the help menu", inline=False)
    embed.add_field(name="$dad_joke", value="Get a random dad joke", inline=False)
    embed.add_field(name="$waifu", value="Get a random waifu picture", inline=False)
    embed.add_field(name="$kitty", value="Get a random kitty cat picture", inline=False)
    embed.add_field(name="$weather <city>", value="Get weather of a city; replace 'city' by city's name", inline=False)
    embed.add_field(name="$meme", value="Get a random meme", inline=False)
    embed.add_field(name="$join", value="Have the bot join the voice channel that the user is current in", inline=False)
    embed.add_field(name="$leave", value="The bot will leave the voice channel", inline=False)
    embed.add_field(name="$download <url> <song_name>", value="The bot will download the youtube song as .mp3 and save it as 'song_name.mp3'; if no <song_name> specified, the file's original name will be used", inline=False)
    embed.add_field(name="$music <song_name>", value="The bot will play the selected song in voice channel", inline=False)
    embed.add_field(name="$music_r", value="The bot will play a random song, use this command again to play another song", inline=False)      
    embed.add_field(name="$song_list", value="The bot will display a list of songs downloaded", inline=False)
    embed.add_field(name="$pause", value="The bot will pause current song", inline=False)
    embed.add_field(name="$tictactoe <player1> <player2>", value="Start TicTacToe game, replace <player> by @discord_username", inline=False)
    embed.add_field(name="$mark <position>" , value="Place a mark on the board, position = integer ranging from 1 to 9", inline=False)
    embed.add_field(name="$quit", value="Quit the current TicTacToe game", inline=False)
    embed.add_field(name="$pokemon <name>", value="Find information about the pokemon", inline=False)


    return embed

# get a list of all songs
def get_song_list():
    list = os.listdir("song/")
    embed = discord.Embed(
        title="Song List",
        color=discord.Color.blurple()
    )

    counter = 1

    for song in list:
        embed.add_field(name=str(counter) + '. ', value=song[:-4], inline=False)
        counter += 1
    return embed

# download the song using youtube_dl
def download_yt(url, song_name=''):
    song = song_name
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }]
    }
    # file will be downloaded in the root directory
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                if song_name:
                    os.rename(file, song_name + ".mp3")
                else:
                    song_name = file
                    song = file.replace(" ", "-")
                    print(song)
    # move the newly downloaded song to the desired directory
    if ".mp3" in song:
        os.replace(song_name, "song/" + song)   
    else:
        os.replace(song_name + ".mp3", "song/" + song_name + ".mp3")    

# check win condition for TicTacToe
def check_win(board):

    # checking rows
    if board[0] == board[1] == board[2] == ":regional_indicator_o:" or board[0] == board[1] == board[2] == ":regional_indicator_x:":
        return True
    if board[3] == board[4] == board[5] == ":regional_indicator_o:" or board[3] == board[4] == board[5] == ":regional_indicator_x:":
        return True
    if board[6] == board[7] == board[8] == ":regional_indicator_o:" or board[6] == board[7] == board[8] == ":regional_indicator_x:":
        return True
    
    #checking columns
    if board[0] == board[3] == board[6] == ":regional_indicator_o:" or board[0] == board[3] == board[6] == ":regional_indicator_x:":
        return True
    if board[1] == board[4] == board[7] == ":regional_indicator_o:" or board[1] == board[4] == board[7] == ":regional_indicator_x:":
        return True
    if board[2] == board[5] == board[8] == ":regional_indicator_o:" or board[2] == board[5] == board[8] == ":regional_indicator_o:":
        return True

    #diagnal
    if board[0] == board[4] == board[8] == ":regional_indicator_o:" or board[0] == board[4] == board[8] == ":regional_indicator_x:":
        return True
    if board[2] == board[4] == board[6] == ":regional_indicator_o:" or board[2] == board[4] == board[6] == ":regional_indicator_x:":
        return True
    
    return False
        