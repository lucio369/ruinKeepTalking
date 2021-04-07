import discord, os, random, traceback
from discord.ext import commands
TOKEN=str(open("tokenFile.txt", "r").read())
bot=commands.Bot(command_prefix='.')
@bot.event
async def init():
    #general
    bot.confirmList=['y','yes','yeah','sure','yep','1','true']
    bot.denyList=['n','no','nope','nah','nahh','0','false']
    bot.num=['0','1','2','3','4','5','6','7','8','9']
    bot.currentCommands=[]
    bot.commandList=['.button',
                    '.compwires',
                    '.help',
                    '.knobs',
                    '.memory',
                    '.morse',
                    '.passwords',
                    '.simonsays',
                    '.whosonfirst',
                    '.wires',
                    '.wireseq',
                    '.mazes',
                    '.keypads',
                    '.vent',
                    '.capacitor']
    bot.helpContent='''```
    Keep Talking and Nobody Explodes Assistant

    Compatible with: Version 1 | Verification Code: 241

    Wires                .wires [number of wires]
    Button               .button [colour of button] [word on button]
    Simon Says           .simonsays [True/False: Vowel in serial num]
    Whos on First        .whosonfirst
    Memory               .memory
    Morse Code           .morse
    Complicated Wires    .compWires
    Wire Sequences       .wireseq
    Passwords            .passwords [first column of characters]
    Knobs                .knobs
    keypads              .keypads
    Mazes                .mazes
    Venting Gas          .vent
    Capacitor Discharge  .capacitor
    Help                 .help [module]

    To enquire more on the bombs attributes, query .help {attribute}:

    indicator
    battery
    port```'''
    bot.helpContentDict={'button':('.button [colour of button] [word on button]\nLaunches module taking the colour and word shown on the button to assist defusal','https://cdn.discordapp.com/attachments/806548674309128242/825419896325668884/unknown.png'),
                    'compwires':('.compWires\nLaunches module to assist defusal','https://cdn.discordapp.com/attachments/806548674309128242/825420247224942622/unknown.png'),
                    'knobs':('.knobs\nLaunches module to assist defusal','https://cdn.discordapp.com/attachments/806548674309128242/825420618756784138/unknown.png'),
                    'memory':('.memory\nLaunches module to assist defusal','https://cdn.discordapp.com/attachments/806548674309128242/825420127453446194/unknown.png'),
                    'morse':('.morse\nLaunches module to assist defusal','https://cdn.discordapp.com/attachments/806548674309128242/825420185082134578/unknown.png'),
                    'passwords':('.passwords [first column of characters]\nLaunches module taking the first column of characters to assist defusal','https://cdn.discordapp.com/attachments/806548674309128242/825420412623650846/unknown.png'),
                    'simonsays':('simonsays [True/False]\nLaunches module taking a true or false response regarding the fact There is a vowel in the serial num to assist defusal','https://cdn.discordapp.com/attachments/806548674309128242/825420007096713216/unknown.png'),
                    'whosonfirst':('.whosonfirst\nLaunches module to assist defusal','https://cdn.discordapp.com/attachments/806548674309128242/825420065822081024/unknown.png'),
                    'wires':('.wires [number of wires]\nLaunches module taking the number of visible wires for the module to assist defusal','https://cdn.discordapp.com/attachments/806548674309128242/825419803807186984/unknown.png'),
                    'wireseq':('.wireseq\nLaunches module to assist defusal','https://cdn.discordapp.com/attachments/806548674309128242/825420295040532540/unknown.png'),
                    'mazes':('.mazes\nLaunches module to assist defusal','https://cdn.discordapp.com/attachments/806548674309128242/826024165705383936/unknown.png'),
                    'vent':('The following is the documentation for this module','https://cdn.discordapp.com/attachments/806548674309128242/826024495025225738/unknown.png'),
                    'capacitor':('The following is the documentation for this module','https://cdn.discordapp.com/attachments/806548674309128242/826024708704174180/unknown.png'),
                    'keypads':('.keypads\nLaunches module to assist defusal','https://cdn.discordapp.com/attachments/806548674309128242/826025024557154314/unknown.png'),
                    'indicator':('The following are the potencial indicators','https://cdn.discordapp.com/attachments/806548674309128242/826037750868344832/unknown.png'),
                    'battery':('The following are the potencial battery types','https://cdn.discordapp.com/attachments/806548674309128242/826038100907786290/unknown.png'),
                    'port':('The following are the potencial ports','https://cdn.discordapp.com/attachments/806548674309128242/826038471462223882/unknown.png')
                    }
    await bot.initModConst()
    await bot.initModVar()
