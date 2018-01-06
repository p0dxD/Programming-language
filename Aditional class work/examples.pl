%appends a list to it
append([],L,L).
append([X|L], M, [X|N]) :- append(L,M,N).

%sees if it contains it
member(X,[X|_R]).
member(X,[_Y|_R]) :- member(X,_R).

%this is more like remove
select(X,[X|R],R).
select(X,[F|R],[F|S]) :- select(X,R,S).

%reverse
reverse([],X,X).
reverse([X|Y],Z,W) :- reverse(Y,[X|Z],W).

%permutations
perm([],[]).
perm([X|Y],Z) :- perm(Y,W), select(X,Z,W).

%% t(X) :- 1.
%% t(X,Y) :- t(X).

add(X,Y, Z) :- Z is X + Y.

fib(0,0).
fib(1,1).
%% fib(X, E) :- D is X-1, G is X-2, fib(D, _T), fib(G, _P), E is _T + _P.