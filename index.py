import random       # gay
import requests     # cat
import json         # cat
import aiohttp      # emoji creation
from datetime import datetime, time, timedelta   # stan
import asyncio      # stan

import discord
from discord.ext import commands
intents = discord.Intents.all()
intents.members = True
intents.presences = True
intents.typing = True
intents.reactions = True
client = commands.Bot(command_prefix='.', intents=intents, help_command=None)

from env import TOKEN
from other import generate_keysmash, responses, rainbow_words, sad_words
client.load_extension('music')

start_time = datetime.now()

@client.event
async def on_ready():
    print(f'Logged in as {client.user}!')
    await client.change_presence(activity=discord.Activity(
        type=discord.ActivityType.listening,
        name=f'{client.command_prefix}help'))
    print("\nServers: ")
    for guild in client.guilds:
        print(f"- {guild.name} ({guild.member_count} members)")
    print(f"\nStart time: {start_time}\n")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    await client.process_commands(message)

    # Responding to rainbows
    text = message.content.lower()
    if not text:
        return
    if text[0] != client.command_prefix \
            and not any(word in text for word in sad_words) \
            and any(word in text for word in rainbow_words):
        rand = random.randint(0, 100)
        if rand < 1:    # 1% chance lol
            return await message.channel.send(generate_keysmash())
        elif rand > 5:  # 5% chance
            return await message.channel.send(random.choice(responses))

    if greeting_required(text):
        async with message.channel.typing():
            faces = [":3", ":3", ":D", ":)", ":))", ":)))", "^-^", "^_^", "<3", "!", "!!", '', '']
            possible_names = [message.author.name, message.author.nick]
            name_to_use = random.choice(possible_names).lower()
        if len(name_to_use.split()) > 3:
            return await message.channel.send(f'hi, {name_to_use} {random.choice(faces)}')
        return await message.channel.send(f'hi {name_to_use} {random.choice(faces)}')

    # Responding to "no homo", "aaaa", etc
    if "no homo" in text:
        if random.randint(0, 10) > 8:
            return await message.channel.send(f'not even a little? :pleading:')
    if len(message.content) > 3 and (text == len(text) * 'a' or text == len(text) * 'A'):
        return await message.channel.send(text)
    if "mwah" in text:
        # https://stackoverflow.com/questions/53636253/discord-bot-adding-reactions-to-a-message-discord-py-no-custom-emojis
        return await message.add_reaction("💋");
    if "μωμ" in text:
        return await message.channel.send("μωμ")
    if text == "yay":
        return await message.channel.send("yay");
    if text == "joe" or text == "jo":
        return await message.channel.send("joe mama");

    if text[0] == client.command_prefix:
        return

    # Qubitz responds to uwu words only if the message sent was not a command
    # directly to them
    uwu_word = ""
    if "uwu" in text:
        uwu_word = "uwu"
    elif "owo" in text:
        uwu_word = "owo"
    else:
        return
    punctuation_array = ["?", "!", "~"]
    for word in text.split():
        if uwu_word in word:
            last_letters = word[word.index(uwu_word):]
            for char in last_letters:
                if char not in punctuation_array:
                    last_letters.replace(char, '')
            puncts = {
                    "?": word.count("?"),
                    "!": word.count("!"),
                    "~": word.count("~"),
                    }
            if len(word) > 999:
                return await message.channel.send("...okay you win ;-;")
            most_common_punct = max(puncts, key=puncts.get)
            uwu_response = uwu_word + puncts[most_common_punct] * 2 * most_common_punct
            return await message.channel.send(uwu_response)

def greeting_required(text):
    greetings = ["hi", "hello", "greetings", "welcome"]
    for greeting in greetings:
        if f'{greeting} qubitz' in text or f'{greeting}, qubitz' in text:
            return True

