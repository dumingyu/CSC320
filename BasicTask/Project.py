# Solver Sudoku Project
# CSC 320
# Mingyu Du & Tianyi Zhao
#==============================================================================
from __future__ import division
import sys
import math
import subprocess
from subprocess import call
import time
#==============================================================================
def prettyPrint(puzzle):
	length = len(puzzle)
	row = int(math.sqrt(length))
	section = int(math.sqrt(row))
	numsec = int(row/section)
	count = 0

	#print starting row
	sys.stdout.write(u'\u2554')
	for i in range(0,numsec):
		if i!=0:
			sys.stdout.write(u'\u2566')
		for j in range(0,(section*3)-1):
			sys.stdout.write(u'\u2550')
	print u'\u2557'

	for n in range(0,numsec):
		if n!=0:
			sys.stdout.write(u'\u2560')
			for k in range(0,numsec):
				if k!=0:
					sys.stdout.write(u'\u256C')
				for l in range(0,(section*3)-1):
					sys.stdout.write(u'\u2550')
			print u'\u2563'
		for s in range(0,section):
			for i in range(0,numsec):
				sys.stdout.write(u'\u2551')
				for j in range(0,section):
					sys.stdout.write("%2d"%puzzle[count])
					if j != section-1:
						sys.stdout.write(" ")
					count +=1
			print u'\u2551'

	#print ending row
	sys.stdout.write(u'\u255A')
	for i in range(0,numsec):
		if i!=0:
			sys.stdout.write(u'\u2569')
		for j in range(0,(section*3)-1):
			sys.stdout.write(u'\u2550')
	print u'\u255D'
#==============================================================================
def checkMiniSat():
	if call(['which','minisat'])==0:
		print "You are running << Minisat 1 >>"
	elif call(['which','minisat2']) ==0:
		print "You are running << Minisat 2 >>"
	else:
		print "Ain't no minisat here!!"
		return
#==============================================================================
def toBase10(num):
	return (num-1)%9+1
#==============================================================================
def toBase9(i,j,k):
	return str((i-1)*81+(j-1)*9+k)
#==============================================================================
def getdimacs(puzzle):
	xaxis = 1
	yaxis = 1
	count = 0
	dimacs = []
	while(xaxis < 10):
		#print count
		if puzzle[count] == 0:
			dimnum = ((81*(int(float(xaxis)) - 1)) + (9*(int(float(yaxis)) - 1)) + ((int(float(puzzle[count]))) + 1))
		else:
			dimnum = ((81*(int(float(xaxis)) - 1)) + (9*(int(float(yaxis)) - 1)) + ((int(float(puzzle[count]))) ))
		dimacs.append(dimnum)
		yaxis += 1
		if(yaxis == 10):
			xaxis += 1
			yaxis = 1
		count += 1

	return dimacs

#Every cell contains at least one number
#==============================================================================
def numcell(outfile, ret, puzzle):
	try:
		outfile = open("input", "a")
	except:
		print "Can't open file to write!"
	for i in range(0, len(ret)):
		if(puzzle[i] != '0'):
			outfile.write(str(ret[i]) + ' 0\n')
		else:
			loc = divmod(i, 9)
			for x in range(1, 10):
				num = (loc[0]*81+loc[1]*9+x)
				outfile.write(str(num) + ' ')
			outfile.write('0\n')

# #==============================================================================
def onenumrow(outfile):
	try:
		outfile = open("input", "a")
	except:
		print "Can't open file to write!"
	for i in range(1, 10): #for each row
		for k in range(1, 10):
			for j in range(1, 9):
				for l in range(j+1, 10):
					outfile.write("-" + toBase9(i,j,k) + " -" + toBase9(i,l,k) + " 0\n")

# #==============================================================================
def onenumcol(outfile):
	try:
		outfile = open("input", "a")
	except:
		print "Can't open file to write!"
	for j in range(1, 10):
		for k in range(1, 10):
			for i in range (1, 9):
				for l in range(i+1, 10):
					outfile.write("-" + toBase9(i,j,k) + " -" + toBase9(l,j,k) + " 0\n")
# #==============================================================================
def onenumblock(outfile):
	try:
		outfile = open("input", "a")
	except:
		print "Can't open file to write!"
	for k in range(1, 10):
		for a in range(0, 3):
			for b in range(0, 3):
				for u in range(1, 4):
					for v in range(1, 3):
						for w in range(v+1, 4):
							outfile.write("-" + toBase9(3*a+u,3*b+v,k) + " -" + toBase9(3*a+u,3*b+w,k) + " 0\n")
	for k in range(1, 10):
		for a in range(0, 3):
			for b in range(0, 3):
				for u in range(1, 3):
					for v in range(1, 4):
						for w in range(u+1, 4):
							for t in range(1, 4):
								outfile.write("-" + toBase9(3*a+u,3*b+v,k) + " -" + toBase9(3*a+w,3*b+t,k) + " 0\n")
#==============================================================================
def createcnf(ret, puzzle):
	canwrite = False
	try:
		outfile = open("input", "w")
		canwrite = True
	except:
		print "Can't open file to write!"
	if canwrite:
		with outfile:
			outfile.write('p cnf 729 5529\n')

		numcell(outfile, ret, puzzle)
		onenumrow(outfile)
		onenumcol(outfile)
		onenumblock(outfile)

#==============================================================================


#==============================================================================
def getsolved():
	try:
		file = open("output", "r")
	except:
		print "Can't open file to write!"
		return
	solved = []
	for num in file.read().split():
		if num.isdigit() and num > 0:
			solved.append(int(toBase10(int(num))))
	return solved
	
#=============================================================================#
# sud2sat is implemented here
#=============================================================================#
def sud2sat(puzzle):
	createcnf(getdimacs(puzzle),puzzle)




#=============================================================================#
# sat2sud is implemented here
#=============================================================================#
def sat2sud():
	#run minisat
	subprocess.call(["minisat","input","output"])
	prettyPrint(getsolved())	



#==============================================================================
def main():
	start = time.clock()
	#check MiniSAT version
	checkMiniSat()

	#-- INPUT CHECK
	if (len(sys.argv)!=2):
		print "Usage: python Project.py <input-file>"
		return
	try:			# check if can open file
		with open(sys.argv[1],'r') as infile:
			puzzle = infile.read().replace('\n', '').replace('?', '0').replace('*', '0').replace('.', '0')
	except IndexError: 	# read from stdin if no file
		infile = sys.stdin
	except IOError:		# file doesn't exist so print error!
		print("File specified does not exist!")

	print "PUZZLE:"
	print puzzle

	sud2sat(puzzle)
	sat2sud()
	totalTime = time.clock()-start
	print "Time used :", totalTime, "seconds"
	
#==============================================================================
if __name__ == "__main__":
	main()
