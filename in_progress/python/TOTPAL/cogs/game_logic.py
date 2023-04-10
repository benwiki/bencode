from lib2to3.pytree import generate_matches
import random
import re
from time import sleep
from typing import Optional
import discord
from discord.ext import commands

Fellow = discord.User | discord.Member


class GameLogic(commands.Cog):

    def __init__(self, client):
        self.client = client

        self.people: dict[Fellow, list[str]] = {}
        self.points: dict[Fellow, int] = {}
        self.starting_people: list[Fellow] = []
        self.speakers: list[Fellow] = []
        self.gamechannel: Optional[discord.TextChannel] = None
        self.game_started: bool = False
        self.reset_confirmation: bool = True
        self.guesser: Optional[Fellow] = None
        self.person_to_guess: Optional[Fellow] = None
        self.round: int = 1
        self.confirmation_message: Optional[discord.Message] = None

        self.resetmessage = "Full reset or reset points? React on this message with :regional_indicator_f: (full) / :regional_indicator_p: (points)"
        self.conf_message = "Are you sure? React on this message with :white_check_mark: (yes) / :x: (no) / :a: (always)!"

        self.number = {
            1: "one",
            2: "two",
            3: "three",
            4: "four",
            5: "five",
            6: "six",
            7: "seven",
            8: "eight",
            9: "nine"
        }

        try:
            self.confirmation = eval(open("confirmation.txt", "r").read())
        except FileNotFoundError:
            self.confirmation = {
                'full_reset': '-',
                'point_reset': '-'
            }
            with open("confirmation.txt", "w") as f:
                f.write(str(self.confirmation))

    def cluster_by_points(self, points: dict[Fellow, int]) -> dict[int, list[str]]:
        cluster: dict[int, list[str]] = {}
        for user, pt in points.items():
            cluster[pt] = cluster.get(pt, []) + [user.name]
        return cluster

    def reset(self, full=True):
        if full:
            self.people = {}
            self.gamechannel = None
            self.points = {}
        self.starting_people = []
        self.speakers = []
        self.game_started = False
        self.guesser = None
        self.round = 1
        self.person_to_guess = None

    def user_by_id(self, id: int) -> Optional[Fellow]:
        for user in self.people:
            if user.id == id:
                return user
        return None

    def mention(self, command: str, msg: discord.Message, error_msg: str):
        def take_func(func):
            async def wrapper():
                match = re.fullmatch(command + r" <@!(\d+)>", msg.content)
                if match is not None:
                    id = int(match.group(1))
                    mentioned = self.user_by_id(id)
                    if mentioned is not None:
                        await func(mentioned)
                    else:
                        await self.gamechannel.send("I don't know this person... Do they [-play]?")
                else:
                    await self.gamechannel.send(error_msg)
            return wrapper
        return take_func

