'''
pybiddie interpreter
takes in a string in the form of a python dictionary, executes it, and returns the given result

'''
import sys

exec(open("parsebiddie.py").read())

def evalExp(env, inst):
    if type(inst) == dict:
        for label in inst:
            children = inst[label]
            if label == "Decimal":
                return (env, inst[label][0])
            if label == "Integer":
                return (env, inst[label][0])
            if label == "Variable":
                return (env, evalExp(env, env[inst[label][0]])[1])
            if label == "String":
                return (env, inst[label][0])
            if label == "Not":
                return (env,not evalExp(env, inst[label][0])[1])
            else:
                v1 = evalExp(env, inst[label][0])[1]
                v2 = evalExp(env, inst[label][1])[1]
                if label == "Plus":
                    return (env, v1+v2)
                if label == "Minus":
                    return (env, v1-v2)
                if label == "Times":
                    return (env, v1*v2)
                if label == "Divide":
                    return (env, v1/v2)
                if label == "Mod":
                    return (env, v1%v2)
                if label == "Equals":
                    return (env, v1 == v2)
                if label == "Not Equals":
                    return (env, v1 != v2)
                if label == "GTE":
                    return (env, v1 >= v2)
                if label == "LTE":
                    return (env, v1 <= v2)
                if label == "Greater Than":
                    return (env, v1 > v2)
                if label == "Less Than":
                    return (env, v1 < v2)
                if label == "And":
                    if v1 == False:
                        return (env, False)
                    elif v2 == False:
                        return (env, False)
                    else:
                        return (env, True)
                if label == "Or":
                    if v1 == True or v2 == True:
                        return (env, True)
                    else:
                        return (env, False)
    else:
        if inst == "True":
            return (env, True)
        if inst == "False":
            return (env, False)
            

def execProgram(env, inst):
    if type(inst) == dict:
        for label in inst:
            children = inst[label]
                #Assignment program
            if label == "Assign":
                #Check that you are trying to assign to a variable
                if not children[0]["Variable"] is None:
                    varname = children[0]["Variable"][0]
                else:
                    sys.exit("aaah: invalid assignment variable name")
                #Store the subprogram in the environment - it will be evaluated upon calling the variable for the first time
                env[varname] = children[1]
                return execProgram(env, children[2])
            #Print program
            if label == "Print":
                print(evalExp(env, children[0])[1])
                return execProgram(env, children[1])
    else:
        if inst[0] == "End":
            return (env, [])


def interpret(s):
    (env, p) = execProgram({}, tokenizeAndParse(s))

#print(interpret('x is so 5.5 was like x was like "hi"'))
#print(interpret("was like just can't just can't the best"))
print(interpret("was like 6 is literally 5"))
