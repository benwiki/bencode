from dataclasses import dataclass, field
from typing import Optional
import discord
from discord.ext import commands
import random
from time import sleep

client = commands.Bot(command_prefix=".")

people: dict[str, list[str]] = {}
points: dict[str, int] = {}
starting_people: list[str] = []
available_articles: list[tuple[str, str]] = []
gamechannel = None
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


def reset():
    global people, round, points, starting_people, available_articles, game_started, gamechannel, reset_confirmation, guesser, person_to_guess
    people = {}
    points = {}
    starting_people = []
    available_articles = []
    gamechannel = None
    game_started = False
    reset_confirmation = True
    guesser = None
    round = 1
    person_to_guess = None


@client.event
async def on_ready():
    print("I'm ready.", str(client.user))

@client.event
async def on_message(msg):
    global people, round, points, starting_people, available_articles, game_started, gamechannel, reset_confirmation, guesser, person_to_guess

    if not msg.content.startswith("-reset"):
        reset_confirmation = True

    author = msg.author.name

    # reset
    # start
    # set, setguesser, rollguesser, participate, setchannel
    # stop, guess, get
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
            if author != guesser:
                await msg.channel.send("You are not the guesser!")
                return True
            if id == "get" and person_to_guess is not None:
                await msg.channel.send("You must guess before asking for a new one!")
                return True
        if id in ('set', 'rollguesser', 'setguesser', 'participate', 'setchannel', 'start'):
            if game_started:
                await msg.channel.send("The game has already started!")
                return True
            if id != 'participate' and author not in people:
                await msg.channel.send(f"{author}, you need to [-participate]!")
                return True
            if id == 'participate' and author in people:
                await msg.channel.send(f"{author}, you're already in!")
                return True
            if id == "start" and guesser is None:
                await msg.channel.send(f"There's no guesser yet!\n"
                "Type [-rollguesser] to select guesser randomly,\n"
                "or [-setguesser {name\_without\_#id}] to set guesser manually!")
                return True
        
        return False
    #-------------------------------------------------------------------------------------------------------
    if msg.content.startswith("-get"):
        if await issue('get'): return
        art_with_P = random.choice(available_articles)
        article, person_to_guess = art_with_P
        available_articles.remove(art_with_P)
        await msg.channel.send(f'"{article}"')    
    #-------------------------------------------------------------------------------------------------------
    elif msg.content.startswith("-guess"):
        if await issue('guess'): return
        guess = msg.content[7:]
        if guess == "":
            await gamechannel.send("You didn't mention anybody!\nThe correct way: [-setguesser {name\_without\_#id}]")
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
                reset()
            else:
                await gamechannel.send("Points:\n - " + '\n - '.join(f"{P}: {pt}" for P, pt in points.items()))
                await gamechannel.send(f"Round {round}!")
                person_to_guess = None
            

    #-------------------------------------------------------------------------------------------------------
    elif msg.content.startswith("-stop"):
        if await issue('stop'): return
        await gamechannel.send("Game is over!\n"
                                + "Points:\n - " + '\n - '.join(f"{P}: {pt}" for P, pt in points.items()) + '\n'
                                + f"Winner(s): {', '.join(cluster_by_points(points)[max(points.values())])}"
        )
        reset()
    
    ############################################################################################################

    elif msg.content.startswith("-setchannel"):
        if await issue('setchannel'): return
        gamechannel = msg.channel
        await msg.channel.send(f'Channel "{gamechannel}" set as game channel!')
    #-------------------------------------------------------------------------------------------------------
    elif msg.content.startswith("-participate"):
        if await issue('participate'): return
        people[author] = []
        await msg.channel.send(f"You're in, {author}!")
    #-------------------------------------------------------------------------------------------------------
    elif msg.content.startswith("-rollguesser"):
        if await issue('rollguesser'): return
        guesser = random.choice(list(people.keys()))
        available_articles = [(word, P) for P, words in people.items() for word in words if P != guesser]
        await gamechannel.send(f"The guesser is: {guesser}! Aye aye, Captain!\nEveryone, type [-start] to start the game!")
    #-------------------------------------------------------------------------------------------------------
    elif msg.content.startswith("-setguesser"):
        if await issue('setguesser'): return
        guesser = msg.content[12:]
        if guesser == "":
            await gamechannel.send("You gave me no guesser to set!")
        elif guesser not in people:
            await gamechannel.send(f"I don't know {guesser}... Did (s)he [-participate]?")
        else:
            available_articles = [(word, P) for P, words in people.items() for word in words if P != guesser]
            await gamechannel.send(f"The guesser is: {guesser}! Aye aye, Captain!\nEveryone, type [-start] to start the game!")
    #-------------------------------------------------------------------------------------------------------
    elif msg.content.startswith("-set"):
        if await issue('set'): return
        article = msg.content[5:]
        if len(article) > 0:
            people[author] = people.get(author, []) + [article]
            await msg.channel.send(article+" stored. All articles:\n - " + "\n - ".join(people[author]))
        else:
            await msg.channel.send("You gave me nothin' to set")
    #-------------------------------------------------------------------------------------------------------
    elif msg.content.startswith("-start"):
        if await issue('start'): return
        article_num = len(people[author])
        if article_num == 0:
            await gamechannel.send(f"{author}, you did't give any articles yet!")
        elif article_num < len(people)-1:
            await gamechannel.send(f"{author}, you only have {article_num} articles, you need at least {len(people)-1}!")
        elif author in starting_people:
            await gamechannel.send(f"{author}, you already voted for start!")
        else:
            starting_people.append(author)
            people_num_diff = len(people)-len(starting_people)
            if people_num_diff == 0:
                await gamechannel.send(f'{author} was the last one to vote! Game begins with people:\n - ' + '\n - '.join(starting_people))
                await gamechannel.send(f">>> Round 1! <<<\n{guesser}, you may [-get] the first article!")
                points = {P: 0 for P in people}
                game_started = True
            else:
                await gamechannel.send(f"{author} votes for a start! People remaining:\n - "
                + '\n - '.join(P for P in people if P not in starting_people))
    #-------------------------------------------------------------------------------------------------------
    elif msg.content.startswith("-reset"):
        if reset_confirmation:
            await msg.channel.send("Are you sure? If yes, -reset again! If no, -yeet!")
            reset_confirmation = False
            return
        reset()
        await msg.channel.send("Reset done")
    #-------------------------------------------------------------------------------------------------------
    elif msg.content.startswith("-greet"):
        await msg.channel.send("Hi I'm here!")
    #-------------------------------------------------------------------------------------------------------
    elif msg.content.startswith("-yeet"):
        await msg.channel.send("ʇǝǝʎ")
    #-------------------------------------------------------------------------------------------------------
    elif msg.content.startswith("-debug"):
        await msg.channel.send('\n'.join(map(str, (people, points, starting_people, available_articles, gamechannel, game_started, reset_confirmation, guesser, round, person_to_guess))))

client.run('NzEzMDQ0NjU2MTAzMDk2Mzky.Xs5xDQ.j3Rkcn6uLPO0-mqOjJUmMl41_Pw')