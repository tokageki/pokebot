#inclu de base avec python

from discord.ext.commands import has_permissions, CheckFailure
from random import randint
import asyncio
import time
from random import randint




#autres
import discord
from discord.ext import commands
import pymongo

myclient = pymongo.MongoClient("<yourMongoUrl>")
mydb = myclient["<yourDataBaseName>"]



botOwnerId = <yourId>
streamUrl = "<yourStreamUrl"
botWebsiteUrl = "<yourWebsite"

gifError = "<errorImageUrl>"
gifWarning = "<warningImageUrl>"
gifNoProblem = "<noProblemImageUrl>"


botToken = "<yourBotToken>"

#migration faite
#définis le préfixe en fonction du serveur
def get_prefix(client, message):
    mycol = mydb["serverPrefix"]
    myquery = { "serverId": message.guild.id }
    result = mycol.find_one(myquery)
    if result == None :
        mydict = { "serverId": message.guild.id, "serverName": message.guild.name, "prefix": ";" }
        mycol.insert_one(mydict)
        server_prefix = ";"
    else :
        server_prefix = mycol.find_one( { "serverId": message.guild.id }, { "_id": 0, "serverName": 0, "serverId": 0} )
        server_prefix = server_prefix['prefix']
    return server_prefix
        



#definis le préfix
bot = commands.Bot(command_prefix= get_prefix)

#supprime la commande help pour la remplacer plus tard
bot.remove_command("help")



@bot.event 
async def on_ready():
    #Définition du jeu du bot sur ".help"
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game('.help'))
    #Affiche que la connection a bien été effectuée
    print(f'connecté en tant que {bot.user}')


#migration faite
#commande help, liste toutes les commandes
@bot.command()
async def help(ctx):
        #Commande help dans un "Embed" de couleur verte
        #reste des commandes    
        embed = discord.Embed(title="Commandes disponibles", description="Liste des commandes disponibles", color=0x2e8b57)
        embed.add_field(name="help", value="affiche ce menu", inline=False)
        embed.add_field(name="changeprefix <prefix>", value="change le prefixe du bot (admins seulement)", inline=False)
        embed.add_field(name="addreset <nom de l'event> <taux> <image shiny> <image normal> <delais de la commande en minutes>", value="crée un nouvel event (admins seulement)", inline=False)
        embed.add_field(name="delreset <nom de l'event>", value="supprime un event (admins seulement)", inline=False)
        embed.add_field(name="reset list", value="affiche la liste des resets disponibles", inline=False)
        embed.add_field(name="reset <nom de l'event>", value="reset un event (EN COURS DE CRÉATION)", inline=False)
        embed.add_field(name="shiny <@user(facultatif)>", value="donne la liste des shinys de la personne", inline=False)
        embed.set_footer(text="T-PokeBot help")  
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/724993070114013337/725045208655593482/Tokabot.png")
        embed.set_author(name="T-Pokebot", url=botWebsiteUrl, icon_url="https://cdn.discordapp.com/attachments/724993070114013337/725044258134032475/bowdenfond.jpg")
        await ctx.channel.send(embed=embed)

        #affichage des commandes de developpement
        author = ctx.message.author
        if author == bot.get_user(botOwnerId):
        #Commande help dans un "Embed" de couleur rouge ne s'affichant que quand l'utilisateur entrant la commande est le propriétaire du bot
        #Cela me permet d'avoir dans mon help mes commandes de configuration du bot, étant bloquées pour les autres, ils n'ont pas besoin de les voir
            embed = discord.Embed(title="Commandes de developpement", description="Liste des commandes de developpement", color=0x8B0000)
            #Commandes de developpement et de configuration du bot
            embed.add_field(name="listen/play/watch/stream <mot>", value="change le statut du bot (propriétaire du bot seulement)", inline=False)
            embed.add_field(name="addemote <emote>", value="ajoute une emote dans la liste des emotes du bot (propriétaire du bot seulement)", inline=False)
            embed.add_field(name="addanimatedemote <emotename> <emoteid>", value="ajoute une emote animée dans la liste des emotes du bot (propriétaire du bot seulement)", inline=False)
            await ctx.channel.send(embed=embed)

        
        #ajoute une emote custom en réaction depuis le tableau "EMOTES"
        #utiliser la commande addemote suivi d'une emote pour en ajouter
        mycol = mydb["emotes"] #se connecte dans la db "emote"
        numberOfEmotes = mycol.find_one() #recupère une donnée, si la db est vide None est retourné
        test = mycol.aggregate([{"$sample":{"size":1}}])
        emote = list(test)[0]["emoteData"]
        if numberOfEmotes == None : #si la db est vide, le bot envoie un embed pour demander d'ajouter une emote avec addemote
            embed = discord.Embed(title="ERREUR", description=f"Pensez à ajouter une emote avec la commande addemote !", color=0xFF7F00)
            embed.set_thumbnail(url=gifWarning)
            await ctx.channel.send(embed=embed)
        else :
            await ctx.message.add_reaction(emote) #ajoute l'emote en reaction


