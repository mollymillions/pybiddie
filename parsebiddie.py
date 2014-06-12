'''
pybiddie parser

logical keywords:
false - lol no
true - the best
&& - needs
|| - like whatever
== - is literally
!= - just can't
> - like crazy
< - basic
>= - kind of like crazy
<= - kind of basic
if - literally
else if - or like
else - so like
end if - right?
while - basically
end while - you know?

arithmetic keywords:
+ - and then
- - but not
* - totally wants
/ - totally has
% - like leftover

method keywords:
declare method - do you know (name)
arguments - listen
return - can you just
end method - so yeah
call method - is that (name)
print - was like
assignment - is so
'''
import re
import sys

reservedKeywords = ["lol","no","the","best","needs","like","whatever","is","literally","just","can't","crazy","basic","kind","of","or","so","right?","basically","you","know?","and","then","but","not","totally","wants","has","leftover","do","know","listen","can","just","yeah","that","was"]

def parseNumber(tokens):
    if "." in tokens[0]:
        splittok = re.split(r"(.)",tokens[0])
        splittok = [t for t in splittok if not t.isspace() and not t=="" and not t=="."]
        if re.compile(r"(0|[1-9][0-9]*)").match(splittok[0]) and re.compile(r"(0|[1-9][0-9]*)").match(splittok[1]):
            return ({"Decimal": [float(tokens[0])]}, tokens[1:])
    elif re.compile(r"(0|[1-9][0-9]*)").match(tokens[0]):
        return ({"Integer": [int(tokens[0])]}, tokens[1:])
    else:
        sys.exit("ewww: invalid number format")

def parseVariable(tokens):
    if re.compile(r"[a-z][A-Za-z]*").match(tokens[0]):
        if tokens[0] in reservedKeywords:
            sys.exit("ewww: invalid variable name; reserved keyword")
        else:
            return ({"Variable": [tokens[0]]}, tokens[1:])

def parsePrint(tokens, printtok):
    #First piece of string - remove beginning "
    if tokens[0][0] == '"':
        tokens[0] = tokens[0][1:]
        #Check to see if it's a single word string
        if tokens[0][len(tokens[0])-1] != '"':
            printtok+=tokens[0]
            printtok+=" "
        else:
            tokens[0] = tokens[0][0:len(tokens[0])-1]
            printtok+=tokens[0]
            return ({"String":[printtok]}, tokens[1:])
    i=1
    while tokens[i][len(tokens[i])-1] != '"':
        if tokens[i][0] == '"':
            sys.exit("ewww: malformed print string; escape quotation marks")
        printtok+=tokens[i]
        printtok+=" "
        i+=1
        if len(tokens[i:]) < 1:
            sys.exit("ewww: malformed print string; forgot closing quotation marks?")
    #Last piece of string - remove trailing " and return printstring
    if tokens[i][0] == '"':
        sys.exit("ewww: malformed print string; escape quotation marks")
    tokens[i] = tokens[i][0:len(tokens[i])-1]
    printtok+= tokens[i]
    return ({"String":[printtok]}, tokens[i+1:])


def parseFormula(tmp, top=True):
    tokens = tmp[0:]
    r = leftFormula(tokens, False)

