import copy
from collections import deque 
import sys
import re
keywords = ["room", "booths","dimension","target","position",
"horizon"]
#size
maxMoves = 0
numberOfBooths = 0
positions = {}
target = {}
dimensions = {}
roomSize = []

def nonblank_lines(f):
    for l in f:
        line = l.rstrip()
        line = l.lstrip()
        for key in keywords:
            if (re.match(key+r'\(\d+(, \d+)*\)\.',line)):
                parse_line(line, key)

def parse_line(op, key):
    global maxMoves
    global numberOfBooths
    global positions
    global roomSize
    global target
    global dimensions

    values = re.findall('\d+', op)
    if key is keywords[0]:
        roomSize = values
    elif key is keywords[1]:
        numberOfBooths = values.pop()
    elif key is keywords[2]:
        dimensions.update({values.pop(0):tuple(values)})
    elif key is keywords[3]:
        target.update({values.pop(0):tuple(values)})
    elif key is keywords[4]:
        positions.update({values.pop(0):tuple(values)})
    elif key is keywords[5]:
        maxMoves = values.pop()

def bfs(initialObjects,dimensions,roomSize,maxSteps,startingMatrix,answerMatrix):
	initialSteps = 0
	alreadyExplored = []
	queue = deque([(startingMatrix,initialObjects,initialSteps)]) #create queue 
	while len(queue)>0: #make sure there are nodes to check left
		node = queue.popleft() #grab the first node
		currentMatrix = node[0]
		plainObjects = node[1]
		# print("plainObjects: ", node)
		numberOfSteps = node[2]
		# print("trying:",currentMatrix,"\nSteps: ",numberOfSteps)
		#we already saw this one
		if currentMatrix in alreadyExplored:
			continue
		#check if its the answer
		if are_equal(currentMatrix,answerMatrix):
			return "moves("+str(numberOfSteps)+")."
		if maxSteps < numberOfSteps:
			return "more than "+str(maxSteps) +" steps required, quitting"
		#add it to already explored
		alreadyExplored.append(currentMatrix)
		#if not an answer we generate all posible moves from this graph
		for key, value in plainObjects.items():
			moveUp = move_up(roomSize,key,value,plainObjects,dimensions,currentMatrix,numberOfSteps)
			moveDown = move_down(roomSize,key,value,plainObjects,dimensions,currentMatrix,numberOfSteps)
			moveRight = move_right(roomSize,key,value,plainObjects,dimensions,currentMatrix,numberOfSteps)
			moveLeft = move_left(roomSize,key,value,plainObjects,dimensions,currentMatrix,numberOfSteps)

			if moveUp:
				queue.append(moveUp)
			if moveDown:
				queue.append(moveDown)
			if moveRight:
				queue.append(moveRight)
			if moveLeft:
				queue.append(moveLeft)
	print("No answer found")


	'''The initial objects should contain a matrix, dimensions'''
def move_up(roomSize,key,objectA,objects,dimensions,matrix,steps):
	'''If a matrix is found it will return the updated information 
	like input else it will return an empty list'''
	temp1 = int(objectA[1])+1
	# print("in up key:",key)
	#new tuple
	# print("before",objectA)
	# objectA = {key: (objectA[0],str(temp1))}
	tempObjects = copy.deepcopy(objects)
	tempCopy = {key: (objectA[0],str(temp1))}
	tempObjects.update(tempCopy)
	# print("after",objectA)
	if temp1 >= int(roomSize[1]):
		# print("out of bounds")
		return []
	newMatrix = create_matrix_with_new_point(roomSize, matrix, dimensions, tempCopy)
	# print("NEW MATRIX UP: ", newMatrix)
	#if the matrix is empty this means sometihng went wrong, return empty
	if newMatrix:
		# print("Can move up")
		return [newMatrix,tempObjects,steps+1]
	else:
		# print("TEST")
		return []

