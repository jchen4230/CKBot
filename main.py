import discord
import time
import csv
import os
from operator import itemgetter
import time
import datetime
import random

#####
num_scoreboard = 10
#####
responses = {"devious": "<:devious:1003987786384285768>",
             "pansive": "when you come home and theres no hummus left but your daughter said she didnt eat it but its really obvious she did but you let it go, whats done is done",
             "pint": "https://cdn.discordapp.com/attachments/886520869587935282/1008954189428293752/unknown.png",
             "bird": "https://cdn.discordapp.com/attachments/866306442675224606/1008955809507586068/unknown.png",
             "rubidance": "https://tenor.com/view/blackpink-dancing-jisoo-dance-lisa-gif-18921168",
             "pills": "did you mean .solve? :slight_smile:",
             "pillscounter": "did you mean .solvecounter? :slight_smile:",
             "sleep": "gn cutie",
             "mtx": "Introducing microtransactions!!\nEvery $1 you donate to puzzlesoc (beem @jchen4230) you will be awarded with an additional 100 puzzles solved",
             "turtle": "https://cdn.discordapp.com/attachments/866306442675224606/1013730778573717516/unknown.png",
             "slay": "would you rather slay so hard that the word slay loses all meaning or never slay again",
             "tim": "https://cdn.discordapp.com/attachments/866306442675224606/1014181450125410324/unknown.png",
             "merch": "https://cdn.discordapp.com/attachments/866306442675224606/1017348093701804062/unknown.png",
             "natisv": "https://cdn.discordapp.com/attachments/859825475048177674/1027208282894508133/unknown.png"
             }
names = ["josh", "bruce", "ryan", "joey", "eva", "shannon", "ppie", "fifi", "kenzo", "tlgeotau", "wobo", "punda", "anthea",
         "blake", "penguin", "lachlan", "zaeema", "diya", "livia", "sabina", "ed", "numor", "dante", "knightsy",
         "alvin", "kelvin", "peanut", "clam", "calvin", "sam", "cedric", "dlegend", "jason", "tristan", "kim", "weekly",
         "natisv", "simon", "jack", "elliot", "skelly", "edwin", "andy", "harris"]

with open('.token', 'r') as f:
    TOKEN = f.read()

if not os.path.exists("pills.csv"):
    with open("pills.csv", "w") as f:
        f.write("userid,username,count\n")

def increment_pill(userid, username):
    updated = False
    with open('pills.csv', 'r', encoding="utf-8") as old_file, open('new_pills.csv', 'w+', encoding="utf-8") as new_file:
        for row in old_file:
            row_content = row.split(',')
            if row_content[0] == str(userid):
                row_content[2] = str(int(row_content[2]) + 1)
                new_file.write(str(','.join(row_content)))
                new_file.write("\n")
                updated = True
            else:
                new_file.write(row)
        if not updated:
            new_file.write(f"{str(userid)},{username[:-5]},1\n")
    os.remove('pills.csv')
    os.rename('new_pills.csv', 'pills.csv')

class MyClient(discord.Client):
    @staticmethod
    async def on_ready():
        global helped
        print('\nOnline')
        print('We have logged in as {0.user}'.format(client))
        # print(str(discord.utils.get(client.get_all_members(), name="testname", discriminator="6665").id))
        helped = False

    async def on_message(self, message):

        if message.content.startswith('.'):
            global helped
            print(f"{datetime.datetime.now().strftime('%d/%m %H:%M:%S.%f')} {str(await client.fetch_user(message.author.id))}: {message.content}")

            if message.author.id == self.user.id:
                return

            elif message.content.startswith('.help'):
                await message.channel.send("scream all you want")
                async with message.channel.typing():
                    time.sleep(0.5)
                    await message.channel.send("nobody's coming to help you")
                helped = True

            elif message.content == ".solve":
                increment_pill(message.author.id, str(await client.fetch_user(message.author.id)))
                await message.add_reaction("<:kannaHeart:887587368280940566>")

            elif message.content[1:].lower() in responses:
                await message.channel.send(responses[message.content[1:].lower()])

            elif message.content[1:].lower() == "ppie":
                x = random.random()
                if x < 0.5:
                    # copious
                    await message.channel.send("https://cdn.discordapp.com/attachments/886520869587935282/1010432711028117544/IMG_3175.png")
                elif x < 0.9:
                    await message.channel.send("https://cdn.discordapp.com/attachments/866306442675224606/1022021570211893258/unknown.png")
                else:
                    await message.channel.send(
                        "https://cdn.discordapp.com/attachments/866306442675224606/1025228937724436520/IMG_3722.png")

            elif message.content[1:].lower() in names:
                await message.channel.send(f"hi {message.content[1:]} :smiling_face_with_3_hearts:")

            elif message.content == ".solvecounter":
                pill_list = []
                with open('pills.csv', newline='', encoding="utf-8") as f:
                    for user in csv.DictReader(f):
                        pill_list.append([user["userid"], int(user["count"]), user["username"]])
                pill_list = sorted(pill_list, key=itemgetter(1))  # sorting list in decreasing order
                pill_list = pill_list[::-1]

                displaylist = []
                for i in range(0, num_scoreboard):
                    try:
                        displaylist.append(f"{str(i + 1)}. **{pill_list[i][2]}** has solved **{str(pill_list[i][1])}** puzzle{'' if pill_list[i][1] == '1' else 's'}.")
                    except IndexError:
                        pass
                embed = discord.Embed(title="Top " + str(num_scoreboard) + " puzzlers",
                                      description="\n".join(displaylist), color=0xffa500)

                await message.channel.send(embed=embed)

            elif message.content.startswith('.alzm'):
                channel = client.get_channel(503533739104665632)
                await channel.send("who are you calling property?")

            elif helped is True and "wtf" in message.content:
                await message.channel.send("don't speak unless spoken to")

            else:
                helped = False

intents = discord.Intents().all()
activity = discord.Activity(name='with puzzles', type=discord.ActivityType.playing)
client = MyClient(intents=intents, activity=activity)
client.run(TOKEN)
