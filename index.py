#config
import discord
from discord.ext import commands
client = commands.Bot(command_prefix='>')
import time #for joke
import random #for returning "gay rights!"
import math #for conversions
#config for api stuff
from discord.utils import get 
import requests 
import json 
from env import TOKEN #there's a file called env.py where i've defined my token
                    #so i can import TOKEN from there rather than including it here in plaintext

#signing in
@client.event
async def on_ready():
    print(f'Logged in as {client.user}!')


#main, basically :)
@client.event
async def on_message(message):
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f'{client.command_prefix}h'))
    if message.author == client.user:
        return
    rainbow_words = ["gay","rainbow","lgbt","queer","wholesome","women","men","gender is"]
    for word in rainbow_words:
        if word in message.content.lower():
            responses = [
                "gay rights!",
                ":rainbow: gay rights! :rainbow:",
                "gay rights!",
                "women with swords,,,,,,",
                "do you listen to girl in red?",
                "do u listen 2 girl in red :eyes:",
                "women do be pretty though",
                "women in suits....... yes",
                "love has no gender ^-^",
                "love! has! no! gender!!!",
                "be proud of who you are! :rainbow_flag:",
                ":rainbow_flag:",
                ":rainbow:",
                "gay",
                "gay ^-^"
            ]
            rand = random.randint(0,len(responses)+10)
            if rand >= len(responses)+5:
                keysmash = generate_keysmash()
                print(f'Generating keysmash: {keysmash}\n')
                await message.channel.send(keysmash)
            else:
                if rand < len(responses):
                    await message.channel.send(responses[rand])
            break
    await client.process_commands(message)


def generate_keysmash():
    keysmash_length = random.randint(7,20)
    valid_characters = ["a","s","s","s","s","s","d","d","g","d","f","g","h","j","j","j","j","k","k","k","k","l","z","x","w",";",";",";",";","v","v",".",","]
    keysmash = ""
    for i in range(keysmash_length):
        random_char = random.randint(0,len(valid_characters)-1)
        keysmash += valid_characters[random_char]
    enders = [":rainbow:","wammen","yes",":two_hearts:",":weary:",":rainbow_flag","<3"]
    return f'{keysmash} {random.choice(enders)}'

    

