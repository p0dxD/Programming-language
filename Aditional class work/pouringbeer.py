import copy
from collections import deque 
import sys
import re

keywords = ["vessels", "source","people","capacity","horizon"]
#size
vessels = 0
source = 0
people = 0
capacity = {}
horizon = 0

def bfs(initialArray,capacities,initial_steps,people,splitAmount,horizon):
    alreadyExplored = []
    queue = deque([(initialArray,initial_steps)]) #create queue 
    while len(queue)>0: #make sure there are nodes to check left
        node = queue.popleft() #grab the first node
        currentConfiguration = node[0]
        steps = node[1]
        # print("trying:",currentMatrix,"\nSteps: ",numberOfSteps)
        #we already saw this one
        if currentConfiguration in alreadyExplored:
            continue
        #check if its the answer
        if is_correct(currentConfiguration,splitAmount,people):
            return "split(yes)."
        if horizon < steps:
            return ("split(no).")
        # #add it to already explored
        alreadyExplored.append(currentConfiguration)

        #if not an answer we generate all posible moves from this graph
        index = 0
        options = []
        for i in currentConfiguration:
            #add to queue here check if already in checked before adding to queue
            for j in range(len(currentConfiguration)):
                currentState = getState(currentConfiguration,index, j, capacities)
                options.append(currentState)
        #         print(currentState)
            index+=1
        #     print("i:\n",i)
        #remove duplicates
        b_set = set(map(tuple,options))  #need to convert the inner lists to tuples so they are hashable
        b = map(list,b_set) #Now convert tuples back into lists 
        # print(list(b))

        for lst in b:
            #put in queue
            queue.append([lst,steps+1])
    return ("split(no).")



def getState(arrayCurrentState ,currentVessel, toVessel, capacities):
    # print("inside get states")
    arr = arrayCurrentState[:]
    toVesselMaxCapacity = capacities.get(toVessel+1)
    # print("ARRAY: ",toVessel," current ", currentVessel)
    toVesselCurrentCapacity = arr[toVessel]
    currentVesselCurrentCapacity = arr[currentVessel]
    # print(arr[currentVessel])
    # print(arr[toVessel], "capacity: ", toVesselMaxCapacity, "toVesselCurrentCapacity:",toVesselCurrentCapacity)
    if(toVesselMaxCapacity-toVesselCurrentCapacity)>=0 and (currentVessel != toVessel):
        needed = toVesselMaxCapacity-toVesselCurrentCapacity
        if(currentVesselCurrentCapacity-needed) >= 0:
            # print("Left: ",currentVesselCurrentCapacity-needed)
            tranfer = currentVesselCurrentCapacity-needed
            #update the array with new value
            arr[currentVessel] = tranfer
            arr[toVessel] = arr[toVessel] + needed
            # print("new array: ", arr)
        elif(needed > currentVesselCurrentCapacity):
            # print("test")
            arr[toVessel] = arr[toVessel] + currentVesselCurrentCapacity
            arr[currentVessel] = 0
            # print("new array: ", arr)
        # print("needed: ", needed)
    return arr

def create_initial_state(source, capacities):
    size = len(capacities)
    # print("source key:, ",source) 
    arr = []
    for key, value in capacities.items():
        if key == source:
            arr.append(value)
        else:
            arr.append(0)
    # print(arr)
    return arr

def is_correct(arr, partition, numberPeople):
    total = 0
    peopleCounter = 0
    for i in arr:
        if(total+i) < partition:
            total+=i
        elif (total+i) == partition:
            peopleCounter+=1
            total=0
        if peopleCounter > numberPeople:
            break
    return (peopleCounter == numberPeople)

def nonblank_lines(f):
    for l in f:
        line = l.rstrip()
        line = l.lstrip()
        for key in keywords:
            if (re.match(key+r'\(\d+(, \d+)*\)\.',line)):
                parse_line(line, key)

def parse_line(op, key):
    global vessels
    global source
    global people
    global capacity
    global horizon

    values = re.findall('\d+', op)
    if key is keywords[0]:
        vessels = int(values.pop())
    elif key is keywords[1]:
        source = int(values.pop())
    elif key is keywords[2]:
        people = int(values.pop())
    elif key is keywords[3]:
        capacity.update({int(values.pop(0)):int(values.pop(0))})
    elif key is keywords[4]:
        horizon = int(values.pop())

def print_current_values():
    print ("vessels: ", vessels, "\nsource:",source
    ,"\npeople:",people,"\ncapacity:",capacity,"\nhorizon:",horizon)

def main():
    f = open(sys.argv[1], 'r')
    nonblank_lines(f)
    initial_array = create_initial_state(source,capacity)
    print(bfs(initial_array,capacity,0,people,(capacity.get(source)/people),horizon))

    f.close()


main()