#inclu de base avec python

from discord.ext.commands import has_permissions, CheckFailure
from random import randint
import sqlite3
import asyncio
import time
from random import randint

#autres
import discord
from discord.ext import commands


botOwnerId = "your id"
streamUrl = "your website"
botWebsiteUrl = "botwebsite" #en attendant d'avoir un site pour le bot ^^

botToken = "Your token here"


#définis le préfixe en fonction du serveur
def get_prefix(client, message):
    donnee = (message.guild.id, )
    c.execute("SELECT prefix FROM server WHERE id_server = ?", donnee)
    server_prefix = c.fetchone()
    return server_prefix


#definis le préfix
bot = commands.Bot(command_prefix= get_prefix)

#supprime la commande help pour la remplacer plus tard
bot.remove_command("help")


#création de la db
conn = sqlite3.connect('pokebot.db')
c = conn.cursor()


#Création d'un tableau contenant les infos du serveur
c.execute("""CREATE TABLE IF NOT EXISTS SERVER (
        id_server           INTEGER             PRIMARY KEY,
        name                VARCHAR             NOT NULL,
        prefix              VARCHAR(20)         DEFAULT         '.'
        )""")


#Création d'un tableau contenant les données de chaque utilisateur en fonction du serveur (events obtenus, etc)
c.execute("""CREATE TABLE IF NOT EXISTS USERS_DATA (
        id                  INTEGER         PRIMARY KEY         AUTOINCREMENT,
        id_user             INTEGER         NOT NULL,
        id_server           INTEGER         NOT NULL,
        event_name          VARCHAR(100)    NOT NULL,
        user_name           VARCHAR(100)    NOT NULL,
        server_name         VARCHAR(100)    NOT NULL
        )""")


#Création d'un tableau contenant les events en fonction du serveur
#event_id est composé de server_id + event_name, soit (server_id)_(event_name)
c.execute("""CREATE TABLE IF NOT EXISTS EVENTS (
        server_id           VARCHAR(100)    NOT NULL,
        event_id            VARCHAR(100)    PRIMARY KEY,
        server_name         VARCHAR(100)    NOT NULL,
        creator             VARCHAR(100)    NOT NULL,
        event_name          VARCHAR(100)    NOT NULL,
        rate                INTEGER         NOT NULL,
        shiny_lien          VARCHAR(100)    NOT NULL,
        normal_lien         VARCHAR(100)    NOT NULL,
        delais              INTEGER(100)    NOT NULL
        )""")


#user_event_id est composé de server_id + event_name + user_id, soit (server_id)_(event_name)
c.execute("""CREATE TABLE IF NOT EXISTS DELAIS (
        server_id           INTEGER         NOT NULL,
        user_id             INTEGER         NOT NULL,
        event_id            VARCHAR(100)    NOT NULL,
        event_name          VARCHAR(100)    NOT NULL,
        user_event_id       VARCHAR(100)    PRIMARY KEY,
        cooldown            INTEGER         NOT NULL
        )""")

#création d'un tableau qui contient les emotes custom que le bot peut utiliser
c.execute("""CREATE TABLE IF NOT EXISTS EMOTES (
        emoteNumber         INTEGER         PRIMARY KEY,
        emoteId             VARCHAR(100)    NOT NULL
        )""")




@bot.event 
async def on_ready():
    #Définition du jeu du bot sur ".help"
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game('.help'))
    #Affiche que la connection a bien été effectuée
    print(f'connecté en tant que {bot.user}')


@bot.event
async def on_guild_join(guild):
    #Quand le bot rejoint un serveur, il sauvegarde son id, son nom et son prefixe utilisé de base (le ".") dans la base de donnée
    c.execute("INSERT INTO SERVER VALUES (?, ?, ?)", ((guild.id),(guild.name),"."))
    conn.commit()





