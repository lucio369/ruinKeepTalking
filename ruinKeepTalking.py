import discord, os, random
from discord.ext import commands
TOKEN=str(open("tokenFile.txt", "r").read())
bot=commands.Bot(command_prefix='.')

@bot.event
async def init():
    #general
    bot.ytzCommands=[['.button',False],
                 ['.compWires',False],
                 ['.help',False],
                 ['.knobs',False],
                 ['.memory',False],
                 ['.morse',False],
                 ['.passwords',False],
                 ['.simonsays',False],
                 ['.whosonfirst',False],
                 ['.wires',False],
                 ['.wireseq',False]]
    bot.currentModules=[]#???
    bot.freshUser=True
    bot.currentModule=''
    bot.params=[]
    bot.bigtquotetuple=('Wanna go on GTA?','oi','mum has taken my phone and ipad','do you mind if you can send me Gricias hw and the first section of isaac physics please?','thanks bro ❤',
    "this is the first time we've both been on at the same time and we said that we'd both play GTA?",'speaking of which...wanna play?',"kl",'fuck cs, rooski game',
    "I'm not shit, I just don't like how intense it is.",'I prefer casual games',"this is the first time we've both been on at the same time and we said that we'd both play GTA?")
    bot.bullying=eval(open("bullyingFile.txt", "r").read())
    bot.genMessage=['https://media.discordapp.net/attachments/663457975813275675/756241309496377414/tumblr_m7qou3Xlgi1qap9uuo1_500.gif',
                    '<:WeirdChamp:765501746951749642> You better not be like this on the road trip',
                    'Yoonkook = yoongi + jungkook',
                    '```nonce```']
    bot.bullyIndex=0
    bot.currentChannel=''
    bot.switchChannelOutput='''
===============================================================================
{channelName}
    '''
    await bot.initModVar()
@bot.event
async def initModVar():
    #wires
    bot.itCounter=0
    bot.QAsked=False

    #button variables
    bot.qIndex=0
    bot.holdButton=None
    bot.haltButton=False
    #button constants
    bot.questions=(('blueabort','',True),
           (' detonate','multiple batteries',False),
           ('white ','label CAR',True),
           ('  ','more than two batteries and label FRK',False),
           ('yellow ','',True),
           ('redhold','',False),
           ('  ','',True))

################################################################################################################################
@bot.event
async def Shit(ctx):
    message='''```
    Wires              Finds correct wire based off user input | .wires [number of wires]
    Button             Finds correct button based off user input | .button [colour of button] [word on button]
    Simon Says         Finds correct button based off user input | .simonsays [number of strikes]
    Whos on First      puts to word response from input word | .whosonfirst
    Memory             returns appropriate button to press based off user input | .memory
    Morse Code         works out valid word and frequency encoded in morse | .morse
    Complicated Wires  responds correct response for each wire based off user input | .compWires
    Wire Sequences     decides which wires to cut based off user input | .wireseq
    Passwords          figures out which word is the password from given characters | .passwords
    Knobs              outputs direction from given 12 bit number | .knobs
    Help               does this shit```'''
    await ctx.channel.send(message)
