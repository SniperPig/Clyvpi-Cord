import os
import random

import discord

from dotenv import load_dotenv

from discord.ext import commands
import csv



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

@bot.command(name='temp', help='~ Responds with bread')
async def temp(ctx, number=21):
    response = 'Temperature is set to ' + str(number)
    await ctx.send(response)


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

@bot.command(name='formatting', help='~ Testing of the formatting with discord')
async def formatting(ctx):
    embed=discord.Embed(
    title="Pi4 Data (Click for Dashboard)",
        url="",
        description="Data processed by the Pi",
        color=discord.Color.orange())
    embed.set_author(name="Clyvpi-Cord", url="https://discord.gg/fjcydncUkb", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/1200px-Python-logo-notext.svg.png")
    #embed.set_author(name=ctx.author.display_name, url="https://twitter.com/RealDrewData", icon_url=ctx.author.avatar_url)
    embed.set_thumbnail(url="https://www.raspberrypi.org/app/uploads/2011/10/Raspi-PGB001.png")
    embed.add_field(name="*Temperature*", value=f'''**Current Temperature:** 25(C)
    **Current Humidity:** 50%
    **Average Temperature Today:** 20(C)''', inline=False)
    embed.add_field(name="Test", value=f'''**LED ON**''', inline=False)
    embed.add_field(name="__Underline__", value="Surround your text in double underscores (\_\_)", inline=False)
    embed.add_field(name="~~Strikethrough~~", value="Surround your text in double tildes (\~\~)", inline=False)
    embed.add_field(name="`Code Chunks`", value="Surround your text in backticks (\`)", inline=False)
    embed.add_field(name="Blockquotes", value="> Start your text with a greater than symbol (\>)", inline=False)
    embed.add_field(name="Secrets", value="||Surround your text with double pipes (\|\|)||", inline=False)
    embed.set_footer(text="This is an automatically updated message!")
    await ctx.send(embed=embed)

def read_csv():
    final_string = ""
    with open('MQTT_file.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            print(
                f'\t{row["Parameter"]} has value {row["Value"]}')
            final_string += f'\t{row["Parameter"]} has value {row["Value"]}'
            line_count += 1
        print(f'Processed {line_count} lines.')
        return final_string

@bot.command(name='showtemp', help='~ Testing')
async def showtemp(ctx):
    channel = bot.get_channel(896192318711955477)
    print("Sending the temperature")
    send_string = read_csv()

    await channel.send(str(send_string))
    await ctx.send(str(send_string))

bot.run(TOKEN)