def parseTerm(tmp, top=True):
    tokens = tmp[0:]
    r = leftTerm(tokens, False)
    if not r is None:
        (e1, tokens) = r
        if len(tokens) > 0:
            if tokens[0] == "and" and tokens[1] == "then":
                r = parseTerm(tokens[2:], False)
                if not r is None:
                    (e2, tokens) = r
                    return ({"Plus":[e1,e2]}, tokens)
            elif tokens[0] == "but" and tokens[1] == "not":
                r = parseTerm(tokens[2:], False)
                if not r is None:
                    (e2, tokens) = r
                    return ({"Minus":[e1,e2]}, tokens)
            elif tokens[0] == "totally" and tokens[1] == "wants":
                r = parseTerm(tokens[2:], False)
                if not r is None:
                    (e2, tokens) = r
                    return ({"Times":[e1,e2]}, tokens)
            elif tokens[0] == "totally" and tokens[1] == "has":
                r = parseTerm(tokens[2:], False)
                if not r is None:
                    (e2, tokens) = r
                    return ({"Divide":[e1,e2]}, tokens)
            elif tokens[0] == "like" and tokens[1] == "leftover":
                r = parseTerm(tokens[2:], False)
                if not r is None:
                    (e2,tokens) = r
                    return ({"Mod":[e1,e2]}, tokens)
            else:
                return (e1, tokens)
        else:
            return (e1, tokens)
    else:
        sys.exit("ewww: invalid term/formula")

def leftTerm(tmp, top=True):
    tokens = tmp[0:]
    r = parseVariable(tokens)
    if not r is None:
        return r
    tokens = tmp[0:]
    r = parseNumber(tokens)
    if not r is None:
        return r

def parseFormula(tmp, top=True):
    tokens = tmp[0:]
    r = leftFormula(tokens, False)
    if not r is None:
        (e1, tokens) = r
        if len(tokens) > 0:
            if tokens[0] == "needs":
                r = parseFormula(tokens[1:], False)
                if not r is None: 
                    (e2, tokens) = r
                    return ({"And":[e1,e2]}, tokens)
            elif tokens[0] == "like" and tokens[1] == "whatever":
                r = parseFormula(tokens[2:], False)
                if not r is None:
                    (e2, tokens) = r
                    return ({"Or":[e1,e2]}, tokens)
            elif tokens[0] == "is" and tokens[1] == "literally":
                r = parseFormula(tokens[2:], False)
                if not r is None:
                    (e2, tokens) = r
                    return ({"Equals":[e1,e2]}, tokens)
            elif tokens[0] == "could" and tokens[1] == "you" and tokens[2] == "not":
                r = parseFormula(tokens[3:], False)
                if not r is None:
                    (e2, tokens) = r
                    return ({"Not Equals":[e1,e2]}, tokens)
            elif tokens[0] == "kind" and tokens[1] == "of":
                if tokens[2] == "like" and tokens[3] == "crazy":
                    r = parseFormula(tokens[4:], False)
                    if not r is None:
                        (e2, tokens) = r
                        return ({"GTE":[e1,e2]}, tokens)
                if tokens[2] == "basic":
                    r = parseFormula(tokens[3:])
                    if not r is None:
                        (e2, tokens) = r
                        return ({"LTE":[e1,e2]})
            elif tokens[0] == "basic":
                r = parseFormula(tokens[1:])
                if not r is None:
                    (e2, tokens) = r
                    return ({"Less Than":[e1,e2]}, tokens)
            elif tokens[0] == "like" and tokens[1] == "crazy":
                r = parseFormula(tokens[1:])
                if not r is None:
                    (e2, tokens) = r
                    return ({"Greater Than":[e1,e2]}, tokens)
            else: 
                return (e1, tokens)
        else:
            return (e1, tokens)
    else:
        r = parseTerm(tokens)
        if not r is None:
            return r

def leftFormula(tmp, top = True):
    tokens = tmp[0:]
    if tokens[0] == "lol" and tokens[1] == "no":
        return ("False", tokens[2:])
    elif tokens[0] == "the" and tokens[1] == "best":
        return ("True", tokens[2:])
    elif tokens[0] == "just" and tokens[1] == "can't":
        (st, rest) = parseFormula(tokens[2:])
        return ({"Not":[st]}, rest)