@bot.event
async def Wires(ctx,noWires):
    'Wires'
    index=noWires-3
    error=False
    questions=[[['No red?','Cut second wire'],['Last wire is white?','Cut last wire'],['More than one blue wire?','Cut last blue wire'],['None true?','Cut last wire']],
               [['More than 1 red and last digit of serial odd','Cut last red wire'],['Last wire yellow and no red wires?','Cut first wire'],['Exactly one blue wire?','Cut first wire'],['More than one yellow wire?','Cut last wire'],['None true?','Cut second wire']],
               [['Last wire black and last digit of serial odd?','Cut fourth wire'],['Exactly one red and more than one yellow?','Cut first wire'],['No black wires?','Cut second wire'],['None true?','Cut first wire']],
               [['No yellow and last digit of series is odd?','Cut third wire'],['Exactly one yellow and more than one white?','Cut fourth wire'],['No red?','Cut last wire'],['None true?','Cut fourth wire']]]
    if bot.QAsked==True:
        if ctx.content=='yes':
            await ctx.channel.send('```'+questions[index][bot.itCounter][1]+'```')
            await bot.initModVar()
            await bot.clearCurrentUser(ctx)
            return
        elif ctx.content=='no':
            bot.itCounter=bot.itCounter+1
            bot.QAsked=False
        else:
            await ctx.channel.send('```bad response. restart.```')
            await bot.initModVar()
            await bot.clearCurrentUser(ctx)
            return
    if bot.QAsked==False:
        if index>=len(questions) or index<0:
            await ctx.channel.send('```bad conditions. restart.```')
            await bot.initModVar()
            await bot.clearCurrentUser(ctx)
        elif bot.itCounter==len(questions[index]):
            await ctx.channel.send('```end of conditions```')
            await bot.initModVar()
            await bot.clearCurrentUser(ctx)
        else:
            await ctx.channel.send('```'+questions[index][bot.itCounter][0]+'```')
            bot.QAsked=True
    await bot.saveCurrentUser(ctx,[bot.itCounter,bot.QAsked])

@bot.event
async def Button(ctx,colour,word):
    'Button'
    if bot.haltButton==True:
        bot.haltButton=False
        if ctx.content=='yes':
            bot.holdButton=bot.questions[bot.qIndex][2]
        elif ctx.content=='no':
            bot.qIndex=bot.qIndex+1
        else:
            await ctx.channel.send('```bad conditions- restart```')
            await bot.initModVar()
            await bot.clearCurrentUser(ctx)
            return
    if bot.holdButton!=None:
        if bot.holdButton==True:
            await ctx.channel.send('```hold button```')
            await ctx.channel.send('''```
Do the following according to the colour of the light strip:

blue:    release when 4 in any position
---------------------------------------
white:   release when 1 in any position
---------------------------------------
yellow:  release when 5 in any position
---------------------------------------
None:    release when 1 in any position```''')
        elif bot.holdButton==False:
            await ctx.channel.send('```click button```')
        await bot.initModVar()
        await bot.clearCurrentUser(ctx)
        return
    pass1=True
    if bot.questions[bot.qIndex][0]!=colour+word:
        if ' ' in bot.questions[bot.qIndex][0]:
            if bot.questions[bot.qIndex][0]!=' '+word:
                if bot.questions[bot.qIndex][0]!=colour+' ':
                    if bot.questions[bot.qIndex][0]!='  ':
                        pass1=False
        else:
            pass1=False
    if pass1==True:
        if bot.questions[bot.qIndex][1]!='':
            await ctx.channel.send(bot.questions[bot.qIndex][1]+'?')
            bot.haltButton=True
        else:
            bot.holdButton=bot.questions[bot.qIndex][2]
            await bot.Button(ctx,colour,word)
            return
    else:
        bot.qIndex=bot.qIndex+1
        await bot.Button(ctx,colour,word)
        return
    await bot.saveCurrentUser(ctx,[bot.haltButton,bot.holdButton,bot.qIndex])
    return

