import sys
import re
import itertools
import copy
from collections import OrderedDict
keywords = ["people", "locations","preferences","location","prefer"]

people = 0
locations = 0
preferences = 0
location = {}
prefer = {}

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
    global location
    global prefer

    values = re.findall('\d+', op)
    if key is keywords[0]:
        people = int(values.pop(0))
    elif key is keywords[1]:
        preferences = int(values.pop(0))
    elif key is keywords[2]:
        preferences = int(values.pop(0))
    elif key is keywords[3]:
        if int(values[0]) in location:
            location.get(int(values.pop(0))).extend(list(map(int, values)))
        else:
            location.update({int(values.pop(0)):list(map(int, values))})
    elif key is keywords[4]:
        if int(values[0]) in prefer:
            prefer.get(int(values.pop(0))).extend(list(map(int, values)))
        else:
            prefer.update({int(values.pop(0)):list(map(int, values))})

def print_current_values():
    print ("people: ", people, "\nlocations:",locations
    ,"\npreferences:",preferences,"\nlocation:",location,"\nprefer",prefer)

def min_max_for_time(location):
    times = []
    for key, value in location.items():
        times.extend(value[1:])
    return [min(times),max(times)]

def get_satisfaction(prefer, location, permutation, current_time):
    least_satisfied = 123123123
    permutationSize = len(permutation)
    # print("permutation:",permutation)
    #get the locations we can go to
    for perm in permutation[:]:
        tempLoc = location.get(perm)
        if check_if_it_is_within_time_frame(perm,tempLoc, current_time):
            permutation.remove(perm)
    #we have our locations now we can see the satisfaction of each person
    valuesSatisfaction = []
    sumValues = 0
    for key, value in prefer.items():
        temp = get_satisfaction_of_person(value[:], permutation[:], permutationSize)
        valuesSatisfaction.append(temp)
        sumValues +=temp
        if least_satisfied > temp:
            least_satisfied = temp
    # print(valuesSatisfaction)
    # print("LEAST SATISFIED",least_satisfied, "Sum:",sumValues)
    return [least_satisfied,sumValues,valuesSatisfaction]

def get_satisfaction_of_person(personPlaces, locationsThatWereSelected,permutationSize):
    satisfaction = 0
    # print("Location selected:",locationsThatWereSelected)
    for loc in personPlaces[:]:
        # print("locations",loc)
        if loc in locationsThatWereSelected:
            # print("YES",satisfaction)
            personPlaces.remove(loc)
            satisfaction+=1
    # print(personPlaces)
    if personPlaces:
        # print("has something satisfaction",satisfaction)
        return satisfaction
    else:
        # print("has all",permutationSize)
        return permutationSize

def check_if_it_is_within_time_frame(perm,tempLoc, current_time):
    # print("perm",perm,"temp: ",tempLoc,"current_time:" ,current_time)
    current_hour = current_time[0]
    eventStartTime = tempLoc[1]
    if current_hour < eventStartTime:
        current_hour = eventStartTime
        current_time[0] = eventStartTime
    #we dont have time for anything else, remove it from list
    if current_time[0] == current_time[1]:
        # print("this")
        return True
    time_within_timeframe = (tempLoc[2] - current_hour)
    # print("time_within_timeframe",time_within_timeframe)
    if time_within_timeframe >= 0:
        time_it_takes = tempLoc[0]
        if (time_within_timeframe - time_it_takes) >=0:
            # print("it fits updating time",time_it_takes,current_time)
            current_time[0] = current_time[0] + time_it_takes
            return False
    return True




def main():
    f = open(sys.argv[1], 'r')
    nonblank_lines(f)
    # print_current_values()

    listOfPlaces = []
    for key, value in prefer.items():
        listOfPlaces.extend(value)

    minValue = min(listOfPlaces)
    maxValue = max(listOfPlaces)


    permutations = list(itertools.permutations(range(minValue, maxValue+1),maxValue))

    #obtain min and max for time
    times = min_max_for_time(location)

    # get_satisfaction(prefer, place, list(permutations[0]), times)
    bestSatisfaction = [0,0,[0,0]]
    least_satisfied = maxValue
    for perm in permutations:
        temp = get_satisfaction(prefer, location, list(perm) , times[:])
        # print(temp)
        if temp[0] > bestSatisfaction[0]:
            # print("least HERE", bestSatisfaction,least_satisfied)
            bestSatisfaction = temp
            least_satisfied = temp
        
    # print(bestSatisfaction)
    print("satisfaction("+str(bestSatisfaction[0])+").")
    f.close()

main()