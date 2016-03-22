import numpy as np

# Individual cell constraints
for i in range(1,10):
	for j in range(1,10):
		for k in range(1,10):
			print 100*i+10*j+k,
		print '0'

# All Diff 
for i in range(1,10):
	for j in range(1,10):
		for v in range(1,10):
			for k in range(v+1,10):
				print -i*100-j*10-v , -i*100-j*10-k, '0'


# Row constraints	
for i in range(1,10):
	for j in range(1,10):
		for k in range(1,10):
			print 100*j+10*k+i,
		print '0'


# Row All Diff 
for i in range(1,10):
	for j in range(1,10):

		for v in range(1,10):
			for k in range(v+1,10):
				print -i*100-v*10-j , -i*100-k*10-j, '0'
		# break
	# break


# Col constraints
for i in range(1,10):
	for j in range(1,10):
		for k in range(1,10):
			print 100*k+10*j+i,
		print '0'

# Col All Diff
for i in range(1,10):
	for j in range(1,10):

		for v in range(1,10):
			for k in range(v+1,10):
				print -v*100-i*10-j , -k*100-i*10-j, '0'
		# break
	# break


# Box constraints
blocks = []
for i in range(1,10):
	for m in range(0,3):
		for n in range(0,3):
			block =[]
			for j in range(1,4):
				for k in range(1,4):
					# for u in range(1,4):
					# 	for v in range(1,4):
					block.append(100*(3*m+j)+10*(3*n+k)+i)		 
							# print 	100*(3*m+j)+10*(3*n+k)+(u),100*(3*m+j)+10*(3*n+k)+(u),0
			blocks.append(block)
	# break

# Box All diff constraints
for block in blocks:
	for i in range(0,len(block)):
		for j in range(i+1,len(block)):
			print -block[i], -block[j], 0
	# break