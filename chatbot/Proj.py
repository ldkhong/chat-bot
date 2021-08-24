import CYKParse
import Tree

import PeriodicTable
from PeriodicTable import getInformation,countElements,nonmetal_element
from random import randint
import GrammarRule
from GrammarRule import grammarPeriodic
import re #tokenize input from user

user_bye = ['goodbye','bye','see you', 'see ya', 'leave', 'exit']
user_short_repsonse = ['ok','i see', 'got it', 'thank you','thanks']

greetings = ['Hi','Hello', 'Hi there', 'Hi ya']

greetings2 = ['How can I help you?','Do you have any questions for me?']

farewells = ['Goodbye!', 'Bye Bye!','See you later!', 'OK, bye.', 'See ya!']
farewells_2 =['',' Have a great day!','',' Have a good one!', ' Have a nice day','']

start = ['','Well! ','','hmmm..','']
end = ['', ' Any other questions?','',' Any more questions?','',' Any more questions you wanna ask?','']

reply_thanks = ['You\'re welcome!','No problem!','No worries!','Don\'t mention it. Any more questions?', 'My pleasure.','Anytime.','Sure!']
end_2= [ 'Any other questions?', 'Any more questions?', 'Any more questions you wanna ask?']

errors = ['Could you repeat that please?','Sorry, I didn\'t get that.','Oops, I didn\'t get that.','hmmm.. I\'ve never heard that before. Not sure how to respond to that.','Sorry, I don\'t know how to answer that.','Sorry, I don\'t know what that means.']

requestInfo = {
        'username': '',
        'element':[],
        'info': '',
        'count':'',
        'number':'',
        'adj':'',
        'compare': -2,
        'locate':[],
        'table': False,
        'greet': False,
}
prevInfo = {}
WQuestion = False
YNQuestion = False
Unknown = False
usePrevInfo = False
# Given the collection of parse trees returned by CYKParse, this function
# returns the one corresponding to the complete sentence.
def getSentenceParse(T):
    sentenceTrees = { k: v for k,v in T.items() if k.startswith('S/0') }
    if not sentenceTrees: # if sentenceTrees is empty
        return None
    else:
        completeSentenceTree = max(sentenceTrees.keys())
        #print('getSentenceParse', completeSentenceTree)
        return T[completeSentenceTree]

# Processes the leaves of the parse tree to pull out the user's request.
def updateRequestInfo(Tr):
    global requestInfo, WQuestion, Unknown, YNQuestion, usePrevInfo
    lookingForName = False
    lookingForlocate = False
    lookingForNum = False
    leaves = Tr.getLeaves()
    length = len(leaves)
    Noun = ['position','mass','symbol','electron','electrons','protons','proton','number','numbers','nonmetal','metal']
    
    for i,leaf in enumerate(leaves):
        #print(leaf, end = ' ')
        if leaf[0] == 'Unknown':
            Unknown = True
            break
   
        leaf_1_lower = leaf[1].lower()
        if i == 0:
            if leaf[0] == 'WQuestion':
                WQuestion = True
                if leaf_1_lower == 'where':
                    requestInfo['info'] = 'position'
                elif leaf_1_lower == 'who':
                    requestInfo['info'] = "discovered_by"
                elif leaf_1_lower == 'how' and i + 2 < length: 
                    if leaves[i+1][1] == 'many':
                        requestInfo['count'] = leaves[i+2][1]
                    elif leaves[i+1][1] == 'about':
                        usePrevInfo = True
                elif leaf_1_lower == 'what' and i + 2 < length: 
                    if leaves[i+1][1] == 'about':
                        usePrevInfo = True

            if leaf[0] == 'Verb':
                YNQuestion = True
        if leaf_1_lower == 'its' or leaf_1_lower == 'it':
            if prevInfo and len(prevInfo['element']) > 0:
                requestInfo['element'].append(prevInfo['element'][0])
            else:
                Unknown = True
                break
            
        if leaf_1_lower == 'in' or leaf_1_lower == 'on':
            lookingForlocate = True

        if leaf_1_lower in ['row','period','group','column'] and lookingForlocate:
            if i + 1 < length:   
                requestInfo['locate']=[leaf[1],leaves[i+1][1]]
            else:
                requestInfo['locate']=[leaf[1],'']

        if leaf[0] == 'Adverb':
            if leaf_1_lower == 'more' or leaf_1_lower == 'most':
                requestInfo['compare'] = 0
            elif leaf_1_lower == 'less' or leaf_1_lower == 'least':
                requestInfo['compare'] = -1

        if leaf[0] == 'Adjective':
            requestInfo['adj'] = leaf_1_lower
        if (leaf[0] == 'Greeting'):
            requestInfo['greet'] = True
        if leaf[0] == 'Element' or leaf[0] == 'Symbol':
            requestInfo['element'].append(leaf)       
        if leaf_1_lower in Noun:
            requestInfo['info'] = leaf[1]
        if leaf_1_lower == 'name' or leaf_1_lower == 'am':
            lookingForName = True
            requestInfo['username'] = ''
        if lookingForName and leaf[0] == 'Name':
            if requestInfo['username'] != '':
                requestInfo['username'] += ' '
            requestInfo['username'] += leaf[1]
        if leaf_1_lower == 'table':
            requestInfo['table'] = True
        if leaf[0] == 'Number':
            requestInfo['number'] = int (leaf[1])
            lookingForNum = True
        if lookingForNum and leaf[0] == 'Noun':
            requestInfo['info'] = leaf[1]
    #print('\n')
