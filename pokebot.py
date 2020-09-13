#included with python

from discord.ext.commands import has_permissions, CheckFailure
from random import randint
import asyncio
import time
from random import randint




#other
import discord
from discord.ext import commands
import pymongo

myclient = pymongo.MongoClient("<Your Mongo Connection URL>")
mydb = myclient["pokebotdb"]

botInviteLink = "<Your invite link>"



botOwnerId = <your id>
streamUrl = "https://www.twitch.tv/tokageki_"

gifError = "https://cdn.discordapp.com/attachments/724993070114013337/725405379827204196/giphy_3.gif"
gifWarning = "https://cdn.discordapp.com/attachments/724993070114013337/752586818419032115/ezgif-2-654548aaf3d8.gif"
gifNoProblem = "https://cdn.discordapp.com/attachments/724993070114013337/725413003607932938/DisastrousIllfatedDaddylonglegs-size_restricted.gif"


botToken = "<your token>"


#define the prefix with the db
def get_prefix(client, message):
    mycol = mydb["serverPrefix"]
    myquery = { "serverId": message.guild.id }
    result = mycol.find_one(myquery)
    if result == None :
        mydict = { "serverId": message.guild.id, "serverName": message.guild.name, "prefix": "." }
        mycol.insert_one(mydict)
        server_prefix = "."
    else :
        server_prefix = mycol.find_one( { "serverId": message.guild.id }, { "_id": 0, "serverName": 0, "serverId": 0} )
        server_prefix = server_prefix['prefix']
    return server_prefix
        



#define the prefix
bot = commands.Bot(command_prefix= get_prefix)

bot.remove_command("help")



@bot.event 
async def on_ready():
    #Définition du jeu du bot sur ".help"
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game('.help'))
    #Affiche que la connection a bien été effectuée
    print(f'connected as {bot.user} with mongodb.')



#help command
@bot.command()
async def help(ctx, command):
        #Commande help dans un "Embed" de couleur verte
        #reste des commandes
        embed = discord.Embed(title=f"available commands", description="List of available commands", color=0x2e8b57)
        embed.set_footer(text="T-PokeBot help")  
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/724993070114013337/725045208655593482/Tokabot.png")
        embed.set_author(name="T-Pokebot", url=botInviteLink, icon_url="https://cdn.discordapp.com/attachments/724993070114013337/725044258134032475/bowdenfond.jpg")
        if command == "bot" :
            embed.add_field(name=".help", value="display this menu", inline=False)
            embed.add_field(name=".changeprefix <prefix>", value="change the bot prefix (admins only)", inline=False)
        elif command == "game" :
            embed.add_field(name=".reset list", value="displays the list of available resets", inline=False)
            embed.add_field(name=".reset <eventName>", value="reset an event", inline=False)
            embed.add_field(name=".shiny <@user(optionnal)>", value="give a lists of the user's shinys", inline=False)
        elif command == "creation" :
            embed.add_field(name=".addreset <eventName> <rate> <shinyImage> <normalImage> <delay in minutes>", value="create a new event (admins only)", inline=False)
            embed.add_field(name=".delreset <eventName>", value="delete the event (admins only)", inline=False)
        elif command == "info" :
            embed.add_field(name=".invite", value="gives the bot invitation link", inline=False)
            embed.add_field(name="[support server]", value="https://discord.gg/C9Ju53W", inline=False)
        else : 
            embed.add_field(name="<:settings:754796965774229574> bot configuration", value="```.help bot```", inline=True)
            embed.add_field(name="<:gamepad:754790281827582074> game", value="```.help game```", inline=True)
            embed.add_field(name="🖌️ event creation", value="```.help creation```", inline=True)
            embed.add_field(name="<:info:754797358415347742> bot info", value="```.help info```", inline=True)
        await ctx.channel.send(embed=embed)
        #display developpement commands
        author = ctx.message.author
        if author == bot.get_user(botOwnerId):
        #Commande help dans un "Embed" de couleur rouge ne s'affichant que quand l'utilisateur entrant la commande est le propriétaire du bot
        #Cela me permet d'avoir dans mon help mes commandes de configuration du bot, étant bloquées pour les autres, ils n'ont pas besoin de les voir
            embed = discord.Embed(title="developpement commands", description="list of developpement commands", color=0x8B0000)
            #Commandes de developpement et de configuration du bot
            embed.add_field(name="listen/play/watch/stream <mot>", value="change bot status (bot owner only)", inline=False)
            embed.add_field(name="addemote <emote>", value="add an emote to the bot emote list (bot owner only)", inline=False)
            embed.add_field(name="addanimatedemote <emotename> <emoteid>", value="add an animated emote to the bot emote list (bot owner only)", inline=False)
            await ctx.channel.send(embed=embed)            
        #add a custom emote in reaction
        mycol = mydb["emotes"]
        numberOfEmotes = mycol.find_one()
        test = mycol.aggregate([{"$sample":{"size":1}}])
        emote = list(test)[0]["emoteData"]
        if numberOfEmotes == None : 
            embed = discord.Embed(title="EMOTE", description= "Think to add emote with the addemote command !", color=0xFF7F00)
            embed.set_thumbnail(url=gifWarning)
            await ctx.channel.send(embed=embed)
        else :
            await ctx.message.add_reaction(emote)

                              
