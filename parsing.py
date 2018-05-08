from nltk import Nonterminal, nonterminals, Production, CFG
from nltk.parse import RecursiveDescentParser, ShiftReduceParser, BottomUpChartParser, TopDownChartParser
def load_file_as_string(filename,mode):
    file_object  = open(filename, mode)
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
    return grammar_string

grammar_string = load_file_as_string("Grammar.gr",'r')
vocab_string = load_file_as_string("new_vocab_file.txt",'r')
grammar = CFG.fromstring(grammar_string+"\n"+vocab_string)
sentence1 = 'set y to 4 times 6'.split()
rd = TopDownChartParser(grammar)
for t in rd.parse(sentence1):
    print("t",t)









# grammar_text = file_object.readlines()
# first_line = file_object.readline(3)
# print("first_line",first_line)
# print("file_object",file_object)
# print("grammar_text",grammar_text)