# Format a reply to the user, based on what the user wrote.
def reply():
    global greetings , farewells, end, start, haveGreeted
    global requestInfo, errors, WQuestion, Unknown, YNQuestion, prevInfo
    haveGreeted = False
    print("Bot:",end=" ")
    # check for greeting
    if Unknown:
        print(errors[randint(0,len(errors) - 1)])
    else:
        if requestInfo['greet']: 
            if requestInfo['username'] != '':
                print(greetings[randint(0,1)]+',',requestInfo['username'] + '.', end = ' ')
            else:
                print(greetings[randint(0,3)] + '.', end = ' ')

            print('I am Evee - an A.I assistant in Chemistry.',greetings2[randint(0,len(greetings2)-1)])
            requestInfo['greet'] = False
            haveGreeted = True

        if usePrevInfo:
            if bool(prevInfo):
                if len(requestInfo['element']) == 0 and len(prevInfo['element'])> 0:
                    requestInfo['element'] = prevInfo['element']
                elif requestInfo['info'] == '':
                    requestInfo['info'] = prevInfo['info']
            else:
                print(errors[randint(0,len(errors) - 1)])
                return

        if WQuestion:
            # check ask for element
            rep = []
            if len(requestInfo['element']) == 1:
                rep = repWhatQuestion()
                print(start[randint(0,len(start)-1)] + rep + end[randint(0,len(end)-1)])
            elif len(requestInfo['element']) >1 and requestInfo['compare']!= -2:
                if requestInfo['adj'].lower() in['reactive','metallic','nonmetallic']:
                    rep,_ = repReactive()
                    print(start[randint(0,len(start)-1)]+rep[randint(0,len(rep)-1)]+end[randint(0,len(end)-1)])
                else:
                    print(errors[randint(0,len(errors) - 1)])
            # check for how many questions
            elif requestInfo['count'] != '':
                rep = repHowManyQuestion()
                print(start[randint(0,len(start)-1)]+rep[randint(0,len(rep)-1)]+end[randint(0,len(end)-1)])

            # answer general question if ask about the table
            elif requestInfo['table']:
                print('The periodic table is a tabular array of the chemical elements organized by atomic number, from the element with the lowest atomic number, hydrogen, to the element with the highest atomic number, oganesson.')       
            else:
                print(errors[randint(0,len(errors) - 1)])

        elif YNQuestion:
            rep = YesNo()
            print(start[randint(0,len(start)-1)]+rep[randint(0,len(rep)-1)]+end[randint(0,len(end)-1)])
            
        #handle unexpected reply / input
        elif not haveGreeted:
            print(errors[randint(0,len(errors) - 1)])

    # reset request info
    prevInfo = requestInfo.copy()
    resetInfo()
    print()
    return

