
Group members: Mingyu Du & Tianyi Zhao
Note: in this folder, we try to complete extended tasks 1&3.
Environment: Ubuntu 16.04 LTS

1.This folder includes: 

	sud2sat.java
	
	sat2sud.java

	satz.c(another SAT-solver)
	
	README.txt

	satz213(it is a folder that contains the SAT-solver and A README file)


2.How to encode (transform a puzzle into a standard cnf format):
	
	1. Compile sud2sat.java:
				
		javac sud2sat.java

	
	2. Run CNF with the input file *.txt, for example:
			
		java sud2sat test.txt

	3. The encoded file SATinput.txt is created:
		
		first, you need to complie satz.c, the command is 'gcc -O3 -o satz satz.c'(To compile under Unix (or Linux))

		Call: satz <cnf-file>, where <cnf-file> is a file in DIMACS cnf format.
		or: satz -s <cnf-file> to avoid the preprocessing which adds resolvents of
		length<=3.

		second, Run SAT Solver with SATinput.txt(the cnf-file) as an input, get the output file from SAT

			SAToutput.txt

	(Note:The SAT Solver we are using is Satz (contributed by Chu-Min Li), more details are in the folder satz213,
  	which can be found at http://www.cs.ubc.ca/~hoos/SATLIB/solvers.html)


3.How to decode (get the result from SAToutput):

	1. Compile sat2sud.java:

		javac sat2sud.java

	2. Run Result with the SAToutput.txt as an argument:		

		java sat2sud SAToutput.txt

	3. The solution of the puzzle stored in solution.txt

