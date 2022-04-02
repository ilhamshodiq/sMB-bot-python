import os
import discord
import asyncio
from keep_alive import keep_alive
from discord.ext import commands
import random
import datetime
import pytz
import youtube_dl
import pafy
import requests

#APInya weathermap
api_key = "f55290c77e1a327777c1a4ed66896ef9"#pake keymu sendiri lah..
base_url = "http://api.openweathermap.org/data/2.5/weather?"

#timezone wib
wib = pytz.timezone('Asia/Jakarta')
current_time = datetime.datetime.now(wib)

# client = discord.Client() # not used
commands = commands.Bot(command_prefix='')  #make command tapi gamake :v

f = open('pesan.txt', 'r')
file_contents = f.read()

f2 = open('commands.txt', 'r')
file_commands = f2.read()
f3 = open('commands2.txt', 'r')
file_commands2 = f3.read()


@commands.event
async def on_ready():
    await commands.change_presence(activity=discord.Game(name="ELDEN RING")
                                   )
    print('Masuk dengan {0.user}'.format(commands))

#command cuaca
@commands.command()
async def cuaca(ctx, *, city: str):
    city_name = city
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    x = response.json()
    channel = ctx.message.channel
    if x["cod"] != "404":
        async with channel.typing():
          y = x["main"]
          current_temperature = y["temp"]
          current_temperature_celsiuis = str(round(current_temperature - 273.15))
          current_pressure = y["pressure"]
          current_humidity = y["humidity"]
          z = x["weather"]
          weather_description = z[0]["description"]
          embed = discord.Embed(title=f"Cuaca di {city_name}",
                            color=ctx.guild.me.top_role.color,
                            timestamp=ctx.message.created_at,)
          embed.add_field(name="Deskripsi", value=f"**{weather_description}**", inline=False)
          embed.add_field(name="Temperatur(C)", value=f"**{current_temperature_celsiuis}°C**", inline=False)
          embed.add_field(name="Kelembapan(%)", value=f"**{current_humidity}%**", inline=False)
          embed.add_field(name="Tekanan Atmosfir(hPa)", value=f"**{current_pressure}hPa**", inline=False)
          embed.set_thumbnail(url="https://i.ibb.co/CMrsxdX/weather.png")
          embed.set_footer(text=f"Requested by {ctx.author.name}")
          await channel.send(embed=embed)
    else:
          await channel.send("City not found.")


@commands.command()
async def katakan(ctx, *, question):
    message = ctx.message
    await message.delete()

    await ctx.send(f"{question}")


@commands.command()
async def p(ctx):
    await ctx.send('{} ms'.format(round(commands.latency * 1000)))