@help.error
async def help_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title=f"available commands", description="List of available commands", color=0x2e8b57)
        embed.set_footer(text="T-PokeBot help")  
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/724993070114013337/725045208655593482/Tokabot.png")
        embed.set_author(name="T-Pokebot", url=botInviteLink, icon_url="https://cdn.discordapp.com/attachments/724993070114013337/725044258134032475/bowdenfond.jpg")
        embed.add_field(name="<:settings:754796965774229574> bot configuration", value="```.help bot```", inline=True)
        embed.add_field(name="<:gamepad:754790281827582074> game", value="```.help game```", inline=True)
        embed.add_field(name="🖌️ event creation", value="```.help creation```", inline=True)
        embed.add_field(name="<:info:754797358415347742> bot info", value="```.help info```", inline=True)
        await ctx.channel.send(embed=embed)


#migration faite
@bot.command()
async def addemote(ctx,*,emojiId): #ajoute une emote dans la liste des emotes custom que le bot peut utiliser
    author = ctx.message.author
    if author == bot.get_user(botOwnerId): #verifie que c'est le propriétaire qui utilise la commande 
        mycol = mydb["emotes"]
        mydict = { "emoteData": emojiId }
        mycol.insert_one(mydict)
        embed = discord.Embed(title="EMOTE", description=f"Emote {emojiId} added", color=0x2e8b57) #valide que l'emote a été ajoutée
        embed.set_thumbnail(url=gifNoProblem)
        await ctx.channel.send(embed=embed)   
    else : 
        embed = discord.Embed(title="ERROR", description=f"You can't do this !", color=0x8B0000)
        embed.set_thumbnail(url=gifError)
        await ctx.channel.send(embed=embed)

@addemote.error
async def addemote_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="ERROR", description=f"Missing Argument !", color=0x8B0000)
        embed.set_thumbnail(url=gifError)
        await ctx.channel.send(embed=embed)
        


#migration faite
@bot.command()
async def addanimatedemote(ctx, emoteName, emoteId):
    author = ctx.message.author
    if author == bot.get_user(botOwnerId):
        emote = f"<a:{emoteName}:{emoteId}>"
        mycol = mydb["emotes"]
        mydict = { "emoteData": emote }
        mycol.insert_one(mydict)
        embed = discord.Embed(title="ANIMATED EMOTE", description=f"Animated emote {emote} added.", color=0x2e8b57)
        embed.set_thumbnail(url=f"https://cdn.discordapp.com/emojis/{emoteId}.gif?v=1")
        await ctx.channel.send(embed=embed)
    else : 
        embed = discord.Embed(title="ERROR", description=f"You can't do this !", color=0x8B0000)
        embed.set_thumbnail(url=gifError)
        await ctx.channel.send(embed=embed)

