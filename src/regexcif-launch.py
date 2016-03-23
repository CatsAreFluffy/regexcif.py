import re #dont kill me, just for preprocessing
with open("regexcif-src.py") as x,open("regexcif.py","w") as w:
    y=re.sub("( *)##restart(\n\1pass)?","""
\\1##restart
\\1if len(stack)==0: #no backtrack points
\\1    start+=1
\\1    if start>len(inp):
\\1        return []
\\1    if debug:print("next start")
\\1    inindex,tkindex=start,0
\\1else:
\\1    if debug:print("stack popped")
\\1    inindex,tkindex=stack.pop()
""".strip("\n"),"\n".join(x.read().split("\n")[1:]))
    #print(y) #print the code to stdout
    #w.write(y) #output the code to regexcif.py
    exec(y) #run the code
