const Discord = require('discord.js');
const bot = new Discord.Client();
const guilds = new Discord.Guild(bot,)
const config = require("./config.json");   
const emojiCharacters = require("./emojiCharacters.js");
const ytdl = require('ytdl-core');
/*const { Permissions } = require('discord.js');
const flags = [
	'MANAGE_CHANNELS',
	'EMBED_LINKS',
	'ATTACH_FILES',
	'READ_MESSAGE_HISTORY',
	'MANAGE_ROLES',
];
const permissions = new Permissions(3172352);
https://discord.com/oauth2/authorize?client_id=722289214363926592&scope=bot&permissions=3172352*/

bot.on('ready', () => {
    // const { prefix, token } = require('./config.json');
    console.log(`Logged in as ${bot.user.tag}!`); 
    console.log("Now in " + bot.guilds.cache.size + " guilds :D");
});

bot.on('disconnect', () => {
    console.log('Disconnect!');
});

bot.on("guildCreate", guild => {
    const canal = guild.channels.cache.find(channel => channel.type === 'text' && channel.permissionsFor(guild.me).has('SEND_MESSAGES'));
    canal.send("hello!! I'm Bitz and it's good to meet y'all! my command prefix is `!`, and you can see my documentation at `!help` :))");
    console.log(`Joined ${bot.guilds.cache.name}!`);
});