@client.command(aliases=['help', 'h'])
async def _help(ctx):
    embed = discord.Embed(title="Help",
            description=f'Prefix: `{client.command_prefix}`',
            color=0xb2558d)
    embed.add_field(name=f"`{client.command_prefix}ping` (aka `p`)",
            value="Performs a ping to see if the bot is up.",
            inline=False)
    embed.add_field(name=f'`{client.command_prefix}create_emoji emojiname` (aka `create`, `emoji`)',
            value="Sets attached image as a custom server emoji with the given name.",
            inline=False)
    embed.add_field(name=f'`{client.command_prefix}info` (aka `i`)',
            value="Gets guild and user information.",
            inline=False)
    embed.add_field(name=f"`{client.command_prefix}uwuify something` (aka `uwu`)",
            value="Uwuifies your message, deleting the command message.",
            inline=False)
    embed.add_field(name=f"`{client.command_prefix}echo something`",
            value="Echoes back your message, deleting the command message.",
            inline=False)
    embed.add_field(name=f"`{client.command_prefix}cat` (aka `c`)",
            value="Shows a cat from https://api.thecatapi.com/v1/images/search.",
            inline=False)
    embed.add_field(name=f'`{client.command_prefix}list`',
            value="Lists each role and everyone in them.", inline=False)
    embed.add_field(name=f'`{client.command_prefix}find foo`',
            value="Prints a list of everyone with role `foo`.", inline=False)
    embed.set_footer(text="Contact radix#9084 with issues.")
    return await ctx.send(embed=embed)

@client.command(aliases=['ping'])
async def _ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)} ms :)')

@client.command(aliases=['emoji', 'create', 'create_emoji'])
async def _create_emoji(ctx, *args):
    async with ctx.typing():
        if len(args) == 0:
            return await ctx.send(f'Error: give the emoji a name!')
    name = args[0]
    if len(name) < 2 or len(name) > 32:
        return await ctx.send(f'Error: the emoji\'s name must be between 2 and 32 in length.')
    if name in str(ctx.guild.emojis):
        return await ctx.send(f'Error: that name is taken!')
    try:
        attachment_url = ctx.message.attachments[0].url
    except IndexError:
        return await ctx.send(f'Error: please attach the image to your message. Also, Discord won\'t let me set external images as emojis, so please attach/upload the image instead of sending a link :(')

    extensions = [".png",".jpg",".jpeg"]
    if not any(ext in attachment_url.lower() for ext in extensions):
        return await ctx.send(f'Error: please make sure the image is `.png`, `.jpg`, or `.jpeg` format.')

    if len(ctx.guild.emojis) >= ctx.guild.emoji_limit:
        await ctx.send(f'Error: all the emoji spots ({ctx.guild.emoji_limit}) are already taken!')

    async with aiohttp.ClientSession() as session:
        async with session.get(attachment_url, timeout = 20) as response:
            if response.status == 200:
                image_bytes = await response.content.read()
                try:
                    emoji = await ctx.guild.create_custom_emoji(name=name, image=image_bytes)
                except aiohttp.ServerTimeoutError:
                    return await ctx.send(f'Sorry, server timed out! Try again?')
                except Exception as e:
                    if "String value did not match validation regex" in str(e):
                        return await ctx.send(f'Sorry, special characters aren\'t allowed!')
                    return await ctx.send(e)
                await ctx.send(f'New emoji: <:{emoji.name}:{emoji.id}> (`<:{emoji.name}:{emoji.id}>`)')
            else:
                await ctx.send(f'Something went wrong, please contact radix#9084 :(')

@client.command(aliases=['cat', 'c'])
async def _cat(ctx):
    async with ctx.typing():
        response = requests.get("https://api.thecatapi.com/v1/images/search")
    json_data = json.loads(response.text)[0]
    await ctx.send(json_data["url"])

@client.command(aliases=['info', 'i'])
async def _info(ctx, *args):
    def _details():
        guild_details = f'{ctx.guild}'
        guild_details += f'\nID: `{ctx.guild.id}`'
        guild_details += f'\n{ctx.guild.member_count} members'
        embed = discord.Embed(title="Information", description=guild_details, color=0xb2558d)

        for m in ctx.guild.members:
            if m.nick:
                name = m.nick
            else:
                name = m.name

            member_details = f'Username: {m.name}#{m.discriminator}'
            member_details += f'\nID: `{m.id}`'
            member_details += f'\nJoined on {m.joined_at.strftime("%-d %b %Y")}'
            if len(m.activities):
                gerund = str(m.activities[0].type)
                gerund = gerund[gerund.index('.')+1:]+" "
                if gerund == "listening ":
                    gerund += "to "
                if gerund == "custom ":
                    gerund = ""
                member_details += f'\nStatus: {gerund}{m.activities[0].name}'
            else:
                member_details += f'\nNo current activities'
            embed.add_field(name=f'{name}', value=member_details, inline=False)
        return embed
    await ctx.send(embed=_details())

