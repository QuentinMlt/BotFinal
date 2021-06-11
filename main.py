import discord
import json
import requests
import youtube_dl
from discord.ext import commands
import os
from asyncio.windows_events import NULL
from discord import message
from discord.user import User
import sqlite3
import random
from bs4 import BeautifulSoup


###########################################

#Connexion
connexion = sqlite3.connect('basededonnees.db')

# Récupération d'un curseur
curseur = connexion.cursor()

# Création de la table scores
curseur.execute("""
    CREATE TABLE IF NOT EXISTS userTeamHeros (
    user_id INTEGER NOT NULL,
    name_hero TEXT,
    img TEXT,
    intelligence INTEGER,
    strength INTEGER,
    speed INTEGER,
    durability INTEGER,
    power INTEGER,
    combat INTEGER,
    id INTEGER NOT NULL
    )
    """)

bot = commands.Bot(command_prefix="?", description="Lyrify le BG")

@bot.event
async def on_ready():
    print("Prêt à partir Chef !")



@bot.command()
async def l(ctx, *request):
    request = " ".join(request)
    url = f"https://some-random-api.ml/lyrics?title={request}"
    response = requests.get(url)
    data = response.text
    parsed = json.loads(data)  # API stuff.
    titre = parsed["title"]
    image = parsed["thumbnail"]
    image = image["genius"]
    song = parsed["lyrics"]
    artist = parsed["author"]  # Making variables to make life easier later (F strings)


    form1 = discord.Embed(title=titre, description=artist, colour=discord.Colour.orange())
    form1.set_thumbnail(url=image)
    form1.set_footer(text=song[0:1900])
    form2 = discord.Embed(title="", description="", colour=discord.Colour.orange())
    form2.set_footer(text=song[1900:3900])
    form3 = discord.Embed(title="", description="", colour=discord.Colour.orange())
    form3.set_footer(text=song[3900:5900])
    form4 = discord.Embed(title="", description="", colour=discord.Colour.orange())
    form4.set_footer(text=song[5900:])
    await ctx.send(embed=form1)
    await ctx.send(embed=form2)
    await ctx.send(embed=form3)
    await ctx.send(embed=form4)



@bot.command()
async def play(ctx, url : str):
    print("je suis la")
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("attends que la musique se finisse ou kick moi")
        return

    channel = ctx.author.voice.channel
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name=channel.name)
    await voiceChannel.connect()
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))