def WhosOnFirst():
    'Whos on First'
    displayList=[['yes','left middle'],['first','top right'],['display','bottom right'],['okay','top right'],
                 ['says','bottom right'],['nothing','middle left'],['','bottom left'],['blank','middle right'],['no','bottom right'],
                 ['led','middle left'],['lead','bottom right'],['read','middle right'],['red','middle right'],['reed','bottom left'],
                 ['leed','bottom left'],['hold on','bottom right'],['you','middle right'],['you are','bottom right'],
                 ['your','middle right'],['youre','middle right'],['ur','top left'],['there','bottom right'],
                 ['theyre','bottom left'],['their','middle right'],['they are','middle left'],
                 ['see','bottom right'],['c','top right'],['cee','bottom right']]
    potencialList=[['YES', 'OKAY', 'WHAT', 'MIDDLE', 'LEFT', 'PRESS', 'RIGHT', 'BLANK', 'READY', 'NO', 'FIRST', 'UHHH', 'NOTHING', 'WAIT'],
     ['LEFT', 'OKAY', 'YES', 'MIDDLE', 'NO', 'RIGHT', 'NOTHING', 'UHHH', 'WAIT', 'READY', 'BLANK', 'WHAT', 'PRESS', 'FIRST'],
     ['BLANK', 'UHHH', 'WAIT', 'FIRST', 'WHAT', 'READY', 'RIGHT', 'YES', 'NOTHING', 'LEFT', 'PRESS', 'OKAY', 'NO', 'MIDDLE'],
     ['WAIT', 'RIGHT', 'OKAY', 'MIDDLE', 'BLANK', 'PRESS', 'READY', 'NOTHING', 'NO', 'WHAT', 'LEFT', 'UHHH', 'YES', 'FIRST'],
     ['UHHH', 'RIGHT', 'OKAY', 'MIDDLE', 'YES', 'BLANK', 'NO', 'PRESS', 'LEFT', 'WHAT', 'WAIT', 'FIRST', 'NOTHING', 'READY'],
     ['OKAY', 'RIGHT', 'UHHH', 'MIDDLE', 'FIRST', 'WHAT', 'PRESS', 'READY', 'NOTHING', 'YES', 'LEFT', 'BLANK', 'NO', 'WAIT'],
     ['UHHH', 'WHAT', 'LEFT', 'NOTHING', 'READY', 'BLANK', 'MIDDLE', 'NO', 'OKAY', 'FIRST', 'WAIT', 'YES', 'PRESS', 'RIGHT'],
     ['READY', 'NOTHING', 'LEFT', 'WHAT', 'OKAY', 'YES', 'RIGHT', 'NO', 'PRESS', 'BLANK', 'UHHH', 'MIDDLE', 'WAIT', 'FIRST'],
     ['RIGHT', 'LEFT', 'FIRST', 'NO', 'MIDDLE', 'YES', 'BLANK', 'WHAT', 'UHHH', 'WAIT', 'PRESS', 'READY', 'OKAY', 'NOTHING'],
     ['YES', 'NOTHING', 'READY', 'PRESS', 'NO', 'WAIT', 'WHAT', 'RIGHT', 'MIDDLE', 'LEFT', 'UHHH', 'BLANK', 'OKAY', 'FIRST'],
     ['BLANK', 'READY', 'OKAY', 'WHAT', 'NOTHING', 'PRESS', 'NO', 'WAIT', 'LEFT', 'MIDDLE', 'RIGHT', 'FIRST', 'UHHH', 'YES'],
     ['MIDDLE', 'NO', 'FIRST', 'YES', 'UHHH', 'NOTHING', 'WAIT', 'OKAY', 'LEFT', 'READY', 'BLANK', 'PRESS', 'WHAT', 'RIGHT'],
     ['UHHH', 'NO', 'BLANK', 'OKAY', 'YES', 'LEFT', 'FIRST', 'PRESS', 'WHAT', 'WAIT', 'NOTHING', 'READY', 'RIGHT', 'MIDDLE'],
     ['RIGHT', 'MIDDLE', 'YES', 'READY', 'PRESS', 'OKAY', 'NOTHING', 'UHHH', 'BLANK', 'LEFT', 'FIRST', 'WHAT', 'NO', 'WAIT'],
     ['SURE', 'YOUARE', 'YOUR', 'YOURE', 'NEXT', 'UHHUH', 'UR', 'HOLD', 'WHAT', 'YOU', 'UHUH', 'LIKE', 'DONE', 'U'],
     ['YOUR', 'NEXT', 'LIKE', 'UHHUH', 'WHAT', 'DONE', 'UHUH', 'HOLD', 'YOU', 'U', 'YOURE', 'SURE', 'UR', 'YOUARE'],
     ['UHUH', 'YOUARE', 'UHHUH', 'YOUR', 'NEXT', 'UR', 'SURE', 'U', 'YOURE', 'YOU', 'WHAT', 'HOLD', 'LIKE', 'DONE'],
     ['YOU', 'YOURE', 'UR', 'NEXT', 'UHUH', 'YOUARE', 'U', 'YOUR', 'WHAT', 'UHHUH', 'SURE', 'DONE', 'LIKE', 'HOLD'],
     ['DONE', 'U', 'UR', 'UHHUH', 'WHAT', 'SURE', 'YOUR', 'HOLD', 'YOURE', 'LIKE', 'NEXT', 'UHUH', 'YOUARE', 'YOU'],
     ['UHHUH', 'SURE', 'NEXT', 'WHAT', 'YOURE', 'UR', 'UHUH', 'DONE', 'U', 'YOU', 'LIKE', 'HOLD', 'YOUARE', 'YOUR'],
     ['UHHUH', 'YOUR', 'YOUARE', 'YOU', 'DONE', 'HOLD', 'UHUH', 'NEXT', 'SURE', 'LIKE', 'YOURE', 'UR', 'U', 'WHAT'],
     ['UR', 'U', 'YOUARE', 'YOURE', 'NEXT', 'UHUH', 'DONE', 'YOU', 'UHHUH', 'LIKE', 'YOUR', 'SURE', 'HOLD', 'WHAT'],
     ['YOU', 'HOLD', 'YOURE', 'YOUR', 'U', 'DONE', 'UHUH', 'LIKE', 'YOUARE', 'UHHUH', 'UR', 'NEXT', 'WHAT', 'SURE'],
     ['SURE', 'UHHUH', 'NEXT', 'WHAT', 'YOUR', 'UR', 'YOURE', 'HOLD', 'LIKE', 'YOU', 'U', 'YOUARE', 'UHUH', 'DONE'],
     ['WHAT', 'UHHUH', 'UHUH', 'YOUR', 'HOLD', 'SURE', 'NEXT', 'LIKE', 'DONE', 'YOUARE', 'UR', 'YOURE', 'U', 'YOU'],
     ['YOUARE', 'U', 'DONE', 'UHUH', 'YOU', 'UR', 'SURE', 'WHAT', 'YOURE', 'NEXT', 'HOLD', 'UHHUH', 'YOUR', 'LIKE'],
     ['YOUARE', 'DONE', 'LIKE', 'YOURE', 'YOU', 'HOLD', 'UHHUH', 'UR', 'SURE', 'U', 'WHAT', 'NEXT', 'YOUR', 'UHUH'],
     ['YOURE', 'NEXT', 'U', 'UR', 'HOLD', 'DONE', 'UHUH', 'WHAT', 'UHHUH', 'YOU', 'LIKE', 'SURE', 'YOUARE', 'YOUR']]
    leave=False
    index=0
    while leave==False:
        display=input('what is the word?')
        for i in range(0,len(displayList)-1):
            if displayList[i][0]==display:
                index=i
        try:
            whichList=input(displayList[index][1]+': ')
        except:
            print('item not in list')
            leave=True
            break
        if whichList=='ready':
            listNum=0
        elif whichList=='first':
            listNum=1
        elif whichList=='no':
            listNum=2            
        elif whichList=='blank':
            listNum=3        
        elif whichList=='nothing':
            listNum=4
        elif whichList=='yes':
            listNum=5            
        elif whichList=='what':
            listNum=6
        elif whichList=='uhhh':
            listNum=7
        elif whichList=='left':
            listNum=8            
        elif whichList=='right':
            listNum=9        
        elif whichList=='middle':
            listNum=10
        elif whichList=='okay':
            listNum=11            
        elif whichList=='wait':
            listNum=12
        elif whichList=='press':
            listNum=13
        elif whichList=='you':
            listNum=14           
        elif whichList=='you are':
            listNum=15        
        elif whichList=='your':
            listNum=16
        elif whichList=='youre':
            listNum=17            
        elif whichList=='ur':
            listNum=18
        elif whichList=='u':
            listNum=19
        elif whichList=='uh huh':
            listNum=20           
        elif whichList=='uh uh':
            listNum=21       
        elif whichList=='what':
            listNum=22
        elif whichList=='done':
            listNum=23           
        elif whichList=='next':
            listNum=24
        elif whichList=='hold':
            listNum=25
        elif whichList=='sure':
            listNum=26            
        elif whichList=='like':
            listNum=27
        print(potencialList[listNum])
        if input('done?'=='y'):
            leave=True

