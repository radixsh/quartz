# Bitz? Quartz?
I began developing an uwubot named Bitz for Discord in June 2020, in discord.js because
the first guides I found were in JavaScript. This turned out to be very misguided,
because discord.py is much better. I realized that when our AP Computer
Science Principles teacher taught us the basics of discord.py later that
year. Mostly over the 2020 summer, I developed both bots and hosted them on my 
Chromebook. I've wanted to translate Bitz's uwubot 
functionalities to Python for a while, 
and I finally did today, almost two years later. Bitz, 
the original uwubot I created, has been translated to Python and conflated with 
Quartz's capabilities to form a bot I call Qubitz. 
     
Qubitz's functionalities include: 
- `uwuify [any message here]`: Uwuifies your messages, turning "hello" into "hewwo" and so on. 
- `echo [any message here]`: Anyone can `echo` anything, which is a good feature for pseudo-anonymity and general shenanigans.
- `emoji [name]`: Create custom emojis by running this command and attaching an image file. If Qubitz has the necessary permissions, the image will be uploaded as a custom emoji in that guild.
- `purge [1 < n < 100]`: Mass-delete the `n` most recent messages (as long as they are under 14 days old) in the current channel.
- `info`: Get data about the guild.
- `cat`: sends a cat picture using https://api.thecatapi.com/v1/images/search

## Technologies used
- [discord.py](https://discordpy.readthedocs.io/en/latest/index.html)
- [discord.ext.commands](https://discordpy.readthedocs.io/en/latest/ext/commands/index.html)
- [nodemon](https://nodemon.io/) v2.0.7
    - [`nodemon --exec python3 hello.py`](https://stackoverflow.com/questions/65021005/how-to-run-python-3-with-nodemon)
- [Cat API](https://thecatapi.com/)
- [Official Joke API](https://official-joke-api.appspot.com/)

## Usage
To set Qubitz up locally, you'll need python3. Install discord, requests, and aiohttp, then clone this repo.
```sh
$ git clone https://github.com/radradix/quartz
$ cd quartz/
```
You'll also need an API token, which you do by going to your Discord [developer portal](https://discord.com/developers/applications) and creating an application. Click the subheading "bot" in the menubar on the left and add a bot, and a secret token will have been generated under the bot's username. 

Create a file called `env.py` with this as its contents: 
```sh
TOKEN = "your-token-here-between-quotes"
```

In the developer portal again, under Bot, enable the server members and message content intents.
Under OAuth2 > URL Generator, generate an invite link by selecting `bot` scope
and adding the following permissions:
- Read Messages/View Channels
- Send Mesages
- Manage Messages
- Embed Links
- Attach Files
- Use External Emojis
- Add Reactions
- Connect
- Speak
For me, this yielded [this link](https://discord.com/api/oauth2/authorize?client_id=812437788535423008&permissions=3468352&scope=bot).

Then you can run Qubitz:
```
$ python3 index.py

# or, if you're a cool kid and you have nodemon
$ nodemon --exec python3 index.py
```

## Acknowledgements
- [aiohttp documentation](https://docs.aiohttp.org/en/stable/client.html), especially [this comparison](https://docs.aiohttp.org/en/stable/http_request_lifecycle.html#aiohttp-request-lifecycle) between aiohttp and requests
- and, of course, places where people before me have asked questions:
    - [get a picture from a message](https://stackoverflow.com/questions/55206958/get-a-picture-from-the-message) (Stack Overflow)
    - [take file as argument](https://stackoverflow.com/questions/59181208/discord-py-bot-take-file-as-argument-to-command) (Stack Overflow)
    - [Discord bot send attachments](https://www.reddit.com/r/learnpython/comments/9ishxs/discord_bot_send_attachments/e6m0trf/) (Reddit): pointed me to aiohttp
    - [using nodemon with python3](https://stackoverflow.com/questions/65021005/how-to-run-python-3-with-nodemon) (Stack Overflow)

## License
GNU GPLv3. Be nice. 