@bot.command()
async def leave(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_connected():
       voiceChannel = await voice.disconnect()
       """
    else:
        await ctx.send("**Je suis deja pas la idiot !! **")
        """






@bot.command()
async def coucou(ctx):
    print("coucou")
    await ctx.send("Coucou")


@bot.command()
async def parle(ctx):
    print("Qu'il était présent pour vous écouter")
    await ctx.send("Qu'il était présent pour vous écouter", tts=True)  # pour parle avec le tts
    # await ctx.send("Qu'il était présent pour vous écouter")


@bot.command()
async def bonjour(ctx):
    print("bonjour")
    await ctx.send("Salut, je suis T'Choupi le GOAT de tous les autres bots sur ce serveur ! :D")


@bot.command()
async def serverInfo(ctx):
    server = ctx.guild
    numberOfTextChannels = len(server.text_channels)
    numberOfVoiceChannels = len(server.voice_channels)
    serverDescription = server.description
    numberOfPerson = server.member_count
    serverName = server.name
    message = f"Le serveur **{serverName}** contient {numberOfPerson} personnes. \n La description du serveur : {serverDescription}. \n Ce serveur possède {numberOfTextChannels} & {numberOfVoiceChannels} salons écrit et vocaux"
    await ctx.send(message)


@bot.command()
async def say(ctx, *texte):
    text = texte
    messages = await ctx.channel.history(limit=1).flatten()
    for message in messages:
        await message.delete()
    await ctx.send(" ".join(text))  # met un espace entre chaque element de la liste


@bot.command()
async def stylesay(ctx, *texte):
    stylechar = "𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭"
    styleText = []
    for word in texte:
        word = word.lower()
        for char in word:
            if char.isalpha():
                index = ord(char) - ord("a")
                transformed = stylechar[index]
                styleText.append(transformed)
            else:
                styleText.append(char)
        styleText.append(" ")
    messages = await ctx.channel.history(limit=1).flatten()
    for message in messages:
        await message.delete()
    await ctx.send("".join(styleText))


@bot.command()
async def clear(ctx, nombre: int):
    messages = await ctx.channel.history(limit=nombre + 1).flatten()
    for message in messages:
        await message.delete()
    await ctx.send("```LE CHAT A ÉTÉ CLEAR```")


@bot.command()
async def kick(ctx, user: discord.User, *reason):
    reason = " ".join(reason)
    await ctx.guild.kick(user, reason=reason)
    await ctx.send(f"```J'ai kick {user}, ce grand fou.```")


@bot.command()
async def ban(ctx, user: discord.User, *reason):
    reason = " ".join(reason)
    embed = discord.Embed(title="**Banissement**", description="DEHOOOORS !", colour=discord.Colour.orange())
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    embed.set_thumbnail(url="https://media.giphy.com/media/vrHLuzCYQPzzuhyogX/giphy.gif")
    embed.add_field(name="Membre banni", value=user.name, inline=True)
    embed.add_field(name="Raison", value=reason, inline=True)
    embed.add_field(name="Modérateur", value=ctx.author.name, inline=True)
    embed.add_field(name="Bot", value="Moi aussi je l'aimais pas de toute façon", inline=False)
    await ctx.send(embed=embed)
    await ctx.guild.ban(user, reason=reason)


@bot.command()
async def banInfo(ctx):
    bannedName = []
    bannedUsers = await ctx.guild.bans()

    await ctx.send(f"```Voila toutes les personnes bannis du serveur {ctx.guild.name} : ```")
    for i in bannedUsers:
        bannedName.append(str(i.user.name))
    pseudo = "\n".join(bannedName)
    await ctx.send(f"**{pseudo}**")


@bot.command()
async def unban(ctx, user, *reason):
    reason = " ".join(reason)
    userName, userId = user.split("#")
    bannedUsers = await ctx.guild.bans()
    for i in bannedUsers:
        if i.user.name == userName and i.user.discriminator == userId:
            await ctx.guild.unban(i.user, reason=reason)
            await ctx.send(f"```J'ai unban {user}, en vrai je l'aime bien.```")
            return
    await ctx.send(f"```Je trouve pas {user}, t'es sûr que tu l'as ban même ? :/```")


@bot.command()
async def memeRandom(ctx):
    html_page = requests.get('https://imgflip.com/i/')
    soup = BeautifulSoup(html_page.content, 'html.parser')
    warning = soup.find('div', class_="pause-wrap")
    book_container = warning
    images = book_container.findAll('img')
    example = images[0]
    example = example.attrs['src'].replace("//i.imgflip.com/", "https://i.imgflip.com/")
    embed = discord.Embed(title="**Memes générateur**", colour=discord.Colour.orange())
    embed.set_image(url=example)
    await ctx.send(embed=embed)


@bot.command()
async def herosRandom(ctx):
    random_id = random.randint(1, 731)
    url = f"https://superheroapi.com/api/1709029455960535/{random_id}"
    response = requests.get(url)
    data = response.text
    parsed = json.loads(data)  # API stuff.
    name = parsed["name"]
    img = parsed["image"]
    img = img["url"]

    powerstats = parsed["powerstats"]
    intelligence = powerstats["intelligence"]
    strength = powerstats["strength"]
    speed = powerstats["speed"]
    durability = powerstats["durability"]
    power = powerstats["power"]
    combat = powerstats["combat"]
    id = parsed["id"]

    embed = discord.Embed(title="**Héros**", colour=discord.Colour.orange())
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    embed.set_image(url=img)
    embed.add_field(name="Nom", value=name, inline=True)
    embed.add_field(name="Intelligence", value=intelligence, inline=False)
    embed.add_field(name="Force", value=strength, inline=True)
    embed.add_field(name="Vitesse", value=speed, inline=True)
    embed.add_field(name="Résistance", value=durability, inline=False)
    embed.add_field(name="Puissance", value=power, inline=True)
    embed.add_field(name="Combat", value=combat, inline=True)
    embed.add_field(name="Numéro", value=id + " / 731", inline=False)

    message = await ctx.send(embed=embed)
    await message.add_reaction("✅")
    await message.add_reaction("❌")

    def checkEmoji(reaction, user):
        return ctx.message.author == user and message.id == reaction.message.id and (
                    str(reaction.emoji) == "✅" or str(reaction.emoji) == "❌")

    reaction, user = await bot.wait_for("reaction_add", timeout=10, check=checkEmoji)
    if reaction.emoji == "✅":
        result = curseur.execute(
            f"SELECT * FROM userTeamHeros WHERE user_id = {ctx.message.author.id}")  # WHERE user = {ctx.message.author.id}
        if result:
            i = 0
            for row in result:
                i += 1
            if i == 6:
                await ctx.send(f"Vous possedez déjà 6 héros dans votre team ! faites **!heroList** pour les voir")
            else:
                await ctx.send(f"**{name}** a été ajouté a votre Team de héros")
                # Insertion des données
                curseur.execute("INSERT INTO userTeamHeros VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
                ctx.message.author.id, name, img, intelligence, strength, speed, durability, power, combat, id))
                # Validation
                connexion.commit()

    else:
        await ctx.send(f"**{name}** n'a pas été ajouté a votre Team de héros")


@bot.command()
async def herosList(ctx):
    result = curseur.execute(
        f"SELECT * FROM userTeamHeros WHERE user_id = {ctx.message.author.id}")  # WHERE user = {ctx.message.author.id}
    if result:
        i = 1
        for row in result:
            await ctx.send(f"{i}. **{row[1]}**")
            i += 1
    else:
        await ctx.send("Vous n'avez pas encore engagé de héros dans votre team")


