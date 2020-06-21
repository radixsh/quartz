# bitz — discord bot
bitz is a simple discord bot written with [node.js](https://nodejs.org/en/). bitz can delete messages, echo messages, create polls, and perform pings; bitz also responds rather interestingly to certain "owo", "uwu", and keysmash messages. :)

## table of contents
1. [general info](#general-info)
2. [technologies](#technologies)
3. [setup](#setup)
4. [functionalities](#functionalities)
5. [examples](#examples)
6. [project status](#project-status)
7. [sources](#sources)
8. [license](#license)

## general info
i created bitz for three reasons: 
* to learn a bit of javascript to complement my basic understanding of html and css, 
* to apply what i learned in class studying java this past year, and 
* to have fun creating a bot for friends in the summer. 

in retrospect i could've chosen to learn python and use that to write bitz, but to be honest it was hard enough figuring out the discord api already, as well as fun enough learning where exactly my java knowledge ends and the discord.js documentation (and stack overflow wisdom!) begins.

## technologies
this project is created with: 
* [node.js](https://nodejs.org/en/)
* [discord.js v12.2.0](https://discord.js.org/#/) ([documentation](https://discordjs-fork.readthedocs.io/en/latest/index.html))
* [discord api](https://discord.com/developers/docs/intro) 
* [nodemon](https://www.npmjs.com/package/nodemon) v2.0.4 — a tool that helps develop node.js based applications by automatically restarting the node application when file changes in the directory are detected.

## setup
to replicate bitz, [...]

(a discord api key is necessary in the config.json file)

## functionalities
[...]

## examples
[...]

## project status
bitz is still in development, testing regularly in discord. eventually the sandbox guild will go public, the link will be here, and support will be available. 

currently, my next steps are: 
* address the bug that the message `uwowo` returns `uwowo` rather than `owo` 
* plan out and implement a randomized `owo`/`uwu` system (i.e., at random times, start `owo`/`uwu` chains independently)

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
released under the [gnu gpl v2](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html) license.

bitz was named by my close friend tomega500#4689. artwork was also created by him. 