def Memory():
    'Memory'
    leave=False
    memoryArray=[]#pos,value
    stage=0
    num=['0','1','2','3','4','5','6','7','8','9']
    #num,command (s=slot,w=writing,p=position index,l=label index)
    commandList=[['2s','2s','3s','4s'],
                 ['4w','2p','1s','1p'],
                 ['2l','1l','3s','4w'],
                 ['1p','1s','2p','2p'],
                 ['1l','2l','4l','3l']]
    while leave==False and stage<5:
        currentCommand=[]
        request=int(input("Display: "))
        currentCommand=list(commandList[stage][request-1])
        requestValue=int(currentCommand[0])
        phrase=currentCommand[1]
        if phrase=='s':
            print('Position ',requestValue)
        elif phrase=='w':
            print('Label ',requestValue)
        elif phrase=='p':
            print('Position ',memoryArray[requestValue-1][0])
        elif phrase=='l':
            print('Label ',memoryArray[requestValue-1][1])

        posvalue=input('position+value (num1num2): ')
        list(posvalue)

        memoryArray.append([posvalue[0],posvalue[1]])
        stage=stage+1

        if input('leave? ')=='y':
            leave=True
            
def MorseCode():
    'Morse Code'
    leave=False
    letterList=[]
    morseArray=[['a','.-'],['b','-...'],['c','-.-.'],['d','-..'],['e','.'],['f','..-.'],
                ['g','--.'],['h','....'],['i','..'],['j','.---'],['k','-.-'],['l','.-..'],
                ['m','--'],['n','-.'],['o','---'],['p','.--.'],['q','--.-'],['r','.-.'],
                ['s','...'],['t','-'],['u','..-'],['v','...-'],['w','.--'],['x','-..-'],
                ['y','-.--'],['z','--..'],['0','-----'],['1','.----'],['2','..---'],['3','...--'],['4','....-'],['5','.....'],
                ['6','-....'],['7','--...'],['8','---..'],['9','----.']]
    wordList=[['shell','3.505'],['halls','3.515'],['slick','3.522'],['trick','3.532'],['boxes','3.535'],['leaks','3.542'],
              ['strobe','3.545'],['bistro','3.552'],['flick','3.555'],['bombs','3.565'],['break','3.572'],
              ['brick','3.575'],['steak','3.582'],['sting','3.592'],['vector','3.595'],['beats','3.600']]
    while leave==False:
        letter=input('morseCode (.-): ')
        for i in range(0,len(morseArray)):
            if morseArray[i][1]==letter:
                letterList.append(morseArray[i][0])

        possWordIndex=[]
        for i in range(0,len(wordList)):
            fail=False
            for j in range(0,len(letterList)):
                if letterList[j] not in wordList[i][0]:
                    fail=True
                if j==len(letterList)-1 and fail==False:
                    possWordIndex.append(i)

        if len(possWordIndex)==0:
            print('Error')
            leave=True
        elif len(possWordIndex)>1:
            print('More letters needed')
        else:
            leave=True
            print(wordList[possWordIndex[0]][0],'| Frequency:',wordList[possWordIndex[0]][1])

