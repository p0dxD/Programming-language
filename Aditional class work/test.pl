p(X) :- q(X,_). 
q(1,a).
q(2,a).
q(5,c).
q(X) :- p(Y), X is Y*2.


brown(bear). 
big(bear). 
gray(elephant). 
big(elephant). 
black(cat). 
small(cat). 
dark(Z) :- black(Z).
dark(Z) :- brown(Z). 
dangerous(X) :- dark(X), big(X).


length([], 0).

length([_|Xs], M):-
	length(Xs, N), M is N+1.

same(X, Y) :- 
(X = 0 -> Y is 5
	; Y is 10).

max(X,Y,Z) :- 
( X =< Y
	-> Z = Y 
	; Z = X ).


factorial(N, F) :-
   (N > 0
	-> N1 is N-1, 
	factorial(N1, F1),
	F is N*F1 ; F = 1).

%removes an element from the list
select(X,[],_) :- fail.% not needed

select(X, [X|Ys], Ys).

select(X, [Y|Ys], [Y|Zs]) :-
        select(X, Ys, Zs).

%permutes all values
permute([], []). 

permute([X|Xs], Ys) :-
         permute(Xs, Zs),
         select(X, Ys, Zs).

my_last([], 0). 
my_last([H], H).
my_last([H1,H2|T], X):-
	my_last([H2|T], X).
	
compress([],[]).
compress([X],[X]).
compress([X,X|Xs],Zs) :- 
	compress([X|Xs],Zs).
compress([X,Y|Ys],[X|Zs]) :- 
	X \= Y, 
	compress([Y|Ys],Zs).



