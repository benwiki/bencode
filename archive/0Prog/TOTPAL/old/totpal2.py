from dataclasses import dataclass, field
import re
from typing import Optional
import discord
from discord.ext import commands
import random
from time import sleep

client = commands.Bot(command_prefix=".")

people: dict[str, list[str]] = {}
points: dict[str, int] = {}
starting_people: list[str] = []
speakers: list[str] = []
gamechannel: Optional[discord.TextChannel] = None
game_started: bool = False
reset_confirmation: bool = True
guesser: Optional[str] = None
person_to_guess: Optional[str] = None
round: int = 1


async def swap_key_value(d: dict) -> dict:
    return {value: key for key, value in d.items()}


def cluster_by_points(points: dict[str, int]) -> dict[int, list[str]]:
    cluster: dict[int, list[str]] = {}
    for name, pt in points.items():
        cluster[pt] = cluster.get(pt, []) + [name]
    return cluster


def reset(full=True):
    global people, round, points, starting_people, speakers, game_started, gamechannel, reset_confirmation, guesser, person_to_guess
    if full:
        people = {}
        gamechannel = None
        points = {}
    starting_people = []
    speakers = []
    game_started = False
    reset_confirmation = True
    guesser = None
    round = 1
    person_to_guess = None


@client.event
async def on_ready():
    print("I'm ready.", str(client.user))

