import random
from datetime import datetime, time, timedelta   # stan
import asyncio
from env import PREFIX 

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

        # Sleep until tomorrow, at which point the loop will start a new
        # iteration
        tomorrow = datetime.combine(now.date() + timedelta(days=1), time(0))
        seconds = (tomorrow - now).total_seconds()
        await asyncio.sleep(seconds)


def greeting_required(text):
    greetings = ["hi", "hello", "greetings", "welcome"]
    for greeting in greetings:
        if f'{greeting} qubitz' in text or f'{greeting}, qubitz' in text:
            return True


async def greet(message):
    async with message.channel.typing():
        faces = [":3", ":3", ":D", ":)", ":))", ":)))", "^-^", "^_^", "<3", "!", "!!", '', '']
        possible_names = [message.author.name, message.author.nick]
        name_to_use = random.choice(possible_names).lower()
    if len(name_to_use.split()) > 3:
        return await message.channel.send(f'hi, {name_to_use} {random.choice(faces)}')
    return await message.channel.send(f'hi {name_to_use} {random.choice(faces)}')


async def echo_uwu(message):
    text = message.content.lower()
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
            uwu_response = (uwu_word 
                            + puncts[most_common_punct] * 2 * most_common_punct)
            return await message.channel.send(uwu_response)


def is_rainbow(text):
    return (text[0] != PREFIX 
            and any(word in text for word in rainbow_words)
            and not any(word in text for word in sad_words))

async def be_rainbow (message):
    rand = random.randint(0, 100)
    if rand < 1:    # 1% chance lol
        return await message.channel.send(generate_keysmash())
    elif rand > 3:  # 5% chance
        return await message.channel.send(random.choice(responses))


def generate_keysmash():
    valid_characters = [
        "a","s","s","s","s","s",
        "d","d","g","d","f","g","h",
        "j","j","j","j","k","k","k","k",
        "l","z","x","w",";",";",";",";",
        "v","v",","
    ]
    keysmash = ""
    for i in range(random.randint(7, 20)):
        keysmash += random.choice(valid_characters)
    enders = [
        ":rainbow:",
        ":two_hearts:",
        ":pleading:",
        ":rainbow_flag:",
        "uwu",
        "<3",
        "", "", "", "", "", "", "", "", "",
        ",", 
        ",,",
    ]
    return f'{keysmash} {random.choice(enders)}'

responses = [
        "gay rights!",
        ":rainbow: gay rights! :rainbow:",
        "gay rights!",
        "gay rights!",
        "gay rights!",
        ":rainbow_flag:",
        ":rainbow_flag:",
        ":rainbow_flag:",
        ":rainbow_flag:",
        ":rainbow_flag:",
        ":rainbow:",
        "gay",
        "gay",
        "gay :D",
        "gay ^-^"
]

rainbow_words = [
    "gay",
    " gae ",
    " bi ",
    "sapphic",
    "lesbian",
    "lgbt",
    "queer",
    "wlw",
    "mlm",
]

sad_words = [
    "bible",
    "suicide",
    "depress",
    "anxi",
    "pain",
    "die",
    "death",
    "D:",
    ":/",
    ":(",
    "hate",
    "sad",
    "mad",
    "angry"
    "slur",
    "phobia",
    "tokenism",
    "stereotype",
    "anti",
    "pox",
    "sexually transmitted",
    "std",
    "sti",
    "hiv",
    "aids",
    "disease",
    "epidemi",
]
