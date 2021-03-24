# Quartz
Quartz is a discord.py bot I created for APCSP class. Main functionalities include: 
- connect to some public APIs 
   - `joke`: sends a joke from https://official-joke-api.appspot.com/random_joke
   - `cat`: sends a cat picture from https://api.thecatapi.com/v1/images/search
   - `dog`: sends a dog picture from https://dog.ceo/api/breeds/image/random
   - `bitcoin`: sends Bitcoin conversion rates from https://api.coindesk.com/v1/bpi/currentprice.json
- `shift_forward [shift=1] [foo]`: shifts `foo` forward `shift` spaces in the ASCII table
- `shift_backward [shift=1] [foo]`: shifts `foo` back `shift` spaces in the ASCII table
- `emoji [name]`: Custom emoji uploading is now supported! Run this command, and attach the image file. If Quartz has the necessary permissions, the image will be uploaded as a custom emoji in that guild. 

## Technologies used
- [discord.py](https://discordpy.readthedocs.io/en/latest/index.html)
- [discord.ext.commands](https://discordpy.readthedocs.io/en/latest/ext/commands/index.html)
- [nodemon](https://nodemon.io/)
- [Dog API](https://dog.ceo/dog-api/)
- [Cat API](https://thecatapi.com/)
- [Official Joke API](https://official-joke-api.appspot.com/)
- [CoinDesk](https://api.coindesk.com/v1/bpi/currentprice.json)
- [nodemon](https://nodemon.io/) v2.0.7

## Usage
Add my instance of Quartz to your own Discord guild with [this link](https://discord.com/oauth2/authorize?client_id=812437788535423008&permissions=4027051088&scope=bot).

To set Quartz up locally, you'll need python3. 
```sh
#install dependencies that aren't in standard library
$ pip install discord
$ pip install requests
$ pip install aiohttp

#clone this repository
$ git clone https://github.com/radradix/quartz
$ cd quartz/
```
You'll also need an API token, which you do by going to your Discord [developer portal](https://discord.com/developers/applications) and creating an application. Click the subheading "bot" in the menubar on the left and add a bot, and a secret token will have been generated under the bot's username. 

Create an env.py file (`touch env.py`) and populate it using your text editor of choice:
```sh
TOKEN = "your-token-here-between-quotes"
```

Add your bot to a server using the developer portal again, and use permissions integer `4027051088`. Then it should be ready to go:
```
$ python3 index.py
```

## Acknowledgements
- [aiohttp documentation](https://docs.aiohttp.org/en/stable/client.html), especially [this comparison](https://docs.aiohttp.org/en/stable/http_request_lifecycle.html#aiohttp-request-lifecycle) between aiohttp and requests
- and, of course, places where people before me have asked questions:
   - [get a picture from a message](https://stackoverflow.com/questions/55206958/get-a-picture-from-the-message) (Stack Overflow)
   - [take file as argument](https://stackoverflow.com/questions/59181208/discord-py-bot-take-file-as-argument-to-command) (Stack Overflow)
   - [Discord bot send attachments](https://www.reddit.com/r/learnpython/comments/9ishxs/discord_bot_send_attachments/e6m0trf/) (Reddit): pointed me to aiohttp

## License
GNU GPLv3. Be nice. 