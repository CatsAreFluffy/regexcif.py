def tokenize(reg,debug=False):
    '''Tokenizes reg'''
    tokens=[""]
    incharclass=False
    for i in reg: #tokenize input
        if debug:print("tokens",tokens[1:],incharclass)
        if incharclass: #character class
            if i=="]" and tokens[-1][-1]!="\\":
                incharclass=False
            else:
                tokens[-1]+=i
        elif i=="+": #repeat 1-inf
            tokens+=["+"]
        elif i=="[": #enter character class
            incharclass=True
            tokens+=["\\"]
        else: #character
            tokens+=["\\"+i]
    return tokens[1:]
def items(x,y):
    '''x is an iterable, y is a list of arguments to slicing'''
    if len(y)<3:
        return x[y[0]:y[1]]
    else:
        return x[y[0]:y[1]:y[2]]
def match(reg,inp,dotokenize=True,debug=False):
    '''reg is the regex,
inp is what you want to match,
tokenize controls tokenizing (provide a tokenized regex as reg instead)
returns [start,end] of match'''
    if dotokenize:
        tokens=tokenize(reg)
    else:
        tokens=reg
    tkindex=0 #position in token list
    inindex=0 #position in input
    start=0 #start of match
    stack=[] #store backtracking points format=[inindex,tkindex]
    while tkindex<len(tokens): #stay in the regex
        if debug:print("stack",stack,start,"regex",tkindex,tokens[tkindex],"text",inindex,inp[inindex] if inindex<len(inp) else "out of text")
        if tokens[tkindex][0]=="\\": #character/char class
            if inindex==len(inp): #fell out of the text
                ##restart
                if len(stack)==0: #no backtrack points
                    start+=1
                    if start>len(inp):
                        return []
                    if debug:print("next start")
                    inindex,tkindex=start,0
                else:
                    if debug:print("stack popped")
                    inindex,tkindex=stack.pop()
                pass
            else: #still in the text
                if inp[inindex] in tokens[tkindex][1:]:
                    tkindex+=1
                    inindex+=1
                else:
                    ##restart
                    if len(stack)==0: #no backtrack points
                        start+=1
                        if start>len(inp):
                            return []
                        if debug:print("next start")
                        inindex,tkindex=start,0
                    else:
                        if debug:print("stack popped")
                        inindex,tkindex=stack.pop()
                    pass
        elif tokens[tkindex ]=="+":
            if tokens[tkindex-1]!=")": #no group behind (groups not implemented yet, so always the case)
                stack+=[[inindex,tkindex+1]]
                tkindex-=1
    return [start,inindex]
#examples
#print(match("d+c+","abcddbddcc",True,True))
#print(items("abcddbddcc",match("d+c+","abcddbddcc")))