#help
@client.command(aliases=['h'])
async def get_help(ctx):
    embed = discord.Embed(title="Help", description=f'Prefix: `{client.command_prefix}`', color=0xb2558d)
    embed.add_field(name=f"`{client.command_prefix}ping`", 
            value="Performs a ping to see if the bot is up.", inline=False)
    embed.add_field(name=f"`{client.command_prefix}quote` (aka `q`)", 
            value="Returns a randomly selected quote from a (pitifully small; please contact @radix#4520 with ideas!) array.", inline=False)
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
    quotes = [
            '"Caring for myself is not self-indulgence, it is self-preservation, and that is an act of political warfare. -Audre Lorde',
            '"Prettiness is not a rent you pay for occupying space." -Erin McKean',
            '"Hope will never be silent." -Harvey Milk',
            '"You never completely have your rights, one person, until you all have your rights." -Marsha P. Johnson',
            '"How many years has it taken people to realize that we are all brothers and sisters and human beings in the human race?" -Marsha P. Johnson',
            '"Non-conformity is the only real passion worth being ruled by." -Julian Assange',
            '"One of the best ways to achieve justice is to expose injustice." -Julian Assange',
            '"Power is a thing of perception. They don\'t need to be able to kill you. They just need you to think they are able to kill you." -Julian Assange',
            '"Be ashamed to die until you have won some victory for humanity." -Horace Mann',
            '"Sleep heavily and know that I am here with you now. The past is gone, and cannot harm you anymore. And while the future is fast coming for you, it always flinches first and settles in as the gentle present. This now, this us? We can cope with that. We can do this together. You and I, drowsily, but comfortably." -*Welcome to Night Vale*',
            '"Somewhere there is a map, and on that map is Earth, and attached to Earth is an arrow that says your name and lists your lifespan. Some of you die standing. Others sitting. Many of you die in cars. I can never die. It is difficult for me to understand the concept that I am attempting to convey. I cannot show you this vision, but you may imagine it. Step forward and tell someone of it, please." -*Welcome to Night Vale*, "Pyramid"',
            '"If pigs could fly, yes, of course I would vote for the Democratic Party, but pigs don\'t fly." -Jill Brown',
            '"Three o\'clock is always too late or too early for anything you want to do." -Jean-Paul Sartre',
            '"Acting is a question of absorbing other people\'s personalities and adding some of your own experience." -Jean-Paul Sartre',
            '"The tax collectors will not move when you are staring directly into their soulless eyes. However, you may soon tire of making eye contact with them, especially when doing important things like paying your bills, eating dinner, or pretending to be a koi fish — and that is when they move." -Kitty Heart, in the style of *Welcome to Night Vale*',
            '"Never underestimate the determination of a kid who is time-rich and cash-poor." -Cory Doctorow, *Little Brother*',
            '"Somewhere, something incredible is waiting to be known."',
            '"The fact that we live at the bottom of a deep gravity well, on the surface of a gas covered planet going around a nuclear fireball 90 million miles away and think this to be normal is obviously some indication of how skewed our perspective tends to be." -Douglas Adams, *The Salmon of Doubt: Hitchhiking the Galaxy One Last Time*',
            '"I\'m sure the universe is full of intelligent life. It\'s just been too intelligent to come here." -Arthur C. Clarke',
            '"An expert is a person who has made all the mistakes that can be made in a very narrow field." -Niels Bohr',
            '"Everything must be made as simple as possible. But not simpler." -Albert Einstein',
            '"The good thing about science is that it\'s true whether or not you believe in it." -Neil deGrasse Tyson',
            'If the facts don\'t fit the theory, change the facts." -Albert Einstein',
            '"It would be possible to describe everything scientifically, but it would make no sense; it would be without meaning, as if you described a Beethoven symphony as a variation of wave pressure." -Albert Einstein',
            '"Have you ever been in love? Horrible isn\'t it? It makes you so vulnerable. It opens your chest and it opens up your heart and it means that someone can get inside you and mess you up." -Neil Gaiman, *The Sandman, Vol. 9: The Kindly Ones*',
            '"The saddest aspect of life right now is that science gathers knowledge faster than society gathers wisdom." -Isaac Asimov',
            '"Everything that is beautiful and noble is the product of reason and calculation." -Charles Baudelaire',
            'As a place, Night Vale is terrifying. There are a lot of things that don\'t make sense and people are dying constantly. But the thing about real life is that it\'s terrifying and there are lots of things that don\'t make sense and people are dying constantly. In Night Vale, it\'s aliens. In real life, it\'s cancer… but it\'s still the same thing." -Joseph Fink, on *Night Vale* and life',
            '"We are such stuff\nAs dreams are made on; and our little life\nIs rounded with a sleep." -The Tempest, Act 4, Scene 1',
            '\'A writer,\' she said, \'is a kind of octopus among human beings.\'" -Hans Christian Andersen, *The Wood Nymph*',
            'I’m not saying this in order to criticize, but this is sheer nonsense!" -Niels Bohr',
            '"Cynics are - beneath it all - only idealists with awkwardly high standards." -Alain de Botton',
            '"When you see something that is technically sweet, you go ahead and do it and you argue about what to do about it only after you have had your technical success. That is the way it was with the atomic bomb." -J. Robert Oppenheimer',
            '"Any man whose errors take ten years to correct is quite a man." -J. Robert Oppenheimer',
            '"One has to look out for engineers - they begin with sewing machines and end up with the atomic bomb." -Marcel Pagnol',
            '"I was born not knowing and have had only a little time to change that here and there." -Richard P. Feynman',
            '"It has not yet become obvious to me that there\'s no real problem. I cannot define the real problem; therefore, I suspect there\'s no real problem, but I\'m not sure there\'s no real problem." -Richard P. Feynman',
            '"If I could explain it to the average person, it wouldn\'t have been worth the Nobel Prize." -Richard P. Feynman',
            '"If you never did you should. These things are fun, and fun is good." -Dr. Seuss',
            '"Your mountain is waiting. So… get on your way!" -Dr. Seuss',
            '"True love never had an ending." -Anonymous',
            '"And O there are days in this life, worth life and worth death." -Charles Dickens, *Our Mutual Friend*',
            '"You can\'t blame gravity for falling in love." -Albert Einstein',
            '"Only two things are infinite, the universe and human stupidity, and I’m not so sure about the former." -Albert Einstein',
            '"\'Lovely\' is a lovely word that should be used more often." -Jennifer Niven, *All the Bright Places*',
            '"It\'s so lovely to be lovely to the one I love." -Jennifer Niven, *All the Bright Places*',
            '"If anyone could have saved me, it would have been you." -Virginia Woolf',
            '"I am rooted, but I flow." -Virginia Woolf',
            '"Once you hear the details of victory, it is hard to distinguish it from a defeat." -Jean-Paul Sartre',
            '"Who would not trade a raven for a dove?" -Shakespeare, *A Midsummer Night\'s Dream*',
            '"We are all made of molecules." -Susan Nielsen',
            '"My own brain is to me the most unaccountable of machinery - always buzzing, humming, soaring roaring diving, and then buried in mud. And why? What’s this passion for?" -Virginia Woolf',
            '"Isn’t it strange that we talk least about the things that we think about most?" -Charles Lindbergh',
            '"The art of living is the art of knowing how to believe lies." -Cesare Pavese',
            '"We do not remember days, we remember moments." -Cesare Pavese',
            '"If it were possible to have a life absolutely free from every feeling of sin, what a terrifying vacuum it would be." -Cesare Pavese',
            '"All sins have their origin in a sense of inferiority otherwise known as ambition." -Cesare Pavese',
            '"Nothing is worth more than this day." -Johann Wolfgang von Goethe',
            '"If society fits you comfortably enough, you call it freedom." -Robert Frost',
            '"Stupidity is a talent for misconception." -Edgar Allen Poe',
            '"Science has not yet taught us if madness is or is not the sublimity of intelligence." -Edgar Allen Poe',
            '"I have great faith in fools; self-confidence, my friends call it." -Edgar Allen Poe',
            '"I became insane, with long intervals of horrible sanity." -Edgar Allen Poe',
            '"Do not go where the path may lead, go instead where there is no path and leave a trail." -Ralph Waldo Emerson',
            '"Write it on your heart that every day is the best day in the year." -Ralph Waldo Emerson',
            '"Yesterday is but today’s memory, and tomorrow is today’s dream." -Khalil Gibran',
            '"No pen, no ink, no table, no room, no time, no quiet, no inclination." -James Joyce',
            '"Where is the life we lost in living? Where is the wisdom we have lost in knowledge? Where is the knowledge we have lost in information?" -T. S. Eliot',
            '"All that is gold does not glitter, not all those who wander are lost; the old that is strong does not wither, deep roots are not reached by the frost." -J. R. R. Tolkien',
            '"I cannot express it: but surely you and everybody have a notion that there is, or should be, an existence of yours beyond you." -Emily Bronte',
            '"Terror made me cruel." -Emily Bronte',
            '"You shall know the truth, and the truth shall make you mad." -Aldous Huxley',
            '"Science has explained nothing; the more we know the more fantastic the world becomes and the profounder the surrounding darkness." -Aldous Huxley',
            '"No amount of experimentation can ever prove me right; a single experiment can prove me wrong." -Albert Einstein',
            '"You gain strength, courage, and confidence by every experience in which you really stop to look fear in the face. You are able to say to yourself, \'I lived through this horror. I can take the next thing that comes along." -Eleanor Roosevelt',
            '"Good artists copy, great artists steal." -Pablo Picasso'
    ]
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
    if len(args) == 0: # >forward
        f'Error: must be in format `{client.command_prefix}shift_forward message`.'
    elif len(args) == 1 or not args[0].isdigit(): # >forward 24
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
            return f'Error: specified shift too big (ASCII table ends after 1114111 entries ;-;)'
        else:
            new_position = ord_of_character+shift
        encoded_string += chr(new_position)
    return encoded_string+""

    
#ascii table decode
@client.command(aliases=['back'])
async def shift_back(ctx,*args):
    await ctx.send(shifted_back(args))
def shifted_back(args):
    if len(args) == 0: # >forward
        f'Error: must be in format `{client.command_prefix}shift_forward message`.'
    elif len(args) == 1 or not args[0].isdigit(): # >forward 24
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
            return f'Error: specified shift too big (ASCII table ends after 1114111 entries ;-;)'
        else:
            new_position = ord_of_character-shift
        encoded_string += chr(new_position)
    return encoded_string+""

#info
@client.command(aliases=['i'])
async def info(ctx):
    await ctx.send( f'**{ctx.author}** ({ctx.author.id}) joined **{ctx.guild}** ({ctx.guild.id}) **at {ctx.author.joined_at}.**' )

client.run(TOKEN)