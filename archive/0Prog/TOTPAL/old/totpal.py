import discord
from discord.ext import commands
from random import randint

client = commands.Bot(command_prefix = ".")

people: dict[str, list[str]] = {}
starting_people: list[str] = []
gamechannel: str = ''

@client.event
async def on_ready():
    print("ready,", str(client.user))

@client.event
async def on_message(msg):
    
    global people, gamechannel
    
    if msg.content.startswith("-setchannel"):
        gamechannel = msg.channel.id
    
    if msg.content.startswith("-participate"):
        people[str(msg.author)] = []
        await msg.channel.send(f"You're in, {msg.author}!")

    if msg.content.startswith("-set"):
        author = str(msg.author)
        if author not in people:
            await msg.channel.send(f"{msg.author}, you need to -participate!")
        else:
            word = msg.content[4:]
            if len(word) > 0:
                people[author].append(word)
                await msg.channel.send(msg.content[4:]+" stored. All words:\n - " + "\n - ".join(people[author]))
            else:
                await msg.channel.send("You gave me nothin' to set")
        
    if msg.content.startswith("-start"):
        author = str(msg.author)
        if len(people[author]) == 0:
            await msg.channel.send(f"{author}, you did't give any words yet!")
        # elif len(people[msg.author]) < len(people):
        #     await msg.channel.send(f"{msg.author}, you only have {len(people[msg.author])} words, you need at least {len(people)}!")
        elif author not in people:
            await msg.channel.send(f"{author}, you need to -participate!")
        elif author in starting_people:
            await msg.channel.send(f"{author}, you already voted for start!")
        else:
            starting_people.append(author)
            people_num_diff = len(people)-len(starting_people)
            if people_num_diff == 0:
                await msg.channel.send(f'{author} was the last one to vote! Game begins with people:\n - ' + '\n - '.join(starting_people))
                
            else:
                await msg.channel.send(f"{author} votes for a start! People remaining:\n - " + '\n - '.join(P for P in people if P not in starting_people))
            
    if msg.content.startswith("-reset"):
        people = {}
        await msg.channel.send("Reset done")
        
    if msg.content.startswith("-greet"):
        await msg.channel.send("Hi I'm here!")
        
    if msg.content.startswith("-yeet"):
        await msg.channel.send("ʇǝǝʎ")

client.run('NzEzMDQ0NjU2MTAzMDk2Mzky.Xs5xDQ.j3Rkcn6uLPO0-mqOjJUmMl41_Pw')
