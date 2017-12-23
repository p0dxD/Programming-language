import sys
import re
keywords = ["dishes", "hot","separation","table_width","dish_width",
"demand"]

separation = 0
numberOfDishes = 0
firstKindOfDisheshot = 0
table_width = 0
dish_width = {}
demand = {}

def nonblank_lines(f):
    for l in f:
        line = l.rstrip()
        line = l.lstrip()
        for key in keywords:
            if (re.match(key+r'\(\d+(, \d+)*\)\.',line)):
            	parse_line(line, key)

def parse_line(op, key):
    global separation
    global numberOfDishes
    global firstKindOfDisheshot
    global table_width
    global dish_width
    global demand

    values = re.findall('\d+', op)
    if key is keywords[0]:
        numberOfDishes = int(values.pop(0))
    elif key is keywords[1]:
        firstKindOfDisheshot = int(values.pop(0))
    elif key is keywords[2]:
        separation = int(values.pop(0))
    elif key is keywords[3]:
        table_width = int(values.pop(0))
    elif key is keywords[4]:
        dish_width.update({int(values.pop(0)):int(values.pop(0))})
    elif key is keywords[5]:
        demand.update({int(values.pop(0)):int(values.pop(0))})

def print_current_values():
    print ("dishes: ", numberOfDishes, "\nhot:",firstKindOfDisheshot
    ,"\nseparation:",separation,"\ntable_width:",table_width,"\ndish_width:",dish_width
    ,"\ndemand:",demand)

def getNumberOfTables(sortedDishes, tableSize,separation):
	tableNumber = 0
	while(sortedDishes):
		tableNumber+=1
		tempTableSize = tableSize
		biggestItem = sortedDishes.pop(len(sortedDishes)-1)
		tempTableSize -= biggestItem[1]
		currentType = biggestItem[0]

		#second take
		# coldList = [cold for cold in sortedDishes if cold[0] is "cold"]
		# hotList = [hot for hot in sortedDishes if hot[0] is "hot"]
		# print("Cold List: ", coldList)
		# print("Hot list: ", hotList)

		# if currentType is "hot":
		# 	for hot in hotList:
		while(True):
			done = False		
			for dish in sortedDishes[:]:
				#sametype lets try adding this one
				if dish[0] is currentType:
					if (tempTableSize-dish[1]) > 0:
						#pop this element
						sortedDishes.remove(dish)
						#tempTableSize new size
						tempTableSize -= dish[1]
						continue
					elif (tempTableSize-dish[1]) == 0:
						sortedDishes.remove(dish)
						done = True
						break
			#no element of same type found
			if done:
				break
			elif tempTableSize > 0:
				#we still got space check with the smallest one now
				if not sortedDishes:
					break
				tempElement = sortedDishes[0]
				tempTableSize2 = tempTableSize - (tempElement[1]+separation)
				if tempTableSize2 >= 0:
					sortedDishes.pop(0)
					tempTableSize -= tempTableSize2
				elif tempTableSize2 < 0:
					break
			if tempTableSize == 0:
				break

	return tableNumber


def main():
	f = open(sys.argv[1], 'r')
	nonblank_lines(f)
	#put them in a list
	dishesHotLeft = firstKindOfDisheshot
	typeOfDish = "hot"
	dishesDict = []#has 
	for key, value in demand.items():
		if dishesHotLeft <= 0:
			typeOfDish = "cold"
		for i in range(value):
			dishesDict.append((typeOfDish,dish_width.get(key)))
		dishesHotLeft-=1
	# 		#going to the next type
	#sort them by length
	dishesDict.sort(key=lambda tup: tup[1])
	# print(dishesDict)
	# print_current_values()
	print("tables("+str(getNumberOfTables(dishesDict, table_width,separation))+").")
	f.close()


main()