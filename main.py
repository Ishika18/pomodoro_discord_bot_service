import os
import json
import discord
import requests

API_URL = os.environ['API_URL']
GUILD = os.environ['GUILD']
TOKEN = os.environ['TOKEN']


# dummy test function for getting from api
def get_quote():
    response = requests.get(
        "https://zenquotes.io/api/random"
    )
    json_data = json.loads(response.text)
    quote = f"{json_data[0]['q']} - {json_data[0]['a']}"
    print(quote)
    return quote


# gets schedule from pomodoroAPI
def get_schedule(user_id):
  response = requests.get(
   API_URL + "schedule/" + user_id
  )
  json_data = json.loads(response.text)
  #parse json_data
  #return parsed json_data


# sends commitment to pomodoroAPI
def send_commitment(user_id, name, location, notes, minutes, repeats, url, start, end):
    api_url = API_URL + "commitment/"
    commitment = {
        "name": name,
        "location": location,
        "notes": notes,
        "minutes": minutes,
        "repeats": repeats,
        "url": url,
        "start": start,
        "end": end
    }

    response = requests.post(api_url + user_id, data=commitment)


# sends goal to pomodoroAPI
def send_goal(user_id, name, location, notes, totalTime, priority, endDate, minTaskTime):
    api_url = API_URL + "goal/"

    # at start, timeLeft = totalTime
    goal = {
        "name": name,
        "location": location,
        "notes": notes,
        "totalTime": totalTime,
        "timeLeft": totalTime,
        "priority": priority,
        "endDate": endDate,
        "minTaskTime": minTaskTime
    }

    response = requests.post(api_url + user_id, data=goal)

    def delete_commitment(user_id, commitment_name):
        pass

    def delete_goal(user_id, goal_name):
        pass

    def get_user_commit():
        pass


async def get_user_commit(channel, message, name):
    print("in helper")

    print(message.author.name + "%23" + message.author.discriminator)
    user_id = message.author.name + "%23" + message.author.discriminator

    def check(m):
        return m.author == message.author and m.channel == channel

    await channel.send("Enter a location:")
    location = await client.wait_for("message", check=check)
    await channel.send(f"Location {location.content}")

    await channel.send("Enter notes:")
    notes = await client.wait_for("message", check=check)
    await channel.send(f"Notes {notes.content}")

    await channel.send("Enter minutes: ")
    minutes = await client.wait_for("message", check=check)
    await channel.send(f"Minutes {minutes.content}")

    await channel.send("Enter repeats (MON, TUES, WED...) (blank if none):")
    repeats = await client.wait_for("message", check=check)
    await channel.send(f"Repeats {repeats.content}")

    await channel.send("Enter url: (leave blank if none)")
    url = await client.wait_for("message", check=check)
    await channel.send(f"Location {url.content}")

    await channel.send("Enter start time (like '2022-10-3 8:30:0'):")
    start_time = await client.wait_for("message", check=check)
    await channel.send(f"Start {start_time.content}")

    await channel.send("Enter end date: (like '2022-10-3'):")
    end_time = await client.wait_for("message", check=check)
    await channel.send(f"End {end_time.content}")
    print("end of helper")
    # send_commitment(user_id, name, location, notes, minutes, repeats, url, start_time, end_time)


async def get_user_goal(channel, message, name):
    print("in helper")

    print(message.author.name + "%23" + message.author.discriminator)
    user_id = message.author.name + "%23" + message.author.discriminator

    def check(m):
        return m.author == message.author and m.channel == channel

    await channel.send("Enter a location:")
    location = await client.wait_for("message", check=check)
    await channel.send(f"Location {location.content}")

    await channel.send("Enter notes:")
    notes = await client.wait_for("message", check=check)
    await channel.send(f"Notes {notes.content}")

    await channel.send("Enter total time: ")
    totalTime = await client.wait_for("message", check=check)
    await channel.send(f"Total Time {totalTime.content}")

    await channel.send("Enter priority: (0-10) (0 is highest)")
    priority = await client.wait_for("message", check=check)
    await channel.send(f"Location {priority.content}")

    await channel.send("Enter endDate (like '2022-10-3'):")
    endDate = await client.wait_for("message", check=check)
    await channel.send(f"Start {endDate.content}")

    await channel.send("Enter minimum task time:")
    minTaskTime = await client.wait_for("message", check=check)
    await channel.send(f"End {minTaskTime.content}")
    print("end of helper")
    # send_goal(user_id, name, location, notes, totalTime, priority, endDate, minTaskTime)


# bot stuff starts here:
client = discord.Client()


@client.event
async def on_ready():
    print("client logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    # for guild in client.guilds:
    #   for member in guild.members:
    #     print(member.name)

    channel = message.channel

    if message.author == client.user:
        return

    # dummy
    if message.content.startswith("!ping"):
        print("started with ping")
        await message.channel.send(get_quote())

    if message.content.startswith("!schedule"):
        user_id = message.author.name + "%23" + message.author.discriminator
        await message.channel.send(get_schedule(user_id))

    if message.content.startswith("!addCommitment "):
        commitment = message.content.split("!addCommitment ", 1)[1]
        commitment_array = commitment.split(" ")
        name = commitment_array
        await message.channel.send(f"Name: {name[0]}")
        await get_user_commit(channel, message, name)
        await message.channel.send("commitment added")

    if message.content.startswith("!addGoal "):
        goal = message.content.split("!addGoal ", 1)[1]
        goal_array = goal.split(" ")
        name = goal_array
        await message.channel.send(f"Name: {name[0]}")
        await get_user_goal(channel, message, name)
        await message.channel.send("goal added")


# client.run(os.getenv("TOKEN"))
client.run(TOKEN)