#commande help, liste toutes les commandes
@bot.command()
async def help(ctx):
        author = ctx.message.author
        if author == bot.get_user(botOwnerId):

        #Commande help dans un "Embed" de couleur rouge ne s'affichant que quand l'utilisateur entrant la commande est le propriétaire du bot
        #Cela me permet d'avoir dans mon help mes commandes de configuration du bot, étant bloquées pour les autres, ils n'ont pas besoin de les voir
            embed = discord.Embed(title="Commandes disponibles", description="Liste des commandes disponibles", color=0x8B0000)
            #Commandes de developpement et de configuration du bot
            embed.add_field(name="serverlist", value="donne la liste des serveurs sur lequel est le bot (propriétaire du bot seulement)", inline=False)
            embed.add_field(name="listen/play/watch/stream <mot>", value="change le statut du bot (propriétaire du bot seulement)", inline=False)
            embed.add_field(name="addemote <emote>", value="ajoute une emote dans la liste des emotes du bot (propriétaire du bot seulement)", inline=False)
            embed.add_field(name="addanimatedemote <emotename> <emoteid>", value="ajoute une emote animée dans la liste des emotes du bot (propriétaire du bot seulement)", inline=False)
        else :

            #Commande help dans un "Embed" de couleur verte
            embed = discord.Embed(title="Commandes disponibles", description="Liste des commandes disponibles", color=0x2e8b57)

        #reste des commandes    
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
        
        #ajoute une emote custom en réaction depuis le tableau "EMOTES"
        #utiliser la commande addemote suivi d'une emote pour en ajouter
        c.execute("SELECT COUNT(*) FROM EMOTES")
        countOfEmotes = c.fetchone()
        randomNumber = randint(1,countOfEmotes[0]) #prends une emote aléatoire dans la liste
        c.execute("SELECT emoteId FROM EMOTES WHERE emoteNumber = ?",(randomNumber,))
        emoji = c.fetchone()
        await ctx.message.add_reaction(emoji[0]) #ajoute l'emote en reaction



@bot.command()
async def addemote(ctx,*,emojiId): #ajoute une emote dans la liste des emotes custom que le bot peut utiliser
    author = ctx.message.author
    if author == bot.get_user(botOwnerId): #verifie que c'est le propriétaire qui utilise la commande 
        c.execute("INSERT INTO EMOTES VALUES (?,?)", (None,emojiId))
        conn.commit()
        embed = discord.Embed(title="EMOTE", description=f"Emote {emojiId} ajoutée", color=0x2e8b57) #valide que l'emote a été ajoutée
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/724993070114013337/725413003607932938/DisastrousIllfatedDaddylonglegs-size_restricted.gif")
        await ctx.channel.send(embed=embed)
        
    else : 
        embed = discord.Embed(title="ERREUR", description=f"Vous ne pouvez pas faire cela !", color=0x8B0000)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/724993070114013337/725405379827204196/giphy_3.gif")
        await ctx.channel.send(embed=embed)


@bot.command()
async def addanimatedemote(ctx, emoteName, emoteId): #ajoute une emote animée dans la liste des emotes custom que le bot peut utiliser
    author = ctx.message.author
    if author == bot.get_user(botOwnerId): #verifie que c'est le propriétaire qui utilise la commande
        emote = f"<a:{emoteName}:{emoteId}>"
        c.execute("INSERT INTO EMOTES VALUES (?,?)", (None,emote))
        conn.commit()
        embed = discord.Embed(title="EMOTE", description=f"Emote {emote} ajoutée", color=0x2e8b57) #valide que l'emote a été ajoutée
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/724993070114013337/725413003607932938/DisastrousIllfatedDaddylonglegs-size_restricted.gif")
        await ctx.channel.send(embed=embed)
    else : 
        embed = discord.Embed(title="ERREUR", description=f"Vous ne pouvez pas faire cela !", color=0x8B0000)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/724993070114013337/725405379827204196/giphy_3.gif")
        await ctx.channel.send(embed=embed)


@bot.command()
@commands.has_permissions(administrator=True)
async def clearshiny(ctx,member: discord.Member = None):
    serverId = ctx.guild.id
    if member == None :
        member = ctx.message.author
    userId = member.id
    c.execute("DELETE FROM USERS_DATA WHERE id_server = ? AND id_user = ?", (serverId,userId))
    conn.commit()
    embed = discord.Embed(title="RESETS", description=f"Les resets de cet utilisateur ont été supprimés", color=0x2e8b57) 
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/724993070114013337/725413003607932938/DisastrousIllfatedDaddylonglegs-size_restricted.gif")
    await ctx.channel.send(embed=embed)


@clearshiny.error
async def clearshiny_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title="ERREUR", description=f"Vous n'avez pas les permissions.", color=0x8B0000)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/724993070114013337/725405379827204196/giphy_3.gif")
        await ctx.channel.send(embed=embed)