#reply what/where/else,how many when - 1 element appear on the question
def repWhatQuestion():
    global requestInfo
    element = requestInfo['element'][0][1].lower()
    rep = ''

    if requestInfo['info'] == 'position': 
        group = getInfo(0,'xpos')
        period = getInfo(0,'ypos')
        rep = element.capitalize()+ " is located in group " + str(group) + " and period " + str(period) + " of the periodic table."

    elif requestInfo['info'] == 'mass':
        mass = getInfo(0,"atomic_mass")
        rep = "The atomic/molar mass of " + element.capitalize() + " is %.2f" % mass + ' g/mol.'
    
    elif requestInfo['info'] == 'symbol':
        rep = "The symbol of " + element.capitalize() + " is "+ getInfo(0,"symbol") + "."

    elif requestInfo['info'] == "discovered_by":
        if 'unknown' in getInfo(0,"discovered_by"):
            rep = 'It is a mystery. The first person who discovered ' +  element.capitalize() + ' is unknown.'
        else:
            rep = element.capitalize() + ' was found by ' + getInfo(0,"discovered_by") + '.'
    elif requestInfo['info'].lower() in ['electron','electrons','protons','proton','number','numbers']:
        parameter = requestInfo['info'].lower() if requestInfo['info'].lower() not in ['number','numbers'] else 'atomic number'
        rep = element.capitalize() + ' has ' + str(getInfo(0,'number')) + ' '+ parameter + '.'
    else:
        rep = getInfo(0,'summary')
    
    return rep

# rep compare reactivity/eclectronegativity/nonmetal/metallic
def repReactive():
    global requestInfo 
    rep = ['Sorry, I cannot compare that. Elements have to be in the same category (metal or nonmetal).', 'It is impossible for me to compare the reactivity of metal and nonmetal elements', 'This is a difficult questrion. I cannot decide which is stronger']

    element_en = {}
    en_list = []

    en_list.append(getInfo(0,"electronegativity_pauling"))
    element_en[en_list[0]] = requestInfo['element'][0][1]
    metal = checkMetal(0)
    found = False
    for i in range(1,len(requestInfo['element'])):
        if checkMetal(i) != metal:
            found = True
            
        en_list.append(getInfo(i,"electronegativity_pauling"))
        element_en[en_list[-1]] = requestInfo['element'][i][1]
    if found and requestInfo['adj'] == 'reactive':
        return rep, ''

    en_list = sorted(en_list)
    reply = []
    i = requestInfo['compare']
    compare = 'more' if i == 0 else 'less'

    if (requestInfo['adj'] == 'reactive' and metal == 0) or requestInfo['adj'] == 'nonmetallic':
        i = 0 if i == -1 else -1

    reply.append('It definitely is ' + element_en[en_list[i]]+'. ')
    reply.append('I am totally sure with you that it is '+ element_en[en_list[i]]+'. ')
    reply.append('Definitely, '+ element_en[en_list[i]]+'. ' )
    rep = element_en[en_list[i]] + ' is ' + compare + ' ' + requestInfo['adj']+ ' than'

    for j in en_list:
        if element_en[j] != element_en[en_list[i]]:
            rep += ' ' + element_en[j] + ','
    reply.append(rep[:-1] + '.')
    reply.append(rep[:-1] + '.')

    return reply, element_en[en_list[i]]

