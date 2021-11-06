import os
import random

import discord

from dotenv import load_dotenv

from discord.ext import commands




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

@bot.command(name='allstar', help='~ Responds with Allstar')
async def bread(ctx, number=1):
    await ctx.send('''
    Smash Mouth - All Star
    
Somebody once told me the world is gonna roll me
I ain't the sharpest tool in the shed
She was looking kind of dumb with her finger and her thumb
In the shape of an "L" on her forehead

Well the years start coming and they don't stop coming
Fed to the rules and I hit the ground running
Didn't make sense not to live for fun
Your brain gets smart but your head gets dumb

So much to do, so much to see
So what's wrong with taking the back streets?
You'll never know if you don't go
You'll never shine if you don't glow

Hey now, you're an all-star, get your game on, go play
Hey now, you're a rock star, get the show on, get paid
And all that glitters is gold
Only shooting stars break the mold

It's a cool place and they say it gets colder
You're bundled up now, wait 'til you get older
But the meteor men beg to differ
Judging by the hole in the satellite picture

The ice we skate is getting pretty thin
The water's getting warm so you might as well swim
My world's on fire, how about yours?
That's the way I like it and I'll never get bored

    ''')
    await ctx.send('''
    Hey now, you're an all-star, get your game on, go play
Hey now, you're a rock star, get the show on, get paid
All that glitters is gold
Only shooting stars break the mold

Hey now, you're an all-star, get your game on, go play
Hey now, you're a rock star, get the show, on get paid
And all that glitters is gold
Only shooting stars

Somebody once asked could I spare some change for gas?
I need to get myself away from this place
I said, "Yup" what a concept
I could use a little fuel myself

And we could all use a little change
Well, the years start coming and they don't stop coming
Fed to the rules and I hit the ground running
Didn't make sense not to live for fun

Your brain gets smart but your head gets dumb
So much to do, so much to see
So what's wrong with taking the back streets?
You'll never know if you don't go (go!)

You'll never shine if you don't glow
Hey now, you're an all-star, get your game on, go play
Hey now, you're a rock star, get the show on, get paid
And all that glitters is gold

Only shooting stars break the mold
And all that glitters is gold
Only shooting stars break the mold
    ''')

bot.run(TOKEN)