def parseProgram(tokens, top=True):
    if len(tokens) == 0 or tokens == []:
        return ("End", [])
    #Print statement
    if (len(tokens) < 2) and tokens[0] != "right?":
        sys.exit("ewww: invalid input program")
    if tokens[0] == "was" and tokens[1] == "like":
        printtok = tokens[2:]
        if printtok == []:
            sys.exit("ewww: invalid print string length")
        if printtok[0][0] == '"':
            (printstr,rest) = parsePrint(printtok,"")
        else:
            r = parseFormula(printtok)
            if not r is None:
                (printstr, rest) = r
            else:
                r = parseTerm(printtok)
                if not r is None:
                    (printstr, rest) = r
                else:
                    sys.exit("ewww: invalid print string")
        return ({"Print": [printstr,parseProgram(rest)]})
    #While loop
    if tokens[0] == "basically":
        (cond,body) = parseFormula(tokens[1:])
        (action,rest) = parseProgram(body[1:])
        return ({"While":[cond, action, rest]})
    #If loop
    if tokens[0] == "literally":
        (cond,body) = parseFormula(tokens[1:])
        (action,rest) = parseProgram(body[1:])
        return ({"If":[cond,action,rest]})
    #End of while loop
    if tokens[0] == "you" and tokens[1] == "know?":
        return parseProgram(tokens[2:])
    #Else if loop
    if tokens[0] == "or" and tokens[1] == "like":
        (cond,body) = parseFormula(tokens[2:])
        (action,rest) = parseProgram(body[1:])
        return ({"Else If":[cond,action,rest]})
    #Else loop
    if tokens[0] == "so" and tokens[1] == "like":
        (action,rest) = parseProgram(tokens[2:])
        return ({"Else":[action,rest]})
    #End of if loop
    if tokens[0] == "right?":
        return parseProgram(tokens[1:])
    #Declaring a function
    if tokens[0] == "do" and tokens[1] == "you" and tokens[2] == "know":
        fname = tokens[3]
        args = []
        i = 5
        if tokens[4] == "listen":
            while tokens[i] != "...":
                args += tokens[i]
                i += 1
            i+=1
        (ftoks,rest) = getBody(tokens[i:])
        fbody = parseProgram(ftoks)
        return ({"Function":[fname,args,fbody,parseProgram(rest)]})
    #Returning from a function
    if tokens[0] == "can" and tokens[1] == "you" and tokens[2] == "just":
        (toreturn,rest) = parseFormula(tokens[3:])
        return ({"Return":[toreturn,parseProgram(rest)]})
    #Breaking in a function
    if tokens[0] == "get" and tokens[1] == "out":
        return ("Break", parseProgram(tokens[2:]))
    #Calling a function
    if tokens[0] == "is" and tokens[1] == "that":
        fname = tokens[2]
        return ({"Call":[fname,parseProgram(tokens[3:])]})
    #Assignment
    v = parseVariable(tokens)
    if not v is None:
        (varname, seq) = v
        if seq[0] == "is" and seq[1] == "so":
            r = parseTerm(seq[2:])
            if not r is None:
                (formula, rest) = r
            else:
                r = parseFormula(seq[2:])
                if not r is None:
                    (formula, rest) = r
            return ({"Assign":[varname,formula,parseProgram(rest)]})
        else:
            sys.exit("ewww: not a valid program")
def getBody(tokens):
    i=0
    while tokens[i] != "so" and tokens[i+1] != "yeah":
        i+=1
    return (tokens[0:i],tokens[i+2:])

def tokenizeAndParse(s):
    tokens = re.split(r"(\s|;|{|})",s)
    tokens = [t for t in tokens if not t.isspace() and not t=="" and not t==";"]
    #(programbody, endtok) = parseProgram(tokens)
    return parseProgram(tokens)

#print(tokenizeAndParse("x is so 5.5 was like 5"))
#print(tokenizeAndParse("literally x so was like 5 or like z so was like 6 so like was like 7 right? was like 10"))
#print(tokenizeAndParse("do you know f1 listen a b c ... was like a was like b was like c can you just 0 so yeah was like 0 was like 1 is that f1"))
#print(tokenizeAndParse('was like "hi its me was like "5"'))

#eof
