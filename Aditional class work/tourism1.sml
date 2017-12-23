
fun map(f,L) = if (L=[]) then []
	else f(hd(L))::(map(f,tl(L)));

fun myInterleave(x,[]) = [[x]]
	| myInterleave(x,h::t) =
	(x::h::t)::(map((fn l => h::l), myInterleave(x,t)));

fun appendAll([]) = []
	|appendAll(z::zs) = z@(appendAll(zs));

fun permute(nil) = [[]]
	| permute(h::t) = appendAll(
	map((fn l => myInterleave(h,l)), permute(t)));

(*Removes element from given list*)
fun remove(x,L) = if (L=[]) then []
	else if x=hd(L)then remove(x,tl(L))
		else hd(L)::remove(x,tl(L));

fun removedupl(L) =
	if (L=[]) then []
		else hd(L)::removedupl(remove(hd(L),tl(L)));

(* Takes in an int and returns the list of sequential generated integers *)
fun generateListForPermutation(x:int):int list = 
	let
		fun genHelper(x:int,L:int list) = if (x = 0) then L
	else genHelper(x-1:int, (x::L):int list);
		in
	genHelper(x,[])
end;

(*Checks if item is in current list*)
fun isInList(item:int, L: int list) =
	if L = [] then false
	else if item = hd(L) then true
	else isInList(item:int, tl(L));

(* get the index of the given value in the list *)
fun indexOf(x:int, L:int list):int = if (L = []) then 0
	else if (x = hd(L)) then 0
	else 1+indexOf(x:int, tl(L):int list);

(*Checks if the current value is less than the value wanted, if so violation*)
fun checkIfViolation(x:int, y:int, L:int list) =
	if (indexOf(x, L) < indexOf(y, L)) then 0 else 1;

(*generates a partial list based on the value provided*)
fun getPartialListForCheckingWithViolations(x:int,L:int list)=
	 if (x=hd(L)) then tl(L)
	 	else (getPartialListForCheckingWithViolations(x:int, tl(L):int list));

(*Creates empty lists to store preferences*)
fun createLists(numPeople:int):int list list = if numPeople = 0 then []
	else ([]:int list)::createLists(numPeople-1:int);

(*checks if tuple of preference is of the person given*)
fun isPersonPreference(person:int, (x,y,z):int*int*int) = if person=x then true else false;

(*Returns all tupples within a list that are from a person as a list of those tuples*)
fun getTuplesSamePerson(person:int, L:(int*int*int) list) = 
	let
		fun getTuplesHelper(person:int,TmpL:(int*int*int) list, L:(int*int*int) list) = 
			if L = nil then TmpL
			else if isPersonPreference(person:int, hd(L):(int*int*int)) 
				then getTuplesHelper(person:int, TmpL@[hd(L)]:(int*int*int) list, tl(L:(int*int*int) list)) 
			else getTuplesHelper(person:int, TmpL:(int*int*int) list, tl(L:(int*int*int) list)) 
	in
		getTuplesHelper(person:int, []:(int*int*int) list, L:(int*int*int) list)
	end;

(*Gets a list starting from the item to the end of the list, a sublist*)
fun getListOfListFromIndexToEnd(item:int, L:int list) =
	let
		val itemIndex = indexOf(item, L)
		val currentIndex = 0
		fun helper(item:int, L:int list, currentIndex: int, result:int list) =
			if L = [] then result
			else if itemIndex < currentIndex then helper(item:int,tl(L), currentIndex+1, result@[hd(L)])
			else helper(item:int,tl(L), currentIndex+1, result)
	in
		helper(item:int, L:int list,currentIndex,[]) 
	end;

(*Example use: getListOfPersonPreferences(getTuplesSamePerson(1,[(1,1,2),(1,2,3),(2,3,2),(2,2,1)]));*)
(*Makes the preferences a list*)
fun getListOfPersonPreferences(L:(int*int*int) list) =
	let
		fun helper(L:(int*int*int) list, P:int list):int list =
			if L=nil then removedupl(P)
			else helper(tl(L):(int*int*int) list, P@makeListOfTupleSecondAndThirdValue(hd(L)):int list)
	in
		helper(L:(int*int*int) list, [])
	end
