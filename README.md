# bitz — discord bot
bitz is a [node.js](https://nodejs.org/en/) discord bot that can delete messages, echo messages, create polls, and perform pings. bitz also responds rather interestingly to certain "owo", "uwu", and keysmash messages. :)

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
* to apply what i learned in class studying java (and learning some git) this past year, and 
* to have fun creating a bot for friends in the summer. 

in retrospect i could've chosen to learn python and use that to write bitz, but to be honest it was hard enough figuring out the discord api already, as well as fun enough learning where exactly my java knowledge ends and the discord.js documentation (and stack overflow wisdom!) begins.

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
```

on debian/ubuntu ([source](https://www.digitalocean.com/community/tutorials/how-to-install-node-js-on-ubuntu-18-04)): 
```
# refresh your local package index
$ sudo apt update

# install node (and hit y when prompted)
# (the package is called nodejs rather than node because of a naming conflict; don't worry about that)
$ sudo apt install nodejs

# to confirm the install worked
$ nodejs -v

# install git (and hit y when prompted)
$ sudo apt-get install git
```

then on your command line, whether mac or linux, run the following:
```
# install discord.js, as well as other dependencies necessary to support playing music
$ npm install discord.js ffmpeg-binaries opusscript ytdl-core --save

# clone this repository
$ git clone https://github.com/radradix/bitz

# go into the newly created repository
$ cd bitz
```

before starting bitz, you'll need to make your own config.json file and put your api token into it. my config.json file is in thie repository — encrypted — as a kind of placeholder (and because it makes it easier for me during development). so create your own config file: 
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
  "ownerID": "519672846075822101"
}
```
(the ownerID line allows me access to any quirks i want to keep to myself :) you can add whatever constants you want, or keep it to just the two lines. just make sure the last line doesn't end with a trailing comma.)

once your bot's been made, you'll need to add it to a discord guild (colloquially, "server") in which you have admin privileges. to do that, go to `https://discord.com/oauth2/authorize?client_id=YOUR_BOT_TOKEN_HERE&scope=bot&permissions=3209216`. obviously, put your own bot's id there. 

once your config file has been created, you're good to go! on mac, run `node index.js` (or `nodemon` if you have that installed). then you're finished!

on ubuntu, you might need to upgrade node if the output of `nodejs -v` is something ridiculously primitive like v4.2.6 (ahem, @ my crouton-ed chromebook). to upgrade node, run this: 
```
# you can use a module called n to upgrade your node package
$ sudo npm install -g n
$ sudo n stable
```
then you can run bitz using `nodejs index.js` (or, if you have it, use `nodemon`.) to be honest, i'm really not sure if this will work. so far it's not working on my chromebook, but then, that's a chromebook. :)

## functionalities
[...]

## examples
[...]

## project status
bitz is still in development, testing regularly in discord. eventually the sandbox guild will go public, the link will be here, and support will be available. 

currently, these are my next steps: 
* properly address errors so that error messages come back nice and neat instead of vomiting themselves into the console
* rewrite the whole thing using switch() case
  * alternately, find a faster way of doing things, and implement that. just, i want to learn a new way to write things than the if/else loops we learned for ap :)
* actually, optimize (and make easily readable) the whole project. right now it has functionality and that's it. 
* plan out and implement a randomized `uwu`/`owo` system (i.e., at random times, perhaps once every couple of days or every 500 to 1000 messages in the guild, send an `uwu` or `owo` independently)

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
