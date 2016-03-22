import numpy as np
import os
import resource
import sys



cmd = 'python staticConstraints.py > constraints'
os.system(cmd)

if len(sys.argv) == 3 :
	inputFileString = sys.argv[1]
	outFileString = sys.argv[2]
else:
	print 'ERROR : input / output file not supplied, or bad format used'
	sys.exit(1)

inputFile = open(str(sys.argv[1]),'rU')
finalOut=open(str(sys.argv[2]),'wb')

for puzzle in inputFile:
	print '\n'
	print puzzle
	cnf=open('cnf.txt','wb')
	for i in range(1,len(puzzle)):
		p=puzzle[i]
		h=(i/9)+1
		k=(i%9)+1

		if p!='.' and p!='\n':
			cnf.write( str(100*h+10*k+int(p)) + ' 0\n' )

	constraints = open('constraints').readlines()

	for c in constraints:
		cnf.write(c)
	cnf.close()

	cmd = './MiniSat_v1.14_linux cnf.txt out.txt'
	os.system(cmd)
	out = open('out.txt')

	sat = out.readline()

	sudoku = np.zeros([9,9],dtype = int)
	if sat.strip() == 'SAT':
		clauses = out.readline()
		# print clauses.strip()
		clauses = clauses.strip().split(' ')
		for c in clauses:
			var = int(c)
			if var > 0:
				h= var/100
				k = (var%100)/10
				v = var%10
				sudoku[h-1,k-1] = v

		# print sudoku
		for row in range(0,9):
			for col in range(0,9):
				finalOut.write(str(sudoku[row,col]))
		finalOut.write('\n')
	
	else:
		finalOut.write('UNSAT ' + puzzle)



finalOut.close()

res = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
print res, 'KB (', res/1024, 'MB) of memory utilized by this program'


print "This is the name of the script: ", sys.argv[0]
print "Number of arguments: ", len(sys.argv)
print "The arguments are: " , str(sys.argv)