#userinfo
@commands.command()
async def userinfo(ctx, member: discord.Member = None):
    await ctx.message.delete()
    if not member:
        member = ctx.message.author
    roles = ([role for role in member.roles[1:]])
    embed = discord.Embed(colour=discord.Colour.random(),
                          title=f"User Info - {member}")
    embed.set_thumbnail(url=member.avatar_url)

    embed.add_field(name="ID:", value=member.id)
    embed.add_field(name="User Name:", value=member.display_name)

    embed.add_field(
        name="Created Account On:",
        value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
    embed.add_field(
        name="Joined Server On:",
        value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC") +
        "\u0020")

    if roles == []:
        embed.add_field(name="Roles:", value="None")
        embed.add_field(name="Highest Role:", value="None")
        await ctx.send(embed=embed)

    else:
        embed.add_field(name="Roles:",
                        value=", ".join([role.mention for role in roles]))
        embed.add_field(name="Highest Role:", value=member.top_role.mention)
        await ctx.send(embed=embed)


#show avatar
@commands.command()
async def avatar(ctx, member: discord.Member):
    show_avatar = discord.Embed(color=discord.Color.dark_purple())
    show_avatar.set_image(url='{}'.format(member.avatar_url))
    await ctx.send(embed=show_avatar)


#download yt mp3
@commands.command()
async def download_mp3(ctx, *, link):
    await ctx.reply('Oke tak download sek..')
    data = link
    url = pafy.new(data)
    print(url.title)
    judul = f'{url.title}.mp3'
    hasil = url.getbestaudio()
    hasil.download(judul)
    await ctx.channel.send(file=discord.File(judul))
    os.remove(judul)


#alarm
@commands.command()
async def ingatkan(ctx, time, *, ingatkan):
    print(time)
    print(ingatkan)
    user = ctx.message.author
    embed = discord.Embed(color=discord.Color.dark_purple(),
                          timestamp=datetime.datetime.now())
    seconds = 0
    if ingatkan is None:
        embed.add_field(
            name='Warning',
            value='Mau minta ingatkan apa bro? yang bener nulisnya.'
        )  # Error message
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
        await ctx.reply(
            f"Ninu ninu!!🔔 tadi {counter} yang lalu, kamu minta ingetin '{ingatkan}'"
        )
        return
    await ctx.send(embed=embed)


#pake event
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

    if pesankeciltanpaspasi.startswith('goodnight'):
        await message.channel.send(file_contents)

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

    if pesankecil.startswith('dor'):
        await message.channel.send('kaget wooyy')

    if pesankecil.startswith('😳'):
        await message.reply('😳👉👈')

    if pesankecil.startswith('-20'):
        await message.reply(
            'https://cdn.discordapp.com/attachments/624472802208251946/916660131268288543/-20.png'
        )

    if pesankecil.startswith('jam berapa sekarang?'):
        embed = discord.Embed(color=discord.Color.dark_purple(),
                              timestamp=datetime.utcnow())
        embed.add_field(name='🕓', value='Jam 👇')
        await message.channel.send(embed=embed)

    #greet in time
    if pesankeciltanpaspasi.startswith('selamatsiang'):
        jamsekarang = current_time.hour
        pesan = ''
        if jamsekarang >= 11 and jamsekarang < 17:
            pesan = 'Siang 🌞'
        elif jamsekarang >= 17 or jamsekarang < 3:
            pesan = 'Udah malem wooyy'
        elif jamsekarang >= 3 and jamsekarang < 11:
            pesan = 'Masih pagi heh'
        await message.channel.send(pesan)
    if pesankeciltanpaspasi.startswith('selamatmalam'):
        jamsekarang = current_time.hour
        pesan = ''
        if jamsekarang >= 11 and jamsekarang < 17:
            pesan = 'Masih siang wooyyy 🌞'
        elif jamsekarang >= 17 or jamsekarang < 3:
            pesan = 'Malemmmm 😴'
        elif jamsekarang >= 3 and jamsekarang < 11:
            pesan = 'Masih pagi heh'
        await message.channel.send(pesan)

    if pesankeciltanpaspasi.startswith('selamatpagi'):
        jamsekarang = current_time.hour
        pesan = ''
        if jamsekarang >= 11 and jamsekarang < 17:
            pesan = 'udah siang wooyyy 🌞'
        elif jamsekarang >= 17 or jamsekarang < 3:
            pesan = 'malem sek'
        elif jamsekarang >= 3 and jamsekarang < 11:
            pesan = 'Pagi............ udah sarapan?'
        await message.channel.send(pesan)
    #############################

    #googlekan
    if pesankecil.startswith('tolong googlekan'):
        masukan = pesankecil
        masukan = masukan.replace('tolong googlekan ', '').replace(' ', '+')
        await message.reply('https://letmegooglethat.com/?q={}'.format(masukan)
                            )

    if pesankecil.startswith('--help'):
        embed = discord.Embed(color=discord.Color.dark_purple())
        embed.add_field(name='**~DAFTAR COMMANDS~**', value=file_commands)
        embed.add_field(name='============', value=file_commands2)
        embed.set_footer(icon_url=commands.user.avatar_url, text='commands')
        await message.channel.send(embed=embed)

    await commands.process_commands(message)


keep_alive()
my_secret = os.environ['TOKEN']
commands.run(my_secret)