@bot.command()
async def clearemote(ctx):
    author = ctx.message.author
    if author == bot.get_user(botOwnerId): #verifie que c'est le propriétaire qui utilise la commande
        c.execute("DELETE FROM EMOTES")
        conn.commit()
        embed = discord.Embed(title="EMOTE", description=f"Les emotes ont été clear", color=0x2e8b57) #valide que l'emote a été ajoutée
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/724993070114013337/725413003607932938/DisastrousIllfatedDaddylonglegs-size_restricted.gif")
        await ctx.channel.send(embed=embed)
    else : 
        embed = discord.Embed(title="ERREUR", description=f"Vous ne pouvez pas faire cela !", color=0x8B0000)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/724993070114013337/725405379827204196/giphy_3.gif")
        await ctx.channel.send(embed=embed)


@bot.command()
@commands.has_permissions(administrator=True)
async def changeprefix(ctx, mot2):
    #Change le prefix du bot sur le serveur
    server_id = ctx.guild.id
    c.execute("UPDATE SERVER SET prefix = ? WHERE id_server = ?", ((mot2), int(ctx.guild.id),))
    conn.commit()
    embed = discord.Embed(title="PREFIX", description=f'Le préfix a été changé pour "{mot2}"', color=0x2e8b57)
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/724993070114013337/725413003607932938/DisastrousIllfatedDaddylonglegs-size_restricted.gif")
    await ctx.channel.send(embed=embed)



@bot.command()
async def serverlist(ctx):
    #affiche la liste des serveurs enregistrés dans la db (propriétaire seulement)
    author = ctx.message.author
    if author == bot.get_user(botOwnerId):
        c.execute("SELECT * FROM SERVER")
        resultats = c.fetchall()
        message = ""
        for resultat in resultats:
            message += str(resultat) + "\n"
        if message != "":
            embed = discord.Embed(title="SERVERLIST", description=message, color=0x2e8b57)
            await ctx.channel.send(embed=embed)
    else : 
        embed = discord.Embed(title="ERREUR", description=f"Vous ne pouvez pas faire cela !", color=0x8B0000)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/724993070114013337/725405379827204196/giphy_3.gif")
        await ctx.channel.send(embed=embed)



@bot.command()
@commands.has_permissions(administrator=True)
async def addreset(ctx, event_name, taux, shiny, pas_shiny, delais):
    #enregistre un event dans le tableau EVENTS de la db
    try:
        int(taux)
        author = ctx.message.author
        server_id = ctx.guild.id
        guild_name = ctx.guild.name
        evenement_id = f"{server_id}_{event_name}"
        c.execute("INSERT INTO EVENTS VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (str(server_id),str(evenement_id),str(guild_name),str(author),str(event_name),int(taux),str(shiny),str(pas_shiny),int(delais)))
        conn.commit()
        embed = discord.Embed(title="RESET", description=f"le reset {event_name} a bien été ajouté", color=0x2e8b57)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/724993070114013337/725413003607932938/DisastrousIllfatedDaddylonglegs-size_restricted.gif")
        await ctx.channel.send(embed=embed)
    except:
        embed = discord.Embed(title="ERREUR", description=f"Le taux rentré n'est pas valide ou l'event a déjà été créé.", color=0x8B0000)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/724993070114013337/725405379827204196/giphy_3.gif")
        await ctx.channel.send(embed=embed)



@bot.command()
@commands.has_permissions(administrator=True) #supprime un reset de la database
async def delreset(ctx, event_name) :
    server_id = ctx.guild.id
    event_id = f"{server_id}_{event_name}"
    c.execute("SELECT COUNT(*) FROM events WHERE Event_id = ?",(event_id,))
    numberEventWithId = c.fetchone()
    if numberEventWithId[0] == 1 :
        try:
            c.execute("DELETE FROM EVENTS WHERE Event_id = ? ",(event_id,))
            conn.commit()
            embed = discord.Embed(title="RESET", description=f"L'event {event_name} a bien été supprimé", color=0x2e8b57)
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/724993070114013337/725413003607932938/DisastrousIllfatedDaddylonglegs-size_restricted.gif")
            await ctx.channel.send(embed=embed)
        except:
            embed = discord.Embed(title="ERREUR", description=f"une erreur s'est produite", color=0x8B0000)
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/724993070114013337/725405379827204196/giphy_3.gif")
            await ctx.channel.send(embed=embed)
    else :
        embed = discord.Embed(title="ERREUR", description=f"Aucun event nommé {event_name} n'a été trouvé.", color=0x8B0000)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/724993070114013337/725405379827204196/giphy_3.gif")
        await ctx.channel.send(embed=embed)



@bot.command() #change le statut du bot
async def watch(ctx,*,film):
    author = ctx.message.author
    if author == bot.get_user(botOwnerId):
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=film))
        embed = discord.Embed(title="WATCH", description=f"Statut changé.", color=0x2e8b57)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/724993070114013337/725413003607932938/DisastrousIllfatedDaddylonglegs-size_restricted.gif")
        await ctx.channel.send(embed=embed)
    else :
        embed = discord.Embed(title="ERREUR", description=f"Vous ne pouvez pas faire cela !", color=0x8B0000)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/724993070114013337/725405379827204196/giphy_3.gif")
        await ctx.channel.send(embed=embed)


