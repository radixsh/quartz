import random
def generate_keysmash():
    valid_characters = [
        "a","s","s","s","s","s",
        "d","d","g","d","f","g","h",
        "j","j","j","j","k","k","k","k",
        "l","z","x","w",";",";",";",";",
        "v","v",","
    ]
    keysmash = ""
    for i in range(random.randint(7,20)):
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
    "gae",
    "sapphic",
    "lesbian",
    "lesbean",
    "rainbow",
    "lgbt",
    "queer",
    "wlw",
    "mlm",
    "nblm",
    "nblnb",
    "nblw",
]
sad_words = [
    "bible",
    "suicide",
    "depress",
    "pain",
    "die",
    "death",
    "yell",
    "D:",
    ":/",
    ":(",
    "hate",
    "sad",
    "mad",
    "anxi",
    "angry"
    "slur",
    "phobi"
]