def ComplicatedWires():        
    'Complicated Wires'
    wireSituation=[['','c'],
                   ['r','s'],['rb','s'],['rs','c'],['rl','b'],['rbs','s'],['rbl','p'],['rsl','b'],['rbsl','d'],
                   ['b','s'],['bs','d'],['bl','p'],['bsl','p'],
                   ['s','c'],['sl','b'],
                   ['l','d']]
    instructions=[['c','Cut Wire'],['d','Do not cut wire'],['s','Cut wire if LAST DIGIT EVEN'],
                 ['p','Cut wire if bomb has PARRALLEL PORT'],['b','Cut wire if bomb has TWO OR MORE batteries']]
    leave=False
    while leave==False:
        situation=''
        if input('red: ')=='y':
            situation=situation+'r'
        if input('blue: ')=='y':
            situation=situation+'b'
        if input('has star: ')=='y':
            situation=situation+'s'
        if input('led on: ')=='y':
            situation=situation+'l'

        for i in range(0,len(wireSituation)):
            if situation==wireSituation[i][0]:
                instruction=wireSituation[i][1]
        for i in range(0,len(instructions)):
            if instructions[i][0]==instruction:
                print()
                print(instructions[i][1])
                print()
        if input('leave? ')=='y':
            leave=True

def WireSequences():
    'Wire Sequences'
    Occurrences=[['C','B','A','AC','B','AC','ABC','AB','B'],
                 ['B','AC','B','A','B','BC','C','AC','A'],
                 ['ABC','AC','B','AC','B','BC','AB','C','C']]
    red=blue=black=0
    leave=False
    while leave==False:
        inputAnswer=False
        if red>len(Occurrences[0])-1 or blue>len(Occurrences[1])-1 or black>len(Occurrences[2])-1:
            leave=True
        elif input('red: ')=='y':
            Occurrence=Occurrences[0][red]
            red=red+1
            inputAnswer=True
        elif input('blue: ')=='y':
            Occurrence=Occurrences[1][blue]
            blue=blue+1
            inputAnswer=True
        elif input('black')=='y':
            Occurrence=Occurrences[2][black]
            black=black+1
            inputAnswer=True
        if inputAnswer==True:
            print('Cut if connected to: ',Occurrence)
        if leave==False:
            if input('leave? ')=='y':
                leave=True

