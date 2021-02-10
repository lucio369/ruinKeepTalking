# ruinKeepTalking - Your bomb defusing assistant
This is a discord api, made using python, made not only for the moderation of a discord server but also to assist a player to defuse a bomb in the game 'Keep Talking and Nobody Explodes'.
Typically the game functions so that one player must defuse the bomb under the advice of another user (the bomb manual reader). 
This bot changes the premise to substitute as the manual reader where the defuser can interact with discord to get the required information. 
Of course, the game is made to challenge the communication of two people but I figured it would be interesting to see how communicating with this AI could carry the same purpose.

As however this api is designed for a personal discord server used by me and my friends, some files are absent. 
Other than the token, these files hold private information concerning discord id's used by my friends and I. As you can tell by the code, it does not necessarily carry out the intended functions.
Instead I programmed the bot to essentially bully any one of us at random for fun.

You could remove these modules in the code or fill them to suit your own server.

## These are the missing files and how they are structured:

*tokenFile.txt* - <discordAPIToken>

*bullyingFile.txt* - {<discordID>:<message1>,<message2>...,<discordID>:<message1>,<message2>...etc}

*sala.txt* - <discordID> //discord ID of the friend you particularly want to tease


Have fun (or don't)