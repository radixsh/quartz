# Bitz? Quartz?
I began developing an uwubot named Bitz for Discord in June 2020, in discord.js
because the first guides I found were in JavaScript. This turned out to be very
misguided, because (as I realized when our AP Computer Science Principles
teacher taught us the basics of discord.py later that year) discord.py is far
superior. Over the summer of 2020, I developed and hosted both bots on my
Chromebook.

I've wanted to translate Bitz's uwubot functionalities to Python for a while,
and I finally did, almost two years later. Bitz, the original uwubot I created,
has been translated to Python and conflated with Quartz's capabilities to form
Qubitz.

## Functionalities
Qubitz's functionalities include:
- `create_emoji [name]`: Create custom emojis by running this command and
  attaching an image file. If Qubitz has the necessary permissions, the image
  will be uploaded as a custom emoji in that guild.
- `info`: Get data about users in the guild.
- `echo [any message here]`: Anyone can `echo` anything, which is a good feature
  for pseudo-anonymity and general shenanigans.
- `uwuify [any message here]`: Uwuifies your messages, turning "hello" into
  "hewwo" and so on.
- `cat`: Get a cat picture using [The Cat API](https://api.thecatapi.com/v1/images/search).
- `list`: List each role, along with the users with that role. This
  functionality was ported from Amicitia, a bot intended to help students in my
  university Discord server find people with the same major. Amicitia's
  dedicated repo is now dead and gone in favor of Qubitz.
- `find [any role here]`: Print a list of everyone with a given role. This
  functionality was ported from Amicitia.

## Technologies
- [discord.py](https://discordpy.readthedocs.io/en/latest/index.html)
- [discord.ext.commands](https://discordpy.readthedocs.io/en/latest/ext/commands/index.html)
- [Discord API](https://discord.com/developers/docs/intro)
- [node.js](https://nodejs.org/en/)
- [nodemon](https://nodemon.io/)
    - [`nodemon --exec python3 hello.py`](https://stackoverflow.com/questions/65021005/how-to-run-python-3-with-nodemon)
- [The Cat API](https://thecatapi.com/)

## Usage
To set Qubitz up locally, you'll need `python3` and the packages for `discord`,
`requests`, and `aiohttp`.

You'll also need an API token, which you do by going to your Discord 
[developer portal](https://discord.com/developers/applications) and creating an
application. Click the subheading "bot" in the menubar on the left and add a
bot, and a secret token will have been generated under the bot's username.

Create a file called `env.py` with this as its contents:
```sh
TOKEN = "your-token-here-between-quotes"
```

In the developer portal again, under Bot, enable the server members and message
content intents. Under OAuth2 > URL Generator, generate an 
[invite link](https://discord.com/api/oauth2/authorize?client_id=812437788535423008&permissions=3468352&scope=bot)
by selecting the "bot" scope and adding the following permissions:
- Read Messages/View Channels
- Send Mesages
- Manage Messages
- Embed Links
- Attach Files
- Use External Emojis
- Add Reactions

Then you can run Qubitz:
```
$ python3 index.py

# Or, if you're a cool kid and you have nodemon:
$ nodemon --exec python3 index.py
```

## Acknowledgements
- [aiohttp documentation](https://docs.aiohttp.org/en/stable/client.html),
  especially [this comparison](https://docs.aiohttp.org/en/stable/http_request_lifecycle.html#aiohttp-request-lifecycle) between aiohttp and requests
- [discord.js guide](https://discordjs.guide/)
    - [Getting user input](https://discordjs.guide/creating-your-bot/commands-with-user-input.html#basic-arguments)
    - [Adding more commands](https://discordjs.guide/creating-your-bot/adding-more-commands.html)
    - [Creating embeds](https://discordjs.guide/popular-topics/embeds.html#embed-preview)
    - [Some basic es6 syntax examples](https://discordjs.guide/additional-info/es6-syntax.html#template-literals)
    - [Dynamically executing commands](https://discordjs.guide/command-handling/dynamic-commands.html#dynamically-executing-commands)
    - [Miscellaneous examples](https://discordjs.guide/popular-topics/miscellaneous-examples.html#play-music-from-youtube), including playing music from youtube and retrieving emoji characters from another file created in the same directory as index.js
- [How to create a music bot](https://www.freecodecamp.org/news/how-to-create-a-music-bot-using-discord-js-4436f5f3f0f8/) (Free Code Camp)
- [Adding a config file](https://anidiots.guide/first-bot/adding-a-config-file) (An Idiot's Guide) – This was helpful for conceptualizing the flow of order when the bot is running under `nodemon`. Using a config file taught me how the config file responds to calls from the index file.
    - [Understanding roles and permissions](https://anidiots.guide/understanding/roles)
- And, of course, places where people before me have asked questions:
    - [Get a picture from a message](https://stackoverflow.com/questions/55206958/get-a-picture-from-the-message) (Stack Overflow)
    - [Take file as argument](https://stackoverflow.com/questions/59181208/discord-py-bot-take-file-as-argument-to-command) (Stack Overflow)
    - [Discord bot send attachments](https://www.reddit.com/r/learnpython/comments/9ishxs/discord_bot_send_attachments/e6m0trf/) (Reddit): pointed me to aiohttp
    - [Using nodemon with python3](https://stackoverflow.com/questions/65021005/how-to-run-python-3-with-nodemon) (Stack Overflow)
- [Eric Yeung's Discord music bot](https://github.com/eric-yeung/Discord-Bot/blob/master/main.py)

Bitz was named by my close friend Tumega500#1234.

## License
Released under [GNU GPL v3](https://www.gnu.org/licenses/gpl-3.0.en.html).
