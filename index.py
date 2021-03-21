#config
import discord
from discord.ext import commands
client = commands.Bot(command_prefix='>')

#dependencies
import time #for joke
import random #for returning "gay rights!"
import math #for conversions
from discord.utils import get 
import requests 
import json

#local stuff
from env import TOKEN 
from other import quotes, responses, generate_keysmash

#signing in
@client.event
async def on_ready():
    print(f'Logged in as {client.user}!')


#main
@client.event
async def on_message(message):
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f'{client.command_prefix}h'))
    if message.author == client.user:
        return
    rainbow_words = ["gay","rainbow","lgbt","queer","wholesome","women","men","gender is"]
    for word in rainbow_words:
        if word in message.content.lower():
            rand = random.randint(0,len(responses)+10)
            if rand >= len(responses)+5:
                keysmash = generate_keysmash()
                print(f'Keysmash generated to respond to {word}: {keysmash}\n')
                await message.channel.send(keysmash)
            else:
                if rand < len(responses):
                    await message.channel.send(responses[rand])
            break
    await client.process_commands(message)


#help
@client.command(aliases=['h'])
async def get_help(ctx):
    embed = discord.Embed(title="Help", description=f'Prefix: `{client.command_prefix}`', color=0xb2558d)
    embed.add_field(name=f"`{client.command_prefix}ping`", 
            value="Performs a ping to see if the bot is up.", inline=False)
    embed.add_field(name=f"`{client.command_prefix}quote` (aka `q`)", 
            value="Returns a randomly selected quote from a predefined array.", inline=False)
    embed.add_field(name=f"`{client.command_prefix}get_joke` (aka `joke`)", 
            value="Gets a joke from https://official-joke-api.appspot.com/random_joke.", inline=False)
    embed.add_field(name=f"`{client.command_prefix}get_cat` (aka `cat`)", 
            value="Gets an image of a cat from https://api.thecatapi.com/v1/images/search.", inline=False)
    embed.add_field(name=f"`{client.command_prefix}get_dog` (aka `dog`)",
            value="Gets an image of a dog from https://dog.ceo/api/breeds/image/random.", inline=False)
    embed.add_field(name=f'`{client.command_prefix}get_bitcoin_rate` (aka `bitcoin`, `bit`)',
            value="Gets current conversion rate from USD or GBP or euros to Bitcoin.", inline=False)
    embed.add_field(name=f'`{client.command_prefix}convert [amount] [currency]`',
            value="Converts `amount` from `currency` (USD, GBP, or euros) to Bitcoin.", inline=False)
    embed.add_field(name=f'`{client.command_prefix}shift_forward [int] [message]` (aka `forward`)',
            value="Encodes a message by rotating it forward along the ASCII table the specified number of spaces (defaults to 1).",inline=False)
    embed.add_field(name=f'`{client.command_prefix}shift_back [int] [message]` (aka `back`)',
            value="Decodes a message by rotating it back along the ASCII table the specified number of spaces (defaults to 1)",inline=False)
    embed.add_field(name=f'`{client.command_prefix}emoji` (aka `e`)', 
            value="Sets attached image as a new server emoji, if there is space. Currently not working.", inline=False)
    embed.set_footer(text="Contact @radix#4520 with issues.")
    await ctx.send(embed=embed)


#ping
@client.command(aliases=['p'])
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency*1000)} ms :)')


#get random quote from a list
@client.command(aliases=['q'])
async def quote(ctx):
    await ctx.send(random.choice(quotes))


#emoji
@client.command(aliases=['e'])
async def emoji(ctx,*args):
    if len(args) == 0:
        return f'Error: filename missing.'
    name = args[0]
    #embed = discord.Embed(title=f'{name}', description="", color=0xb2558d) 
    #file = discord.File("path/to/image/file.png", filename="image.png")
    #embed.set_image(url="https://i.imgur.com/MXsVHZ6.jpg")
    #await ctx.send(embed=embed)

    to_send = discord.File("https://i.imgur.com/MXsVHZ6.jpg", filename="image.png")
    await create_custom_emoji(ctx.guild, name=name, image=to_send)
    await ctx.send(to_send + "adslfkj")
    

    
    

#dog
@client.command(aliases=['dog'])
async def get_dog(ctx):
    response = requests.get("https://dog.ceo/api/breeds/image/random")
    json_data = json.loads(response.text)
    await ctx.send(json_data["message"])


#cat
@client.command(aliases=['cat'])
async def get_cat(ctx):
    response = requests.get("https://api.thecatapi.com/v1/images/search")
    json_data = json.loads(response.text)[0]
    await ctx.send(json_data["url"])


#jokes
@client.command(aliases=['joke'])
async def get_joke(ctx):
    joke = get_joke()
    await ctx.send(joke.split("-")[0])
    time.sleep(3)
    await ctx.send(joke.split("-")[1])
def get_joke():
    response = requests.get("https://official-joke-api.appspot.com/random_joke")
    json_data = json.loads(response.text)
    print(json_data)
    joke = json_data["setup"] + "-" + json_data["punchline"]
    return joke


#bitcoin
@client.command(aliases=['bit','bitcoin'])
async def get_bitcoin_rate(ctx):
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
@client.command(aliases=['c'])
async def convert(ctx, amount, currency):
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
        f'Error: must be in format `{client.command_prefix}shift_forward message`.'
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
        f'Error: must be in format `{client.command_prefix}shift_forward message`.'
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
async def info(ctx):
    await ctx.send( f'**{ctx.author}** ({ctx.author.id}) joined **{ctx.guild}** ({ctx.guild.id}) **at {ctx.author.joined_at}.**' )

client.run(TOKEN)