@addanimatedemote.error
async def addanimatedemote_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument): #si aucun argument n'est donné, le bot donne la liste des events
        embed = discord.Embed(title="ERROR", description=f"Missing argument !", color=0x8B0000)
        embed.set_thumbnail(url=gifError)
        await ctx.channel.send(embed=embed)
        

@bot.command()
async def invite(ctx):
        embed = discord.Embed(title="bot invite link", description=botInviteLink, color=0x2e8b57)
        embed.set_footer(text="T-PokeBot invite link")  
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/724993070114013337/725045208655593482/Tokabot.png")
        embed.set_author(name="T-Pokebot", url=botInviteLink, icon_url="https://cdn.discordapp.com/attachments/724993070114013337/725044258134032475/bowdenfond.jpg")
        await ctx.channel.send(embed=embed)
        
        

@bot.command()
@commands.has_permissions(administrator=True)
async def changeprefix(ctx, mot2):
    mycol = mydb["serverPrefix"]
    myquery = { "serverId": ctx.guild.id }
    newvalues = { "$set": { "prefix": mot2 } }
    mycol.update_one(myquery, newvalues)
    embed = discord.Embed(title="PREFIX", description=f'The prefix has been changed to "{mot2}"', color=0x2e8b57)
    embed.set_thumbnail(url=gifNoProblem)
    await ctx.channel.send(embed=embed)



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
            embed = discord.Embed(title="RESET", description=f"the reset {event_name} has been added", color=0x2e8b57)
            embed.set_thumbnail(url=gifNoProblem)
            await ctx.channel.send(embed=embed)
            await ctx.message.delete()
        else :
            embed = discord.Embed(title="ERROR", description=f"An event with this name has already been created!", color=0x8B0000)
            embed.set_thumbnail(url=gifError)
            await ctx.channel.send(embed=embed)
    except:
        embed = discord.Embed(title="ERROR", description=f"The rate entered is not valid.", color=0x8B0000)
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
        embed = discord.Embed(title="ERROR", description=f"No event named {event_name} was found.", color=0x8B0000)
        embed.set_thumbnail(url=gifError)
        await ctx.channel.send(embed=embed)
    else :
        numberOfEvent = mycol.delete_one(myquery)
        embed = discord.Embed(title="RESET", description=f"The event {event_name} has been successfully deleted", color=0x2e8b57)
        embed.set_thumbnail(url=gifNoProblem)
        await ctx.channel.send(embed=embed)
        




@bot.command() #change le statut du bot
async def watch(ctx,*,film):
    author = ctx.message.author
    if author == bot.get_user(botOwnerId):
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=film))
        embed = discord.Embed(title="WATCH", description=f'Status changed to "__**watch {movie}**__".', color=0x2e8b57)
        embed.set_thumbnail(url=gifNoProblem)
        await ctx.channel.send(embed=embed)
    else :
        embed = discord.Embed(title="ERROR", description=f"You can't do this !", color=0x8B0000)
        embed.set_thumbnail(url=gifError)
        await ctx.channel.send(embed=embed)


@bot.command() #change le statut du bot
async def stream(ctx,*,stream):
    author = ctx.message.author
    if author == bot.get_user(botOwnerId):
        await bot.change_presence(activity=discord.Streaming(name=stream, url=streamUrl))
        embed = discord.Embed(title="STREAM", description=f'Status changed to "__**stream {stream}**__".', color=0x2e8b57)
        embed.set_thumbnail(url=gifNoProblem)
        await ctx.channel.send(embed=embed)
    else :
        embed = discord.Embed(title="ERROR", description=f"You can't do this !", color=0x8B0000)
        embed.set_thumbnail(url=gifError)
        await ctx.channel.send(embed=embed)


@bot.command() #change le statut du bot
async def listen(ctx,*,music):
    author = ctx.message.author
    if author == bot.get_user(botOwnerId):
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=music))
        embed = discord.Embed(title="LISTEN", description=f'Status changed to "__**listen {music}**__".', color=0x2e8b57)
        embed.set_thumbnail(url=gifNoProblem)
        await ctx.channel.send(embed=embed)
    else :
        embed = discord.Embed(title="ERROR", description=f"You can't do this !", color=0x8B0000)
        embed.set_thumbnail(url=gifError)
        await ctx.channel.send(embed=embed)
