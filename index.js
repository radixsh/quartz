const Discord = require('discord.js');
const bot = new Discord.Client();
const guilds = new Discord.Guild(bot,)
const { token, prefix, ownerID} = require("./config.json");   
const emojiCharacters = require("./emojiCharacters.js");
const ytdl = require('ytdl-core');

// https://discord.com/oauth2/authorize?client_id=722289214363926592&scope=bot&permissions=3172352

bot.on('ready', () => {
    console.log(`Logged in as ${bot.user.tag}!`); 
    console.log("Now in " + bot.guilds.cache.size + " guilds :D");
});

bot.on('disconnect', () => {
    console.log('Disconnect!');
});

process.on('unhandledRejection', error => {
    console.error('UNHANDLED PROMISE REJECTION:\n', error);
    //message.channel.send("...meanie butt >:((");
});

bot.on("guildCreate", guild => {
    //message.send("hello!! i'm bitz, and it's good to meet y'all! my command prefix is `!`, and you can see my documentation at `!help` :))");
    console.log(`Joined ${bot.guilds.cache.name}!`);
});

bot.on('message', async message => {
    if(message.author.bot) return;
    // if it starts with the prefix, then separate the message into the command (first term) and the arguments
    const punctuationArray = ["?","!","."];
    if(message.content.substring(0,prefix.length) === prefix){
        var args = message.content.slice(prefix.length).trim().split(/\s+/g); // <-- NOTE TO SELF DO NOT CHANGE
        var command = args.shift().toLowerCase();
        var len = 0;
        for(let i = 0; i < command.length; i++) 
            if(punctuationArray.includes(command[i])) len++;
        if(len === command.length) var isPunctuation = true;
    } else var isPunctuation = false;

   

    var rickWords = ["as;ldsadklfjslfjklsdj",
        "ksdfjsakdlf;aksdl",
        "asdkdksfjdsfkljl",
    ]
    var theMessageContainsARickWord = false;
    for (let i = 0; i < rickWords.length; i++){
        if(message.content.toLowerCase().includes(rickWords[i])){
            theMessageContainsARickWord = true;
            console.log("Rickroll word: " + rickWords[i]);
            break; 
        }
    }
    // if the message doesn't start with `!` or contain a rickWord or an uwuWord, then exit early. NOTE TO SELF DO NOT CHANGE
    if (message.content.substring(0,prefix.length) !== prefix && !theMessageContainsARickWord && !message.content.toLowerCase().includes("uwu") && !message.content.toLowerCase().includes("owo")) return; 
    if(!message.channel.name) {
        isDm = true;
        console.log("\n" + message.createdAt + "\n" + message.author.username + " (dm)");
    } else console.log("\n" + message.createdAt + "\n" + message.author.username + " (#" + message.channel.name + " in " + message.guild.name + ")");
    if(command) console.log("Command: " + command + "\t\tArgs (" + args.length + "): " + args);
    
    // close the bot to everyone except me
    //if(message.author != ownerID) return message.channel.send("sorry, i'm down for testing ;-;");

    if (command === 'ping'){
        const m = await message.channel.send("ping?");
        return m.edit(`pong! latency is ${m.createdTimestamp - message.createdTimestamp} ms :)`);

    } else if(command === "help" || command === "h"){
        const helpEmbed = new Discord.MessageEmbed()
        .setColor('#8db255')
        .setTitle('help')
        //.setURL('https://discord.js.org/')
        //.setAuthor('radix',https://i.imgur.com/wSTFkRM.png')//, 'https://discord.js.org')
        .setDescription("greetings! bitz here ^-^ here's some stuff i do. i don't know why i do these things, but here they are anyway \¯\\\_\(\ツ\)\_\/\¯\n\n(also, i'm just a baby — sorry if stuff goes wrong >.< i don't know a lot yet, but i'm learning!)\n\n")
        .setThumbnail('https://i.imgur.com/r3KSiQ2.png')// https://i.imgur.com/da6KF1H.png')
        .addFields(
            { name: '!h[elp]', value: "shows this help page; no arguments. \n`!h`"},
            { name: '!purge <n>', value: "deletes the `n` most recent messages in the current channel (2 < `n` < 100), and also deletes the command message. (deletion isn't allowed in dms) \n`!purge 20`"},
            //{ name: '\u200B', value: '\u200B' },
            { name: '!echo [foo]', value: "echoes back what you tell it to, deleting the command message (deletion isn't allowed in dms). (it works for one image at a time too). \n`!echo uwu`"},
            { name: '!poll "<polling question>" "<poll answer 1>" "<poll answer 2"> "[poll answer 3]" ...', value: 'creates a poll in an embed, deleting the command message. at least three and no more than ten arguments are permitted, set off by double quotation marks: a question and at least two options. \n`!poll "what\'s your favorite color?" "red" "blue" "green"`'},
            { name: '!ping', value: 'performs a ping; no arguments. \n`!ping`'},
        )
        //.setImage('https://i.imgur.com/VuKlykl.png')
        // .addField('Inline field title', 'Some value here', true)
        // .setTimestamp()
        .setFooter('developed by radix#4520');//, 'https://i.imgur.com/wSTFkRM.png')
        return message.channel.send(helpEmbed);

    } else if (command === 'echo'){
        if(isDm) message.channel.send("(i'm not allowed to delete things in dms :/)");
        var textToEcho = args.join(" ");
        if(args.length === 0) return message.channel.send("**bruh**");
        if(message.attachments.size === 0) message.channel.send(textToEcho);
        else {
            const imageUrl = message.attachments.array()[0].url;
            console.log(imageUrl);
            const echoImg = new Discord.MessageEmbed()
                .setColor('#8db255')
                .setImage(imageUrl)
                .setTimestamp()
            message.channel.send(textToEcho);
            await message.channel.send(echoImg);
        }
        return message.delete().catch(O_o=>{}); 

    } else if(command === "purge") {
        if(isDm) return message.channel.send("(i'm not allowed to delete things in dms :/)");
        const deleteCount = parseInt(args[0], 10);
        if(!deleteCount || deleteCount < 2 || deleteCount > 100)
            return message.channel.send("you're supposed to provide a number between 2 and 100 (inclusive) for the number of messages to delete :/");
        // const fetched = await message.channel.fetchMessages({limit: deleteCount});
        try {message.channel.bulkDelete(deleteCount+1);
        } catch(error) {
            message.reply("something went wrong :/");//error => message.reply("couldn't delete messages because of: ${error}"));
        }
        return;

    } else if(command === "poll"){
        if(args[0].substring(0,1) !== "\"")
            return message.channel.send("...you might wanna check the `!help` page again for the poll syntax :/");
        var poll = args.join(" ");
        console.log("Poll: " + poll);
        var pollQuestion = poll.substring(1,poll.indexOf("\"",1));
        console.log("Question: " + pollQuestion);

        var howManyOptions = 0;
        for(let i = 0; i < poll.length; i++){
            if(poll[i] === "\"")
                howManyOptions++;
        }
        howManyOptions = Number(howManyOptions/2-1);
        if(howManyOptions - Math.floor(howManyOptions) != 0)
            return message.channel.send("errr,,,, think you made a mistake :/");
        if(howManyOptions < 2 || howManyOptions > 10) // [ only one answer option ] or [ over 10 options ] given
            return message.channel.send("you're supposed to provide between 2 and 10 (inclusive) poll options :/");
        
        var pollOptions = []; 
        var nextQuoteIndex = poll.indexOf("\"",poll.indexOf("\"",1));
        nextQuoteIndex = poll.indexOf("\"",nextQuoteIndex+1);
        //console.log("nextQuoteIndex: " + nextQuoteIndex);
        for(let i = 0; i < howManyOptions; i++){
            if(nextQuoteIndex !== -1){
                pollOptions[i] = poll.substring(nextQuoteIndex+1,poll.indexOf("\"",nextQuoteIndex+1));
                nextQuoteIndex = poll.indexOf("\"",nextQuoteIndex+1);
                nextQuoteIndex = poll.indexOf("\"",nextQuoteIndex+1);
                //console.log("pollOptions[" + i + "]: " + pollOptions[i] + "\t\tnextQuoteIndex: " + nextQuoteIndex);
            }
        }
        console.log("Poll options (" + howManyOptions + "): " + pollOptions);
        message.delete().catch(O_o=>{}); 
        var options = "";
        for(let i = 0; i < pollOptions.length; i++)
            options += "\n( " + emojiCharacters[i+1] + " ) " + pollOptions[i]; 
        let embed = new Discord.MessageEmbed()
            .setColor("#8db255")
            .setDescription('▬▬▬▬▬▬▬▬▬** « poll » **▬▬▬▬▬▬▬▬▬▬\n\n**poll question »** ' + pollQuestion + '\n\n**poll options »**' + options)
            .setTimestamp();
        message.channel.send(embed).then(sentEmbed => {
            for(let i = 0; i < pollOptions.length; i++)
                sentEmbed.react(emojiCharacters[i+1]);
        });
        return;

    } else if(!isPunctuation && message.content.substring(0,prefix.length) === prefix)// if the command is unrecognized and it's not just !!!!!
        return message.channel.send("my documentation's at `!help` ^-^");

    // IF IT'S NOT IN THE FORMAT `!COMMAND ARGUMENTS`
    // if rickroll
    var theMessage = message.content.toLowerCase();
    for (let i = 0; i < rickWords.length; i++) {
        if (message.content.toLowerCase().includes(rickWords[i])) {
            console.log(message.content);
            if(message.member.voice.channel){
                // join the vc and play the audio
                message.member.voice.channel.join()
                .then(connection => {
                    const stream = ytdl('https://www.youtube.com/watch?v=dQw4w9WgXcQ', { filter: 'audioonly' });
                    const dispatcher = connection.play(stream);
                    dispatcher.on('end', () => message.member.voice.channel.leave());
                })
                .catch(error => console.log(":/ there was an error: ${error}"));
            } else {
                // send the video in the channel
                message.channel.send("are you okay? here, this might make you feel better >.<");
                const rickroll = new Discord.MessageEmbed()
                    .setColor('#e52d27')
                    .setAuthor('YouTube')//,'https://www.youtube.com/watch?v=dQw4w9WgXcQ')
                    .setTitle('Satisfied')
                    .setURL('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
                    .setDescription("Renée Elise Goldsberry - Topic")
                    .setImage('https://i.imgur.com/rOBJRja.png')
                message.channel.send(rickroll);
            }
            return;
        } 
    }
    // if it's not rickroll-worthy
    if(message.content.includes("\n")){ // if the message has newline char(s) and could therefore potentially contain quoted material
        var notQuotations = message.content.split("\n"); 
        for(let i = 0; i < notQuotations.length; i++){
            if(notQuotations[i].startsWith(">")){
                console.log("[quotation]");
                notQuotations.shift();
                i--;
            }
        }
    } else var notQuotations = message.content.toLowerCase().split(/\s+/g); 
    console.log("Non-quoted text (Array): " + notQuotations);
    theMessage = notQuotations.join(' ');
    console.log("Message (String): " + theMessage);

    if(theMessage.includes("uwu") && theMessage.includes("owo")){
        if(theMessage.indexOf("uwu") < theMessage.indexOf("owo")) 
            var uwuWord = "uwu";
        else 
            var uwuWord = "owo";
    } else{
        if(theMessage.includes("uwu")) 
            var uwuWord = "uwu";
        else if(theMessage.includes("owo")) 
            var uwuWord = "owo";
        else return;
    }
    console.log("uwuWord: " + uwuWord);

    //if(!theMessage.includes(uwuWord)) return; // REDUNDANT
    for(let i = 0; i < notQuotations.length; i++){
        if(notQuotations[i].includes(uwuWord)){
            var lastLetters = notQuotations[i].substring(notQuotations[i].indexOf(uwuWord)+3).split(""); // uwus!! --> s!!; lastLetters is an Array
            console.log("Last letters: " + lastLetters);
            for(let i = 0; i < lastLetters.length; i++){ // owo!s --> !s 
                //console.log(lastLetters);
                if(!punctuationArray.includes(lastLetters[i])){
                    //console.log(lastLetters[i]);
                    lastLetters.splice(i,1);
                    i--;
                } 
            }
            //lastLetters = lastLetters.join(""); // convert from Array to String
            console.log("Last letters, but only punct: " + lastLetters);
            if(lastLetters.includes(".")) 
                return message.channel.send(uwuWord + lastLetters.join("")); 
            else if(lastLetters.includes("?") || lastLetters.includes("!")){
                if(notQuotations[i].length > 1000) 
                    return message.channel.send("...okay you win ;-;");
                else 
                    return message.channel.send(uwuWord + lastLetters.join("") + lastLetters.join("")); 
            } else return message.channel.send(uwuWord);
        }
    }

    if(message.content === "hbjyl") message.channel.send("hbjyl");
});

bot.login(token);
// done: string-owo returns string-owo not owo
// done: owo!s returns owo!s!s not owo!!
// done: if there are both uwu and owo in a message, return whichever is first
// to do: start owo chains randomly on my own
// to do: respond to an uwuWord with ||owo|| if the message is a spoiler
// to do: fix !? issue