@bot.event
async def initModConst():
    #wires constants
    bot.wiresQuestions=[[['No red?','Cut second wire'],['Last wire is white?','Cut last wire'],['More than one blue wire?','Cut last blue wire'],['None true?','Cut last wire']],
               [['More than 1 red and last digit of serial odd','Cut last red wire'],['Last wire yellow and no red wires?','Cut first wire'],['Exactly one blue wire?','Cut first wire'],['More than one yellow wire?','Cut last wire'],['None true?','Cut second wire']],
               [['Last wire black and last digit of serial odd?','Cut fourth wire'],['Exactly one red and more than one yellow?','Cut first wire'],['No black wires?','Cut second wire'],['None true?','Cut first wire']],
               [['No yellow and last digit of series is odd?','Cut third wire'],['Exactly one yellow and more than one white?','Cut fourth wire'],['No red?','Cut last wire'],['None true?','Cut fourth wire']]]
    #button constants
    bot.questions=(('blueabort','',True),
           (' detonate','multiple batteries',False),
           ('white ','label CAR',True),
           ('  ','more than two batteries and label FRK',False),
           ('yellow ','',True),
           ('redhold','',False),
           ('  ','',True))
    #complicated wires constants
    bot.wireSituation=[['','c'],
                       ['r','s'],['rb','s'],['rs','c'],['rl','b'],['rbs','s'],['rbl','p'],['rsl','b'],['rbsl','d'],
                       ['b','s'],['bs','d'],['bl','p'],['bsl','p'],
                       ['s','c'],['sl','b'],
                       ['l','d']]
    bot.instructions={'c':'Cut Wire',
                      'd':'Do not cut wire',
                      's':'Cut wire if LAST DIGIT EVEN',
                      'p':'Cut wire if bomb has PARRALLEL PORT',
                      'b':'Cut wire if bomb has TWO OR MORE batteries'}
    #knobs constants
    bot.knobLEDConfigs=[['010111011011','100111001101'],
                    ['011111010011','100110001001'],
                    ['010000011101','000000011100'],
                    ['110111101110','110111100100']]
    bot.knobDirection=['up','down','left','right']
    #memory constants
    bot.memoryInstructions=[[[2,'p'],[2,'p'],[3,'p'],[4,'p']],
                            [[4,'w'],[0,'s'],[1,'p'],[0,'s']],
                            [[1,'l'],[0,'l'],[3,'p'],[4,'w']],
                            [[0,'s'],[1,'p'],[1,'s'],[1,'s']],
                            [[0,'l'],[1,'l'],[2,'l'],[3,'l']]]
    #morse constants
    bot.morseArray=[['a','.-'],['b','-...'],['c','-.-.'],['d','-..'],['e','.'],['f','..-.'],
                    ['g','--.'],['h','....'],['i','..'],['j','.---'],['k','-.-'],['l','.-..'],
                    ['m','--'],['n','-.'],['o','---'],['p','.--.'],['q','--.-'],['r','.-.'],
                    ['s','...'],['t','-'],['u','..-'],['v','...-'],['w','.--'],['x','-..-'],
                    ['y','-.--'],['z','--..'],['0','-----'],['1','.----'],['2','..---'],['3','...--'],['4','....-'],['5','.....'],
                    ['6','-....'],['7','--...'],['8','---..'],['9','----.']]
    bot.morseWordList=[['shell','3.505'],['halls','3.515'],['slick','3.522'],['trick','3.532'],['boxes','3.535'],['leaks','3.542'],
                  ['strobe','3.545'],['bistro','3.552'],['flick','3.555'],['bombs','3.565'],['break','3.572'],
                  ['brick','3.575'],['steak','3.582'],['sting','3.592'],['vector','3.595'],['beats','3.600']]
    #passwords constants
    bot.passwords=['right', 'plant', 'spell', 'place', 'point',
                   'small', 'study', 'other', 'sound', 'still',
                   'these', 'never', 'their', 'think', 'large',
                   'there', 'thing', 'three', 'house', 'learn',
                   'world', 'great', 'where', 'write', 'first',
                   'water', 'which', 'would', 'every', 'found',
                   'could', 'below', 'after', 'about', 'again']
    #simon says constants
    bot.simonSequence=[[['blue','red','yellow','green'],
    ['yellow','green','blue','red'],
    ['green','red','yellow','blue']],
    [['blue','yellow','green','red'],
    ['red','blue','yellow','green'],
    ['yellow','green','blue','red']]]
    #whos on first constants
    bot.wOFDisplayList=[['yes','left middle'],['first','top right'],['display','bottom right'],['okay','top right'],
                 ['says','bottom right'],['nothing','middle left'],['','bottom left'],['blank','middle right'],['no','bottom right'],
                 ['led','middle left'],['lead','bottom right'],['read','middle right'],['red','middle right'],['reed','bottom left'],
                 ['leed','bottom left'],['hold on','bottom right'],['you','middle right'],['you are','bottom right'],
                 ['your','middle right'],["you're",'middle right'],["youre",'middle right'],['ur','top left'],['there','bottom right'],
                 ["they're",'bottom left'],["theyre",'bottom left'],['their','middle right'],['they are','middle left'],
                 ['see','bottom right'],['c','top right'],['cee','bottom right'],[' ','bottom left']]
    bot.wOFPotencialList=[['READY','YES', 'OKAY', 'WHAT', 'MIDDLE', 'LEFT', 'PRESS', 'RIGHT', 'BLANK', 'READY', 'NO', 'FIRST', 'UHHH', 'NOTHING', 'WAIT'],
     ['FIRST','LEFT', 'OKAY', 'YES', 'MIDDLE', 'NO', 'RIGHT', 'NOTHING', 'UHHH', 'WAIT', 'READY', 'BLANK', 'WHAT', 'PRESS', 'FIRST'],
     ['NO','BLANK', 'UHHH', 'WAIT', 'FIRST', 'WHAT', 'READY', 'RIGHT', 'YES', 'NOTHING', 'LEFT', 'PRESS', 'OKAY', 'NO', 'MIDDLE'],
     ['BLANK','WAIT', 'RIGHT', 'OKAY', 'MIDDLE', 'BLANK', 'PRESS', 'READY', 'NOTHING', 'NO', 'WHAT', 'LEFT', 'UHHH', 'YES', 'FIRST'],
     ['NOTHING','UHHH', 'RIGHT', 'OKAY', 'MIDDLE', 'YES', 'BLANK', 'NO', 'PRESS', 'LEFT', 'WHAT', 'WAIT', 'FIRST', 'NOTHING', 'READY'],
     ['YES','OKAY', 'RIGHT', 'UHHH', 'MIDDLE', 'FIRST', 'WHAT', 'PRESS', 'READY', 'NOTHING', 'YES', 'LEFT', 'BLANK', 'NO', 'WAIT'],
     ['WHAT','UHHH', 'WHAT', 'LEFT', 'NOTHING', 'READY', 'BLANK', 'MIDDLE', 'NO', 'OKAY', 'FIRST', 'WAIT', 'YES', 'PRESS', 'RIGHT'],
     ['UHHH','READY', 'NOTHING', 'LEFT', 'WHAT', 'OKAY', 'YES', 'RIGHT', 'NO', 'PRESS', 'BLANK', 'UHHH', 'MIDDLE', 'WAIT', 'FIRST'],
     ['LEFT','RIGHT', 'LEFT', 'FIRST', 'NO', 'MIDDLE', 'YES', 'BLANK', 'WHAT', 'UHHH', 'WAIT', 'PRESS', 'READY', 'OKAY', 'NOTHING'],
     ['RIGHT','YES', 'NOTHING', 'READY', 'PRESS', 'NO', 'WAIT', 'WHAT', 'RIGHT', 'MIDDLE', 'LEFT', 'UHHH', 'BLANK', 'OKAY', 'FIRST'],
     ['MIDDLE','BLANK', 'READY', 'OKAY', 'WHAT', 'NOTHING', 'PRESS', 'NO', 'WAIT', 'LEFT', 'MIDDLE', 'RIGHT', 'FIRST', 'UHHH', 'YES'],
     ['OKAY','MIDDLE', 'NO', 'FIRST', 'YES', 'UHHH', 'NOTHING', 'WAIT', 'OKAY', 'LEFT', 'READY', 'BLANK', 'PRESS', 'WHAT', 'RIGHT'],
     ['WAIT','UHHH', 'NO', 'BLANK', 'OKAY', 'YES', 'LEFT', 'FIRST', 'PRESS', 'WHAT', 'WAIT', 'NOTHING', 'READY', 'RIGHT', 'MIDDLE'],
     ['PRESS','RIGHT', 'MIDDLE', 'YES', 'READY', 'PRESS', 'OKAY', 'NOTHING', 'UHHH', 'BLANK', 'LEFT', 'FIRST', 'WHAT', 'NO', 'WAIT'],
     ['YOU','SURE', 'YOUARE', 'YOUR', 'YOURE', 'NEXT', 'UHHUH', 'UR', 'HOLD', 'WHAT?', 'YOU', 'UHUH', 'LIKE', 'DONE', 'U'],
     ['YOU ARE','YOUR', 'NEXT', 'LIKE', 'UHHUH', 'WHAT?', 'DONE', 'UHUH', 'HOLD', 'YOU', 'U', 'YOURE', 'SURE', 'UR', 'YOUARE'],
     ['YOUR','UHUH', 'YOUARE', 'UHHUH', 'YOUR', 'NEXT', 'UR', 'SURE', 'U', 'YOURE', 'YOU', 'WHAT?', 'HOLD', 'LIKE', 'DONE'],
     ["YOU'RE",'YOU', 'YOURE', 'UR', 'NEXT', 'UHUH', 'YOUARE', 'U', 'YOUR', 'WHAT?', 'UHHUH', 'SURE', 'DONE', 'LIKE', 'HOLD'],
     ['UR','DONE', 'U', 'UR', 'UHHUH', 'WHAT?', 'SURE', 'YOUR', 'HOLD', 'YOURE', 'LIKE', 'NEXT', 'UHUH', 'YOUARE', 'YOU'],
     ['U','UHHUH', 'SURE', 'NEXT', 'WHAT?', 'YOURE', 'UR', 'UHUH', 'DONE', 'U', 'YOU', 'LIKE', 'HOLD', 'YOUARE', 'YOUR'],
     ['UH HUH','UHHUH', 'YOUR', 'YOUARE', 'YOU', 'DONE', 'HOLD', 'UHUH', 'NEXT', 'SURE', 'LIKE', 'YOURE', 'UR', 'U', 'WHAT?'],
     ['UH UH','UR', 'U', 'YOUARE', 'YOURE', 'NEXT', 'UHUH', 'DONE', 'YOU', 'UHHUH', 'LIKE', 'YOUR', 'SURE', 'HOLD', 'WHAT?'],
     ['WHAT?','YOU', 'HOLD', 'YOURE', 'YOUR', 'U', 'DONE', 'UHUH', 'LIKE', 'YOUARE', 'UHHUH', 'UR', 'NEXT', 'WHAT?', 'SURE'],
     ['DONE','SURE', 'UHHUH', 'NEXT', 'WHAT?', 'YOUR', 'UR', 'YOURE', 'HOLD', 'LIKE', 'YOU', 'U', 'YOUARE', 'UHUH', 'DONE'],
     ['NEXT','WHAT?', 'UHHUH', 'UHUH', 'YOUR', 'HOLD', 'SURE', 'NEXT', 'LIKE', 'DONE', 'YOUARE', 'UR', 'YOURE', 'U', 'YOU'],
     ['HOLD','YOUARE', 'U', 'DONE', 'UHUH', 'YOU', 'UR', 'SURE', 'WHAT?', 'YOURE', 'NEXT', 'HOLD', 'UHHUH', 'YOUR', 'LIKE'],
     ['SURE','YOUARE', 'DONE', 'LIKE', 'YOURE', 'YOU', 'HOLD', 'UHHUH', 'UR', 'SURE', 'U', 'WHAT?', 'NEXT', 'YOUR', 'UHUH'],
     ['LIKE','YOURE', 'NEXT', 'U', 'UR', 'HOLD', 'DONE', 'UHUH', 'WHAT?', 'UHHUH', 'YOU', 'LIKE', 'SURE', 'YOUARE', 'YOUR']]
    #wire sequences constants
    bot.wSeqOccurrences=[['C','B','A','A or C','B','A or C','Cut wire','A or B','B'],
                 ['B','A or C','B','A','B','B or C','C','A or C','A'],
                 ['Cut wire','A or C','B','A or C','B','B or C','A or B','C','C']]