#migration faite
@bot.command()
async def addemote(ctx,*,emojiId): #ajoute une emote dans la liste des emotes custom que le bot peut utiliser
    author = ctx.message.author
    if author == bot.get_user(botOwnerId): #verifie que c'est le propriétaire qui utilise la commande 
        mycol = mydb["emotes"]
        mydict = { "emoteData": emojiId }
        mycol.insert_one(mydict)
        embed = discord.Embed(title="EMOTE", description=f"Emote {emojiId} ajoutée", color=0x2e8b57) #valide que l'emote a été ajoutée
        embed.set_thumbnail(url=gifNoProblem)
        await ctx.channel.send(embed=embed)   
    else : 
        embed = discord.Embed(title="ERREUR", description=f"Vous ne pouvez pas faire cela !", color=0x8B0000)
        embed.set_thumbnail(url=gifError)
        await ctx.channel.send(embed=embed)

@addemote.error
async def addemote_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument): #si aucun argument n'est donné, le bot donne la liste des events
        embed = discord.Embed(title="ERREUR", description=f"Argument manquant !", color=0x8B0000)
        embed.set_thumbnail(url=gifError)
        await ctx.channel.send(embed=embed)
        


#migration faite
@bot.command()
async def addanimatedemote(ctx, emoteName, emoteId): #ajoute une emote animée dans la liste des emotes custom que le bot peut utiliser
    author = ctx.message.author
    if author == bot.get_user(botOwnerId): #verifie que c'est le propriétaire qui utilise la commande
        emote = f"<a:{emoteName}:{emoteId}>"
        mycol = mydb["emotes"]
        mydict = { "emoteData": emote }
        mycol.insert_one(mydict)
        embed = discord.Embed(title="EMOTE ANIMEE", description=f"Emote animée {emote} ajoutée.", color=0x2e8b57) #valide que l'emote a été ajoutée
        embed.set_thumbnail(url=f"https://cdn.discordapp.com/emojis/{emoteId}.gif?v=1")
        await ctx.channel.send(embed=embed)
    else : 
        embed = discord.Embed(title="ERREUR", description=f"Vous ne pouvez pas faire cela !", color=0x8B0000)
        embed.set_thumbnail(url=gifError)
        await ctx.channel.send(embed=embed)

@addanimatedemote.error
async def addanimatedemote_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument): #si aucun argument n'est donné, le bot donne la liste des events
        embed = discord.Embed(title="ERREUR", description=f"Argument manquant !", color=0x8B0000)
        embed.set_thumbnail(url=gifError)
        await ctx.channel.send(embed=embed)
        


#migration faite
@bot.command()
@commands.has_permissions(administrator=True)
async def changeprefix(ctx, mot2):
    mycol = mydb["serverPrefix"]
    myquery = { "serverId": ctx.guild.id }
    newvalues = { "$set": { "prefix": mot2 } }
    mycol.update_one(myquery, newvalues)
    embed = discord.Embed(title="PREFIX", description=f'Le préfix a été changé pour "{mot2}"', color=0x2e8b57)
    embed.set_thumbnail(url=gifNoProblem)
    await ctx.channel.send(embed=embed)


