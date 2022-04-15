from email import message
from turtle import color
import discord
import requests
import io
import aiohttp
import random
from discord.ext import commands

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
        description="All commands listed below",
        color=discord.Color.blurple()
    )
    embed.set_thumbnail(url="https://static.wikia.nocookie.net/gochiusa/images/4/4a/1.png/revision/latest?cb=20200108140610")
    embed.add_field(name="$help", value="Display the help menu", inline=False)
    embed.add_field(name="$dad_joke", value="Get a random dad joke", inline=False)
    embed.add_field(name="$waifu", value="Get a random waifu picture", inline=False)
    embed.add_field(name="$kitty", value="Get a random kitty cat picture", inline=False)
    embed.add_field(name="$weather 'city'", value="Get weather of a city; replace 'city' by city's name", inline=False)
    embed.add_field(name="$meme", value="Get a random meme", inline=False)


    return embed