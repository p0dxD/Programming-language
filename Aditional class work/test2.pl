mother_child(trude, sally). 
father_child(tom, sally). 
father_child(tom, erica). 
father_child(mike, tom).
parent_child(X, Y) :- father_child(X, Y).
parent_child(X, Y) :- mother_child(X, Y).
sibling(X, Y):- parent_child(Z, X), parent_child(Z, Y).


fib(0,0).
fib(1,1).
fib(X, E) :- D is X-1, G is X-2, fib(D, _T), fib(G, _P), E is _T + _P.

fact(1,1).
fact(X,Y) :- Z is X -1, fact(Z, D), Y is X*D.


tes(0).
tes(X) :- Z is X -1, writeln(Z), tes(Z).

people(2). 
locations(4). 
preferences(4).  
order(1, 1, 2). 
order(1, 2, 4). 
order(2, 1, 3). 
order(2, 3, 4). 