def move_down(roomSize,key,objectA,objects,dimensions,matrix,steps):
	'''If a matrix is found it will return the updated information 
	like input else it will return an empty list'''
	temp1 = int(objectA[1])-1
	# print("in down key:",key)
	#new tuple
	# print("before",objectA)
	tempObjects = copy.deepcopy(objects)
	tempCopy = {key: (objectA[0],str(temp1))}
	tempObjects.update(tempCopy)
	# print("after",objectA)
	if temp1 < 0:
		return []
	newMatrix = create_matrix_with_new_point(roomSize, matrix, dimensions, tempCopy)
	#if the matrix is empty this means sometihng went wrong, return empty
	if newMatrix:
		# print("Can move down")
		return [newMatrix,tempObjects,steps+1]
	else:
		return []

def move_left(roomSize,key,objectA,objects,dimensions,matrix,steps):
	'''If a matrix is found it will return the updated information 
	like input else it will return an empty list'''
	temp1 = int(objectA[0])-1
	# print("in left key:",key)
	#new tuple
	# print("before",objectA)
	tempObjects = copy.deepcopy(objects)
	tempCopy = {key: (str(temp1),objectA[1])}
	tempObjects.update(tempCopy)
	# print("after",objectA)
	if temp1 < 0:
		return []
	newMatrix = create_matrix_with_new_point(roomSize, matrix, dimensions, tempCopy)
	#if the matrix is empty this means sometihng went wrong, return empty
	if newMatrix:
		# print("Can move left")
		return [newMatrix,tempObjects,steps+1]
	else:
		return []

def move_right(roomSize,key,objectA,objects,dimensions,matrix,steps):
	'''If a matrix is found it will return the updated information 
	like input else it will return an empty list'''
	temp1 = int(objectA[0])+1
	# print("in right key:",key)
	#new tuple
	# print("before",objectA)
	tempObjects = copy.deepcopy(objects)
	tempCopy = {key: (str(temp1),objectA[1])}
	tempObjects.update(tempCopy)
	# print("after",objectA)
	if temp1 >= int(roomSize[0]):
		return []
	newMatrix = create_matrix_with_new_point(roomSize, matrix, dimensions, tempCopy)
	#if the matrix is empty this means sometihng went wrong, return empty
	if newMatrix:
		# print("Can move right")
		return [newMatrix,tempObjects,steps+1]
	else:
		return []	

def are_equal(matrixOne, matrixTwo):
	return matrixOne == matrixTwo

def print_matrix(matrix):
	for line in matrix:
		print(*line)

def create_matrix_with_new_point(roomSize,createdMatrix, dimensions,target):
	keyTarget, valueTarget = target.popitem()
	createdMatrix = [[subelt.replace(keyTarget,'0') for subelt in individualList] for individualList in createdMatrix]
	for key, value in dimensions.items():
		if key is keyTarget:
			for i in range(int(dimensions.get(key)[0])):
				if (int(valueTarget[0])+i) >= int(roomSize[0]) or (int(valueTarget[0])+i) < 0:
					return []
				for j in range(int(dimensions.get(key)[1])):
					if (int(valueTarget[1])+j) >= int(roomSize[1]) or (int(valueTarget[1])+i) < 0 or createdMatrix[int(valueTarget[0])+i][int(valueTarget[1])+j] != '0':
						return []
					createdMatrix[int(valueTarget[0])+i][int(valueTarget[1])+j] = key		
	return createdMatrix


def create_matrix(width, height,objects,dimensions):
	matrix = []
	row = []
	for i in range(height):
		for j in range(width):
			row.append('0')
		matrix.append(row)
		row = []
	for key, value in objects.items():
		for i in range(int(dimensions.get(key)[0])):
			for j in range(int(dimensions.get(key)[1])):
				matrix[int(value[0])+i][int(value[1])+j] = key	
	return matrix


def print_current_values():
    print ("maxMoves: ", maxMoves, "\nnumberOfBooths:",numberOfBooths
    ,"\npositions:",positions,"\ntarget:",target,"\ndimensions:",dimensions
    ,"\nroomSize:",roomSize)

def main():
	f = open(sys.argv[1], 'r')
	nonblank_lines(f)

	matrix = create_matrix(int(roomSize[0]),int(roomSize[0]),positions,dimensions)
	answerMatrix = create_matrix_with_new_point(roomSize, matrix, dimensions,target)
	print(bfs(positions,dimensions,roomSize,int(maxMoves),matrix,answerMatrix))

	f.close()


main()