@bot.command() #change le statut du bot
async def stream(ctx,*,stream):
    author = ctx.message.author
    if author == bot.get_user(botOwnerId):
        await bot.change_presence(activity=discord.Streaming(name=stream, url=streamUrl))
        embed = discord.Embed(title="STREAM", description=f"Statut changé.", color=0x2e8b57)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/724993070114013337/725413003607932938/DisastrousIllfatedDaddylonglegs-size_restricted.gif")
        await ctx.channel.send(embed=embed)
    else :
        embed = discord.Embed(title="ERREUR", description=f"Vous ne pouvez pas faire cela !", color=0x8B0000)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/724993070114013337/725405379827204196/giphy_3.gif")
        await ctx.channel.send(embed=embed)


@bot.command() #change le statut du bot
async def listen(ctx,*,music):
    author = ctx.message.author
    if author == bot.get_user(botOwnerId):
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=music))
        embed = discord.Embed(title="LISTEN", description=f"Statut changé.", color=0x2e8b57)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/724993070114013337/725413003607932938/DisastrousIllfatedDaddylonglegs-size_restricted.gif")
        await ctx.channel.send(embed=embed)
    else :
        embed = discord.Embed(title="ERREUR", description=f"Vous ne pouvez pas faire cela !", color=0x8B0000)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/724993070114013337/725405379827204196/giphy_3.gif")
        await ctx.channel.send(embed=embed)


@bot.command() #change le statut du bot
async def play(ctx,*,game):
    author = ctx.message.author
    if author == bot.get_user(botOwnerId):
        await bot.change_presence(activity=discord.Game(name=game))
        embed = discord.Embed(title="PLAY", description=f"Statut changé.", color=0x2e8b57)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/724993070114013337/725413003607932938/DisastrousIllfatedDaddylonglegs-size_restricted.gif")
        await ctx.channel.send(embed=embed)
    else :
        embed = discord.Embed(title="ERREUR", description=f"Vous ne pouvez pas faire cela !", color=0x8B0000)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/724993070114013337/725405379827204196/giphy_3.gif")
        await ctx.channel.send(embed=embed)



