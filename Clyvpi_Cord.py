import os
import random

import discord

from dotenv import load_dotenv

from discord.ext import commands
import csv
import ValueStorage
import Clyvpi_DB


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(name='iot', help='~ Responds with a random quote relating to IoT')
async def iot(ctx):
    iot_quotes = [
        'Python is amazing',
        'I sure can\'t wait to do arduino',
        (
            'Get out of my head Get out of my head Get out of my head '
            'Get out of my head Get out of my head Get out of my head Get out of my head '
        ),
    ]

    response = random.choice(iot_quotes)
    await ctx.send(response)


@bot.command(name='bread', help='~ Responds with bread')
async def bread(ctx, number=1):
    message = ''
    for i in range(number):
        message += '🍞'
    await ctx.send(message)


@bot.command(name='forgor', help='~ 💀')
async def forgor(ctx, number=1):
    message = ''
    for i in range(number):
        message += '💀'
    await ctx.send(message)


@bot.command(name='rember', help='~ 😋')
async def forgor(ctx, number=1):
    message = ''
    for i in range(number):
        message += '😋'
    await ctx.send(message)


@bot.command(name='roll_dice', help='~ Simulates rolling dice.')
async def roll(ctx, number_of_dice=1, number_of_sides=6):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))


@bot.command(name='create-channel', help='Creates a new channel')
@commands.has_role('admin')
async def create_channel(ctx, channel_name='Test-Channel'):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        await ctx.send(f'Creating a new channel: {channel_name}')
        await guild.create_text_channel(channel_name)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')


@bot.command(name='status', help='~ Testing of the formatting with discord')
async def status(ctx):
    channel = bot.get_channel(896192318711955477)
    embed=discord.Embed(
    title="Pi4 Data (Click for Dashboard)",
        url="http://127.0.0.1:8050/",
        description="Data processed by the Pi",
        color=discord.Color.purple())
    embed.set_author(name="Clyvpi-Cord", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/1200px-Python-logo-notext.svg.png")
    #embed.set_author(name=ctx.author.display_name, url="https://twitter.com/RealDrewData", icon_url=ctx.author.avatar_url)
    embed.set_thumbnail(url="https://www.raspberrypi.org/app/uploads/2011/10/Raspi-PGB001.png")
    embed.add_field(name="__*ESP Data*__", value=f'''{ValueStorage.read_csv_MQTT()}''', inline=False)
    embed.add_field(name="__*LED*__", value=f'''{ValueStorage.read_from_csv_light()}''', inline=False)
    embed.add_field(name="__*Fan*__", value=f'''{ValueStorage.read_from_csv_fan()}''', inline=False)
    embed.add_field(name='__*Commands*__', value=f'''**Control LED** [`!light on/off`]\n**Control Fan** [`!fan on/off`]''', inline=False)
    await ctx.send("`(This is a test)` The temperature is too high do " + "`!fan on`" + " to turn on the fan")
    await ctx.send(embed=embed)
    await channel.send(embed=embed)


@bot.command(name='formatting', help='~ Testing')
async def formatting(ctx):
    channel = bot.get_channel(896192318711955477)
    print("Sending the temperature")
    send_string = ValueStorage.read_csv_MQTT()
    send_string += ValueStorage.read_from_csv_light()

    await channel.send(str(send_string))
    await ctx.send(str(send_string))


@bot.command(name='light', help='~ Testing')
async def light(ctx, state=""):
    if state.upper() == "ON":
        ValueStorage.write_to_csv_light("ON")
        print("Turning light on")
        await ctx.send("The light will be turned ON")
    elif state.upper() == "OFF":
        ValueStorage.write_to_csv_light("OFF")
        print("Turning light off")
        await ctx.send("The light will be turned OFF")
    else:
        print("Invalid Light Value")
        await ctx.send("Invalid value for light!")


@bot.command(name='fan', help='~ Testing')
async def fan(ctx, state=""):
    if state.upper() == "ON":
        ValueStorage.write_to_csv_fan("ON")
        print("Turning fan on")
        await ctx.send("The fan will be turned ON")
    elif state.upper() == "OFF":
        ValueStorage.write_to_csv_fan("OFF")
        print("Turning fan off")
        await ctx.send("The fan will be turned OFF")
    else:
        print("Invalid Fan Value")
        await ctx.send("Invalid value for fan!")

# Comment this event when not using the Voice Assistant
# @bot.event
# async def on_message(message):
#     if message.content == '!light on':
#         await light(message.channel, "ON")
#     if message.content == '!light off':
#         await light(message.channel, "OFF")

@bot.command(name='rfid', help='~ Testing')
async def rfid(ctx, value='1'):
    await ctx.send("testing rfid start...")
    print("Sending rfid " + str(value))
    Clyvpi_DB.rfidInstance(str(value))
    name = Clyvpi_DB.getUserByRfid(value)
    print(name[0])
    await ctx.send("testing rfid end...")
    await ctx.send("User " + " just swiped his ID")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound): # or discord.ext.commands.errors.CommandNotFound as you wrote
        await ctx.send("Unknown command")

bot.run(TOKEN)