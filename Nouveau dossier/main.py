import json
import requests
import time
import discord
import requests
from discord.ext import commands
bot = commands.Bot(command_prefix="?", description="Lyrify le BG")


@bot.event
async def on_ready():
    print("coucou")




@bot.command()
async def l(ctx,*request):
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
    #await ctx.send("Musique trouvée !!! : **{}** de **{}** \n\n\n".format(titre, artist))
    #await ctx.send(song[0:1999])
    #await ctx.send(song[1999:3999])
    #await ctx.send(song[3999:5999])

    form1 = discord.Embed(title = titre , description=artist, colour=discord.Colour.orange())
    form1.set_thumbnail(url=image)
    form1.set_footer(text=song[0:1900])
    form2 = discord.Embed(title ="" , description="", colour=discord.Colour.orange())
    form2.set_footer(text=song[1900:3900])
    form3 = discord.Embed(title="", description="", colour=discord.Colour.orange())
    form3.set_footer(text=song[3900:5900])
    form4 = discord.Embed(title="", description="", colour=discord.Colour.orange())
    form4.set_footer(text=song[5900:])
    await ctx.send(embed = form1)
    await ctx.send(embed = form2)
    await ctx.send(embed = form3)
    await ctx.send(embed = form4)


    #form2 = discord.Embed(title = "" , description="")
    #form2.description()
    #await ctx.send(embed = form2)







bot.run("ODUxODI4ODI5MDIyMzIyNzM5.YL99aw.LTfa4Dgx769e25QXTZeQLSOYNLw")