import string
#config
import discord
from discord.ext import commands
#client = commands.Bot(command_prefix='>')
intents = discord.Intents.default()
intents.members = True
intents.presences = True
client = commands.Bot(command_prefix='>', intents = intents)

#dependencies
import time #for joke
import random #for returning "gay rights!"
import math #for conversions
from discord.utils import get 
import requests #for talking to cat/dog APIs
import json #for cat/dog APIs
import aiohttp

#local stuff
from env import TOKEN 
from other import generate_keysmash, quotes, responses, rainbow_words, sad_words

#signing in
@client.event
async def on_ready():
    print(f'Logged in as {client.user}!')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f'{client.command_prefix}h'))


#main
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    #responding to rainbows
    msg = message.content.lower().split()
    if any(word in msg for word in sad_words): 
        return
    if any(word in msg for word in rainbow_words):
        #make this weird rand number so that we don't have to generate another random number later to choose which of the responses we send
        rand = random.randint(0,len(responses)+80) 
        try:
            await message.channel.send(responses[rand])
        except IndexError:
            if rand > (len(responses)+50):
                await message.channel.send(generate_keysmash())
        
    #respond to own name
    greetings = ["hi","hello","greetings","welcome"]
    for greeting in greetings:
        if f'{greeting} quartz' in message.content.lower() or f'{greeting}, quartz' in message.content.lower():
            async with message.channel.typing():
                faces = [":3",":3",":D",":)",":))",":)))","^-^","^_^","<3","!","!!"]
                possible_names = [message.author.name,message.author.nick]
                name_to_use = random.choice(possible_names).lower()
            if len(name_to_use.split()) > 3:
                return await message.channel.send(f'hi, {name_to_use} {random.choice(faces)}')    
            await message.channel.send(f'hi {name_to_use} {random.choice(faces)}')

    #responding to "no homo"
    if message.content.lower().translate(str.maketrans('', '', string.punctuation)) == "no homo":
        if random.randint(0,10) > 8:
            await message.channel.send(f'not even a little? {generate_keysmash()}')
        else: 
            await message.channel.send(f'not even a little? :pleading_face:')

    #responding to "aaaaa"
    if message.content.lower() == len(message.content.lower())*'a' and len(message.content) > 2:
        return await message.channel.send(len(message.content.lower())*'a')

    await client.process_commands(message)


#help
@client.command(aliases=['h'])
async def get_help(ctx):
    embed = discord.Embed(title="Help", description=f'Prefix: `{client.command_prefix}`', color=0xb2558d)
    embed.add_field(name=f"`{client.command_prefix}ping` (aka `p`)", 
            value="Performs a ping to see if the bot is up.", inline=False)
    embed.add_field(name=f'`{client.command_prefix}create_emoji foo` (aka `emoji`, `e`)', 
            value="Sets attached image as a custom server emoji with the given name (in this case, \"foo\").", inline=False)
    embed.add_field(name=f'`{client.command_prefix}remove_emoji bar` (aka `remove`, `rm`)',
            value="Removes the custom emoji with the given name.", inline=False)
    embed.add_field(name=f'`{client.command_prefix}info` (aka `i`)',
            value="Gets guild and user information.", inline=True)
    embed.add_field(name=f"`{client.command_prefix}quote` (aka `q`)", 
            value="Returns a randomly selected quote from a predefined array.", inline=True)
    embed.add_field(name=f"`{client.command_prefix}get_joke` (aka `joke`,`j`)", 
            value="Gets a joke from https://official-joke-api.appspot.com/random_joke.", inline=True)
    embed.add_field(name=f"`{client.command_prefix}get_cat` (aka `cat`,`c`)", 
            value="Gets an image of a cat from https://api.thecatapi.com/v1/images/search.", inline=True)
    embed.add_field(name=f"`{client.command_prefix}get_dog` (aka `dog`,`d`)",
            value="Gets an image of a dog from https://dog.ceo/api/breeds/image/random.", inline=True)
    embed.add_field(name=f'`{client.command_prefix}get_bitcoin_rate` (aka `bitcoin`, `bit`)',
            value="Gets current conversion rate from USD or GBP or euros to Bitcoin.", inline=True)
    embed.add_field(name=f'`{client.command_prefix}convert [amount] [currency]`',
            value="Converts `amount` from `currency` (USD, GBP, or euros) to Bitcoin.", inline=True)
    embed.add_field(name=f'`{client.command_prefix}shift_forward [shift=1] foo` (aka `forward`)',
            value="Encodes a message by rotating it forward along the ASCII table the specified number of spaces (defaults to 1).",
            inline=True)
    embed.add_field(name=f'`{client.command_prefix}shift_back [shift=1] bar` (aka `back`)',
            value="Decodes a message by rotating it back along the ASCII table the specified number of spaces (defaults to 1).",
            inline=True)
    embed.set_footer(text="Contact @radix#4520 with issues.")
    await ctx.send(embed=embed)