#migration faite
@bot.command()
@commands.has_permissions(administrator=True)
async def addreset(ctx, event_name, taux, shiny, pas_shiny, delais):
    #enregistre un event dans le tableau EVENTS de la db
    try:
        int(taux)
        
        evenement_id = f"{ctx.guild.id}_{event_name}"
        mycol = mydb["resets"]
        myquery = { "resetId": evenement_id }
        numberOfEvent = mycol.find_one(myquery)
        if numberOfEvent == None :
            mydict = { "serverId": ctx.guild.id, "resetId": evenement_id, "guildName": ctx.guild.name, "resetName": event_name, "taux": taux,"lienShiny": shiny, "lienNormal": pas_shiny, "delais": delais }
            mycol.insert_one(mydict)
            embed = discord.Embed(title="RESET", description=f"le reset {event_name} a bien été ajouté", color=0x2e8b57)
            embed.set_thumbnail(url=gifNoProblem)
            await ctx.channel.send(embed=embed)
            await ctx.message.delete()
        else :
            embed = discord.Embed(title="ERREUR", description=f"Un event portant ce nom a déjà été créé !", color=0x8B0000)
            embed.set_thumbnail(url=gifError)
            await ctx.channel.send(embed=embed)
    except:
        embed = discord.Embed(title="ERREUR", description=f"Le taux rentré n'est pas valide.", color=0x8B0000)
        embed.set_thumbnail(url=gifError)
        await ctx.channel.send(embed=embed)



#migration faite
@bot.command()
@commands.has_permissions(administrator=True) #supprime un reset de la database
async def delreset(ctx, event_name) :
    server_id = ctx.guild.id
    evenement_id = f"{server_id}_{event_name}"
    mycol = mydb["resets"]
    myquery = { "resetId": evenement_id }
    numberOfEvent = mycol.find_one(myquery)
    if numberOfEvent == None :
        embed = discord.Embed(title="ERREUR", description=f"Aucun event nommé {event_name} n'a été trouvé.", color=0x8B0000)
        embed.set_thumbnail(url=gifError)
        await ctx.channel.send(embed=embed)
    else :
        numberOfEvent = mycol.delete_one(myquery)
        embed = discord.Embed(title="RESET", description=f"L'event {event_name} a bien été supprimé", color=0x2e8b57)
        embed.set_thumbnail(url=gifNoProblem)
        await ctx.channel.send(embed=embed)
        




@bot.command() #change le statut du bot
async def watch(ctx,*,film):
    author = ctx.message.author
    if author == bot.get_user(botOwnerId):
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=film))
        embed = discord.Embed(title="WATCH", description=f'Statut changé en "__**regarde {film}**__".', color=0x2e8b57)
        embed.set_thumbnail(url=gifNoProblem)
        await ctx.channel.send(embed=embed)
    else :
        embed = discord.Embed(title="ERREUR", description=f"Vous ne pouvez pas faire cela !", color=0x8B0000)
        embed.set_thumbnail(url=gifError)
        await ctx.channel.send(embed=embed)


@bot.command() #change le statut du bot
async def stream(ctx,*,stream):
    author = ctx.message.author
    if author == bot.get_user(botOwnerId):
        await bot.change_presence(activity=discord.Streaming(name=stream, url=streamUrl))
        embed = discord.Embed(title="STREAM", description=f'Statut changé en "__**stream {stream}**__".', color=0x2e8b57)
        embed.set_thumbnail(url=gifNoProblem)
        await ctx.channel.send(embed=embed)
    else :
        embed = discord.Embed(title="ERREUR", description=f"Vous ne pouvez pas faire cela !", color=0x8B0000)
        embed.set_thumbnail(url=gifError)
        await ctx.channel.send(embed=embed)


