import sys   # for command-line arguments

# @ Name : Lane Gramling
# @ Due Date : March 01, 2019
# @ Brief: Gale-Shapley Stable Matching Algorithm Implementation.
#          Takes an input file and outputs the stable matching of the two input sets.
#  		Usage: python stable_matching_2766765.py <input-file> [output-file]

# Read and parse the input file into a workable object
# (read lines into array, split into subarrays, and parse everything into integers (+ correct offset for 0-based array))
def readInput(filename):
	with open(filename, 'r') as inputFile:
		data = [list(map(lambda x: x and int(x)-1, line.strip("\r\n").split(','))) for line in inputFile]
		data[0][0] += 1
		return (data[2:2+data[0][0]], data[3+data[0][0]:2*data[0][0]+4], data[0][0])

def writeOutput(result, filename): # Format and write file to output (+ correct offset for 1-based numbering)
	with open(filename, 'w') as outFile:
		for pair in result:
			outFile.write(", ".join(map(lambda x: str(x+1), pair)) + "\r\n")
	print("Completed, saved to {}".format(filename))

def stable_matching():
	(men, women, nSize) = readInput(str(sys.argv[1]))

	# Initialize engaged/proposed states & results array
	for n in range(nSize):
		men[n] = {'priorities': [{'womanID': woman, 'proposedto': False} for woman in men[n]], 'engaged': None}
		women[n] = {'priorities': [{'manID': man, 'proposedto': False} for man in women[n]], 'engaged': None}
	result = nSize * [[0,0]]

	while any([man['engaged'] is None for man in men]): # Primary algorithm loop
		for manID, man in enumerate(men):
			if man['engaged'] is None: # Check if the man is engaged
				for woman in man['priorities']: # If not, Check for the women who he hasn't proposed to...
					if not woman['proposedto']: # If he hasn't proposed to woman x along the list, check if they are engaged...
						if women[woman['womanID']]['engaged'] is None: # Engage the two if they should be.
							woman['proposedto'] = True					# Engagement process...
							men[manID]['engaged'] = woman['womanID']    # ...
							women[woman['womanID']]['engaged'] = manID  # ...
							result[manID] = [manID, woman['womanID']]   # ...
							break
						else: # Woman currently engaged to someone else. Make sure the woman prefers their current partner to this man...
							curWomanPriorityList = [man['manID'] for man in women[woman['womanID']]['priorities']]
							if curWomanPriorityList.index(manID) < curWomanPriorityList.index(women[woman['womanID']]['engaged']): # If the woman prefers this man to her fiance, swap.
								woman['proposedto'] = True				    # Engagement process...
								men[manID]['engaged'] = woman['womanID']    # ...
								men[women[woman['womanID']]['engaged']]['engaged'] = None # Free up the woman's former fiance
								women[woman['womanID']]['engaged'] = manID  # ...
								result[manID] = [manID, woman['womanID']]   # ...
								break

	writeOutput(result, len(sys.argv) > 2 and sys.argv[2] or str(str(sys.argv[1]).split('.')[0]) + "_out.txt") # Write to the output file.

if len(sys.argv) < 2:
	print("[Usage]: python stable_matching_2766765.py <input-file> [output-file]")
else:
	stable_matching()
