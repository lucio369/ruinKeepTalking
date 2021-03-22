import discord, os, random
from discord.ext import commands
TOKEN=str(open("tokenFile.txt", "r").read())
bot=commands.Bot(command_prefix='.')

@bot.event
async def init():
    #general
    bot.num=['0','1','2','3','4','5','6','7','8','9']
    bot.ytzCommands=[['.button',False],
                 ['.compwires',False],
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
    try:
        import hajiBajiPrivate
        bot.personalFile=True
        bot.bigtquotetuple=hajiBajiPrivate.bigtquotetuple
        bot.bullying=hajiBajiPrivate.bullying
        bot.genMessage=hajiBajiPrivate.genMessage
        bot.conditionCheck=hajiBajiPrivate.conditionCheck

    except ModuleNotFoundError:
        bot.personalFile=False
    bot.currentChannel=''
    bot.switchChannelOutput='''
===============================================================================
{channelName}
    '''
    bot.busy=False
    bot.helpContent='''```
    Keep Talking and Nobody Explodes Assistant

    Compatible with: Version 1 | Verification Code: 241

    Wires              Finds correct wire based off user input | .wires [number of wires]
    Button             Finds correct button based off user input | .button [colour of button] [word on button]
    Simon Says         Finds correct button based off user input | .simonsays [True/False: Vowel in serial num]
    Whos on First      puts to word response from input word | .whosonfirst
    Memory             returns appropriate button to press based off user input | .memory
    Morse Code         works out valid word and frequency encoded in morse | .morse
    Complicated Wires  responds correct response for each wire based off user input | .compWires
    Wire Sequences     decides which wires to cut based off user input | .wireseq
    Passwords          figures out which word is the password from given characters | .passwords [first column of characters]
    Knobs              outputs direction from given 12 bit number | .knobs
    Help               does this```'''
    await bot.initModVar()
@bot.event
async def initModVar():
    #wires variables
    bot.wiresCounter=0
    bot.wiresQAsked=False

    #wires constants
    bot.wiresQuestions=[[['No red?','Cut second wire'],['Last wire is white?','Cut last wire'],['More than one blue wire?','Cut last blue wire'],['None true?','Cut last wire']],
               [['More than 1 red and last digit of serial odd','Cut last red wire'],['Last wire yellow and no red wires?','Cut first wire'],['Exactly one blue wire?','Cut first wire'],['More than one yellow wire?','Cut last wire'],['None true?','Cut second wire']],
               [['Last wire black and last digit of serial odd?','Cut fourth wire'],['Exactly one red and more than one yellow?','Cut first wire'],['No black wires?','Cut second wire'],['None true?','Cut first wire']],
               [['No yellow and last digit of series is odd?','Cut third wire'],['Exactly one yellow and more than one white?','Cut fourth wire'],['No red?','Cut last wire'],['None true?','Cut fourth wire']]]

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

    #complicated wires constants
    bot.wireSituation=[['','c'],
                       ['r','s'],['rb','s'],['rs','c'],['rl','b'],['rbs','s'],['rbl','p'],['rsl','b'],['rbsl','d'],
                       ['b','s'],['bs','d'],['bl','p'],['bsl','p'],
                       ['s','c'],['sl','b'],
                       ['l','d']]
    bot.instructions=[['c','Cut Wire'],['d','Do not cut wire'],['s','Cut wire if LAST DIGIT EVEN'],
                      ['p','Cut wire if bomb has PARRALLEL PORT'],['b','Cut wire if bomb has TWO OR MORE batteries']]
    bot.cWQuestions=[['red','r'],['blue','b'],['has star','s'],['LED on','l']]

    #complicated wires variables
    bot.situation=''
    bot.cWIndex=0
    bot.cWQAsked=False

    #knobs constants
    bot.knobLEDConfigs=[['010111011011','100111001101'],
                    ['011111010011','100110001001'],
                    ['010000011101','000000011100'],
                    ['110111101110','110111100100']]
    bot.knobDirection=['up','down','left','right']

    #knob variables
    bot.knobBool=False

    #memory constants
    bot.memoryNum=['0','1','2','3','4','5','6','7','8','9']
    bot.memoryCommandList=[['2s','2s','3s','4s'],
                 ['4w','1p','1s','1p'],
                 ['2l','1l','3s','4w'],
                 ['1p','1s','2p','2p'],
                 ['1l','2l','4l','3l']]#num,command (s=literal button,w=written on label,p=position pressed in stage <stage>,l=same written label as stage <stage>)

    #memory variables
    bot.memoryStage=0
    bot.memoryCurrentCommand=[]
    bot.memoryRequest=0
    bot.memoryCurrentCommand=[]
    bot.memoryRequestValue=0
    bot.memoryPhrase=''
    bot.memoryReqData=True
    bot.memoryPushPosVal=False
    bot.memoryPosValue=[]
    bot.memoryArray=[]#pos,valu

    #morse constants
    bot.morseArray=[['a','.-'],['b','-...'],['c','-.-.'],['d','-..'],['e','.'],['f','..-.'],
                    ['g','--.'],['h','....'],['i','..'],['j','.---'],['k','-.-'],['l','.-..'],
                    ['m','--'],['n','-.'],['o','---'],['p','.--.'],['q','--.-'],['r','.-.'],
                    ['s','...'],['t','-'],['u','..-'],['v','...-'],['w','.--'],['x','-..-'],
                    ['y','-.--'],['z','--..'],['0','-----'],['1','.----'],['2','..---'],['3','...--'],['4','....-'],['5','.....'],
                    ['6','-....'],['7','--...'],['8','---..'],['9','----.']]
    bot.wordList=[['shell','3.505'],['halls','3.515'],['slick','3.522'],['trick','3.532'],['boxes','3.535'],['leaks','3.542'],
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

    #password variables
    await bot.PassBuildTree(bot.passwords)
    bot.passwordsError=False
    bot.passwordsFirstPass=False
    bot.passwordCounter=0

    #simon says constants
    bot.simonSequence=[[['blue','red','yellow','green'],
    ['yellow','green','blue','red'],
    ['green','red','yellow','blue']],
    [['blue','yellow','green','red'],
    ['red','blue','yellow','green'],
    ['yellow','green','blue','red']]]

    #simon says variables
    bot.simonOut=[]
    bot.simonStrikes=0
    bot.simonFirstPass=False
    bot.simonVowel=0

    #whos on first constants
    bot.wOFDisplayList=[['yes','left middle'],['first','top right'],['display','bottom right'],['okay','top right'],
                 ['says','bottom right'],['nothing','middle left'],['','bottom left'],['blank','middle right'],['no','bottom right'],
                 ['led','middle left'],['lead','bottom right'],['read','middle right'],['red','middle right'],['reed','bottom left'],
                 ['leed','bottom left'],['hold on','bottom right'],['you','middle right'],['you are','bottom right'],
                 ['your','middle right'],["you're",'middle right'],["youre",'middle right'],['ur','top left'],['there','bottom right'],
                 ["they're",'bottom left'],["theyre",'bottom left'],['their','middle right'],['they are','middle left'],
                 ['see','bottom right'],['c','top right'],['cee','bottom right']]
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

    #whos on first variables
    bot.wOFCounter=0
    bot.wOFFirstPass=False

################################################################################################################################
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
            print(self.data)
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
    except:
        bot.passwordsError=True
        print('Error on 203')

@bot.event
async def Help(ctx):
    await ctx.channel.send(bot.helpContent)
    await bot.clearCurrentUser(ctx)

@bot.event
async def Wires(ctx,noWires):
    'Wires'
    index=noWires-3
    if ctx.content=='exit':
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
        await ctx.channel.send('```What does the display state?```')
        await bot.saveCurrentUser(ctx,[bot.wOFCounter,bot.wOFFirstPass])
        return
    if bot.wOFCounter%2==0:
        print(ctx.content)
        temp=False
        for item in bot.wOFDisplayList:
            if item[0]==ctx.content:
                temp=True
                await ctx.channel.send(('```What does {position} read?```'.format(position=item[1])))
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
                print(item)
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
    if ctx.content=='exit':
        await bot.initModVar()
        await bot.clearCurrentUser(ctx)
        return
    if bot.memoryStage<5:
        if bot.memoryReqData==True:
            await ctx.channel.send('What does the display say?')
            bot.memoryReqData=False
        else:
            if bot.memoryPushPosVal==False:
                tempList=list(ctx.content)
                for character in tempList:
                    if character not in bot.num:
                        await ctx.channel.send('```bad conditions- restart```')
                        await bot.initModVar()
                        await bot.clearCurrentUser(ctx)
                        return
                bot.memoryRequest=int(ctx.content)
                if not (0<bot.memoryRequest<5):
                    await ctx.channel.send('```bad conditions- restart```')
                    await bot.initModVar()
                    await bot.clearCurrentUser(ctx)
                    return
                bot.memoryCurrentCommand=list(bot.memoryCommandList[bot.memoryStage][bot.memoryRequest-1])
                bot.memoryRequestValue=int(bot.memoryCurrentCommand[0])
                bot.memoryPhrase=bot.memoryCurrentCommand[1]
                #num,command (s=literal button,w=written on label,p=position pressed in stage <stage>,l=same written label as stage <stage>)
                if bot.memoryPhrase=='s':#s=literal button
                    memoryOutput='Position '+str(bot.memoryRequestValue)
                    bot.memoryPosValue=[str(bot.memoryRequestValue),'']
                elif bot.memoryPhrase=='w':#w=written on label
                    memoryOutput='Label '+str(bot.memoryRequestValue)
                    bot.memoryPosValue=['',str(bot.memoryRequestValue)]
                elif bot.memoryPhrase=='p':#p=position pressed in stage <stage>
                    memoryOutput='Position '+bot.memoryArray[bot.memoryRequestValue-1][0]
                    bot.memoryPosValue=[bot.memoryArray[bot.memoryRequestValue-1][0],'']
                elif bot.memoryPhrase=='l':#l=same written label as stage <stage>
                    memoryOutput='Label '+bot.memoryArray[bot.memoryRequestValue-1][1]
                    bot.memoryPosValue=['',bot.memoryArray[bot.memoryRequestValue-1][1]]
                if bot.memoryStage!=4:
                    if bot.memoryPhrase in ('s','p'):
                        await ctx.channel.send('''
```{Output}```
What does it say now?'''.format(Output=memoryOutput))
                    else:
                        await ctx.channel.send('''
```{Output}```
What is it's position?'''.format(Output=memoryOutput))
                    bot.memoryPushPosVal=True
                else:
                    await ctx.channel.send('```'+memoryOutput+'```')
                    bot.memoryStage=bot.memoryStage+1
                    await bot.Memory(ctx)
                    return
            else:
                tempList=list(ctx.content)
                for character in tempList:
                    if character not in bot.num:
                        await ctx.channel.send('```bad conditions- restart```')
                        await bot.initModVar()
                        await bot.clearCurrentUser(ctx)
                        return
                bot.memoryRequest=int(ctx.content)
                if not (0<bot.memoryRequest<5):
                    await ctx.channel.send('```bad conditions- restart```')
                    await bot.initModVar()
                    await bot.clearCurrentUser(ctx)
                    return
                for item in range(0,len(bot.memoryPosValue)):#position,value
                    if bot.memoryPosValue[item]=='':
                        bot.memoryPosValue[item]=ctx.content
                bot.memoryStage=bot.memoryStage+1
                bot.memoryPushPosVal=False
                bot.memoryReqData=True
                bot.memoryArray.append(bot.memoryPosValue)
                await bot.saveCurrentUser(ctx,[bot.memoryStage,bot.memoryCurrentCommand,bot.memoryRequest,bot.memoryCurrentCommand,bot.memoryRequestValue,bot.memoryPhrase,bot.memoryReqData,bot.memoryPushPosVal,bot.memoryPosValue,bot.memoryArray])
                await bot.Memory(ctx)
                return
    else:
        await bot.initModVar()
        await bot.clearCurrentUser(ctx)
        return
    await bot.saveCurrentUser(ctx,[bot.memoryStage,bot.memoryCurrentCommand,bot.memoryRequest,bot.memoryCurrentCommand,bot.memoryRequestValue,bot.memoryPhrase,bot.memoryReqData,bot.memoryPushPosVal,bot.memoryPosValue,bot.memoryArray])
    return

@bot.event
async def MorseCode(ctx):
    'Morse Code'
    if ctx.content=='exit':
        await bot.initModVar()
        await bot.clearCurrentUser(ctx)
        return
    if bot.returnPass==False:
        bot.returnPass=True
        await ctx.channel.send('```Send code (.-):```')
        await bot.saveCurrentUser(ctx,[bot.letterList,bot.returnPass,bot.fail])
        return
    for i in range(0,len(bot.morseArray)):
        if bot.morseArray[i][1]==ctx.content and bot.morseArray[i][1] not in bot.letterList:
            bot.letterList.append(bot.morseArray[i][0])
    possWordIndex=[]
    for i in range(0,len(bot.wordList)):
        bot.fail=False
        for j in range(0,len(bot.letterList)):
            if bot.letterList[j] not in bot.wordList[i][0]:
                bot.fail=True
            if j==len(bot.letterList)-1 and bot.fail==False:
                possWordIndex.append(i)

    if len(possWordIndex)==0:
        await ctx.channel.send('```bad conditions- restart```')
        await bot.initModVar()
        await bot.clearCurrentUser(ctx)
        return
    elif len(possWordIndex)>1:
        temp=''
        for ind in possWordIndex:
            temp=temp+bot.wordList[ind][0]+' | Frequency: '+bot.wordList[ind][1]+'\n'
        await ctx.channel.send('''```{data}
More needed: ```'''.format(data=temp))
        await bot.saveCurrentUser(ctx,[bot.letterList,bot.returnPass,bot.fail])
    else:
        await ctx.channel.send('```'+bot.wordList[possWordIndex[0]][0]+' | Frequency: '+bot.wordList[possWordIndex[0]][1]+'```')
        await bot.initModVar()
        await bot.clearCurrentUser(ctx)
        return

@bot.event
async def ComplicatedWires(ctx):
    if ctx.content=='exit':
        await bot.initModVar()
        await bot.clearCurrentUser(ctx)
        return
    if bot.cWIndex<len(bot.cWQuestions):
        if bot.cWQAsked==False:
            await ctx.channel.send(bot.cWQuestions[bot.cWIndex][0]+'?')
            bot.cWQAsked=True
        else:
            if ctx.content=='yes':
                bot.situation=bot.situation+bot.cWQuestions[bot.cWIndex][1]
            elif ctx.content=='no':
                pass
            else:
                await ctx.channel.send('```bad conditions- restart```')
                await bot.initModVar()
                await bot.clearCurrentUser(ctx)
                return
            bot.cWIndex=bot.cWIndex+1
            bot.cWQAsked=False
            await bot.ComplicatedWires(ctx)
            return
    else:
        for i in range(0,len(bot.wireSituation)):
            if bot.situation==bot.wireSituation[i][0]:
                instruction=bot.wireSituation[i][1]
        for i in range(0,len(bot.instructions)):
            if bot.instructions[i][0]==instruction:
                await ctx.channel.send('```'+bot.instructions[i][1]+'```')
                await bot.initModVar()
                await bot.clearCurrentUser(ctx)
                return
    await bot.saveCurrentUser(ctx,[bot.situation,bot.cWIndex,bot.cWQAsked])
    return

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

@bot.event
async def Passwords(ctx):
    'Passwords'
    if bot.passwordsFirstPass==False:
        bot.passwordsFirstPass=True
        try:
            ctx.content=ctx.content.split('.passwords ')[1]
        except IndexError:
            await bot.initModVar()
            await bot.clearCurrentUser(ctx)
            return
        except:
            print('Error on 625')
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
        await bot.initModVar()
        await bot.clearCurrentUser(ctx)
        return
    passed=False
    if bot.knobBool==False:
        await ctx.channel.send('Enter the configuration (Twelve bits)')
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
async def SimonSays(ctx):
    if bot.simonFirstPass==False:
        bot.simonFirstPass=True
        if ctx.content.split('.simonsays ')[1]=='true':
            bot.simonVowel=0
        elif ctx.content.split('.simonsays ')[1]=='false':
            bot.simonVowel=1
        else:
            await ctx.channel.send('```Bad input. Confirm if there is a vowel in the serial number with True or False```')
            await bot.initModVar()
            await bot.clearCurrentUser(ctx)
            return
        await ctx.channel.send('```Now what did simon say?```')
        await bot.saveCurrentUser(ctx,[bot.simonOut,bot.simonStrikes,bot.simonFirstPass,bot.simonVowel])
        return
    elif bot.simonStrikes>2:
        await ctx.channel.send('```Uh too many strikes```')
        await bot.initModVar()
        await bot.clearCurrentUser(ctx)
        return
    elif 'strike' in ctx.content:
        bot.simonStrikes=bot.simonStrikes+1
        await ctx.channel.send('```That was dumb- Next colour please.```')
        await bot.saveCurrentUser(ctx,[bot.simonOut,bot.simonStrikes,bot.simonFirstPass,bot.simonVowel])
        return
    elif ctx.content=='exit':
        await ctx.channel.send('```See ya```')
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
async def clearCurrentUser(ctx):
    bot.ytzCommands=[['.button',False],
                 ['.compwires',False],
                 ['.help',False],
                 ['.knobs',False],
                 ['.memory',False],
                 ['.morse',False],
                 ['.passwords',False],
                 ['.simonsays',False],
                 ['.whosonfirst',False],
                 ['.wires',False],
                 ['.wireseq',False]]
    for user in range(0,len(bot.currentModules)):
        if ctx.author.id==bot.currentModules[user][0]:
            bot.currentModules.pop(user)
    await bot.initModVar()

@bot.event
async def saveCurrentUser(ctx,parametersToSave):
    for user in range(0,len(bot.currentModules)):
        if ctx.author.id==bot.currentModules[user][0]:
            bot.currentModules[user]=[ctx.author.id,bot.command]
            for param in parametersToSave:
                bot.currentModules[user].append(param)
    await bot.initModVar()

@bot.event
async def on_ready():
    await bot.init()
    print("Ready to go")
    await bot.change_presence(activity=discord.Activity(name='and waiting', type=3))

@bot.event
async def runModules(ctx):
    bot.busy=True
    for comm in bot.ytzCommands:
        if comm[1]==True:
            if comm[0]=='.button':
                await bot.Button(ctx,bot.params[0],bot.params[1])
            if comm[0]=='.compwires':
                await bot.ComplicatedWires(ctx)
            if comm[0]=='.help':
                await bot.Help(ctx)
            if comm[0]=='.knobs':
                await bot.Knobs(ctx)
            if comm[0]=='.memory':
                await bot.Memory(ctx)
            if comm[0]=='.morse':
                await bot.MorseCode(ctx)
            if comm[0]=='.passwords':
                await bot.Passwords(ctx)
            if comm[0]=='.simonsays':
                await bot.SimonSays(ctx)
            if comm[0]=='.whosonfirst':
                await bot.WhosOnFirst(ctx)
            if comm[0]=='.wires':
                await bot.Wires(ctx,int(bot.params[0]))
            if comm[0]=='.wireseq':
                await ctx.channel.send('Module status: In development')
@bot.event
async def on_message(message):
    message.content=message.content.lower()
    if message.channel!=bot.currentChannel:
        bot.currentChannel=message.channel
        print(bot.switchChannelOutput.format(channelName=str(bot.currentChannel).upper()))
    attachURLS=' ~ '
    for item in message.attachments:
        attachURLS=attachURLS+item.url+' '
    if attachURLS!=' ~ ':
        pass
        print(message.author.name+': '+message.content+attachURLS)
    else:
        pass
        print(message.author.name+': '+message.content)
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
                        print(bot.currentModule)
                        if bot.currentModule=='.button':
                            bot.haltButton,bot.holdButton,bot.qIndex=bot.currentModules[eachUser][2],bot.currentModules[eachUser][3],bot.currentModules[eachUser][4]
                        elif bot.currentModule=='.wires':
                            bot.wiresCounter,bot.wiresQAsked=bot.currentModules[eachUser][2],bot.currentModules[eachUser][3]
                        elif bot.currentModule=='.compwires':
                            bot.situation,bot.cWIndex,bot.cWQAsked=bot.currentModules[eachUser][2],bot.currentModules[eachUser][3],bot.currentModules[eachUser][4]
                        elif bot.currentModule=='.memory':
                            bot.memoryStage,bot.memoryCurrentCommand,bot.memoryRequest=bot.currentModules[eachUser][2],bot.currentModules[eachUser][3],bot.currentModules[eachUser][4]
                            bot.memoryCurrentCommand,bot.memoryRequestValue,bot.memoryPhrase=bot.currentModules[eachUser][5],bot.currentModules[eachUser][6],bot.currentModules[eachUser][7]
                            bot.memoryReqData,bot.memoryPushPosVal,bot.memoryPosValue=bot.currentModules[eachUser][8],bot.currentModules[eachUser][9],bot.currentModules[eachUser][10]
                            bot.memoryArray=bot.currentModules[eachUser][11]
                        elif bot.currentModule=='.morse':
                            bot.letterList,bot.returnPass,bot.fail=bot.currentModules[eachUser][2],bot.currentModules[eachUser][3],bot.currentModules[eachUser][4]
                        elif bot.currentModule=='.passwords':
                            bot.passRoot,bot.passwordsFirstPass,bot.passwordCounter,bot.passwordsError=bot.currentModules[eachUser][2],bot.currentModules[eachUser][3],bot.currentModules[eachUser][4],bot.currentModules[eachUser][5]
                        elif bot.currentModule=='.simonsays':
                            bot.simonOut,bot.simonStrikes,bot.simonFirstPass,bot.simonVowel=bot.currentModules[eachUser][2],bot.currentModules[eachUser][3],bot.currentModules[eachUser][4],bot.currentModules[eachUser][5]
                        elif bot.currentModule=='.whosonfirst':
                            bot.wOFCounter,bot.wOFFirstPass=bot.currentModules[eachUser][2],bot.currentModules[eachUser][3]
                await bot.runModules(message)
            else:
                comm[1]=False
    if bot.busy==True:
        bot.busy=False
    else:
        if bot.personalFile==True:
            if message.content.startswith(bot.conditionCheck[0][0]):
                await message.channel.send(bot.conditionCheck[0][1])
            elif message.content.startswith(bot.conditionCheck[1][0]) or message.content.startswith(bot.conditionCheck[2][0]):
                await message.channel.send(bot.conditionCheck[1][1])
            elif message.content==bot.conditionCheck[3][0]:
                await message.channel.send(bot.conditionCheck[3][1])
            elif str(bot.user.id) in message.content:
                await message.channel.send(bot.conditionCheck[4])
            elif bot.conditionCheck[5] in message.content:
                randomMess=random.randint(0,len(bot.bigtquotetuple)-1)
                await message.channel.send(bot.bigtquotetuple[randomMess])
            else:
                if random.randint(0,40)==1:
                    if message.author.id not in bot.bullying:
                        randMessage=bot.genMessage[random.randint(0,len(bot.genMessage)-1)]
                    else:
                        randMessage=bot.bullying[message.author.id][random.randint(0,len(bot.bullying[message.author.id])-1)]
                    await message.channel.send(randMessage)

bot.run(TOKEN)
