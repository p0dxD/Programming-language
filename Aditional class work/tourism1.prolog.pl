%Jose Rodriguez
%107927299

violations(A) :- 
	people(B), 
	locations(C), 
	preferences(_D), 
	getUsersPreferences(B,Preferences),
	getAllPermFromTheGivenValue(C,Locations),
	getInitialValueForViolations(Preferences,Locations, InitialViolation),
	goThroughPermutations(Preferences,Locations,InitialViolation, [],R), 
	listMin(R,Min),
	A = Min.

getInitialValueForViolations(_,[],_).
getInitialValueForViolations(ListOfPreferences,[ListToCheckWith|_RestPermu], R) :-
	getViolations(ListOfPreferences,ListToCheckWith,Violations),
	R = Violations.


goThroughPermutations(_,[],0,[]).
goThroughPermutations(ListOfPreferences,[ListToCheckWith|RestPermu],CurrentHighestViolation, L,R):-
	(RestPermu \= [] -> getViolations(ListOfPreferences,ListToCheckWith,Violations),
		appendToList(Violations,L,T2),
		goThroughPermutations(ListOfPreferences,RestPermu,CurrentHighestViolation,T2 ,T3),
		R = T3;
		getViolations(ListOfPreferences,ListToCheckWith,Violations),
		appendToList(Violations,L,R)).


%helper for setting a value if its equal or less 
isLess(X,Y) :- X < Y.

%gets the violation based on one permutation
getViolations(ListOfPreferences, ListToCheckWith,Violations) :-
	Temp = ListToCheckWith,
	iterateThroughPermu(Temp,ListOfPreferences,ListToCheckWith,Violations).

iterateThroughPermu([],_,_,0).
iterateThroughPermu([Item|OtherItemsPermu],ListOfPreferences,ListToCheckWith,R) :-
	iterateThroughPreferences(Item,ListOfPreferences, ListToCheckWith, V1),
	iterateThroughPermu(OtherItemsPermu, ListOfPreferences,ListToCheckWith, V2),
	R is V2 +V1.

%equivalent of for i in range(len(listOfPreferences)):
iterateThroughPreferences(_,[],_,0).
iterateThroughPreferences(Item,[ListOfPreference|RemainingPreferences],ListToCheckWith,R) :-
	test(Item,ListOfPreference,ListToCheckWith,ViolationOfThisList),
	iterateThroughPreferences(Item,RemainingPreferences,ListToCheckWith,R2),
	R is R2 + ViolationOfThisList.

test(Item,ListOfPreference,ListToCheckWith,R) :-  
	(isInList(Item,ListOfPreference)->
	getRestOfList(Item,ListOfPreference, ShortListOfPreferences),
	checkPartialListForViolations(Item,ShortListOfPreferences,ListToCheckWith,Violations),
	R = Violations; R = 0).

%checks if element is within the list 
isInList(X,L) :- member(X,L).

%calculates violations for a given list
checkPartialListForViolations(_,[],_,0).
checkPartialListForViolations(Item, [K|PartialList], ListToCheckWith,NumberViolations):-
	checkIfPointsViolate(Item,K,ListToCheckWith,R1),
	checkPartialListForViolations(Item, PartialList,ListToCheckWith,N2),
	NumberViolations is N2 +R1.

%result is 1 if it does, else is 0, based index
%for testing checkIfPointsViolate([2,3,4,5,1],2,1,R).
checkIfPointsViolate(Item, K, List,Result) :- 
	indexOf(Item,List,R1),
	indexOf(K,List,R2),
	isViolation(R1,R2,Result).

indexOf(_,[],-1).
indexOf(X, [X|_Tail], 0).
indexOf(X, [_|Tail],Y) :- indexOf(X, Tail, Y2),Y is Y2 +1.

%obtains rest of list from a given point
getRestOfList(_,[],[]).
getRestOfList(X,[X|Tail],Tail).
getRestOfList(X, [_|Tail],Y) :- getRestOfList(X,Tail,Y).

%returns 1 if theres a violation, else 0
isViolation(X,Y,Result) :- (X < Y -> Result is 0; Result is 1).

%helpers for getting list of preferences
getFirstValues(X, E) :- findall(Y ,order(X,Y,_Z), E ).

getSecondValues(X, E) :- findall(Z ,order(X,_Y,Z), E ).

testPref(X,Y) :- order(X, A,B), Y = [A|[B]].

getPreference(X, Y) :- 
	findall(Z ,testPref(X,Z), E ),
	my_flatten(E,H),
	compress(H,Y).


my_flatten(X,[X]) :- 
	\+ is_list(X).
my_flatten([],[]).
my_flatten([X|Xs],Zs) :- 
	my_flatten(X,Y), 
	my_flatten(Xs,Ys), 
	append(Y,Ys,Zs).


getUsersPreferences(X, L) :-  generateListForPreferences(X,[],L).

%gets the preferences in a list from all the people
generateListForPreferences(X,L,T) :-
   (X > 1
	-> X1 is X-1, 
	getPreference(X,Y),
	appendToList(Y,L,T2),
	generateListForPreferences(X1, T2, T3),
	T = T3 ; 
	getPreference(X,Y),
	appendToList(Y,L,T)).


%returns a list of the permutations from an integer
%ex. 4...will get [1,2,3,4], then permute it 
getAllPermFromTheGivenValue(X, Y) :- 
generateListForPerm(X, [], T),
findall(Z, permute(T,Z), Y).

generateListForPerm(X,L,T) :-
   (X > 1
	-> X1 is X-1, 
	appendToList(X,L,T2),
	generateListForPerm(X1, T2, T3),
	T = T3 ; appendToList(X,L,T)).

%permutes all values
permute([], []). 

permute([X|Xs], Ys) :-
         permute(Xs, Zs),
         select(X, Ys, Zs).

%appends value to list
appendToList(X, Y, L) :- L = [X|Y].

%for lists
append([],L,L).
append([X|L], M, [X|N]) :- append(L,M,N).

%compresses list 
compress([],[]).

compress([X],[X]).

compress([X,X|Xs],Zs) :- 
	compress([X|Xs],Zs).

compress([X,Y|Ys],[X|Zs]) :- 
	X \= Y, 
	compress([Y|Ys],Zs).

%removes an element from the list
select(_X,[],_) :- fail.% not needed

select(X, [X|Ys], Ys).

select(X, [Y|Ys], [Y|Zs]) :-
        select(X, Ys, Zs).

member(X,[X|_R]).
member(X,[_Y|R]) :- member(X,R).

testTwo(X,Y, R) :- R is min(X, Y).

listMin([L|Tail], Min) :-
    listMin(Tail, L, Min).

listMin([], Min, Min).
listMin([L|Tail], Min0, Min) :-
    Min1 is min(L, Min0),
    listMin(Tail, Min1, Min).