#rep is/does 
def YesNo():
    global requestInfo
    rep = []
    #rep for electrons, protons, atomic numbers, molar mass
    if len(requestInfo['element']) == 1:
        if requestInfo['number'] != '':
            if requestInfo['info'].lower() in ['electron','electrons','protons','proton','number','numbers']:
                compare = getInfo(0,'number')
            elif requestInfo['info'] == 'mass':
                compare = getInfo(0,"atomic_mass")   
            
            if  int(requestInfo['number']) == int(compare+0.5):
                rep.append('Yea, you are right. ' + requestInfo['element'][0][1].capitalize() + ' has '+ str(int(compare+0.5)) + '.')
                rep.append('Yes, it is true. ' + requestInfo['element'][0][1].capitalize() + ' has '+ str(int(compare+0.5)) + '.')
            else:
                rep.append('No, ' + requestInfo['element'][0][1].capitalize() + ' has '+ str(compare) + ' not ' + str(requestInfo['number'])+ '.')
                rep.append('Nope, it is not correct. ' + requestInfo['element'][0][1].capitalize() + ' has '+ str(compare)+'.')

        elif requestInfo['info'] in ['nonmetal','metal']:
            compare = 'metal' if checkMetal(0) else 'nonmetal'

            if  requestInfo['info'] == compare:
                rep.append('Yea, you are right. '+requestInfo['element'][0][1].capitalize() + ' is ' + compare +'.')
                rep.append('Yes, it is true. ' + requestInfo['element'][0][1].capitalize() + ' is ' + compare + '.')
            else:
                rep.append('No, ' + requestInfo['element'][0][1].capitalize() + ' is ' + compare + ' not ' + requestInfo['info'] + '.')
                rep.append('Nope, it is not correct. ' + requestInfo['element'][0][1].capitalize() + ' is ' + compare +'.')


    #rep for symbols and reactive compare
    elif len(requestInfo['element']) == 2:
        if requestInfo['compare'] == -2 and requestInfo['info'] == 'symbol':
            num1 = getInfo(0,'number')
            num2 = getInfo(1,'number')
            if num1 == num2:
                rep.append('Yea, you are right. The symbol of ' + requestInfo['element'][0][1].capitalize() + ' is ' + requestInfo['element'][1][1].capitalize() + '.')
                rep.append('Yes, it is correct. The symbol of ' + requestInfo['element'][0][1].capitalize() + ' is ' + requestInfo['element'][1][1].capitalize() + '.')
            else:
                rep.append('No, the symbol of ' + requestInfo['element'][0][1].capitalize() + ' is ' + compare + ' not ' + requestInfo['info'] + '.')
                rep.append('Nope, it is not correct. The symbol of ' + requestInfo['element'][0][1].capitalize() + ' is ' + compare +'.')

        elif requestInfo['adj'].lower() in['reactive','metallic','nonmetallic']:
            _,temp = repReactive()
            compare = 'more ' if requestInfo['compare'] == 0 else 'less '
            if temp == requestInfo['element'][0][1]:
                rep.append('Yea, you are right. ' + requestInfo['element'][0][1].capitalize() + ' is ' + compare + requestInfo['adj'] + ' than ' + requestInfo['element'][1][1].capitalize() + '.')
                rep.append('Yes, you are right. ' + requestInfo['element'][0][1].capitalize() + ' is ' + compare + requestInfo['adj'] + ' than ' + requestInfo['element'][1][1].capitalize() + '.')
            else:
                rep.append('No, ' + requestInfo['element'][1][1].capitalize() + ' is ' + compare + requestInfo['adj'] + ' than ' + requestInfo['element'][0][1].capitalize() + '.')
                rep.append('Nope, it is not correct. ' + requestInfo['element'][1][1].capitalize() + ' is ' + compare + requestInfo['adj'] + ' than ' + requestInfo['element'][0][1].capitalize() + '.')
    else:
         rep = ['Sorry, I cannot answer this question.', 'I don\'t know how to answer this one. Please ask me another question!', 'Sorry, I don\'t know. Let skip this one.'] 

    return rep