and
	makeListOfTupleSecondAndThirdValue(t:(int*int*int)):int list =
	let
		val second = #2 t;
		val third = #3 t;
	in
		[]@[second]@[third]
	end;

(*Returns the list of all preference for all users in the order*)
fun getListOfAllPreferences(numOfPeople:int , preferences:(int*int*int) list) =
	let
		fun helper(numOfPeople:int, preferences:(int*int*int) list, L:int list list) =
			if (numOfPeople = 0) then L
			else helper((numOfPeople-1), preferences:(int*int*int) list, 
				getListOfPersonPreferences(getTuplesSamePerson(numOfPeople, preferences))::L)
	in
		helper(numOfPeople:int, preferences:(int*int*int) list, []:int list list)
	end;

(*Returns the int with the amount of violations currently in the preference list*)
fun violationForCurrentPreference(C:int list, currentPrefList: int list, item: int) = 
	if currentPrefList = [] then 0 (*We got an empty list*)

	else if isInList(item:int, currentPrefList: int list) then 
		(*Check violations of item*)
		let 
			val currentListUpToIndex =  getListOfListFromIndexToEnd(item,currentPrefList)

			fun helper(C:int list, currentListUpToIndex: int list, item: int, currentCount: int) =
				if currentListUpToIndex = [] then currentCount
				else helper(C, tl(currentListUpToIndex), item, 
					currentCount+checkIfViolation(item, hd(currentListUpToIndex), C))
		in
			helper(C, currentListUpToIndex, item, 0) 
		end
	else 0;(*This element is not on the list lets not worry about it*)


(*Returns the violation for all of the preferences*)
fun getViolationForCurrentItem(P:int list list, C:int list, item:int) =
	let
		val temp = P 
		fun helper(P:int list list, C:int list, currentPrefList: int list list, item: int,
			currentCount: int) = if currentPrefList = [] then currentCount
		else helper(P:int list list, C:int list, tl(currentPrefList), item: int,  
			currentCount+violationForCurrentPreference( C:int list,
				hd(currentPrefList), item: int))
		in
			helper(P:int list list, C:int list, temp, item:int, 0:int)
		end;

(*Get violatiion for current permutation value*)
fun getViolations(listOfPreferences: int list list, listToCheckWith:int list) =
	let
		val temp = listToCheckWith
		fun helper(P:int list list, C:int list, currentItem: int list, currentCount: int) =
			if currentItem = [] then currentCount
			else helper(P:int list list, C:int list, tl(currentItem),
				currentCount+getViolationForCurrentItem(P:int list list, C:int list, hd(currentItem)))
		in
			helper(listOfPreferences: int list list, listToCheckWith:int list,       
				temp: int list, 0: int)
		end;

(*usage: violations(2:int, 4:int, 4:int, [(1, 1, 2),(1, 2, 4),(2, 1, 3),(2, 3, 4)]);*)
(*Main function that will make use of others*)
fun violations(NumberOfPeople:int, NumberOfLocations:int, NumberOfPreferences:int, Preferences:(int * int * int) list) =
	let
		val listOfPlaces = generateListForPermutation(NumberOfLocations)
		(*These we pas to the first function*)
		val permutations = permute(listOfPlaces)
		val listOfPreferences = getListOfAllPreferences(NumberOfPeople, Preferences)
		val tempViolation = getViolations(listOfPreferences, hd(permutations))
		(*val violations = *)
		fun getHighestViolations(permutations:int list list, listOfPreferences: int list list, result: int) =
			if permutations = [] then result
			else getHighestViolations(tl(permutations),listOfPreferences, 
					(if  getViolations(listOfPreferences, hd(permutations)) < result 
						then getViolations(listOfPreferences, hd(permutations)) else result))
	in
		getHighestViolations(tl(permutations), listOfPreferences, tempViolation)
	end;