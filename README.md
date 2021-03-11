# bitz — discord bot 
bitz is a [node.js](https://nodejs.org/en/) discord bot who can echo messages, uwuify messages, delete messages, create polls, and perform pings. bitz also responds to "owo" and "uwu" messages. 

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
* convenient message mass-deletion (honestly, that feature is missing from discord)
* poll creation (another feature missing from discord) 
* anyone can `!echo` anything, which is a good feature for pseudo-anonymity and general shenanigans 
* bonus: will train you to use uwuspeak more often

currently available commands (`!command <argument> [optional argument]`):

* `!h[elp]` : shows this help page
* `!purge <n>` : deletes the `n` most recent messages in the current channel (2 < `n` < 100), and also deletes the command message
* `!echo <foo>` : echoes back what you tell it to, deleting the command message. (it works for one image at a time too)
* `!poll "<polling question>" "<poll answer 1>" "<poll answer 2"> "[poll answer 3]" ...` : creates a poll in an embed, deleting the command message. at least three arguments are necessary, set off by double quotation marks: a question and at least two options.
  + here's what a poll might look like: 
  + ![poll](https://i.imgur.com/GHtRUHem.png)
* `!ping` : performs a ping
* `!uwu` : uwuifies your messages
* `!uwuchannel [-rm]` : uwuifies all future messages in the current channel. the option `-rm` removes this setting.
* `!data` : gets metadata of the current guild and channel, and also gives information about you.


here's some sample console output :)
![sample console output](https://i.imgur.com/aVTbNcQ.png)


## technologies
this project was created with: 
* [node.js](https://nodejs.org/en/) v12.18.0 — an open-source, cross-platform javascript runtime environment that executes javascript code outside a web browser
* [discord.js](https://discord.js.org/#/) v12.2.0 ([documentation](https://discordjs-fork.readthedocs.io/en/latest/index.html)) — a powerful object-oriented node.js module that allows easy interaction with the discord api
* [discord api](https://discord.com/developers/docs/intro) 
* [nodemon](https://www.npmjs.com/package/nodemon) v2.0.4 — a tool that helps develop node.js based applications by automatically restarting the node application when file changes in the directory are detected

## setup
to clone and run this application, you'll need git and node.js (which comes with npm). (nodemon is most helpful during development; you won't need it just to replicate bitz.) 

on mac (i did this): 
```
# you'll need to have homebrew and git first
# here's the installation command for homebrew from https://brew.sh: 
$ /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"

# install git
$ brew install git

# install node.js using homebrew
$ brew install node

# install discord.js
$ npm install discord.js opusscript --save

# clone this repository
$ git clone https://github.com/radradix/bitz

# go into the newly created repository
$ cd bitz
```

before starting bitz, you'll need to make your own config.json file and put your api token into it. my config.json file is in this repository — encrypted — as a kind of placeholder (and because it makes it easier for me during development). so create your own config file: 
```
$ rm config.json
$ touch config.json
```

the config file will hold, at minimum, your token and your chosen command prefix (in the command `!help`, for instance, the prefix is `!`). 

to generate your own api token, go to your [discord developer portal](https://discord.com/developers/applications) and create an application. click the subheading "bot" in the menubar on the left and add a bot, and a token will have been generated under the bot's username. (this token must be kept secret.) here's the format that i used: 
```
{
  "token": "my-token-here-between-quotes",
  "prefix": "!",
  "permittedGuilds": "1234567890"
}
```
(the permittedGuilds line allows you the option to silence bitz everywhere except the sandbox guild, for instance while testing beta features. you can add whatever constants you want to the config file, or keep it to just the two lines — just make sure the last line doesn't end with a trailing comma.)

once your bot's been made, you'll need to add it to a discord guild (colloquially, "server") in which you have admin privileges. to do that, go to `https://discord.com/oauth2/authorize?client_id=YOUR_BOT_TOKEN_HERE&scope=bot&permissions=3209216`. 

on mac at least, run `node index.js` (or `nodemon`) to start bitz. then you're finished!

## project status
bitz is still in development, testing regularly in discord. 

currently, these are my next steps: 
* figure out how to echo images
* daily stan messages
* upload images and turn them into custom server emojis?
* offer option to limit bitz to certain channels in a guild
* offer option to escape certain characters in an uwuchannel

## sources
to create this project, i found the following sources incredibly useful: 
* [*discord.js guide*](https://discordjs.guide/) — an invaluable source of explanations and examples! second only to official documentation! specifically, i used:
  + [getting user input](https://discordjs.guide/creating-your-bot/commands-with-user-input.html#basic-arguments)
  + [adding more commands](https://discordjs.guide/creating-your-bot/adding-more-commands.html)
  + [creating embeds](https://discordjs.guide/popular-topics/embeds.html#embed-preview)
  - [some basic es6 syntax examples](https://discordjs.guide/additional-info/es6-syntax.html#template-literals)
  - [dynamically executing commands](https://discordjs.guide/command-handling/dynamic-commands.html#dynamically-executing-commands)
  - [miscellaneous examples](https://discordjs.guide/popular-topics/miscellaneous-examples.html#play-music-from-youtube), including playing music from youtube and retrieving emoji characters from another file created in the same directory as index.js  
* [how to create a music bot (*free code camp*)](https://www.freecodecamp.org/news/how-to-create-a-music-bot-using-discord-js-4436f5f3f0f8/)
* [*an idiot's guide*](https://anidiots.guide/)
  + [adding a config file](https://anidiots.guide/first-bot/adding-a-config-file) – this was helpful for conceptualizing the flow of order when the bot is running under `nodemon`. using a config file requires understanding of how the config file responds to calls from the index file, as well as comprehension of the syntax necessary to do so. this blew my mind. 
  + [understanding roles and permissions](https://anidiots.guide/understanding/roles)
* [hosting a discord bot](https://www.writebots.com/discord-bot-hosting/#Glitch) — i haven't looked much into this, but i plan to!

## license
released under the [MIT](https://opensource.org/licenses/MIT) license.

bitz was named by my close friend tomega500#4689. artwork was also created by him. 