#reply how many question
def repHowManyQuestion():
    global requestInfo
    number = -1
    answer =['Sorry, I cannot count that.', 'Oops, I cannot answer it']
    #handle count elements 
    if requestInfo['count'] in ['elements','element']:
        locate = requestInfo['locate']
        if len(locate) > 0:
            if locate[0] in ['group','column']: #count elements in group
                if locate[1].isnumeric():
                    if int(locate[1]) > 0 and int(locate[1]) < 19:
                        number = countElements(int(locate[1])-1, True)
                else:
                        number = countElements(locate[1],True)              
            elif locate[0] in ['period', 'row']: #count elements in row
                if locate[1].isnumeric():
                    if int(locate[1]) > 0 and int(locate[1]) < 8:
                        number = countElements(int(locate[1])-1, False)
            #generate response
            if number == -1:
                answer[0] = 'There is no '+ locate[0] + ' ' + locate[1] + ' in the periodic table.'
                answer[1] = 'Out of range.'
            else:
                answer[0] = 'There are '+ str(number) +' elements in '+ locate[0] + ' '+ locate[1]+'.'
                answer[1]=locate[0].capitalize() + ' ' + locate[1] +' has '+ str(number) +' elements.'
                answer[2] ='Definitely, '+str(number)+' elements.'               
        else: # count elements on the periodic tables
            answer[0]='There are 118 elements on the periodic table.'
            answer[1]= 'The periodic table has 118 elements.'
            answer[2]='Definitely, 118 elements.'
    # count columns/ rows on the periodic tables
    elif requestInfo['count'] in ['groups','columns','group','column']:
        answer[0]='There are 18 columns/groups on the periodic table.'
        answer[1]='The periodic table has 18 columns/groups.'
        answer[2]='Definitely, 18 columns/groups.'
        
    elif requestInfo['count'] in ['periods','rows','period','row']:
        answer[0]='There are 7 rows/periods on the periodic table.'
        answer[1]='The periodic table has 7 rows/periods.'
        answer[2]='Definitely, 7 rows/periods.'
    return answer

def resetInfo(): #resey requestInfo{}
    global requestInfo, errors, WQuestion, Unknown, YNQuestion, usePrevInfo
    requestInfo['element'] = []
    requestInfo['info'] =''
    requestInfo['count'] = ''
    requestInfo['locate'] = []
    requestInfo['number'] = ''
    requestInfo['adj'] = ''
    requestInfo['compare'] = -2
    requestInfo['table'] = False
    WQuestion = False
    YNQuestion = False
    Unknown = False
    usePrevInfo = False

def checkSymbol(word): #check if input is element name or sylbol
    return True if word == 'Symbol' else False

def getInfo(i, find = requestInfo['info']): #get information of element on periodic table
    element = requestInfo['element'][i][1].lower()
    isSymbol = checkSymbol(requestInfo['element'][i][0])
    info = getInformation(isSymbol,element,find)
    return info

def checkMetal(i): # check if element is metal or nonmetal
    return  0 if getInfo(i,'number') in nonmetal_element else 1

# A simple hard-coded proof of concept.
def main():
    global requestInfo,errors
    exit = False
    while True:
        rep = False
        user_input = input("User: ")
        for i in user_bye:
            if i.lower() in user_input.lower():
                print("Bot: " + farewells[randint(0,len(farewells)-1)] + farewells_2[randint(0,len(farewells_2)-1)]+" "+requestInfo['username']+'\n')
                exit = True
                break

        token_input = re.findall(r"[\w']+", user_input)
        for i in token_input:
            if 'no' == i.lower():
                print("Bot: " + farewells[randint(0,len(farewells)-1)] + farewells_2[randint(0,len(farewells_2)-1)]+" "+requestInfo['username']+'\n')
                exit = True
                break

        if exit:
            break

        for i in user_short_repsonse:
            if i.lower() in user_input.lower():
                print("Bot:",reply_thanks[randint(0,len(reply_thanks)-1)],end_2[randint(0,len(end_2)-1)]+'\n')
                rep = True
                break

        if 'yes' in user_input.lower() and not rep: #when user answer question from bot
            print("Bot: Ask me, I\'m here to help.\n")
            rep = True
        
        if not rep:
            T, P = CYKParse.CYKParse(token_input, GrammarRule.getGrammarPeriodic())
            sentenceTree = getSentenceParse(T)

            if sentenceTree == None:
                print('Bot:',errors[randint(0,len(errors) - 1)],'\n')
            else:
                updateRequestInfo(sentenceTree)
                reply()

main()