bot.on('message', async message => { 
    var len = 0; // if the message is all "!", then exit early
    for(let i = 0; i < message.content.length; i++) 
        if(message.content[i] === "!") len++;
    if(len === message.content.length || message.author.bot) return;

    if(message.content.substring(0,1) === "!"){
        var args = message.content.slice(config.prefix.length).trim().split(" ");// / +/g);
        var command = args.shift().toLowerCase();
    } 
        /*var args = message.content.split("\n");
        for(let i = 0; i < args.length; i++){
            if(args[i].startsWith(">")){
                console.log("QUOTATION ALERT!");
                args.shift();
                console.log(args);
                i--;
            }
        }*/
    var rickWords = ["as;ld",
        "ajdfk",
        "sjdfk",
        "as;dl",
        "sdajf",
        "asdkf;fkl",
        "aksdl",
        "asdkl",
        "skjdfklsjf",
        "sjdskfjkd",
        "asjdkfjs",
        "sdkjflksdjf",
        "dfklsjf",
        "skdjf",
        "skskj"
    ]
    var theMessageContainsARickWord = false;
    for (let i = 0; i < rickWords.length; i++){
        if(message.content.toLowerCase().includes(rickWords[i])){
            theMessageContainsARickWord = true;
            break; 
        }
    }
    if (message.content.substring(0,1) !== "!" && !theMessageContainsARickWord && !message.content.toLowerCase().includes("uwu") && !message.content.toLowerCase().includes("owo")) return; 
        // if the message doesn't start with `!` or contain a rickWord or contain uwu or contain owo, then end early.
    console.log("\n" + message.author.username);
    if(command) console.log("Command: " + command + "\tArgs (" + args.length + "): " + args);
    
    if (command === 'ping'){
        const m = await message.channel.send("ping?");
        return m.edit(`pong! latency is ${m.createdTimestamp - message.createdTimestamp} ms :)`);
    } else if(command === "help" || command === "h"){
        const helpEmbed = new Discord.MessageEmbed()
        .setColor('#8db255')
        .setTitle('Help')
        // .setURL('https://discord.js.org/')
        // .setAuthor('radix', 'https://i.imgur.com/wSTFkRM.png')//, 'https://discord.js.org')
        .setDescription("Hey, I'm Bitz ^-^ Here's some stuff I do. I don't know why I do these things, but here they are anyway \¯\\\_\(\ツ\)\_\/\¯\n\n(Also, I'm just a baby — sorry if stuff goes wrong >.< I don't know a lot yet, but I'm learning!!!)")
        // .setThumbnail('https://i.imgur.com/wSTFkRM.png')
        .addFields(
            { name: '!purge <n>', value: 'Deletes `n` messages in the current channel (2 < `n` < 100). \n`!purge 20`'},
            //{ name: '\u200B', value: '\u200B' },
            { name: '!echo [foo]', value: 'Echoes back what you tell it to, deleting the command message. \n`!echo foo`'},
            { name: '!poll "<polling question>" "<poll answer 1>" "<poll answer 2"> "[poll answer 3]" ...', value: 'Creates a poll in an embed, deleting the command message. \n`!poll "What\'s your favorite color?" "red" "blue" "green"`'},
            { name: '!ping', value: 'Performs a ping. No arguments. \n`!ping`'},
            { name: '!h[elp]', value: "You're right here, so you must know there are no arguments necessary here either (: \n`!h`"}
        )
        // .addField('Inline field title', 'Some value here', true)
        // .setImage('https://i.imgur.com/wSTFkRM.png')
        // .setTimestamp()
        .setFooter('Developed by radix#4520');//, 'https://i.imgur.com/wSTFkRM.png')
        return message.channel.send(helpEmbed);
    } else if (command === 'echo'){
        const sayMessage = args.join(" ");
        message.delete().catch(O_o=>{}); 
        return message.channel.send(sayMessage);
    } else if(command === "purge") {
        const deleteCount = parseInt(args[0], 10);
        if(!deleteCount || deleteCount < 2 || deleteCount > 100)
            return message.channel.send("you're supposed to provide a number between 2 and 100 (inclusive) for the number of messages to delete :/");
        // const fetched = await message.channel.fetchMessages({limit: deleteCount});
        message.channel.bulkDelete(deleteCount)
        .catch(error => message.reply(`Couldn't delete messages because of: ${error}`));
    } else if(command === "poll"){
        var pollThing = "";
        for(let i = 0; i < args.length; i++)
            pollThing += args[i] + " ";
        //console.log("Poll thing: " + pollThing);
        var pollQuestion = pollThing.substring(1,pollThing.indexOf("\"",1));
        console.log("Poll question: " + pollQuestion);

        var howManyOptions = 0;
        for(let i = 0; i < pollThing.length; i++){
            if(pollThing[i] === "\"")
                howManyOptions++;
        }
        howManyOptions /= 2;
        howManyOptions -= 1;
        console.log("Number of options: " + howManyOptions);
        if(howManyOptions - Math.floor(howManyOptions) != 0)
            return message.channel.send("errr,,,, think you made a mistake with the quotation marks :/");
        if(howManyOptions+1 < 3 || howManyOptions+1 > 11) // only one answer option given, or ~9 options given
            return message.channel.send("you're supposed to provide between 2 and 10 (inclusive) options :/");
        
        var pollOptions = []; 
        var nextQuoteIndex = pollThing.indexOf("\"",pollThing.indexOf("\"",1));
        nextQuoteIndex = pollThing.indexOf("\"",nextQuoteIndex+1);
        //console.log("nextQuoteIndex: " + nextQuoteIndex);
        for(let i = 0; i < howManyOptions; i++){
            pollOptions[i] = pollThing.substring(nextQuoteIndex+1,pollThing.indexOf("\"",nextQuoteIndex+1));
            nextQuoteIndex = pollThing.indexOf("\"",nextQuoteIndex+1);
            nextQuoteIndex = pollThing.indexOf("\"",nextQuoteIndex+1);
            console.log("pollOptions[" + i + "]: " + pollOptions[i] + "\t\tnextQuoteIndex: " + nextQuoteIndex);
        }
        console.log("Poll options: " + pollOptions);
        /*REMOVING EMPTY ELEMENTS: 
        for(let i = 0; i < pollOptions.length; i++){ 
            if(pollOptions[i] === " ") // https://stackoverflow.com/questions/5767325/how-can-i-remove-a-specific-item-from-an-array
                pollOptions.splice(i, 1);
        }
        console.log("Poll options after removing empty elements: " + pollOptions);*/
        message.delete().catch(O_o=>{}); 
        var opciones = "";
        for(let i = 0; i < pollOptions.length; i++){
            opciones += "\n( " + emojiCharacters[i+1] + " )  " + pollOptions[i]; 
            // embed.addField("( " + emojiCharacters[i+1] + " )", pollOptions[i],false);
        }
        let embed = new Discord.MessageEmbed()
            .setColor("#8db255")
            .setDescription('\n▬▬▬▬▬▬▬▬▬**«    Poll    »**▬▬▬▬▬▬▬▬▬▬\n\n**Poll question »** ' + pollQuestion + '\n\n**Poll options »**' + opciones)
            embed.setTimestamp();
            

        message.channel.send(embed).then(sentEmbed => {
            for(let i = 0; i < pollOptions.length; i++){
                sentEmbed.react(emojiCharacters[i+1]);
            }
        })
        return;
    } else if(message.content.substring(0,1) === "!"){ // !command not recognized
        return message.channel.send("my documentation's at `!help` ^-^");
    }
    // else { // IF IT'S NOT IN THE FORMAT `!COMMAND ARGUMENTS`
    var theMessage = message.content.toLowerCase();
    for (let i = 0; i < rickWords.length; i++) {
        if (message.content.toLowerCase().includes(rickWords[i])) {
            // ELEPHANT
            console.log(message.content);
            if(message.member.voice.channel && bot.roles.has('CONNECT') && permissions.has('SPEAK')){
                message.member.voice.channel.join().then(connection => {
                    const stream = ytdl('https://www.youtube.com/watch?v=dQw4w9WgXcQ', { filter: 'audioonly' });
                    const dispatcher = connection.play(stream);
                    dispatcher.on('end', () => message.member.voice.channel.leave());
                });
            } else {
                // send the video in the channel
                message.channel.send("are you okay? here, this might make you feel better >.<");
                // var file = Discord.file("~/onehentwoducks/satisfied.png", filename="image.png"); 
                /*message.channel.send(new Discord.MessageAttachment('satisfied.png', 'satisfied.png') )
                .catch(console.error);*/
                //var image = new Discord.MessageAttachment("satisfied.png", "satisfied.png");
                const rickroll = new Discord.MessageEmbed()
                .setColor('#e52d27')//#B2558D')
                .setAuthor('YouTube')//,'https://www.youtube.com/watch?v=dQw4w9WgXcQ')
                .setTitle('Satisfied')
                .setURL('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
                .setDescription("Renée Elise Goldsberry - Topic")//",'https://www.youtube.com/watch?v=dQw4w9WgXcQ')
                //.addField([Guide]('https://discordjs.guide/' 'optional hovertext'))
                .setImage('https://i.imgur.com/rOBJRja.png')//,'https://www.youtube.com/watch?v=dQw4w9WgXcQ');// attachment://satisfied.png')//http://inthepastlane.com/wp-content/uploads/2016/04/hamilton-logo.jpg')
                //.setThumbnail('https://www.youtube.com/watch?v=InupuylYdcY')
                //.setURL('https://www.youtube.com/watch?v=dQw4w9WgXcQ'));
                message.channel.send(rickroll);
            }
            return;
        } 
    }
    // if it's not rick-roll-worthy
    if(message.content.includes("\n")){ // if the message has newline char(s) and could potentially have quoted material
        var notQuotations = message.content.toLowerCase().toString().split("\n"); // notQuotations is a String array, not a String; therefore, split() cannot be called on it. 
        for(let i = 0; i < notQuotations.length; i++){
            if(notQuotations[i].startsWith(">")){
                console.log("[quotation :)]");
                notQuotations.shift();
                i--;
            }
        }
    } else var notQuotations = message.content.toLowerCase().split(" ");
    console.log("Non-quoted text: " + notQuotations);
    for(let i = 0; i < notQuotations.length; i++){
        if(!notQuotations[i].includes("owo") && !notQuotations[i].includes("uwu")){
            notQuotations.splice(i,1);
            i--;
        }
    }
    console.log("Non-quoted text after removing words that aren't owo/uwu: " + notQuotations);
    theMessage = "";
    for(let i = 0; i < notQuotations.length; i++){
        theMessage += notQuotations[i];
    }
    console.log("Message: " + theMessage);
    if(theMessage.includes("uwu") || theMessage.includes("owo")){
        // const wordsThatMightNotBeUwu = theMessage.split(/\s+/); // / +/g);
        for(let i = 0; i < notQuotations.length; i++){
            if(notQuotations[i].includes("uwu") || notQuotations[i].includes("owo")){
                // lastLetters = wordsThatMightNotBeUwu[i].slice(-1); // uwu!! --> !!
                if(notQuotations[i].includes("uwu")){
                    var lastLetters = notQuotations[i].substring(notQuotations[i].indexOf("uwu")+3);
                } else { //it's an "owo" phrase
                    var lastLetters = notQuotations[i].substring(notQuotations[i].indexOf("owo")+3);
                }
                //console.log("Last letters: " + lastLetters);
                const punctuationArray = ["?","!","."];
                for(let i = 0; i < lastLetters.length-1; i++){
                    if(!punctuationArray.includes(lastLetters.substring(i,i+1))){
                        lastLetters = lastLetters.substring(0,lastLetters.length-1);
                        i--;
                    }
                }
                // console.log("Last letters after punct: " + lastLetters);
                if(!lastLetters){
                    return message.channel.send(notQuotations[i]);
                } else if(lastLetters.includes(".")){
                    return message.channel.send(notQuotations[i]);
                } else if(lastLetters.includes("?") || lastLetters.includes("!")){
                    return message.channel.send(notQuotations[i] + lastLetters);
                } else{ // else, the uwu/owo does not end in !, ?, or .
                    if(notQuotations[i].includes("owo")){
                        // debug: console.log(wordsThatMightNotBeUwu[i].indexOf("owo"),wordsThatMightNotBeUwu[i].indexOf("owo")+3);    
                        return message.channel.send(notQuotations[i].substring(notQuotations[i].indexOf("owo"),notQuotations[i].indexOf("owo")+3));
                    } else if(notQuotations[i].includes("uwu")){
                        return message.channel.send(notQuotations[i].substring(notQuotations[i].indexOf("uwu"),notQuotations[i].indexOf("uwu")+3));
                    }
                }
            }
        }
    }
});

bot.login(config.token);
