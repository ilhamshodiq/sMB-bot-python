import os
import discord
import asyncio
from keep_alive import keep_alive
from discord.ext import commands
import random
import datetime
from datetime import datetime

# client = discord.Client() # not used
commands = commands.Bot(command_prefix='')#make command, tapi gamake :v


@commands.event
async def on_ready():
    print('Masuk dengan {0.user}'.format(commands))

@commands.command()
async def katakan(ctx, *, question):
    message = ctx.message
    await message.delete()
    await ctx.send(f"{question}") #need a fix

@commands.command()
async def p(ctx):
    await ctx.send('{} ms'.format(round(commands.latency * 1000)))


@commands.command()
async def avatar(ctx, member: discord.Member):
    show_avatar = discord.Embed(color=discord.Color.dark_purple())
    show_avatar.set_image(url='{}'.format(member.avatar_url))
    await ctx.send(embed=show_avatar)

@commands.command()
async def ingatkan(ctx, time, *, ingatkan):
    print(time)
    print(ingatkan)
    user = ctx.message.author
    embed = discord.Embed(color=discord.Color.dark_purple(), timestamp=datetime.utcnow())
    seconds = 0
    if ingatkan is None:
        embed.add_field(name='Warning', value='Mau minta ingatkan apa bro? yang bener nulisnya.') # Error message
    if time.lower().endswith("hari"):
        seconds += int(time[:-4]) * 60 * 60 * 24
        counter = f"{seconds // 60 // 60 // 24} hari"
    if time.lower().endswith("jam"):
        seconds += int(time[:-3]) * 60 * 60
        counter = f"{seconds // 60 // 60} jam"
    elif time.lower().endswith("menit"):
        seconds += int(time[:-5]) * 60
        counter = f"{seconds // 60} menit"
    elif time.lower().endswith("detik"):
        seconds += int(time[:-5])
        counter = f"{seconds} detik"
    if seconds == 0:
        embed.add_field(name='Warning',
                        value='tulis yang bener dong waktunya.')

    else:
        await ctx.send(f"Okeee, ntar aku ingetin {ingatkan}, {counter} lagi.")
        await asyncio.sleep(seconds)
        await ctx.reply(f"Ninu ninu!!🔔 tadi {counter} yang lalu, kamu minta ingetin '{ingatkan}'")
        return
    await ctx.send(embed=embed)

@commands.event
async def on_message(message):
    #input dijadiin lower & hilangin spasi
    pesankeciltanpaspasi = message.content.lower().replace(' ', '')
    pesankecil = message.content.lower()

    if message.author == commands.user:
        return

    if pesankeciltanpaspasi.startswith('halo'):
        await message.channel.send('Hallo! :)')

    if message.content.startswith('konnichiwa'):
        await message.channel.send('hilih wibu')

    if message.content.startswith('uwu'):
        await message.channel.send('UwU wiwu')

    if message.content.startswith('apa kabar'):
        await message.channel.send('Alhamdulillah sehat')

    if pesankecil.startswith('pilih'):
        pilihan = pesankecil
        pilihan = pilihan.replace('pilih', '').replace('atau', '')
        pilihan = pilihan.split()
        acakpilihan = random.choice(pilihan)
        await message.channel.send(acakpilihan.title())

    if pesankecil.startswith('tag aku'):
        await message.reply('oke')

    if pesankecil.startswith('terima kasih'):
        await message.reply('sama-sama 😄')

    if pesankecil.startswith('makasih'):
        await message.reply('sama-sama 😄')

    if pesankecil.startswith('door'):
        await message.channel.send('kaget wooyy')

    if pesankecil.startswith('jam berapa sekarang?'):
        embed = discord.Embed(color=discord.Color.dark_purple(), timestamp=datetime.utcnow())
        embed.add_field(name='🕓' ,value='Jam 👇')
        await message.channel.send(embed=embed)
    
    await commands.process_commands(message)


keep_alive()
my_secret = os.environ['TOKEN']#Token bisa di taruh di file json
commands.run(my_secret)
