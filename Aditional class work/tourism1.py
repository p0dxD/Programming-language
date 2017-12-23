import sys
import re
import itertools
import copy
from collections import OrderedDict
keywords = ["people", "locations","preferences","order"]

people = 0
locations = 0
preferences = 0
orders = {}

def nonblank_lines(f):
    for l in f:
        line = l.rstrip()
        line = l.lstrip()
        for key in keywords:
            if (re.match(key+r'\(\d+(, \d+)*\)\.',line)):
                parse_line(line, key)

def parse_line(op, key):
    global people
    global locations
    global preferences
    global orders

    values = re.findall('\d+', op)
    if key is keywords[0]:
        people = int(values.pop(0))
    elif key is keywords[1]:
        locations = int(values.pop(0))
    elif key is keywords[2]:
        preferences = int(values.pop(0))
    elif key is keywords[3]:
        if int(values[0]) in orders:
            orders.get(int(values.pop(0))).append(list(map(int, values)))
        else:
            orders.update({int(values.pop(0)):[list(map(int, values))]})
def getViolations(listOfPreferences, listToCheckWith):
    violations = 0
    for item in listToCheckWith:
        for i in range(len(listOfPreferences)):
            if item not in listOfPreferences[i]:
                continue
            for k in listOfPreferences[i][listOfPreferences[i].index(item)+1:]:
                if listToCheckWith.index(item) < listToCheckWith.index(k):
                    violations+=1
    return violations



def print_current_values():
    print ("people: ", people, "\nlocations:",locations
    ,"\npreferences:",preferences,"\norders:",orders)

def main():
    f = open(sys.argv[1], 'r')
    nonblank_lines(f)
    # print_current_values()
    preferencesList = []
    for key, value in orders.items():
        chainList = list(itertools.chain.from_iterable(value))
        removedDuplicateList = list(OrderedDict.fromkeys(chainList))
        preferencesList.append(removedDuplicateList)

    chainList = list(itertools.chain.from_iterable(preferencesList))
    minValue = min(chainList)
    maxValue = max(chainList)
 
    permutations = list(itertools.permutations(range(minValue, maxValue+1),maxValue))
    violations = getViolations(preferencesList,permutations[0])

    for permu in permutations:
        currentViolation = getViolations(preferencesList,permu)
        if  currentViolation < violations:
            violations = currentViolation
    print("violations("+str(violations)+").")
    f.close()

main()