@client.event
async def on_message(msg: discord.Message):
    print(str(msg.author), repr(msg.author), str(msg.content), repr(msg.content))
    global people, round, points, starting_people, speakers, game_started, gamechannel, reset_confirmation, guesser, person_to_guess

    if not msg.content.startswith("-reset"):
        reset_confirmation = True

    author_name = msg.author.name
    # help
    # participate, set, delete, show, setchannel, setguesser, rollguesser
    # start, get, cancel, guess, stop
    # reset
    async def issue(id: str):
        if id in ('get', 'guess', 'stop', 'start', 'setguesser', 'rollguesser'):
            if gamechannel is None:
                await msg.channel.send(f"No channel specified. Type [-setchannel] in the selected channel!")
                return True
            if msg.channel is not gamechannel:
                await msg.channel.send("This is not the specified game channel!")
                return True
        if id in ('get', 'guess', 'stop'):
            if not game_started:
                await msg.channel.send("The game has not started yet!")
                return True
            if author_name != guesser:
                await msg.channel.send("You are not the guesser!")
                return True
            if id == "get" and person_to_guess is not None:
                await msg.channel.send("You must guess before asking for a new one!")
                return True
        if id in ('set', 'delete', 'rollguesser', 'setguesser', 'participate', 'setchannel', 'start'):
            if game_started:
                await msg.channel.send("The game has already started!")
                return True
            if id != 'participate' and author_name not in people:
                await msg.channel.send(f"{author_name}, you need to [-participate]!")
                return True
            if id == 'participate' and author_name in people:
                await msg.channel.send(f"{author_name}, you're already in!")
                return True
            if id == "start" and guesser is None:
                await msg.channel.send(f"There's no guesser yet!\n"
                "Type [-rollguesser] to select guesser randomly,\n"
                "or [-setguesser {name\_without\_#id}] to set guesser manually!")
                return True
        
        return False
    #-------------------------------------------------------------------------------------------------------
    if msg.content == "-help":
        await msg.channel.send("Coming soon...")
    #-------------------------------------------------------------------------------------------------------
    elif msg.content == "-get":
        if await issue('get'): return
        right_person = random.choice(speakers)
        # article, person_to_guess = art_with_P
        # speakers.remove(art_with_P)
        random_article = random.choice(people[right_person])
        person_to_guess = right_person
        people[right_person].remove(random_article)
        await msg.channel.send(f'"{random_article}"')
    #-------------------------------------------------------------------------------------------------------
    elif msg.content == "-cancel":
        if await issue('cancel'): return
        if gamechannel is not None:
            await gamechannel.send("Article canceled.")
        person_to_guess = None
    #-------------------------------------------------------------------------------------------------------
    elif msg.content.startswith("-guess"):
        if await issue('guess'): return
        guess = msg.content[7:]
        if guess == "":
            await gamechannel.send("You didn't mention anybody!\nThe correct way is: [-setguesser {name\_without\_#id}]")
        elif guesser not in people:
            await gamechannel.send(f"I don't know {guess}... Name sb else!")
        elif guess == guesser:
            await gamechannel.send(f"You can't make a guess on yourself!")
        else:
            await gamechannel.send("That's...")
            sleep(2)
            if guess == person_to_guess:
                await gamechannel.send(f"...right!!! The article was {guess}'s.\n"
                                       f"+1 to {guesser}, +1 to {guess}.")
                points[guesser] += 1
                points[guess] += 1
            else:
                await gamechannel.send(f"...false:( The article was {person_to_guess}'s!\n"
                                       f"+1 to {guess}.")
                points[guess] += 1
            round += 1
            if round == len(people):
                await gamechannel.send("The last round has ended, the Game is over!\n"
                                "Points:\n - " + '\n - '.join(f"{P}: {pt}" for P, pt in points.items()) + '\n'
                                f"Winner(s): {', '.join(cluster_by_points(points)[max(points.values())])}\n"
                                "Congratulations! :tada:"
                      )
                reset(full=False)
            else:
                await gamechannel.send("Points:\n - " + '\n - '.join(f"{P}: {pt}" for P, pt in points.items()))
                await gamechannel.send(f">>> Round {round}!")
                person_to_guess = None
            

    #-------------------------------------------------------------------------------------------------------
    elif msg.content == "-stop":
        if await issue('stop'): return
        await gamechannel.send("Game is over!\n"
                                + "Points:\n - " + '\n - '.join(f"{P}: {pt}" for P, pt in points.items()) + '\n'
                                + f"Winner(s): {', '.join(cluster_by_points(points)[max(points.values())])}"
        )
        reset(full=False)
    
    ############################################################################################################

    elif msg.content == "-setchannel":
        if await issue('setchannel'): return
        gamechannel = msg.channel
        await msg.channel.send(f'Channel "{gamechannel}" set as game channel!')
    #-------------------------------------------------------------------------------------------------------
    elif msg.content == "-participate":
        if await issue('participate'): return
        people[author_name] = []
        await msg.channel.send(f"You're in, {author_name}!")
    #-------------------------------------------------------------------------------------------------------
    elif msg.content == "-rollguesser":
        if await issue('rollguesser'): return
        guesser = random.choice(list(people))
        await gamechannel.send(f"The guesser is: {guesser}! Aye aye, Captain!\nEveryone, type [-start] to start the game!")
    #-------------------------------------------------------------------------------------------------------
    elif msg.content.startswith("-setguesser"):
        if await issue('setguesser'): return
        guesser = msg.content[12:]
        if guesser == "":
            await gamechannel.send("You gave me no guesser to set!")
        elif msg.content[len("-setguesser")] != " ":
            await msg.channel.send("Wrong command!")
        elif guesser not in people:
            await gamechannel.send(f"I don't know {guesser}... Did (s)he [-participate]?")
        else:
            await gamechannel.send(f"The guesser is: {guesser}! Aye aye, Captain!\nEveryone, type [-start] to start the game!")
    #-------------------------------------------------------------------------------------------------------
    elif msg.content.startswith("-set"):
        if await issue('set'): return
        article = msg.content[5:]
        if len(article) == 0:
            await msg.channel.send("You gave me nothin' to set!")
        elif msg.content[len("-set")] != " ":
            await msg.channel.send("Wrong command!")
        else:
            people[author_name] = people.get(author_name, []) + [article]
            await msg.channel.send(f'"{article}" stored. Your articles:\n - {"\n - ".join(people[author_name])}')
    #-------------------------------------------------------------------------------------------------------
    elif msg.content.startswith("-delete"):
        if await issue('set'): return
        article = msg.content[len("-delete")+1:]
        if len(article) == 0:
            await msg.channel.send("You gave me nothin' to delete!")
        elif msg.content[len("-delete")] != " ":
            await msg.channel.send("Wrong command!")
        else:
            try:
                people[author_name].remove(article)
                await msg.channel.send(f'"{article}" deleted! Your articles:\n - {"\n - ".join(people[author_name])}')
            except ValueError:
                await msg.channel.send(f"You don't have any article called \"{article}\"")
    #-------------------------------------------------------------------------------------------------------
    elif msg.content == "-start":
        if await issue('start'): return
        article_num = len(people[author_name])
        if author_name != guesser and article_num == 0:
            await gamechannel.send(f"{author_name}, you did't give any articles yet!")
        elif author_name != guesser and article_num < len(people)-1:
            await gamechannel.send(f"{author_name}, you only have {article_num} articles, you need at least {len(people)-1}!")
        elif author_name in starting_people:
            await gamechannel.send(f"{author_name}, you already voted for start!")
        else:
            starting_people.append(author_name)
            people_num_diff = len(people)-len(starting_people)
            if people_num_diff == 0:
                await gamechannel.send(f'{author_name} was the last one to vote! Game begins with people:\n - ' + '\n - '.join(starting_people))
                await gamechannel.send(f">>> Round 1!\n{guesser}, you may [-get] the first article!")
                points = {P: 0 for P in people}
                # speakers = [(word, P) for P, words in people.items() for word in words if P != guesser]
                speakers = [mensch for mensch in people if mensch != guesser]
                game_started = True
            else:
                await gamechannel.send(f"{author_name} votes for a start! People remaining:\n - "
                + '\n - '.join(P for P in people if P not in starting_people))
    #-------------------------------------------------------------------------------------------------------
    elif msg.content == "-reset":
        if reset_confirmation:
            await msg.channel.send("Are you sure? If yes, -reset again! If no, -yeet!")
            reset_confirmation = False
            return
        reset()
        await msg.channel.send("Reset done")
    ########################################################################################################
    elif msg.content == "-greet":
        await msg.channel.send("Hi I'm here!")
    #-------------------------------------------------------------------------------------------------------
    elif msg.content == "-yeet":
        await msg.channel.send("ʇǝǝʎ")
    #-------------------------------------------------------------------------------------------------------
    elif msg.content == "-debug":
        await msg.channel.send('\n'.join(map(str, (people, points, starting_people, speakers, gamechannel, game_started, reset_confirmation, guesser, round, person_to_guess))))
    else:
        await msg.channel.send("Wrong command!")
    # elif msg.content.startswith

client.run('NzEzMDQ0NjU2MTAzMDk2Mzky.Xs5xDQ.j3Rkcn6uLPO0-mqOjJUmMl41_Pw')