@bot.event
async def initModVar():
    #wires variables
    bot.wiresCounter=0
    bot.wiresQAsked=False
    #button variables
    bot.qIndex=0
    bot.holdButton=None
    bot.haltButton=False
    #complicated wires variables
    bot.situation=''
    bot.cWQAsked=False
    #knob variables
    bot.knobBool=False
    #memory variables
    bot.memoryList=[]
    bot.memoryResponse=['','']
    bot.memoryPOL=''
    bot.memoryQAsked=False
    bot.memoryFirstPass=False
    #password variables
    await bot.PassBuildTree(bot.passwords)
    bot.passwordsError=False
    bot.passwordsFirstPass=False
    bot.passwordCounter=0
    #simon says variables
    bot.simonOut=[]
    bot.simonStrikes=0
    bot.simonFirstPass=False
    bot.simonVowel=0
    #whos on first variables
    bot.wOFCounter=0
    bot.wOFFirstPass=False
    #wire sequences variables
    bot.wSeqRed=bot.wSeqBlue=bot.wSeqBlack=0
    bot.wSeqFirstPass=False
    #morse variables
    bot.morseLetterList=[]
    bot.morseReturnPass=False
    bot.morseFail=False
@bot.event
async def PassBuildTree(aList):
    class passNode:
        def __init__(self,data):
            self.left=None
            self.right=None
            self.data=data

        def insert(self,data):
            if self.data:
                if data<self.data:
                    if self.left==None:
                        self.left=passNode(data)
                    else:
                        self.left.insert(data)
                elif data>self.data:
                    if self.right==None:
                        self.right=passNode(data)
                    else:
                        self.right.insert(data)
            else:
                self.data=data

        def search(self,target,pos):
            if self.data:
                if self.data[pos]==target:
                    return self.data
                elif self.data[pos]>target:
                    if self.left:
                        if self.left.search:
                            return self.left.search(target,pos)
                else:
                    if self.right:
                        if self.right.search:
                            return self.right.search(target,pos)
            return None

        def outputTree(self):
            if self.left:
                self.left.outputTree()
            if self.right:
                self.right.outputTree()

        def preorderWhitelist(self,refList,aList):
            if list(self.data)[bot.passwordCounter] in refList:
                aList.append(self.data)
            if self.left:
                aList=self.left.preorderWhitelist(refList,aList)
            if self.right:
                aList=self.right.preorderWhitelist(refList,aList)
            return aList
    try:
        bot.passRoot=passNode(aList[0])
        for password in range(1,len(aList)):
            bot.passRoot.insert(aList[password])
    except IndexError:
        bot.passwordsError=True