#ping
@client.command(aliases=['p'])
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency*1000)} ms :)')


#get random quote from a list
@client.command(aliases=['q'])
async def quote(ctx):
    async with ctx.typing():
        time.sleep(2)
    await ctx.send(random.choice(quotes))


#emoji
@client.command(aliases=['emoji','e','create'])
async def create_emoji(ctx,*args):
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
                except Exception as exc:
                    if "String value did not match validation regex" in str(exc):
                        return await ctx.send(f'Sorry, special characters aren\'t allowed!')
                    return await ctx.send(exc)
                await ctx.send(f'New emoji: <:{emoji.name}:{emoji.id}> (`<:{emoji.name}:{emoji.id}>`)')
            else:
                await ctx.send(f'Something went wrong, please contact radix#4520 :(')


@client.command(aliases=['remove','rm'])
async def remove_emoji(ctx,*args):
    if len(args) == 0:
        return await ctx.send(f'Send me the emoji to remove!')
    for emoji in ctx.guild.emojis:
        if args[0] in str(emoji):
            await emoji.delete()
            return await ctx.send(f'Successfully deleted that emoji. It is no more.')

#dog
@client.command(aliases=['dog','d'])
async def get_dog(ctx):
    async with ctx.typing():
        response = requests.get("https://dog.ceo/api/breeds/image/random")    
    json_data = json.loads(response.text)
    await ctx.send(json_data["message"])


#cat
@client.command(aliases=['cat','c'])
async def get_cat(ctx):
    async with ctx.typing():
        response = requests.get("https://api.thecatapi.com/v1/images/search")
    json_data = json.loads(response.text)[0]
    await ctx.send(json_data["url"])


#jokes
@client.command(aliases=['joke','j'])
async def get_joke(ctx):
    async with ctx.typing():
        joke = get_joke()
        await ctx.send(joke.split("-")[0])
        time.sleep(3)
        await ctx.send(joke.split("-")[1])
def get_joke():
    response = requests.get("https://official-joke-api.appspot.com/random_joke")
    json_data = json.loads(response.text)
    joke = json_data["setup"] + "-" + json_data["punchline"]
    return joke


#bitcoin
@client.command(aliases=['bit','bitcoin'])
async def get_bitcoin_rate(ctx):
    async with ctx.typing():
        response = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json")
        json_data = json.loads(response.text)
        disclaimer = json_data["disclaimer"]
        usd_rate = json_data["bpi"]["USD"]["rate"]
        gbp_rate = json_data["bpi"]["GBP"]["rate"]
        eur_rate = json_data["bpi"]["EUR"]["rate"]
        date = json_data["time"]["updated"]
    embed = discord.Embed(title="Bitcoin Current Price", description=disclaimer+".", color=0xb2558d)
    embed.add_field(name="United States dollar ($)", value="$"+usd_rate, inline=False)
    embed.add_field(name="British pound sterling (£)", value="£"+gbp_rate, inline=False)
    embed.add_field(name="Euro (€)", value=eur_rate+"€", inline=False)
    embed.set_footer(text=f"As of {date}.")
    await ctx.send(embed=embed)