@bot.command()
async def searchHeros(ctx, *texte):
    text = texte
    nom_hero = " ".join(text)
    print(nom_hero)
    url = f"https://www.superheroapi.com/api.php/1709029455960535/search/{nom_hero}"
    response = requests.get(url)
    data = response.text
    parsed = json.loads(data)  # API stuff.
    result = parsed["results"]
    i = 0
    while i < len(result):
        name = result[i]["name"]
        img = result[i]["image"]
        img = img["url"]

        powerstats = result[i]["powerstats"]
        intelligence = powerstats["intelligence"]
        strength = powerstats["strength"]
        speed = powerstats["speed"]
        durability = powerstats["durability"]
        power = powerstats["power"]
        combat = powerstats["combat"]
        id = result[i]["id"]

        embed = discord.Embed(title="**Héros**", colour=discord.Colour.orange())
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_image(url=img)
        embed.add_field(name="Nom", value=name, inline=True)
        embed.add_field(name="Intelligence", value=intelligence, inline=False)
        embed.add_field(name="Force", value=strength, inline=True)
        embed.add_field(name="Vitesse", value=speed, inline=True)
        embed.add_field(name="Résistance", value=durability, inline=False)
        embed.add_field(name="Puissance", value=power, inline=True)
        embed.add_field(name="Combat", value=combat, inline=True)
        embed.add_field(name="Numéro", value=id + " / 731", inline=False)

        await ctx.send(embed=embed)
        i += 1


@bot.command()
async def herosDelete(ctx, *heros):
    Heros = heros
    Heros = " ".join(Heros)
    print(Heros)
    user_id = ctx.message.author.id
    curseur.execute(f"DELETE FROM userTeamHeros WHERE user_id = {user_id} and name_hero = '{Heros}'")
    connexion.commit()
    await ctx.send(f"**{Heros}** a bien été enlevé de votre team !")


@bot.command()
async def teamDuel(ctx, user_e: discord.User):
    user_enemy_id = user_e.id
    self_user_id = ctx.message.author.id
    self_user_name = ctx.message.author.name
    embed = discord.Embed(title="**Duel**", colour=discord.Colour.orange())
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    embed.set_image(url="https://media.giphy.com/media/1TSuXCZDSDfBMFyQPU/giphy.gif")
    embed.add_field(name="Team de " + ctx.message.author.name, value="------------------------------", inline=True)
    embed.add_field(name="VS", value="----", inline=True)
    embed.add_field(name="Team de " + user_e.name, value="------------------------------", inline=True)

    message = await ctx.send(embed=embed)
    await message.add_reaction("✅")
    await message.add_reaction("❌")

    def checkEmoji(reaction, user):
        return user_e == user and message.id == reaction.message.id and (
                    str(reaction.emoji) == "✅" or str(reaction.emoji) == "❌")

    reaction, user = await bot.wait_for("reaction_add", timeout=10, check=checkEmoji)

    if reaction.emoji == "✅":
        await ctx.send(f"**{user.name}** a accepté de participer au duel contre **{self_user_name}**")

        result_e = curseur.execute(f"SELECT * FROM userTeamHeros WHERE user_id = {user_enemy_id}")
        connexion.commit()
        if result_e:
            moyenne_e = 0
            for row in result_e:
                moyenne_e += row[3] + row[4] + row[5] + row[6] + row[7] + row[8]
            attaque_e = moyenne_e

        result_self = curseur.execute(f"SELECT * FROM userTeamHeros WHERE user_id = {self_user_id}")
        connexion.commit()
        if result_self:
            moyenne = 0
            for row in result_self:
                moyenne += row[3] + row[4] + row[5] + row[6] + row[7] + row[8]
            attaque = moyenne
        print(attaque)
        print(attaque_e)
        print(self_user_id)
        if attaque != NULL and attaque_e != NULL:
            if attaque > attaque_e:
                await ctx.send(f"La valeur de combat de la team de {self_user_name} est de : {attaque}")
                await ctx.send(f"La valeur de combat de la team de {user.name} est de : {attaque_e}")
                await ctx.send(f"Le grand vainqueur de ce combat n'est autre que....**{self_user_name}** ! ")
            if attaque < attaque_e:
                await ctx.send(f"La valeur de combat de la team de {self_user_name} est de : {attaque}")
                await ctx.send(f"La valeur de combat de la team de {user.name} est de : {attaque_e}")
                await ctx.send(f"Le grand vainqueur de ce combat n'est autre que....**{user.name}** ! ")
            if attaque == attaque_e:
                await ctx.send(f"La valeur de combat de la team de {self_user_name} est de : {attaque}")
                await ctx.send(f"La valeur de combat de la team de {user.name} est de : {attaque_e}")
                await ctx.send(
                    f"Le grand vainqueur de ce combat n'est autre que....**Personne** ! une égalité parfaite ! ")
    else:
        await ctx.send(f"**{user.name}** n'a pas voulu participer au duel contre **{self_user_name}**")



bot.run("")