@client.command(aliases=['uwuify', 'uwu'])
async def _uwuify(ctx, *, arg):
    await ctx.message.delete()
    arg = arg.replace("r", "w")
    arg = arg.replace("small", "smol")
    arg = arg.replace("l", "w")
    arg = arg.replace("na","nya")
    arg = arg.replace("no", "nyo")
    # Fix overcorrection
    arg = arg.replace("smow", "smol")
    await ctx.send(arg)

@client.command(aliases=['echo'])
async def _echo(ctx, *, arg):
    await ctx.message.delete()
    await ctx.send(arg)

@client.command(aliases=['uptime', 'up', 'u'])
async def _uptime(ctx):
    current_time = datetime.now()
    delta = int((current_time - start_time).total_seconds())
    d, rem = divmod(delta, 24 * 60 * 60)
    h, rem = divmod(rem, 60 * 60)
    m, s = divmod(rem, 60)
    uptime = f"Uptime: `{d} day{'' if d == 1 else 's'}, "
    uptime += f"{h} hour{'' if h == 1 else 's'}, "
    uptime += f"{m} minute{'' if m == 1 else 's'}, "
    uptime += f"{s} second{'' if s == 1 else 's'}`"
    await ctx.send(uptime)

@client.command(aliases=['list', 'l'])
async def _list_all_roles(ctx, *args):
    ALL_ROLES = {}

    for m in ctx.guild.members:
        for role in m.roles:
            if role.name != "@everyone":
                if role.name in ALL_ROLES:
                    ALL_ROLES[role.name].append(f'`{m.name}#{m.discriminator}`')
                else:
                    ALL_ROLES[role.name] = [f'`{m.name}#{m.discriminator}`']

    for role in ALL_ROLES:
        long_list = f'**{role}**: {", ".join(ALL_ROLES[role])}\n'
        if len(long_list) < 2000:
            await ctx.send(long_list)
        else:
            parts = []
            for i in range(0, len(long_list), 1000):
                parts.append(long_list[i:i+1000])
            if len(parts) > 3:
                await ctx.send(f'(**{role}** has too many people in it to list)')
            else:
                for part in parts:
                    await ctx.send(part)
    return

@client.command(aliases=['find', 'f'])
async def _find_people_with_role(ctx, *, role):
    real_roles = []
    for real_role in ctx.guild.roles:
        real_roles.append(real_role.name)
    if role not in real_roles:
        return await ctx.send("That role does not exist!")

    people_in_role = []
    for m in ctx.guild.members:
        member_specific_roles = []
        for r in m.roles:
            member_specific_roles.append(r.name)
        if role in member_specific_roles:
            people_in_role.append(f'`{m.name}#{m.discriminator}`')

    if not people_in_role:
        return await ctx.send(f'No one with that role!')

    long_list = f'People with role `{role}`:\n'
    for person in people_in_role:
        long_list += f'{person}\n'
    parts = []
    for i in range(0, len(long_list)-1, 1900):
        temp = long_list[i:i+1900].rindex("\n")
        try:
            await ctx.send(long_list[i:temp])
        except:
            print(f'Failed to ctx.send: {long_list[i:temp]}')
    return

# https://stackoverflow.com/questions/63769685/discord-py-how-to-send-a-message-everyday-at-a-specific-time
async def stan():
    # Make sure your guild cache is ready so the channel can be found via get_channel
    await client.wait_until_ready()
    channel = client.get_guild(731654031839330374).get_channel(768001893389303808)
    await channel.send("stan!")

async def daily_stan():
    now = datetime.utcnow()
    # 1am UTC = 6pm PST
    WHEN = time(1, 0, 0)
    # Make sure loop doesn't start after {WHEN} as then it will send
    # immediately the first time as negative seconds will make the sleep yield
    # instantly
    if now.time() > WHEN:
    # Don't start the for loop until tomorrow
        tomorrow = datetime.combine(now.date() + timedelta(days=1), time(0))
        seconds = (tomorrow - now).total_seconds()
        await asyncio.sleep(seconds)
    while True:
        now = datetime.utcnow()
        target_time = datetime.combine(now.date(), WHEN)
        seconds_until_target = (target_time - now).total_seconds()
        # Sleep until we hit the target time
        print(f"Waiting {seconds_until_target} seconds to stan...")
        await asyncio.sleep(seconds_until_target)

        # Call the helper function that sends the message
        await stan()

        # Sleep until tomorrow and then the loop will start a new iteration
        tomorrow = datetime.combine(now.date() + timedelta(days=1), time(0))
        seconds = (tomorrow - now).total_seconds()
        await asyncio.sleep(seconds)

client.loop.create_task(daily_stan())
client.run(TOKEN)