@bot.command() #change le statut du bot
async def listen(ctx,*,music):
    author = ctx.message.author
    if author == bot.get_user(botOwnerId):
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=music))
        embed = discord.Embed(title="LISTEN", description=f'Statut changé en "__**ecoute {music}**__".', color=0x2e8b57)
        embed.set_thumbnail(url=gifNoProblem)
        await ctx.channel.send(embed=embed)
    else :
        embed = discord.Embed(title="ERREUR", description=f"Vous ne pouvez pas faire cela !", color=0x8B0000)
        embed.set_thumbnail(url=gifError)
        await ctx.channel.send(embed=embed)


@bot.command() #change le statut du bot
async def play(ctx,*,game):
    author = ctx.message.author
    if author == bot.get_user(botOwnerId):
        await bot.change_presence(activity=discord.Game(name=game))
        embed = discord.Embed(title="PLAY", description=f'Statut changé en "__**joue à {game}**__".', color=0x2e8b57)
        embed.set_thumbnail(url=gifNoProblem)
        await ctx.channel.send(embed=embed)
    else :
        embed = discord.Embed(title="ERREUR", description=f"Vous ne pouvez pas faire cela !", color=0x8B0000)
        embed.set_thumbnail(url=gifError)
        await ctx.channel.send(embed=embed)


#migration faite
@bot.command() #commande de reset du bot
async def reset(ctx, event_name):
    #si l'utilisateur entre la commande reset list, le bot affiche la liste des resets sur le serveur
    mycol = mydb["resets"]
    if event_name == None or event_name == "list" : 
        myquery = { "serverId": ctx.guild.id }
        message = "__**Voici la liste des events actuels :**__\n"
        for resultat in mycol.find(myquery):
            message += resultat["resetName"] + "\n"
        if message != "":
            embed = discord.Embed(title="RESET", description=message, color=0x2e8b57)
            embed.set_thumbnail(url=gifNoProblem)
            await ctx.channel.send(embed=embed) 
    else :
        eventID = (f"{ctx.guild.id}_{event_name}") #fait l'id de l'event pour le reconnaitre
        userId = ctx.message.author.id
        userEventId = (f"{userId}_{eventID}")
        myquery = { "resetId": eventID }
        result = mycol.find_one(myquery)
        if result != None :
            mycolDelais = mydb["delais"]
            isDelaisCreated = mycolDelais.find_one({ "userEventId": userEventId })
            if isDelaisCreated == None :
                mydict = { "serverId": ctx.guild.id, "userId": userId, "eventId": eventID, "eventName": event_name, "userEventId": userEventId,"cooldown": 0, "username": ctx.message.author.name}
                mycolDelais.insert_one(mydict)

            timestamp = int(time.time())
            myquery = { "userEventId": userEventId }
            lastReset = mycolDelais.find_one(myquery)["cooldown"]
            cooldownInMinutes = int(mycol.find_one({ "resetId" : eventID })["delais"])
            cooldownInSeconds = cooldownInMinutes * 60
            timeResetAllowed = timestamp - cooldownInSeconds
            if lastReset <= timeResetAllowed :
                myquery = { "userEventId": userEventId }
                newvalues = { "$set": { "cooldown": timestamp } }
                mycolDelais.update_one(myquery, newvalues)


                myquery = { "resetId": eventID }
                data = mycol.find_one(myquery)
                nombrealeatoire = randint(1, int(data["taux"]))

                if nombrealeatoire == 1 : 
                    embed = discord.Embed(title="RESET", description=f"**Le {data['resetName']} est shiny ! Bravo ! <a:charizardDancing:725281864297873428>**", color=0xd79a10)
                    lien = data["lienShiny"]
                    embed.set_image(url=lien)
                    await ctx.channel.send(embed=embed)
                    mycolShinyUser = mydb["userData"]
                    mydict = { "userId": userId, "serverId": ctx.guild.id, "eventName": event_name, "userName": ctx.message.author.name, "serverName": ctx.guild.name}
                    mycolShinyUser.insert_one(mydict)

                else :
                    lien = data["lienNormal"]
                    embed = discord.Embed(title="RESET", description=f"Le {data['resetName']} n'est pas shiny... Dommage ! <a:pokewalking:725285728765870080>", color=0x2e8b57)
                    embed.set_image(url=lien)
                    await ctx.channel.send(embed=embed)
                    
            else :
                embed = discord.Embed(title="ERREUR", description=f"Vous ne pouvez pas faire cela !", color=0x8B0000)
                embed.set_thumbnail(url=gifError)
                timeRemaining = lastReset - timeResetAllowed
                if timeRemaining < 60 :
                    embed.add_field(name="temps restant", value=f"vous devez encore attendre {timeRemaining} secondes.", inline=False)
                else :
                    timeRemaining = timeRemaining / 60
                    embed.add_field(name="temps restant", value=f"vous devez encore attendre {int(timeRemaining)} minutes.", inline=False)
                await ctx.channel.send(embed=embed)

        else :
            embed = discord.Embed(title="ERREUR", description=f"Aucun event nommé {event_name} n'a été trouvé.", color=0x8B0000)
            embed.set_thumbnail(url=gifError)
            await ctx.channel.send(embed=embed)



