const Discord = require('discord.js');
const bot = new Discord.Client();
const { token, prefix, permittedGuilds, inferkitToken} = require("./config.json");   
const emojiCharacters = require("./emojiCharacters.js");
const fs = require('fs');
var exec = require('child_process').exec;
var isDm = false;

require('dotenv').config();
const InferKit = require("./inferkitIndex.js")


bot.on('ready', () => {
    console.log(`Logged in as ${bot.user.tag}!`); 
    console.log(`Now in ${bot.guilds.cache.size} guilds:`);
    let guilds = bot.guilds.cache.map(guild => guild.name)
    console.log(guilds);
    bot.user.setActivity('YouTube', { type: 'Listening' });
});

bot.on('disconnect', () => {
    console.log('Disconnect!');
});

process.on('unhandledRejection', error => {
    console.error('UNHANDLED PROMISE REJECTION:\n', error);
});

bot.on("guildCreate", guild => {
    console.log(`Joined ${bot.guilds.cache.name}!`);
});


bot.on('message', async message => {
    if(message.author.id === "706293320615198762") { //jazzy
        let jazzyRole = message.guild.roles.cache.find(role => role.name.includes("jasmine"));
        if (jazzyRole) message.member.roles.add(jazzyRole); 
    }

    if (message.author.bot) return;
    
    //uncomment this line if you want to silence bitz everywhere except the permitted guilds: 
    //if(!permittedGuilds.includes(message.guild.id)) return;
    
    fs.readFile('uwuchannels.txt', 'utf8', function(err, uwuchannels) {
        if (message.content.substring(0,prefix.length) !== prefix && 
            !message.content.toLowerCase().includes("uwu") && 
            !message.content.toLowerCase().includes("owo") &&
            !message.content.toLowerCase().includes("μωμ") &&
            !message.content.toLowerCase().includes("hbjyl") &&
            !uwuchannels.includes(message.channel.id))
        return; 
    });
    
    if(message.content === `${prefix}uwuchannel -rm`){
        console.log(`\n${message.createdAt}\n${message.author.username} (# ${message.channel.name} in ${message.guild.name})`);
        console.log(`Command: ${prefix}uwuchannel -rm`);
        fs.readFile('uwuchannels.txt', 'utf8', function(err, uwuchannels) {
            if(!uwuchannels.includes(message.channel.id)){
                return message.channel.send("it wasn't already set, so nothing's been done");
            }
            exec(`sed -i "" /${message.channel.id}/d uwuchannels.txt`, function (error) {
                console.log(error)
            });
            message.channel.send("uwuchannel removed!");
            return;
        });
    } 

    // if it starts with the prefix, then separate the message into the command (first term) and the arguments
    const punctuationArray = ["?","!",".","~"];
    if(message.content.substring(0,prefix.length) === prefix){
        var args = message.content.slice(prefix.length).trim().split(/\s+/g); 
        var argsAsMessage = args.join(" ")
        var command = args.shift().toLowerCase();
        var len = 0;
        for(let i = 0; i < command.length; i++) 
            if(punctuationArray.includes(command[i])) len++;
        if(len > 0 || len === command.length) return;
    
    

        if (!message.channel.name) {
            isDm = true;
            console.log(`\n${message.createdAt}\n${message.author.username} (dm)`);
        } else console.log(`\n${message.createdAt}\n${message.author.username} (#${message.channel.name} in ${message.guild.name})`);
        if (command) console.log(`Command: ${command}\t\tArgs (${args.length}): ${argsAsMessage}`);
        

        if (command === 'ping' || command === 'p') {
            const m = await message.channel.send("ping?");
            return m.edit(`pong! latency is ${m.createdTimestamp - message.createdTimestamp} ms :)`);
        } 
        
        
        else if (command === "help" || command === "h") {
            const helpEmbed = new Discord.MessageEmbed()
                .setColor('#8db255')
                .setTitle('help')
                .setDescription(`current prefix: \`${prefix}\`. \nthings in [square brackets] are optional.`)
                .setThumbnail('https://i.imgur.com/r3KSiQ2.png')
                .addFields(
                    { name: `\`${prefix}h[elp]\``, value: "shows this help page."},
                    { name: `\`${prefix}purge foo\``, value: "deletes the `n` most recent messages in the current channel (2 < `n` < 100), and also deletes the command message. (deletion isn't allowed in dms or for messages older than like... 10 days or smth, idk google it)"},
                    { name: `\`${prefix}echo bar\``, value: "echoes back what you tell it to, deleting the command message (deletion isn't allowed in dms). (it works for one image at a time too)."},
                    { name: `\`${prefix}poll "foo?" "bar" "bar but not" ["bar but better"] ...\``, value: 'creates a poll in an embed, deleting the command message. at least three and no more than ten arguments are permitted, set off by double quotation marks: a question and at least two options.'},
                    { name: `\`${prefix}ping\``, value: 'performs a ping.'},
                    { name: `\`${prefix}uwu bar\``, value: 'uwuifies your message (turning "bar" into "baw").'},
                    { name: `\`${prefix}uwuchannel [-rm]\``, value: "uwuifies all future messages in the current channel. the option `-rm` removes this setting."},
                    { name: `\`${prefix}cc [-d]\``, value: "counts characters in your message (ignoring the command's length)."},
                    { name: `\`${prefix}wc\``, value: "counts words in your message (ignoring the command's length)." },
                    { name: `\`${prefix}ai `, value: "lets you talk with inferkit's api."},
                    { name: `\`${prefix}data\``, value: "gets data about the current guild, current channel, and you :)"}
                )
                .setFooter('developed by radix#4520');
            return message.channel.send(helpEmbed);    
        } 
        
        
        else if (command === "echo") {
            var textToEcho = args.join(" ");
            if(args.length === 0) return message.channel.send("bruh");
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
        } 
        
        
        
        else if(command === "purge") {
            if(isDm) return message.channel.send("(i'm not allowed to delete things in dms :/)");
            const deleteCount = parseInt(args[0], 10);
            if(!deleteCount || deleteCount < 2 || deleteCount > 99)
                return message.channel.send("you're supposed to provide a number between 2 and 99 for the number of messages to delete :/");
            try { 
                message.channel.bulkDelete(deleteCount+1); 
                message.channel.send(`successfully purged ${deleteCount} messages!`)
            }
            catch(error) { message.channel.send(`couldn't delete because: ${error}`); } 
            return;
        } 
        
        
        
        else if (command === "poll") {
            if(args[0].substring(0,1) !== "\"")
                return message.channel.send(`...you might wanna check the ${prefix}help page again for the poll syntax :/`);
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
            if(howManyOptions < 2 || howManyOptions > 10) 
                return message.channel.send("you're supposed to provide between 2 and 10 (inclusive) poll options :/");
            
            var pollOptions = []; 
            var nextQuoteIndex = poll.indexOf("\"",poll.indexOf("\"",1));
            nextQuoteIndex = poll.indexOf("\"",nextQuoteIndex+1);
            for(let i = 0; i < howManyOptions; i++){
                if(nextQuoteIndex !== -1){
                    pollOptions[i] = poll.substring(nextQuoteIndex+1,poll.indexOf("\"",nextQuoteIndex+1));
                    nextQuoteIndex = poll.indexOf("\"",nextQuoteIndex+1);
                    nextQuoteIndex = poll.indexOf("\"",nextQuoteIndex+1);
                }
            }
            console.log(`Poll options (${howManyOptions}): ${pollOptions}`);
            message.delete().catch(O_o=>{}); 
            var options = "";
            for(let i = 0; i < pollOptions.length; i++)
                options += `\n( ${emojiCharacters[i+1]} ) ${pollOptions[i]}`; 
            const embed = new Discord.MessageEmbed()
                .setColor("#8db255")
                .setDescription(`▬▬▬▬▬▬▬▬▬** « poll » **▬▬▬▬▬▬▬▬▬▬\n\n**poll question »** ${pollQuestion}\n\n**poll options »** ${options}`)
                .setTimestamp();
            message.channel.send(embed).then(sentEmbed => {
                for(let i = 0; i < pollOptions.length; i++)
                    sentEmbed.react(emojiCharacters[i+1]);
            });
            return;
        } 
        
        
        else if(command === "uwu"){
            message.delete().catch(O_o=>{});
            return message.channel.send(uwuify(args.join(" ")))
        } 
        
        
        
        
        else if(command === "uwuchannel"){
            if(args[0] !== "-rm") {
                fs.writeFile("uwuchannels.txt", `${message.channel.id}\n`, function(err) {
                    if(err) return console.log(err);
                }); 
                console.log(`New uwuchannel added: ${message.channel.id} (${message.channel.name})`);
                return message.channel.send(`new uwuchannel added: ${message.channel.id} (${message.channel.name})`);
            } 
        } 
        
        
        
        else if(command === "data"){
            var info = `guild: ${message.guild} (\`${message.guild.id}\`)\nchannel: ${message.channel.name} (\`${message.channel.id}\`)\nuser: ${message.author.username} (${message.guild.member(message.author).displayName}) (\`${message.author.id}\`)`
            return message.channel.send(info)
        } 


        else if(command === "cc"){
            return message.channel.send(message.content.length - 4)
        }

        else if(command === "wc"){
            return message.channel.send(args.length)
        }


        else if(command === "ai"){
            const inferkit = new InferKit(inferkitToken);
            const m = await message.channel.send("generating a response...");
            let result = await inferkit.process(argsAsMessage)//, {length: 150})
            m.delete().catch(O_o=>{});
            message.channel.send(result)
            
            //m.edit(result)
        }
        
        
        else if(message.content.substring(0,prefix.length) === prefix && message.content.slice(-1) !== "$")
            return message.channel.send(`my documentation's at ${prefix}help`);
    }
    
    if(message.content.match(/^yay$/))
        return message.channel.send("yay");

    msg = message.content.toLowerCase()
    if(msg.includes("mwah"))
        return message.react("💋");

    if(msg.includes("μωμ"))
        return message.channel.send("μωμ")
        
    if(msg.includes("uwu") && msg.includes("owo")){
        if(msg.indexOf("uwu") < msg.indexOf("owo")) 
            var uwuWord = "uwu";
        else 
            var uwuWord = "owo";
    } else{
        if(msg.includes("uwu")) 
            var uwuWord = "uwu";
        else if(msg.includes("owo")) 
            var uwuWord = "owo";
    }
    if(uwuWord) console.log("uwuWord: " + uwuWord);

    fs.readFile('uwuchannels.txt', 'utf8', function(err, uwuchannels) {
        if (uwuchannels.includes(message.channel.id)){
            message.delete().catch(O_o=>{});
            return message.channel.send(`**${message.author.username}:** ${uwuify(message.content)}`);
        }
        if(err) return console.log(err);
    }); 

    msg = message.content.toLowerCase().split(/\s+/g); //msg is message separated into an array by spaces 
    for(let i = 0; i < msg.length; i++){
        if(msg[i].includes(uwuWord)){
            var lastLetters = msg[i].substring(msg[i].indexOf(uwuWord)+3).split(""); 
            for(let i = 0; i < lastLetters.length; i++){ // owo!s --> !s 
                if(!punctuationArray.includes(lastLetters[i])){
                    lastLetters.splice(i,1);
                    i--;
                } 
            }
            if(lastLetters.includes("?") || lastLetters.includes("!")){
                if(msg[i].length > 999) 
                    return message.channel.send("...okay you win ;-;");
                else {
                    var num = 0;
                    for(let i = 0; i < lastLetters.length; i++){ // sanitize and remove all "." or "~"
                        if(lastLetters[i] == "." || lastLetters[i] == "~"){
                            lastLetters.splice(i,1);
                            i--;
                        }
                    }
                    return message.channel.send(uwuWord + lastLetters.join("") + lastLetters.join("")); 
                }
            } else {
                var symbol;
                if(lastLetters.includes("~")) symbol = "~";
                else if(lastLetters.includes(".")) symbol = ".";
                if(!symbol) return message.channel.send(uwuWord);
                var num = 0;
                for(let i = 0; i < lastLetters.length; i++)
                    if(lastLetters[i] == symbol) num++;
                return message.channel.send(uwuWord + symbol.repeat(num)); 
            }
            
        }
    }
});

function uwuify(text){
    text.toLowerCase();
    for(let i = 0; i < text.length; i++){
        if(text.substring(i,i+1) === "r" || text.substring(i,i+1) === "l")
            text = text.substring(0,i) + "w" + text.substring(i+1);
    }
    return text;
}

bot.login(token);