@bot.command() #commande de reset du bot
async def reset(ctx, event_name):
    server = ctx.guild.id
    c.execute("SELECT COUNT(*) FROM EMOTES")
    countOfEmotes = c.fetchone()
    randomNumber = randint(1,countOfEmotes[0]) #prends une emote aléatoire dans la liste
    c.execute("SELECT emoteId FROM EMOTES WHERE emoteNumber = ?",(randomNumber,))
    emoji = c.fetchone()
    await ctx.message.add_reaction(emoji[0]) #ajoute l'emote en reaction
    #si l'utilisateur entre la commande reset list, le bot affiche la liste des resets sur le serveur
    if event_name == None or event_name == "list" : 
        c.execute("SELECT event_name FROM events WHERE Server_id = ?",(server,))
        resultats = c.fetchall()
        message = "**Liste des events actuels :**\n"
        for resultat in resultats:
            message += str(resultat[0]) + "\n"
        if message != "":
            embed = discord.Embed(title="RESET", description=message, color=0x2e8b57)
            await ctx.channel.send(embed=embed)
    else :
        eventID = (f"{server}_{event_name}") #fait l'id de l'event pour le reconnaitre
        userId = ctx.message.author.id
        userEventId = (f"{userId}_{eventID}")
        c.execute("SELECT COUNT(*) FROM events WHERE Event_id = ?",(eventID,))
        numberEventWithId = c.fetchone()
        if numberEventWithId[0] == 1 :
            c.execute("SELECT COUNT(*) FROM DELAIS WHERE user_event_id = ?",(userEventId,))
            number = c.fetchone()
            if number[0] == 0 :
                c.execute("INSERT INTO DELAIS VALUES (?,?,?,?,?,?)", (server,userId,eventID,event_name,userEventId,"0"))
                conn.commit()
            timestamp = int(time.time())
            c.execute("SELECT delais FROM events WHERE Event_id = ?",(eventID,))
            cooldownInMinutes = c.fetchone()
            cooldownInSeconds = cooldownInMinutes[0] * 60
            timeResetAllowed = timestamp - cooldownInSeconds
            c.execute("SELECT cooldown FROM delais WHERE user_event_id = ?",(userEventId,))
            lastReset = c.fetchone()
            if lastReset[0] < timeResetAllowed :
                c.execute("Update delais set cooldown = ? where user_event_id = ?",(timestamp, userEventId))
                conn.commit()
                c.execute("SELECT Rate FROM events WHERE Event_id = ?",(eventID,))
                taux = c.fetchone()
                c.execute("SELECT Event_name FROM events WHERE Event_id = ?",(eventID,))
                eventName = c.fetchone()
                nombrealeatoire = randint(1,taux[0]) #génère un nombre aléatoire, si c'est 1 l'event est shiny
                if nombrealeatoire == 1 : 
                    c.execute("SELECT Shiny_lien FROM events WHERE Event_id = ?",(eventID,))
                    lienShiny = c.fetchone()
                    embed = discord.Embed(title="RESET", description=f"**Le {eventName[0]} est shiny ! Bravo ! <a:charizardDancing:725281864297873428>**", color=0xd79a10)
                    embed.set_image(url=lienShiny[0])
                    await ctx.channel.send(embed=embed)
                    userName = ctx.message.author
                    serverName = ctx.guild.name
                    c.execute("INSERT INTO USERS_DATA VALUES (?,?,?,?,?,?)", (None,int(userId),int(server),str(event_name),str(userName),str(serverName)))
                    conn.commit() #ajoute le shiny dans la liste des shinys de l'utilisateur
                else :
                    c.execute("SELECT Normal_lien FROM events WHERE Event_id = ?",(eventID,))
                    lienPasShiny = c.fetchone()
                    embed = discord.Embed(title="RESET", description=f"Le {eventName[0]} n'est pas shiny... Dommage ! <a:pokewalking:725285728765870080>", color=0x2e8b57)
                    embed.set_image(url=lienPasShiny[0])
                    await ctx.channel.send(embed=embed)
            else : 
                embed = discord.Embed(title="ERREUR", description=f"Vous ne pouvez pas faire cela !", color=0x8B0000)
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/724993070114013337/725405379827204196/giphy_3.gif")
                timeRemaining = lastReset[0] - timeResetAllowed
                if timeRemaining < 60 :
                    embed.add_field(name="temps restant", value=f"vous devez encore attendre {timeRemaining} secondes.", inline=False)
                else :
                    timeRemaining = timeRemaining / 60
                    embed.add_field(name="temps restant", value=f"vous devez encore attendre {int(timeRemaining)} minutes.", inline=False)
                await ctx.channel.send(embed=embed)
        else :
            embed = discord.Embed(title="ERREUR", description=f"Aucun event nommé {event_name} n'a été trouvé.", color=0x8B0000)
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/724993070114013337/725405379827204196/giphy_3.gif")
            await ctx.channel.send(embed=embed)
            



@reset.error
async def reset_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument): #si aucun argument n'est donné, le bot donne la liste des events
        server = ctx.guild.id
        c.execute("SELECT event_name FROM events WHERE Server_id = ?",(server,))
        resultats = c.fetchall()
        message = "**Argument manquant**\n**Voici la liste des events actuels :**\n"
        for resultat in resultats:
            message += str(resultat[0]) + "\n"
        if message != "":
            embed = discord.Embed(title="RESET", description=message, color=0x2e8b57)
            await ctx.channel.send(embed=embed)



@bot.command() #donne la liste des shinys d'une personne
async def shiny(ctx, member: discord.Member = None):
    serverId = ctx.guild.id
    if member == None :
        member = ctx.message.author
    userId = member.id
    c.execute("SELECT event_name FROM USERS_DATA WHERE id_user = ? AND id_server = ?",(userId,serverId))
    resultats = c.fetchall()
    message = f"**Voici le(s) shiny(s) de {member} sur ce serveur :**\n"
    for resultat in resultats:
        message += str(resultat[0]) + "\n"
    if message != "":
        embed = discord.Embed(title="RESET", description=message, color=0x2e8b57)
        await ctx.channel.send(embed=embed)



loop = asyncio.get_event_loop()  # Create main loop
try:
    loop.run_until_complete(bot.start(botToken))  # Launch le bot in the main loop
except KeyboardInterrupt:
    # Keyboard interrupt stope la boucle et ferme la db
    conn.close()  #ferme la database
    loop.run_until_complete(bot.logout())