#bitcoin conversions
@client.command()
async def convert(ctx, amount, currency):
    async with ctx.typing():
        response = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json")
        json_data = json.loads(response.text)
        date = json_data["time"]["updated"]
    if "$" in currency or "dollar" in currency or "usd" in currency.lower():
        usd_rate = json_data["bpi"]["USD"]["rate"].replace(",","")
        amount_in_bitcoin = float(usd_rate)*float(amount)
        amount_in_bitcoin = "{:,.2f}".format(amount_in_bitcoin)
        amount = "{:,.2f}".format(float(amount.replace(",","")))
        await ctx.send(f"${amount} is {amount_in_bitcoin} Bitcoin, as of {date}.")
    elif "£" in currency or "pound" in currency or "gbp" in currency.lower():
        gbp_rate = float(json_data["bpi"]["GBP"]["rate"].replace(",",""))
        amount_in_bitcoin = float(gbp_rate)*float(amount)
        amount_in_bitcoin = "{:,.2f}".format(amount_in_bitcoin)
        amount = "{:,.2f}".format(float(amount.replace(",","")))
        await ctx.send(f"£{amount} is {amount_in_bitcoin} Bitcoin, as of {date}.")
    elif "€" in currency or "euro" in currency.lower():
        eur_rate = float(json_data["bpi"]["EUR"]["rate"].replace(",",""))
        amount_in_bitcoin = float(eur_rate)*float(amount)
        amount_in_bitcoin = "{:,.2f}".format(amount_in_bitcoin)
        amount = "{:,.2f}".format(float(amount.replace(",","")))
        await ctx.send(f"{amount}€ is {amount_in_bitcoin} Bitcoin, as of {date}.")


#ascii table encode
@client.command(aliases=['forward'])
async def shift_forward(ctx,*args):
    await ctx.send(shifted_forward(args))
def shifted_forward(args):
    if len(args) == 0: 
        return f'Error: must be in format `{client.command_prefix}shift_forward message`.'
    elif len(args) == 1 or not args[0].isdigit(): 
        shift = 1
        message_as_string = ' '.join(args)
    else:
        shift = int(args[0])
        message_as_string = ' '.join(args[1:])
    encoded_string = "" 
    for i in range(len(message_as_string)):
        ord_of_character = ord(message_as_string[i])
        if ord_of_character == 32:
            new_position = ord_of_character
        elif ord_of_character+shift > 1114111:
            return f'Error: specified shift too big (ASCII table ends after 1114111 entries)'
        else:
            new_position = ord_of_character+shift
        encoded_string += chr(new_position)
    return encoded_string+""

    
#ascii table decode
@client.command(aliases=['back'])
async def shift_back(ctx,*args):
    await ctx.send(shifted_back(args))
def shifted_back(args):
    if len(args) == 0: 
        return f'Error: must be in format `{client.command_prefix}shift_forward message`.'
    elif len(args) == 1 or not args[0].isdigit():
        shift = 1
        message_as_string = ' '.join(args)
    else:
        shift = int(args[0])
        message_as_string = ' '.join(args[1:])
    encoded_string = "" 
    for i in range(len(message_as_string)):
        ord_of_character = ord(message_as_string[i])
        if ord_of_character == 32:
            new_position = ord_of_character
        elif ord_of_character-shift > 1114111:
            return f'Error: specified shift too big (ASCII table ends after 1114111 entries)'
        else:
            new_position = ord_of_character-shift
        encoded_string += chr(new_position)
    return encoded_string+""

#info
@client.command(aliases=['i'])
async def info(ctx,*args):
    def get_details(target):
        guild_details = f'{ctx.guild}'
        guild_details += f'\nID: `{ctx.guild.id}`'
        guild_details += f'\n{ctx.guild.member_count} members'
        if len(ctx.guild.premium_subscribers) == 1:
            guild_details += f'\n1 Nitro supporter'
        else: 
            guild_details += f'\n{len(ctx.guild.premium_subscribers)} Nitro supporters'
        '''nitro names:
        if not len(ctx.guild.premium_subscribers) == 0:
            for s in ctx.guild.premium_subscribers:
                boosters += f'{s.name}#{s.discriminator},'
            details += f'\nBoosters: {boosters}
        '''
        embed = discord.Embed(title="Information", description=guild_details, color=0xb2558d)

        for m in ctx.guild.members:
            if m.bot == True or m == target:
                if m.nick == None:
                    name = m.name
                else: 
                    name = m.nick
                member_details = f'Username: `{m.name}#{m.discriminator}`'
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
                embed.add_field(name=f'{name}', value=member_details, inline=True)
        return embed
    await ctx.send(embed=get_details(ctx.author))

    
@client.command(aliases=['act','a'])
async def activities(ctx,*args):
    for m in ctx.guild.members:
            if m.bot == True: 
                if len(m.activities) != 0:
                    gerund = str(m.activities[0].type)
                    return await ctx.send(gerund[gerund.index('.')+1:])
                else: 
                    return
        

client.run(TOKEN)