@bot.event
async def Help(ctx,params):
    try:
        await ctx.channel.send('```'+bot.helpContentDict[params[0]][0]+'```'+bot.helpContentDict[params[0]][1])
    except:
        await ctx.channel.send(bot.helpContent)
    await bot.clearCurrentUser(ctx)
@bot.event
async def Wires(ctx,noWires):
    'Wires'
    index=noWires-3
    if ctx.content=='exit':
        await ctx.channel.send('```Exiting module```')
        await bot.initModVar()
        await bot.clearCurrentUser(ctx)
        return
    if bot.wiresQAsked==True:
        if ctx.content=='yes':
            await ctx.channel.send('```'+bot.wiresQuestions[index][bot.wiresCounter][1]+'```')
            await bot.initModVar()
            await bot.clearCurrentUser(ctx)
            return
        elif ctx.content=='no':
            bot.wiresCounter=bot.wiresCounter+1
            bot.wiresQAsked=False
        else:
            await ctx.channel.send('```bad conditions- restart```')
            await bot.initModVar()
            await bot.clearCurrentUser(ctx)
            return
    if bot.wiresQAsked==False:
        if index>=len(bot.wiresQuestions) or index<0:
            await ctx.channel.send('```bad conditions- restart```')
            await bot.initModVar()
            await bot.clearCurrentUser(ctx)
        elif bot.wiresCounter==len(bot.wiresQuestions[index]):
            await ctx.channel.send('```end of conditions```')
            await bot.initModVar()
            await bot.clearCurrentUser(ctx)
        else:
            await ctx.channel.send(bot.wiresQuestions[index][bot.wiresCounter][0])
            bot.wiresQAsked=True
    await bot.saveCurrentUser(ctx,[bot.wiresCounter,bot.wiresQAsked])
