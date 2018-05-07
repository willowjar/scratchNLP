from nltk import Nonterminal, nonterminals, Production, CFG
from nltk.parse import RecursiveDescentParser
file_object  = open("Grammar.gr", 'r')
grammar_string = ""
for line in file_object: 
    #avoid empty lines
    if len(line)>1:
        found = line.find("#")
        if found==-1:
            grammar_string = grammar_string+line+"\n"
        else:
            #contains a comment
            if not(found==0):
                #assuming if a line is commented, the comment is in begining
                raise Exception("partially commented grammar rule!")
file_object.close()
# get rid of last "\n"
grammar_string = grammar_string[0:len(grammar_string)-1]
grammar = CFG.fromstring(grammar_string)
print("grammar CFG",grammar)
sentence1 = 'the cat chased the dog'.split()
rd = RecursiveDescentParser(grammar)
for t in rd.parse(sentence1):
    print(t)









# grammar_text = file_object.readlines()
# first_line = file_object.readline(3)
# print("first_line",first_line)
# print("file_object",file_object)
# print("grammar_text",grammar_text)