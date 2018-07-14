#############################
## by Hannah Kleidermacher ##
##       13 July 2018      ##
#############################
def findName(fn, uid):
    # PASS FILE NAME STR; UID INT
    # RETURNS UID'S CORRESPONDING NAME, IF EXISTS
    file = open(fn, 'r')
    lines = file.readlines()

    uidFound = False
    currentName = ''
    currentUID = 1

    for line in lines:
        if 'Package [' in line:
            currentName = line[line.find('[')+1:line.find(']')]
        elif 'userId=' in line:
            currentUID = int(line[line.find('=')+1:line.find('\n')])
        elif 'sharedUser=' in line:
            currentName = line[line.find('{')+9:line.find('/')]
        elif currentUID == uid:
            return currentName
    return 'no name'