@bot.event
async def Button(ctx,colour,word):
    'Button'
    if ctx.content=='exit':
        await ctx.channel.send('```Exiting module```')
        await bot.initModVar()
        await bot.clearCurrentUser(ctx)
        return
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
            await ctx.channel.send('''```
Hold Button

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
@bot.event
async def WhosOnFirst(ctx):
    'Whos on First'
    if bot.wOFFirstPass==False:
        bot.wOFFirstPass=True
        await ctx.channel.send('What does the display state?')
        await bot.saveCurrentUser(ctx,[bot.wOFCounter,bot.wOFFirstPass])
        return
    if bot.wOFCounter%2==0:
        temp=False
        for item in bot.wOFDisplayList:
            if item[0]==ctx.content:
                temp=True
                await ctx.channel.send('What does {position} read?'.format(position=item[1]))
        if temp==False:
            if ctx.content=='exit':
                await ctx.channel.send('```Exiting module```')
            else:
                await ctx.channel.send('```You have input erroneous data. Exiting module```')
            await bot.initModVar()
            await bot.clearCurrentUser(ctx)
            return
    else:
        temp=''
        for item in bot.wOFPotencialList:
            if item[0]==ctx.content.upper():
                for pot in range(1,len(item)):
                    temp=temp+'\n'+item[pot]
        if temp!='':
            await ctx.channel.send(('```Read the following to the defuser:{output}```'.format(output=temp)))
            await ctx.channel.send('What does the display state?')
        else:
            if ctx.content=='exit':
                await ctx.channel.send('```Exiting module```')
            else:
                await ctx.channel.send('```You have input erroneous data. Exiting module```')
            await bot.initModVar()
            await bot.clearCurrentUser(ctx)
            return
    bot.wOFCounter=bot.wOFCounter+1
    await bot.saveCurrentUser(ctx,[bot.wOFCounter,bot.wOFFirstPass])
@bot.event
async def Memory(ctx):
    #ctx = display
    if ctx.content=='exit':
        await ctx.channel.send('```Exiting module```')
        await bot.initModVar()
        await bot.clearCurrentUser(ctx)
        return
    if bot.memoryFirstPass==False:
        bot.memoryFirstPass=True
        await ctx.channel.send('What does the display state?')
        await bot.saveCurrentUser(ctx,[bot.memoryList,bot.memoryResponse,bot.memoryPOL,bot.memoryQAsked,bot.memoryFirstPass])
        return
    try:
        if int(ctx.content) not in range(1,5):
            raise ValueError('user input out of range or wrong type')
    except:
        await ctx.channel.send('```Sent erroneous input, exiting module```')
        await bot.initModVar()
        await bot.clearCurrentUser(ctx)
        return
    if bot.memoryQAsked==False:
        bot.memoryResponse=bot.memoryInstructions[len(bot.memoryList)][int(ctx.content)-1]
        await bot.MemoryRespond()
        if bot.memoryList[len(bot.memoryList)-1][0]==None:#no position
            bot.memoryPOL='position'
        elif bot.memoryList[len(bot.memoryList)-1][1]==None:#no label
            bot.memoryPOL='label'
        await ctx.channel.send('```{out}```send the {query} of the button pressed by the defuser'.format(out=bot.memoryResponse,query=bot.memoryPOL))
        bot.memoryQAsked=True
    #ctx = button pressed
    else:
        if bot.memoryPOL=='position':
            bot.memoryList[len(bot.memoryList)-1][0]=int(ctx.content)-1
        elif bot.memoryPOL=='label':
            bot.memoryList[len(bot.memoryList)-1][1]=int(ctx.content)
        bot.memoryQAsked=False
        await ctx.channel.send('What does the display state?')
    await bot.saveCurrentUser(ctx,[bot.memoryList,bot.memoryResponse,bot.memoryPOL,bot.memoryQAsked,bot.memoryFirstPass])
@bot.event
async def MemoryRespond():
#p=position, w=label, #s=same position in stage <>, l=same label in stage<>
#POSITION,LABEL
    if bot.memoryResponse[1]=='p':
        bot.memoryList.append([bot.memoryResponse[0],None])
        bot.memoryResponse='position '+str(bot.memoryResponse[0])
    elif bot.memoryResponse[1]=='w':
        bot.memoryList.append([None,bot.memoryResponse[0]])
        bot.memoryResponse='label '+str(bot.memoryResponse[0])
    elif bot.memoryResponse[1]=='s':
        bot.memoryList.append([bot.memoryList[bot.memoryResponse[0]][0],None])
        bot.memoryResponse='position '+str(bot.memoryList[bot.memoryResponse[0]][0])
    elif bot.memoryResponse[1]=='l':
        bot.memoryList.append([None,bot.memoryList[bot.memoryResponse[0]][1]])
        bot.memoryResponse='label '+str(bot.memoryList[bot.memoryResponse[0]][1])
@bot.event
async def MorseCode(ctx):
    'Morse Code'
    if ctx.content=='exit':
        await ctx.channel.send('```Exiting module```')
        await bot.initModVar()
        await bot.clearCurrentUser(ctx)
        return
    if bot.morseReturnPass==False:
        bot.morseReturnPass=True
        await ctx.channel.send('Send code (.-):')
        await bot.saveCurrentUser(ctx,[bot.morseLetterList,bot.morseReturnPass,bot.morseFail])
        return
    for i in range(0,len(bot.morseArray)):
        if bot.morseArray[i][1]==ctx.content and bot.morseArray[i][1] not in bot.morseLetterList:
            bot.morseLetterList.append(bot.morseArray[i][0])
    possWordIndex=[]
    for i in range(0,len(bot.morseWordList)):
        bot.morseFail=False
        for j in range(0,len(bot.morseLetterList)):
            if bot.morseLetterList[j] not in bot.morseWordList[i][0]:
                bot.morseFail=True
            if j==len(bot.morseLetterList)-1 and bot.morseFail==False:
                possWordIndex.append(i)

    if len(possWordIndex)==0:
        await ctx.channel.send('```bad conditions- restart```')
        await bot.initModVar()
        await bot.clearCurrentUser(ctx)
        return
    elif len(possWordIndex)>1:
        temp=''
        for ind in possWordIndex:
            temp=temp+bot.morseWordList[ind][0]+' | Frequency: '+bot.morseWordList[ind][1]+'\n'
        await ctx.channel.send('''```{data}
More needed: ```'''.format(data=temp))
        await bot.saveCurrentUser(ctx,[bot.morseLetterList,bot.morseReturnPass,bot.morseFail])
    else:
        await ctx.channel.send('```'+bot.morseWordList[possWordIndex[0]][0]+' | Frequency: '+bot.morseWordList[possWordIndex[0]][1]+'```')
        await bot.initModVar()
        await bot.clearCurrentUser(ctx)
        return
@bot.event
async def ComplicatedWires(ctx):
    if ctx.content=='exit':
        await ctx.channel.send('```Exiting module```')
        await bot.initModVar()
        await bot.clearCurrentUser(ctx)
        return
    if bot.cWQAsked==False:
        bot.cWQAsked=True
        await ctx.channel.send('Respond with 1 or 0 (true or false) for the following:\n```<red> <blue> <has star> <LED on>```\ninput should look similar to this: 0101')
    else:
        counter=0
        for i in list(ctx.content):
            if i=='1':
                if counter==0:
                    bot.situation=bot.situation+'r'
                elif counter==1:
                    bot.situation=bot.situation+'b'
                elif counter==2:
                    bot.situation=bot.situation+'s'
                elif counter==3:
                    bot.situation=bot.situation+'l'
                else:
                    await ctx.channel.send('```Too many bits! Exiting module```')
                    await bot.initModVar()
                    await bot.clearCurrentUser(ctx)
                    return
            counter=counter+1
        #form situation
        instruction=''
        for i in bot.wireSituation:
            if bot.situation==i[0]:
                instruction=i[1]
        #try:
        await ctx.channel.send('```'+bot.instructions[instruction]+'```'+'Send next wire or "exit"\nR B S L')
        bot.situation=''
        #except:
        '''
        await ctx.channel.send('```Impossible. Exiting module```')
        await bot.initModVar()
        await bot.clearCurrentUser(ctx)
        return
        '''
    await bot.saveCurrentUser(ctx,[bot.situation,bot.cWQAsked])
    return
@bot.event
async def WireSequences(ctx):
    'Wire Sequences'
    if bot.wSeqFirstPass==False:
        bot.wSeqFirstPass=True
        await ctx.channel.send('What colour is the first wire?')
        await bot.saveCurrentUser(ctx,[bot.wSeqRed,bot.wSeqBlue,bot.wSeqBlack,bot.wSeqFirstPass])
        return
    try:
        if ctx.content=='red':
            output=bot.wSeqOccurrences[0][bot.wSeqRed]
            bot.wSeqRed=bot.wSeqRed+1
        elif ctx.content=='blue':
            output=bot.wSeqOccurrences[1][bot.wSeqBlue]
            bot.wSeqBlue=bot.wSeqBlue+1
        elif ctx.content=='black':
            output=bot.wSeqOccurrences[2][bot.wSeqBlack]
            bot.wSeqBlack=bot.wSeqBlack+1
        else:
            if ctx.content=='exit':
                await ctx.channel.send('```Exiting module```')
            else:
                await ctx.channel.send('```You have input erroneous data. Exiting module```')
            await bot.initModVar()
            await bot.clearCurrentUser(ctx)
            return
    except IndexError:
        await ctx.channel.send('```Impossible. Exiting Module```')
    if output=='Cut wire':
        await ctx.channel.send('```Cut wire```')
    else:
        await ctx.channel.send(('```Cut the wire if connected to: {out}```'.format(out=output)))
    await ctx.channel.send('What colour is the next wire?')
    await bot.saveCurrentUser(ctx,[bot.wSeqRed,bot.wSeqBlue,bot.wSeqBlack,bot.wSeqFirstPass])
@bot.event
async def Passwords(ctx):
    'Passwords'
    if ctx.content=='exit':
        await ctx.channel.send('```Exiting module```')
    if bot.passwordsFirstPass==False:
        bot.passwordsFirstPass=True
        try:
            ctx.content=ctx.content.split('.passwords ')[1]
        except IndexError:
            await ctx.channel.send('```Send the appropriate parameters. That first row of characters alongside the function call```')
            await bot.initModVar()
            await bot.clearCurrentUser(ctx)
            return
    tempRef=list(ctx.content)
    passWhitelist=bot.passRoot.preorderWhitelist(tempRef,[])
    await bot.PassBuildTree(passWhitelist)
    if bot.passwordsError==True:
        await bot.initModVar()
        await bot.clearCurrentUser(ctx)
        return
    outputString=''
    for password in passWhitelist:
        outputString=outputString+password+'\n'
    await ctx.channel.send(('```\n{output}```').format(output=outputString))
    bot.passwordCounter=bot.passwordCounter+1
    if len(passWhitelist)>1 and bot.passwordCounter<6:
        await ctx.channel.send('Send the characters in slot: '+str(bot.passwordCounter+1))##'len(whitelist)'
        await bot.saveCurrentUser(ctx,[bot.passRoot,bot.passwordsFirstPass,bot.passwordCounter,bot.passwordsError])
    else:
        await bot.initModVar()
        await bot.clearCurrentUser(ctx)
@bot.event
async def Knobs(ctx):
    if ctx.content=='exit':
        await ctx.channel.send('```Exiting module```')
        await bot.initModVar()
        await bot.clearCurrentUser(ctx)
        return
    passed=False
    if bot.knobBool==False:
        await ctx.channel.send('Enter the configuration: e.g. 100111001101')
        bot.knobBool=True
    else:
        for i in range(0,len(bot.knobLEDConfigs)):
            for j in range(0,len(bot.knobLEDConfigs[i])):
                if ctx.content==bot.knobLEDConfigs[i][j]:
                    await ctx.channel.send('```Set to: '+bot.knobDirection[i]+'```')
                    passed=True
                    await bot.initModVar()
                    await bot.clearCurrentUser(ctx)
                    return
        if passed!=True:
            await ctx.channel.send('```bad conditions- restart```')
            await bot.initModVar()
            await bot.clearCurrentUser(ctx)
            return
    await bot.saveCurrentUser(ctx,[bot.knobBool])
    return
@bot.event
async def SimonSays(ctx,param):
    if bot.simonFirstPass==False:
        bot.simonFirstPass=True
        if param in bot.confirmList:
            bot.simonVowel=0
        elif param in bot.denyList:
            bot.simonVowel=1
        else:
            await ctx.channel.send('```Bad input. Confirm if there is a vowel in the serial number with y or n```')
            await bot.initModVar()
            await bot.clearCurrentUser(ctx)
            return
        await ctx.channel.send('Now what did simon say?')
        await bot.saveCurrentUser(ctx,[bot.simonOut,bot.simonStrikes,bot.simonFirstPass,bot.simonVowel])
        return
    elif bot.simonStrikes>2:
        await ctx.channel.send('```Uh too many strikes. Exiting```')
        await bot.initModVar()
        await bot.clearCurrentUser(ctx)
        return
    elif 'strike' in ctx.content:
        bot.simonStrikes=bot.simonStrikes+1
    elif ctx.content=='exit':
        await ctx.channel.send('```Exiting module```')
        await bot.initModVar()
        await bot.clearCurrentUser(ctx)
        return
    elif ctx.content=='red':
        bot.simonOut.append(0)
    elif ctx.content=='blue':
        bot.simonOut.append(1)
    elif ctx.content=='green':
        bot.simonOut.append(2)
    elif ctx.content=='yellow':
        bot.simonOut.append(3)
    else:
        await ctx.channel.send('```Bad input. Enter a colour next time```')
        await bot.initModVar()
        await bot.clearCurrentUser(ctx)
        return
    temp=''
    for item in bot.simonOut:
        temp=temp+'\n'+bot.simonSequence[bot.simonVowel][bot.simonStrikes][item]
    await ctx.channel.send(('```{output}```').format(output=temp))
    await ctx.channel.send('send the next colour or "exit"')
    await bot.saveCurrentUser(ctx,[bot.simonOut,bot.simonStrikes,bot.simonFirstPass,bot.simonVowel])
    return
@bot.event
async def Keypads(ctx):
    await ctx.channel.send('```Good luck```https://cdn.discordapp.com/attachments/806548674309128242/826021656476385290/unknown.png')
    await bot.clearCurrentUser(ctx)
@bot.event
async def Mazes(ctx):
    await ctx.channel.send('```Good Luck```https://cdn.discordapp.com/attachments/806548674309128242/826022923172315136/unknown.png')
    await bot.clearCurrentUser(ctx)
@bot.event
async def Vent(ctx):
    await ctx.channel.send('```Good Luck```https://cdn.discordapp.com/attachments/806548674309128242/826024495025225738/unknown.png')
    await bot.clearCurrentUser(ctx)
@bot.event
async def Capacitor(ctx):
    await ctx.channel.send('```Good Luck```https://cdn.discordapp.com/attachments/806548674309128242/826024708704174180/unknown.png')
    await bot.clearCurrentUser(ctx)
@bot.event
async def clearCurrentUser(ctx):
    for user in range(0,len(bot.currentCommands)):
        if bot.currentCommands[user][:2]==[ctx.guild.id,ctx.author.id]:
            bot.currentCommands.pop(user)
            await bot.initModVar()
            return
@bot.event
async def saveCurrentUser(ctx,parametersToSave):
    for user in range(0,len(bot.currentCommands)):
        if bot.currentCommands[user][:2]==[ctx.guild.id,ctx.author.id]:
            bot.currentCommands[user][4]=parametersToSave
            await bot.initModVar()
            return
@bot.event
async def on_ready():
    await bot.init()
    await bot.change_presence(activity=discord.Activity(name='and waiting', type=3))
    print("Ready to go")
@bot.event
async def runModules(ctx,mod,params):
    if mod=='.button':
        if len(params)==2:
            await bot.Button(ctx,params[0],params[1])
        else:
            await ctx.channel.send('```Insufficient parameters (colour and word only)```')
            await bot.clearCurrentUser(ctx)
            return
    elif mod=='.compwires':
        await bot.ComplicatedWires(ctx)
    elif mod=='.help':
        await bot.Help(ctx,params)
    elif mod=='.knobs':
        await bot.Knobs(ctx)
    elif mod=='.memory':
        await bot.Memory(ctx)
    elif mod=='.morse':
        await bot.MorseCode(ctx)
    elif mod=='.passwords':
        await bot.Passwords(ctx)
    elif mod=='.simonsays':
        if len(params)==1:
            await bot.SimonSays(ctx,params[0])
        else:
            await ctx.channel.send('```Insufficient parameters (include y or n)```')
            await bot.clearCurrentUser(ctx)
            return
    elif mod=='.whosonfirst':
        await bot.WhosOnFirst(ctx)
    elif mod=='.wires':
        for char in params[0]:
            if char not in bot.num:
                await ctx.channel.send('```Incorrect type for parameter (number of wires only)```')
                await bot.clearCurrentUser(ctx)
                return
        await bot.Wires(ctx,int(params[0]))
    elif mod=='.wireseq':
        await bot.WireSequences(ctx)
    elif mod=='.keypads':
        await bot.Keypads(ctx)
    elif mod=='.mazes':
        await bot.Mazes(ctx)
    elif mod=='.vent':
        await bot.Vent(ctx)
    elif mod=='.capacitor':
        await bot.Capacitor(ctx)
@bot.event
async def on_message(ctx):
    try:
        print(ctx.author.name+': '+ctx.content)
        fUser=True
        for job in bot.currentCommands:
            if job[0:2]==[ctx.guild.id,ctx.author.id]:
                fUser=False
        if fUser==True:
            if ctx.content.split(' ')[0] in bot.commandList:
                for comm in bot.commandList:
                    if comm==ctx.content.split(' ')[0]:
                        bot.currentCommands.append([ctx.guild.id,ctx.author.id,comm])
                        bot.currentCommands[len(bot.currentCommands)-1].append(ctx.content.split(' ')[1:len(ctx.content.split(' '))])
                        bot.currentCommands[len(bot.currentCommands)-1].append([])
        for job in bot.currentCommands:
            if job[:2]==[ctx.guild.id,ctx.author.id]:
                if job==bot.currentCommands[len(bot.currentCommands)-1] and fUser==True:
                    pass
                else:
                    if job[2]=='.button':
                        bot.haltButton,bot.holdButton,bot.qIndex=job[4]
                    elif job[2]=='.wires':
                        bot.wiresCounter,bot.wiresQAsked=job[4]
                    elif job[2]=='.compwires':
                        bot.situation,bot.cWQAsked=job[4]
                    elif job[2]=='.memory':
                        bot.memoryList,bot.memoryResponse,bot.memoryPOL,bot.memoryQAsked,bot.memoryFirstPass=job[4]
                    elif job[2]=='.morse':
                        bot.morseLetterList,bot.morseReturnPass,bot.morseFail=job[4]
                    elif job[2]=='.passwords':
                        bot.passRoot,bot.passwordsFirstPass,bot.passwordCounter,bot.passwordsError=job[4]
                    elif job[2]=='.simonsays':
                        bot.simonOut,bot.simonStrikes,bot.simonFirstPass,bot.simonVowel=job[4]
                    elif job[2]=='.whosonfirst':
                        bot.wOFCounter,bot.wOFFirstPass=job[4]
                    elif job[2]=='.wireseq':
                        bot.wSeqRed,bot.wSeqBlue,bot.wSeqBlack,bot.wSeqFirstPass=job[4]
                    elif job[2]=='.knobs':
                        bot.knobBool=job[4]
                await bot.runModules(ctx,job[2],job[3])
    except:
        await bot.clearCurrentUser(ctx)
        await ctx.channel.send(('<@!196348156751904769>```{error}```'.format(error=traceback.format_exc())))
        await ctx.channel.send('```Sorry, not your fault. Try again```')
bot.run(TOKEN)