#traduit jusqu'ici

@bot.command() #change le statut du bot 
async def play(ctx,*,game):
    author = ctx.message.author
    if author == bot.get_user(botOwnerId):
        await bot.change_presence(activity=discord.Game(name=game))
        embed = discord.Embed(title="PLAY", description=f'Status changed to "__**play {game}**__".', color=0x2e8b57)
        embed.set_thumbnail(url=gifNoProblem)
        await ctx.channel.send(embed=embed)
    else :
        embed = discord.Embed(title="ERROR", description=f"You can't do this !", color=0x8B0000)
        embed.set_thumbnail(url=gifError)
        await ctx.channel.send(embed=embed)



@bot.command() #reset command
async def reset(ctx, event_name):
    mycol = mydb["resets"]
    #display the list of event if event name == list
    if event_name == None or event_name == "list" : 
        myquery = { "serverId": ctx.guild.id }
        message = "__**Current events:**__\n"
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
                    embed = discord.Embed(title="RESET", description=f"**The {data['resetName']} is shiny ! Well done ! <a:charizardDancing:725281864297873428>**", color=0xd79a10)
                    lien = data["lienShiny"]
                    embed.set_image(url=lien)
                    await ctx.channel.send(embed=embed)
                    mycolShinyUser = mydb["userData"]
                    mydict = { "userId": userId, "serverId": ctx.guild.id, "eventName": event_name, "userName": ctx.message.author.name, "serverName": ctx.guild.name}
                    mycolShinyUser.insert_one(mydict)

                else :
                    lien = data["lienNormal"]
                    embed = discord.Embed(title="RESET", description=f"The {data['resetName']} is not shiny ... it will be for another time ! <a:pokewalking:725285728765870080>", color=0x2e8b57)
                    embed.set_image(url=lien)
                    await ctx.channel.send(embed=embed)
                    
            else :
                embed = discord.Embed(title="ERROR", description=f"You can't do this !", color=0x8B0000)
                embed.set_thumbnail(url=gifError)
                timeRemaining = lastReset - timeResetAllowed
                if timeRemaining < 60 :
                    embed.add_field(name="TIME LEFT", value=f"Please wait {timeRemaining} second(s) before using this command again.", inline=False)
                else :
                    timeRemaining = timeRemaining / 60
                    embed.add_field(name="TIME LEFT", value=f"Please wait {timeRemaining} minute(s) before using this command again.", inline=False)
                await ctx.channel.send(embed=embed)

        else :
            embed = discord.Embed(title="ERROR", description=f"No event named {event_name} was found.", color=0x8B0000)
            embed.set_thumbnail(url=gifError)
            await ctx.channel.send(embed=embed)



@reset.error
async def reset_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument): #si aucun argument n'est donné, le bot donne la liste des events
        mycol = mydb["resets"]
        myquery = { "serverId": ctx.guild.id }
        message = "**Missing argument**\n\n__**Current events :**__\n"
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
    message = f"**list of {member}'s shiny(s) on this server :**\n"
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
        embed = discord.Embed(title="ERROR", description=f"No shiny was found in {member.name}'s list.", color=0x8B0000)
        embed.set_thumbnail(url=gifError)
        await ctx.channel.send(embed=embed)
    else :
        numberOfEvent = mycol.delete_one(myquery)
        embed = discord.Embed(title="SHINYS", description=f"{Member.name}'s shinys have been deleted", color=0x2e8b57)
        embed.set_thumbnail(url=gifNoProblem)
        await ctx.channel.send(embed=embed)




@clearshiny.error
async def clearshiny_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title="ERREUR", description=f"You can't do this !", color=0x8B0000)
        embed.set_thumbnail(url=gifError)
        await ctx.channel.send(embed=embed)




loop = asyncio.get_event_loop()  # Create main loop
try:
    loop.run_until_complete(bot.start(botToken))  
except KeyboardInterrupt:
    loop.run_until_complete(bot.logout())

