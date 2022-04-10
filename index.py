import string
import discord
from discord.ext import commands
intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.typing = True
intents.reactions = True
client = commands.Bot(command_prefix='>', intents=intents, help_command=None)

# dependencies
import random       #for returning "gay rights!"
import math         #for conversions
from discord.utils import get 
import requests     #for talking to cat API
import json         #for cat API
import aiohttp

# local 
from env import TOKEN 
from other import generate_keysmash, responses, rainbow_words, sad_words

@client.event
async def on_ready():
    print(f'Logged in as {client.user}!')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f'{client.command_prefix}h'))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    await client.process_commands(message)
    
    # responding to rainbows
    text = message.content.lower() 
    if not any(word in text for word in sad_words) \
               and any(word in text for word in rainbow_words):
        # make this weird rand number so that we don't have to generate another random number later to choose which of the responses we send
        rand = random.randint(0, len(responses) + 80) 
        try:
            return await message.channel.send(responses[rand])
        except IndexError:
            if rand > (len(responses) + 50):
                return await message.channel.send(generate_keysmash())
        
    if should_respond_to_own_name(text):
        async with message.channel.typing():
            faces = [":3", ":3", ":D", ":)", ":))", ":)))", "^-^", "^_^", "<3", "!", "!!", '', '']
            possible_names = [message.author.name, message.author.nick]
            name_to_use = random.choice(possible_names).lower()
        if len(name_to_use.split()) > 3:
            return await message.channel.send(f'hi, {name_to_use} {random.choice(faces)}')    
        return await message.channel.send(f'hi {name_to_use} {random.choice(faces)}')

    # responding to "no homo"
    if "no homo" in text: 
        if random.randint(0, 10) > 8:
            return await message.channel.send(f'not even a little? {generate_keysmash()}')

    # responding to "aaaaa"
    if text == len(text) * 'a' and len(message.content) > 3:
        return await message.channel.send(len(text) * 'a')

    if "mwah" in text: 
        # https://stackoverflow.com/questions/53636253/discord-bot-adding-reactions-to-a-message-discord-py-no-custom-emojis
        return await message.add_reaction("💋");
    if "μωμ" in text:
        return await message.channel.send("μωμ")
    if text == "yay": 
        return await message.channel.send("yay");
    if text == "joe" or text == "jo":
        return await message.channel.send("joe mama");
   
    uwu_word = ""
    if "uwu" in text and ">uwuify" not in text:
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
            return await message.channel.send(uwu_word + puncts[most_common_punct] * 2 * most_common_punct)

@client.command(aliases=['help', 'h'])
async def _help(ctx):
    embed = discord.Embed(title="Help", 
            description=f'Prefix: `{client.command_prefix}`', 
            color=0xb2558d)
    embed.add_field(name=f"`{client.command_prefix}ping` (aka `p`)",
            value="Performs a ping to see if the bot is up.", 
            inline=False)
    embed.add_field(name=f'`{client.command_prefix}create_emoji foo` (aka `create`, `emoji`)', 
            value="Sets attached image as a custom server emoji with the given name (in this case, \"foo\").", 
            inline=False)
    embed.add_field(name=f'`{client.command_prefix}info` (aka `i`)',
            value="Gets guild and user information.", 
            inline=False)
    embed.add_field(name=f"`{client.command_prefix}uwuify some message here` (aka `uwu`)", 
            value="Uwuifies your message.", 
            inline=False)
    embed.add_field(name=f"`{client.command_prefix}cat` (aka `c`)", 
            value="Gets an image of a cat from https://api.thecatapi.com/v1/images/search.", 
            inline=False)
    embed.add_field(name=f"`{client.command_prefix}echo something`", 
            value="Echoes back what you tell it to, deleting the command message.",
            inline=False)
    embed.set_footer(text="Contact @radix#9084 with issues.")
    return await ctx.send(embed=embed)

@client.command(aliases=['ping', 'p'])
async def _ping(ctx):
    await ctx.send(f'Pong! {round(client.latency*1000)} ms :)')

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
            if (m.nick == None):
                name = m.name
            else: 
                name = m.nick
            
            member_details = f'Username: {m.name}#{m.discriminator}'
            member_details += f'\nID: `{m.id}`'
            member_details += f'\nJoined on {m.joined_at.strftime("%-d %b %Y")}'# at %H:%M:%S %Z")}'
            if len(m.activities) != 0:
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
    text = arg.replace("r", "w").replace("l", "w")
    await ctx.send(text)

@client.command(aliases=['echo'])
async def _echo(ctx, *, arg):
    await ctx.send(arg)

def should_respond_to_own_name(text):
    greetings = ["hi", "hello", "greetings", "welcome"]
    for greeting in greetings:
        if f'{greeting} quartz' in text or f'{greeting}, quartz' in text:
            return True

@client.command(aliases=['purge'])
async def _purge(ctx, *argv):
    # https://stackoverflow.com/questions/69589089/takes-1-positional-argument-but-2-were-given-discord-py
    if ctx.guild is None:
        return await ctx.send("Sorry, I can't delete messages in DMs")

    try:
        num = int(argv[0])
    except:
        return await ctx.send(f"Usage: `{client.command_prefix}purge n`, where 1 < n < 100") 
    if num <= 1 or num >= 100: 
        return await ctx.send(f"Usage: `{client.command_prefix}purge n`, where 1 < n < 100") 

    try:
        await ctx.channel.purge(limit=int(num))
        return await ctx.send(f"*Successfully deleted {num} messages :)*", delete_after=3)
    except Exception as e:
        return await ctx.send(f"Couldn't delete because {e}")

client.run(TOKEN)