# ###################################################################################################################

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        print(reaction.message.channel, self.gamechannel, reaction.message, self.confirmation_message, str(reaction.emoji))
        if reaction.message.channel == self.gamechannel:
            print("CHANNEL CORRECT")
            if reaction.message == self.confirmation_message:
                print("MESSAGE CORRECT")
                match str(reaction.emoji):
                    case "🇫":
                        if self.confirmation["full_reset"] == "A":
                            await self.gamechannel.send("Full reset done!")
                            self.confirmation_message = None
                            self.reset(full=True)
                        else:
                            self.confirmation["full_reset"] = "!"
                            self.confirmation_message = await self.gamechannel.send(self.conf_message)
                    case "🇵":
                        print("POINTS")
                        if self.confirmation["point_reset"] == "A":
                            self.points = {}
                            await self.gamechannel.send("Points resetted!")
                            self.confirmation_message = None
                        else:
                            self.confirmation["point_reset"] = "!"
                            self.confirmation_message = await self.gamechannel.send(self.conf_message)
                    case "✅":
                        print("dsldkssdas")
                        if self.confirmation["full_reset"] == "!":
                            self.confirmation["full_reset"] = "-"
                            await self.gamechannel.send("Full reset done!")
                            self.reset(full=True)
                        elif self.confirmation["point_reset"] == "!":
                            self.confirmation["point_reset"] = "-"
                            self.points = {}
                            await self.gamechannel.send("Points resetted!")
                        self.confirmation_message = None
                    case "🅰️":
                        if self.confirmation["full_reset"] == "!":
                            self.confirmation["full_reset"] = "A"
                            await self.gamechannel.send("Full reset done! No confirmation from now on!")
                            self.reset(full=True)
                        elif self.confirmation["point_reset"] == "!":
                            self.confirmation["point_reset"] = "A"
                            self.points = {}
                            await self.gamechannel.send("Points resetted! No confirmation from now on!")
                        self.confirmation_message = None
                    case "❌":
                        if self.confirmation["full_reset"] == "!":
                            self.confirmation["full_reset"] = "-"
                        elif self.confirmation["point_reset"] == "!":
                            self.confirmation["point_reset"] = "-"
                        await self.gamechannel.send("Reset canceled.")
                        self.confirmation_message = None

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        print(str(msg.author), repr(msg.author), msg.content)

        author_name = msg.author.name

        # ----- COMMANDS -----
        # help
        # play, set, delete, show, setchannel, setguesser, rollguesser
        # start, get, cancel, guess, stop
        # reset

        async def next_round():
            self.round += 1
            if self.round == len(self.people):
                await self.gamechannel.send("The last round has ended, the Game is over!\nPoints:\n - " + '\n - '.join(f"{P}: {pt}" for P, pt in self.points.items()) + "\n" + f"Winner(s): " + ', '.join(self.cluster_by_points(self.points)[max(self.points.values())]) + "\n" + "Congratulations! :tada:")
                self.reset(full=False)
            else:
                await self.gamechannel.send("Points:\n - " + '\n - '.join(f"{P}: {pt}" for P, pt in self.points.items()))
                await self.gamechannel.send(f">>> Round :{self.number[self.round]}:!")
                self.person_to_guess = None

        # ----------------------------------------------------------------------------------
        async def issue(id: str) -> bool:
            # --- DURING GAME ---
            if id in ('get', 'guess', 'stop', 'cancel'):
                if not self.game_started:
                    await msg.channel.send("The game has not started yet!")
                    return True
                if msg.author != self.guesser:
                    await msg.channel.send("You are not the guesser!")
                    return True
                if id == "get" and self.person_to_guess is not None:
                    await msg.channel.send("You must guess before asking for a new one!")
                    return True
            # --- BEFORE GAME ---
            if id in ('set', 'delete', 'show', 'rollguesser', 'setguesser', 'play', 'setchannel', 'start'):
                if self.game_started:
                    await msg.channel.send("The game has already started!")
                    return True
                if id != 'play' and msg.author not in self.people:
                    await msg.channel.send(f"{author_name}, you need to [-play]!")
                    return True
                if id == 'play' and msg.author in self.people:
                    await msg.channel.send(f"{author_name}, you're already in!")
                    return True
                if id == "start" and self.guesser is None:
                    await msg.channel.send("There's no guesser yet!\nType [-rollguesser] to select guesser randomly,\nor [-setguesser @name] to set guesser manually!")
                    return True
                if id == "start" and not self.speakers:
                    await msg.channel.send("How do you plan to play the game alone? `:P`")
                    return True
            # --- CHANNEL SPECIFICATION ---
            if id in ('get', 'cancel', 'guess', 'stop', 'start', 'setguesser', 'rollguesser', 'reset'):
                if self.gamechannel is None:
                    await msg.channel.send("No channel specified. Type [-setchannel] in the selected channel!")
                    return True
                if msg.channel is not self.gamechannel:
                    await msg.channel.send("This is not the specified game channel!")
                    return True
            # --- NO ISSUE ---
            return False
        # -------------------------------------------------------------------------------------------------------
        # #######################################################################################################
        # -------------------------------------------------------------------------------------------------------
        if msg.content == "-help":
            await msg.channel.send(
    """Available commands:
[GENERAL]
-help (display this help message)
-reset (
[BEFORE GAME]
-play (join game)
-set
-delete
-show
-setchannel
-setguesser
-rollguesser
[DURING GAME]
-start
-get
-cancel
-guess
-stop""")
        # -------------------------------------------------------------------------------------------------------
        elif msg.content == "-get":
            if await issue('get'):
                return
            right_person = random.choice(self.speakers)
            random_article = random.choice(self.people[right_person])
            self.person_to_guess = right_person
            self.people[right_person].remove(random_article)
            await msg.channel.send(f'"{random_article}"')
        # -------------------------------------------------------------------------------------------------------
        elif msg.content == "-cancel":
            if await issue('cancel'):
                return
            self.person_to_guess = None
            await self.gamechannel.send("Article canceled.")
        # -------------------------------------------------------------------------------------------------------
        elif msg.content.startswith("-guess"):
            if await issue('guess'):
                return

            @self.mention("-guess", msg, "The correct way to guess is: [-guess @name]")
            async def guess(mentioned):
                if mentioned.id == self.guesser.id:
                    await self.gamechannel.send(f"You can't make a guess on yourself!")
                else:
                    await self.gamechannel.send("That's...")
                    sleep(2)
                    if mentioned.id == self.person_to_guess.id:
                        await self.gamechannel.send(f"...right!!! The article was {mentioned.name}'s.\n+1 to {self.guesser.name}, +1 to {mentioned.name}.")
                        self.points[self.guesser] += 1
                        self.points[mentioned] += 1
                    else:
                        await self.gamechannel.send(f"...false:( The article was {self.person_to_guess.name}'s!\n+1 to {mentioned.name}.")
                        self.points[mentioned] += 1
                    await next_round()
            await guess()

        # -------------------------------------------------------------------------------------------------------
        elif msg.content == "-stop":
            if await issue('stop'):
                return
            await self.gamechannel.send("Game is over!\nPoints:\n - " + '\n - '.join(f"{P}: {pt}" for P, pt in self.points.items()) + '\n' + f"Winner(s): " + ', '.join(self.cluster_by_points(self.points)[max(self.points.values())]))
            self.reset(full=False)

        # ###########################################################################################################

        elif msg.content == "-setchannel":
            if await issue('setchannel'):
                return
            self.gamechannel = msg.channel
            await msg.channel.send(f'Channel "{self.gamechannel}" set as game channel!')
        # -------------------------------------------------------------------------------------------------------
        elif msg.content == "-play":
            if await issue('play'):
                return
            self.people[msg.author] = []
            await msg.channel.send(f"You're in, {author_name}!")
            if self.gamechannel is None:
                self.gamechannel = msg.channel
                await msg.channel.send(f'Channel "{self.gamechannel}" automatically set as game channel!')
        # -------------------------------------------------------------------------------------------------------
        elif msg.content == "-rollguesser":
            if await issue('rollguesser'):
                return
            self.guesser = random.choice(list(self.people))
            await self.gamechannel.send(f"The guesser is: {self.guesser.name}! Aye aye, Captain!\nEveryone, type [-start] to start the game!")
        # -------------------------------------------------------------------------------------------------------
        elif msg.content.startswith("-setguesser"):
            if await issue('setguesser'):
                return

            @self.mention("-setguesser", msg, "The correct way to set a guesser is: [-setguesser @name]")
            async def setguesser(pot_guesser):
                self.guesser = pot_guesser
                await self.gamechannel.send(f"The guesser is: {self.guesser.name}! Aye aye, Captain!\n" + "Everyone, type [-start] to start the game!")
            await setguesser()
        # -------------------------------------------------------------------------------------------------------
        elif msg.content.startswith("-set"):
            if await issue('set'):
                return
            article = msg.content[len("-set")+1:]
            if len(article) == 0:
                await msg.channel.send("You gave me nothin' to set!")
            elif msg.content[len("-set")] != " ":
                await msg.channel.send("Wrong command!")
            else:
                print(article, self.people[msg.author], msg.author)
                self.people[msg.author] = self.people.get(msg.author, []) + [article]
                await msg.channel.send(f'"{article}" stored. Your articles:\n - ' + "\n - ".join(self.people[msg.author]))
        # -------------------------------------------------------------------------------------------------------
        elif msg.content.startswith("-delete"):
            if await issue('set'):
                return
            article = msg.content[len("-delete")+1:]
            if len(article) == 0:
                await msg.channel.send("You gave me nothin' to delete!")
            elif msg.content[len("-delete")] != " ":
                await msg.channel.send("Wrong command!")
            else:
                try:
                    self.people[msg.author].remove(article)
                    await msg.channel.send(f'"{article}" deleted! Your articles:\n - ' + "\n - ".join(self.people[msg.author]))
                except ValueError:
                    await msg.channel.send(f"You don't have any articles called \"{article}\"")
        # -------------------------------------------------------------------------------------------------------
        elif msg.content == "-show":
            if await issue('show'):
                return
            await msg.channel.send(f'Your articles:\n - ' + "\n - ".join(self.people[msg.author]))
        # -------------------------------------------------------------------------------------------------------
        elif msg.content == "-start":
            if await issue('start'):
                return
            article_num = len(self.people[msg.author])
            if msg.author.id != self.guesser.id and article_num == 0:
                await self.gamechannel.send(f"{author_name}, you did't give any articles yet!")
            elif msg.author.id != self.guesser.id and article_num < len(self.people)-1:
                await self.gamechannel.send(f"{author_name}, you only have {article_num} articles, you need at least {len(self.people)-1}!")
            elif msg.author in self.starting_people:
                await self.gamechannel.send(f"{author_name}, you already voted for start!")
            else:
                self.starting_people.append(msg.author)
                people_num_diff = len(self.people)-len(self.starting_people)
                if people_num_diff == 0:
                    await self.gamechannel.send(f'{author_name} was the last one to vote! Game begins with people:\n - ' + '\n - '.join(map(lambda P: P.name, self.starting_people)))
                    await self.gamechannel.send(f">>> Round :{self.number[1]}:!\n{self.guesser.name}, you may [-get] the first article!")
                    self.points = {P: 0 for P in self.people}
                    self.speakers = [fellow for fellow in self.people if fellow != self.guesser]
                    self.game_started = True
                else:
                    await self.gamechannel.send(f"{author_name} votes for a start! People remaining:\n - " + '\n - '.join(map(lambda P: P.name, (P for P in self.people if P not in self.starting_people))))
        # -------------------------------------------------------------------------------------------------------
        elif msg.content == "-reset":
            self.confirmation_message = await msg.channel.send(self.resetmessage)
        # #######################################################################################################
        elif msg.content == "-greet":
            await msg.channel.send("Hi I'm here!")
        # -------------------------------------------------------------------------------------------------------
        elif msg.content == "-yeet":
            await msg.channel.send("ʇǝǝʎ")
        # -------------------------------------------------------------------------------------------------------
        elif msg.content == "-debug":
            if msg.author.id != 348976146689294336: return
            await msg.channel.send('\n'.join(map(str, (
                self.people, self.points, self.starting_people, self.speakers,
                self.gamechannel, self.game_started,
                self.guesser, self.round, self.person_to_guess
            ))))
        # -------------------------------------------------------------------------------------------------------
        elif msg.content.startswith("-"):
            await msg.channel.send("Wrong command!")


async def setup(bot):
    await bot.add_cog(GameLogic(bot))