@reset.error
async def reset_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument): #si aucun argument n'est donné, le bot donne la liste des events
        mycol = mydb["resets"]
        myquery = { "serverId": ctx.guild.id }
        message = "**Argument manquant**\n\n__**Voici la liste des events actuels :**__\n"
        for resultat in mycol.find(myquery):
            message += resultat["resetName"] + "\n"
        if message != "":
            embed = discord.Embed(title="RESET", description=message, color=0xFF7F00)
            embed.set_thumbnail(url=gifWarning)
            await ctx.channel.send(embed=embed)




#migration faite
@bot.command() #donne la liste des shinys d'une personne
async def shiny(ctx, member: discord.Member = None):
    if member == None :
        member = ctx.message.author
    mycol = mydb["userData"]
    myquery = { "userId": member.id, "serverId": ctx.guild.id}
    message = f"**Voici le(s) shiny(s) de {member} sur ce serveur :**\n"
    for resultat in mycol.find(myquery):
        message += resultat["eventName"] + "\n"
    if message != "":
        embed = discord.Embed(title="SHINYS", description=message, color=0xFF7F00)
        embed.set_thumbnail(url=gifWarning)
        await ctx.channel.send(embed=embed)




#migration manquante
@bot.command()
@commands.has_permissions(administrator=True)
async def clearshiny(ctx,member: discord.Member = None):
    if member == None :
        member = ctx.message.author
    mycol = mydb["userData"]
    myquery = { "serverId": ctx.guild.id }
    numberOfEvent = mycol.find_one(myquery)
    if numberOfEvent == None :
        embed = discord.Embed(title="ERREUR", description=f"Aucun shiny n'a été trouvé dans la liste de {member.name}.", color=0x8B0000)
        embed.set_thumbnail(url=gifError)
        await ctx.channel.send(embed=embed)
    else :
        numberOfEvent = mycol.delete_one(myquery)
        embed = discord.Embed(title="SHINYS", description=f"Les shinys de {member.name} ont bien étés supprimés", color=0x2e8b57)
        embed.set_thumbnail(url=gifNoProblem)
        await ctx.channel.send(embed=embed)




@clearshiny.error
async def clearshiny_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title="ERREUR", description=f"Vous n'avez pas les permissions.", color=0x8B0000)
        embed.set_thumbnail(url=gifError)
        await ctx.channel.send(embed=embed)




loop = asyncio.get_event_loop()  # Create main loop
try:
    loop.run_until_complete(bot.start(botToken))  # Launch le bot in the main loop
except KeyboardInterrupt:
    # Keyboard interrupt stope la boucle et ferme la db
    loop.run_until_complete(bot.logout())