def Passwords():
    'Passwords'
    passwords=['right','plant','spell','place','point',#0-4
                'small','study','other','sound','still',#5-9
                'these','never','their','think','large',#10-14
                'there','thing','three','house','learn',#15-19
                'world','great','where','write','first',#20-24
                'water','which','would','every','found',#25-29
                'could','below','after','about','again']#30-34
    
    tempPasswords=['right','plant','spell','place','point',#0-4
                'small','study','other','sound','still',#5-9
                'these','never','their','think','large',#10-14
                'there','thing','three','house','learn',#15-19
                'world','great','where','write','first',#20-24
                'water','which','would','every','found',#25-29
                'could','below','after','about','again']#30-34
    leave=False
    emptInput=input()
    index=0
    passIndexes=[]
    count0=count1=0
    while leave==False:#loop
        while count0<(len(emptInput)-1):#every input item
            count0=count0+1
            count1=0
            while count1<(len(passwords)-1):#every password item
                print(emptInput[count0])
                print(passwords[count1])
                print('-----------------------------------------------------------------')
                count1=count1+1
                
def Knobs():
    'Knobs'
    ledConfigs=[['010111011011','100111001101'],
                ['011111010011','100110001001'],
                ['010000011101','000000011100'],
                ['110111101110','110111100100']]
    direction=['up','down','left','right']
    config=input('Enter the configuration (010111011011): ')
    for i in range(0,len(ledConfigs)):
        for j in range(0,len(ledConfigs[i])):
            if config==ledConfigs[i][j]:
                print('Set to:',direction[i])

@bot.event
async def clearCurrentUser(ctx):
    bot.ytzCommands=[['.button',False],
                 ['.compWires',False],
                 ['.help',False],
                 ['.knobs',False],
                 ['.memory',False],
                 ['.morse',False],
                 ['.passwords',False],
                 ['.simonsays',False],
                 ['.whosonfirst',False],
                 ['.wires',False],
                 ['.wireseq',False]]
    print(bot.currentModules)
    for user in range(0,len(bot.currentModules)):
        if ctx.author.id==bot.currentModules[user][0]:
            bot.currentModules.pop(user)
            return

@bot.event
async def saveCurrentUser(ctx,parametersToSave):
    for user in range(0,len(bot.currentModules)):
        if ctx.author.id==bot.currentModules[user][0]:
            bot.currentModules[user]=[ctx.author.id,bot.command]
            for param in parametersToSave:
                bot.currentModules[user].append(param)
            return
                
