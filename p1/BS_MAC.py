import numpy as np
import sys
import time

def genConstraintGraph():
	g = np.zeros([81,81],dtype=int)

	for i in range(81):
		row_idx = i/9
		col_idx = i%9

		blk_x = row_idx/3
		blk_y = col_idx/3
		
		for j in range(9):
			g[i,row_idx*9+j] = 1
			g[i,j*9+col_idx] = 1

		for k in range(3):
			for l in range(3):
				g[i,(blk_x*3+k)*9+(blk_y*3)+l] = 1

		g[i,i] = 0
	return g

cg = genConstraintGraph()

class Var(object):

	def __init__(self, index, domain,domain_length,neighbors):
		self.domain = domain
		self.value = None
		self.index = index
		self.dom_l = domain_length
		self.neighbors = neighbors

	def set_value(self,val):
		self.value = val

def applyAC3(sudoku):
	arcs = []
	for s in sudoku:
		for n in s.neighbors:
			arcs.append((s.index,n))

	while len(arcs) != 0:
		arc = arcs[0]
		arcs = arcs[1:]

		if revise(sudoku,arc):
			if sudoku[arc[0]].dom_l == 0:
				return False
			for n in sudoku[arc[0]].neighbors:
				arcs.append((n,arc[0]))

	return True

def revise(sudoku,arc):
	revised = False
	for d in sudoku[arc[0]].domain:
		flag = True
		for e in sudoku[arc[1]].domain:
			if e!=d:
				flag = False
				break
		if flag:
			sudoku[arc[0]].domain.remove(d)
			sudoku[arc[0]].dom_l -= 1
			revised = True
	return revised


def check(var,sudoku):

	for n in var.neighbors:
		if sudoku[n].value is not None and sudoku[n].value == var.value:
			return False
	return True


def applyLCV(var,sudoku):
	min_c = np.zeros(var.dom_l,dtype=int)
	for i in range(var.dom_l):
		x = var.domain[i]
		min_d = 10
		for n in var.neighbors:
			if sudoku[n].value == None:
				if x in sudoku[n].domain and sudoku[n].dom_l - 1 < min_d:
					min_d = sudoku[n].dom_l - 1
				elif sudoku[n].dom_l < min_d:
					min_d = sudoku[n].dom_l
		min_c[i] = min_d

	t = zip(min_c,var.domain)
	t.sort(reverse=True)

	return t


def applyMAC(var,sudoku):
	arcs = []
	for n in var.neighbors:
		arcs.append((n,var.index))


	while len(arcs) != 0:
		arc = arcs[0]

		arcs = arcs[1:]

		if revise(sudoku,arc):
			if sudoku[arc[0]].dom_l == 0:
				return False
			for n in sudoku[arc[0]].neighbors:
				arcs.append((n,arc[0]))
	return True

def solveSudoku(sudoku, sorted_sudoku,varIdx):
	if varIdx == 81:
		return True
	var = sorted_sudoku[varIdx]
	if var.dom_l>1:

		lcv_domain = applyLCV(var,sudoku)


		for d_l,d in lcv_domain:
			
			if d_l == 0:
				break

			var.set_value(d)
			status = check(var,sudoku)
			if status is True:
				old_sudoku = []
				for s in sudoku:
					old_sudoku.append(list(s.domain))

				var.domain = [d]
				var.dom_l = 1
				inference = applyMAC(var,sudoku)
				if inference is True:
					result = solveSudoku(sudoku, sorted_sudoku,varIdx+1)
					if result is True:
						return True
				for i in range(len(sudoku)):
					sudoku[i].domain = old_sudoku[i]
					sudoku[i].dom_l = len(old_sudoku[i])

	else:

		for d in var.domain:
			var.set_value(d)
			status = check(var,sudoku)
			if status is True:
				old_sudoku = []
				for s in sudoku:
					old_sudoku.append(list(s.domain))

				inference = applyMAC(var,sudoku)
				if inference is True:
					result = solveSudoku(sudoku, sorted_sudoku,varIdx+1)
					if result is True:
						return True
				for i in range(len(sudoku)):
					sudoku[i].domain = old_sudoku[i]
					sudoku[i].dom_l = len(old_sudoku[i])

	var.set_value(None)	
	solveSudoku.back_tracks += 1		
	return False

def findNeighbors(index):
	n = []
	for i in range(81):
		if i != index and cg[i,index] == 1:
			n.append(i)
	return n

def BS_MAC(puzzle):
	# for i in range(9):
	# 	for j in range(9):
	# 		print puzzle[9*i+j],
	# 	print

	sudoku = []
	for i in range(len(puzzle)):
		nb = findNeighbors(i)
		p = puzzle[i]
		if p == '.':
			sudoku.append(Var(index = i, domain = range(1,10),domain_length = 9,neighbors = nb))
		else:
			sudoku.append(Var(index = i, domain = [int(p)], domain_length = 1,neighbors = nb))

	sorted_sudoku = sorted(sudoku, key=lambda var:var.dom_l)

	solveSudoku.back_tracks = 0

	status = solveSudoku(sudoku, sorted_sudoku,0)

	if status:
		solution = ''
		for i in range(9):
			for j in range(9):
				solution += str(sudoku[9*i+j].value)
		return solution

	else:
		return None




if __name__ == '__main__':
	puzzles = open(sys.argv[1],'rU')
	output = open(sys.argv[2],'wb')
	count = 0
	for p in puzzles:
		print 'Solving', p.strip()
		start = time.time()
		solution = BS_MAC(p.strip())
		end = time.time()
		if solution is None:
			print 'Cannot be solved!'
			output.write('UNSAT '+p.strip()+'\n')
		else:
			print 'Solved!'
			output.write(solution+'\n')
		print 'Finished in %ds'%(end-start)
		# if count >=2:
		# 	break
		# count+=1
	output.close()