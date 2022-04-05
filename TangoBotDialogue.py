#TangoBots Dialogue Project

class Rule:

def main():
    #reads file
    file = open('C:/Users/colli/Downloads/Dialogue.txt', 'r')
    topics = []
    for line in file:
        #Gets rid of tabbed white space and new lines
        line = line.replace("\t", "")
        line = line.replace("\n", "")
        #ignores comments
        if(line[0] != '#'):
            line = line.split(":")
            if(line[0][0] == '~'):
                topics.append(line)
            else:
                print(line[0][0])
    file.close()

main()