@bot.event
async def on_ready():
    await bot.init()
    print("Now copying Thomas")
    await bot.change_presence(activity=discord.Activity(name="Australian and Canadian women", type=3))

@bot.event
async def runModules(ctx):
    for comm in bot.ytzCommands:
        if comm[1]==True:
            if comm[0]=='.button':
                await bot.Button(ctx,bot.params[0],bot.params[1])
            if comm[0]=='.compWires':
                await message.channel.send('In development')
            if comm[0]=='.help':
                await bot.Shit(ctx)
                await bot.clearCurrentUser(ctx)
            if comm[0]=='.knobs':
                await message.channel.send('In development')
            if comm[0]=='.memory':
                await message.channel.send('In development')
            if comm[0]=='.morse':
                await message.channel.send('In development')
            if comm[0]=='.passwords':
                await message.channel.send('In development')
            if comm[0]=='.simonsays':
                await message.channel.send('In development')
            if comm[0]=='.whosonfirst':
                await message.channel.send('In development')
            if comm[0]=='.wires':
                await bot.Wires(ctx,int(bot.params[0]))
            if comm[0]=='.wireseq':
                await message.channel.send('In development')
@bot.event
async def on_message(message):
    message.content=message.content.lower()
    if message.channel!=bot.currentChannel:
        bot.currentChannel=message.channel
        print(bot.switchChannelOutput.format(channelName=str(bot.currentChannel).upper()))
    print(message.author.name+': '+message.content)
    attachURLS=' ~ '
    for item in message.attachments:
        attachURLS=attachURLS+item.url+' '
    print(message.author.name+': '+message.content++attachURLS)
    if message.author==bot.user:
        return
##The above is for the shell: outputting the message content (essentially sniffing the server tbh)
    bot.freshUser=True
    for user in bot.currentModules:
        if user[0]==message.author.id:
            bot.freshUser=False
            bot.currentModule=user[1]
    splitMessage=message.content.split(' ')
    if bot.freshUser==True:
        bot.command=splitMessage[0]
        for comm in bot.ytzCommands:
            if comm[0]==bot.command:
                comm[1]=True
                bot.params=splitMessage
                bot.params.pop(0)
                bot.currentModules.append([message.author.id,bot.command])
                await bot.runModules(message)
            else:
                comm[1]=False
    else:
        for comm in bot.ytzCommands:
            if comm[0]==bot.currentModule:
                comm[1]=True
                for eachUser in range(0,len(bot.currentModules)):
                    if bot.currentModules[eachUser][1]==bot.currentModule:
                        if bot.currentModule=='.button':
                            bot.haltButton,bot.holdButton,bot.qIndex=bot.currentModules[eachUser][2],bot.currentModules[eachUser][3],bot.currentModules[eachUser][4]
                        elif bot.currentModule=='.wires':
                            bot.itCounter,bot.QAsked=bot.currentModules[eachUser][2],bot.currentModules[eachUser][3]
                await bot.runModules(message)
            else:
                comm[1]=False
    if message.content.startswith('thanks'):
        await message.channel.send('no worries')
    elif message.content.startswith('fuck off') or message.content.startswith('fuck you'):
        await message.channel.send('no u')
    elif message.content=='ping':
        await message.channel.send('pong')
    elif message.content.startswith(str(open("sala.txt", "r").read())):
        await message.channel.send(str(open("sala.txt", "r").read())+' can you send the maths homework?')
    elif str(open("sala.txt", "r").read()) in message.content:
        randomThomas=random.randint(0,len(bot.bigtquotetuple)-1)
        await message.channel.send(bot.bigtquotetuple[randomThomas])
    else:
        if random.randint(0,40)==1:
            if message.author.id not in bot.bullying:
                randMessage=bot.genMessage[random.randint(0,len(bot.genMessage)-1)]
            else:
                randMessage=bot.bullying[message.author.id][random.randint(0,len(bot.bullying[message.author.id])-1)]
            await message.channel.send(randMessage)
    
bot.run(TOKEN)
