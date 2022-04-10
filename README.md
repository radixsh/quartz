<<<<<<< HEAD
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
=======
# bitz — discord bot
bitz is a [node.js](https://nodejs.org/en/) discord bot who can echo messages, uwuify messages, delete messages, and create polls. their most distinctive feature is that they respond to messages containing the strings `owo` and `uwu`.

bitz was named by my close friend tumega500#4689; their profile picture art was also created by him.

## table of contents  
1. [general info](#general-info)
2. [features](#features)
3. [technologies](#technologies)
4. [setup](#setup)
5. [project status](#project-status)
6. [sources](#sources)
7. [license](#license)

## general info
i created bitz for three reasons:
* to learn a bit of javascript to complement my basic understanding of html and css,
* to apply what i learned in apcsa in junior year, and
* to have fun creating a bot for friends in the summer.

i could've chosen to learn python and use that to write bitz, but to be honest it was hard enough figuring out the discord api already, as well as fun enough learning how to use the discord.js documentation (and stack overflow wisdom!) to do what i wanted to do.

## features
* convenient mass-deletion of recent messages (honestly, that feature is missing from discord)
* poll creation (another feature missing from discord)
* anyone can `$echo` anything, which is a good feature for pseudo-anonymity and general shenanigans
* bonus: will train you to use uwuspeak more often

currently available commands (`$command <argument> [optional argument]`):

* `$purge num` : deletes the `num` most recent messages in the current channel (2 < `num` < 100), and also deletes the command message
* `$echo foo` : echoes back what you tell it to, deleting the command message.
* `$poll "foo?" "bar" "bar but not" "[bar but better]" ...` : creates a poll in an embed, deleting the command message. at least three arguments are necessary, set off by double quotation marks: a question and at least two options.
* `$uwu bar` : uwuifies your messages (turning `bar` into `baw`)
* `$uwuchannel [-rm]` : uwuifies all future messages in the current channel. the option `-rm` removes this setting.
* `$cc[d]` : counts characters in your message (ignoring the command's length). use `ccd` instead to delete the message.
* `$wc[d]` counts words in your message separated by spaces and em dashes (ignoring the command's length). use `wcd` instead to delete the message.
* `$data` : gets data about the current guild, current channel, and you :)

## technologies
this project was created with:
* [node.js](https://nodejs.org/en/) v12.18.0: an open-source, cross-platform javascript runtime environment that executes javascript code outside a web browser
* [discord.js](https://discord.js.org/#/) v12.2.0 ([documentation](https://discordjs-fork.readthedocs.io/en/latest/index.html)): a powerful object-oriented node.js module that allows easy interaction with the discord api
* [discord api](https://discord.com/developers/docs/intro)
* [nodemon](https://www.npmjs.com/package/nodemon) v2.0.4: a tool that helps develop node.js based applications by automatically restarting the node application when file changes in the directory are detected

## setup
to clone and run this application, you'll need git and node.js (which comes with npm). clone it with `git clone https://github.com/radradix/bitz`. before starting bitz, you'll need to make your own config.json file, which will look something like this:

```js
{
     "token": "your-token-here",
     "prefix": "$",
     "permittedGuilds": ["1234567890"]
}
```

to generate an api token, go to the [discord developer portal](https://discord.com/developers/applications) and create an application. click the subheading "bot" in the menubar on the left and add a bot, and a secret token will have been generated under the bot's username.

(the permittedGuilds line allows you the option to silence bitz everywhere except the sandbox guild, for instance while testing beta features. you can add whatever constants you want to the config file; just make sure the last line doesn't end with a trailing comma.)

once your bot's been made, you'll need to add it to a discord guild (colloquially, "server") in which you have admin privileges. to do that, go to your developer portal again and create a bot invite link with the permissions integer `10304`.

finally, run `node index.js` (or `nodemon`) to start bitz. then you're finished!

## project status
bitz is phasing out of development since i realized that time-based tasks are much better supported in discord.ext.tasks (an extension to discord.py, rather than discord.js).

## sources
to create this project, i found the following sources incredibly useful:
* [*discord.js guide*](https://discordjs.guide/) — an invaluable source of explanations and examples! second only to official documentation! specifically, i used:
  + [getting user input](https://discordjs.guide/creating-your-bot/commands-with-user-input.html#basic-arguments)
  + [adding more commands](https://discordjs.guide/creating-your-bot/adding-more-commands.html)
  + [creating embeds](https://discordjs.guide/popular-topics/embeds.html#embed-preview)
  + [some basic es6 syntax examples](https://discordjs.guide/additional-info/es6-syntax.html#template-literals)
  + [dynamically executing commands](https://discordjs.guide/command-handling/dynamic-commands.html#dynamically-executing-commands)
  + [miscellaneous examples](https://discordjs.guide/popular-topics/miscellaneous-examples.html#play-music-from-youtube), including playing music from youtube and retrieving emoji characters from another file created in the same directory as index.js  
* [how to create a music bot (*free code camp*)](https://www.freecodecamp.org/news/how-to-create-a-music-bot-using-discord-js-4436f5f3f0f8/)
* [*an idiot's guide*](https://anidiots.guide/)
  + [adding a config file](https://anidiots.guide/first-bot/adding-a-config-file) – this was helpful for conceptualizing the flow of order when the bot is running under `nodemon`. using a config file requires understanding of how the config file responds to calls from the index file, as well as comprehension of the syntax necessary to do so. this blew my mind.
  + [understanding roles and permissions](https://anidiots.guide/understanding/roles)

## license
released under [GNU GPL v3](https://www.gnu.org/licenses/gpl-3.0.en.html).
>>>>>>> bitz/master
