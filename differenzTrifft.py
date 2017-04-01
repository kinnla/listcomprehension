import random
import statistics

# create differences

# the optimal vector found so far
# initial value is the equal vector
opt_vector = None

# difference of completions in the so far optimal vector
# initially zero, to be evaluated in the first round
opt_mean = float("inf")

#differences = [abs(random.randint(1, 6) - random.randint(1, 6)) for _ in range(100000)]
differences = []

# generates the differences
def gen_differences(vector):
	counter = 0
	while True:
		if counter >= len(differences):
			differences.append(abs(random.randint(1, 6) - random.randint(1, 6)))
		yield differences[counter]
		counter += 1

# generates new vectors by altering the given one in one coordinate
def gen_vectors(vector):
	
	# if called first time, return the default vector
	if vector == None:
		yield [3, 3, 3, 3, 3, 3]

	# init modifiers 
	modifiers = [(a, b) for a in range(6) for b in range(6) if a != b]
	random.shuffle(modifiers)
	for counter in range(len(modifiers)):
		# prepare next round
		v = list(vector)
		v[modifiers[counter][0]] -= 1
		v[modifiers[counter][1]] += 1

		# assert all values to be nonegative
		if all(n >= 0 for n in v):
			yield v

complete = False
while not complete:

	# try to find a better vector
	for vector in gen_vectors(opt_vector):
		complete = True

		results = []
		generator = gen_differences(vector)
		for _ in range(2000):
			counter = 0
			v = list(vector)
			while any(n > 0 for n in v):
				diff = next(generator)
				v[diff] = max(v[diff] - 1, 0)
				counter += 1

			# one set completed. Add counter to results.
			results.append(counter)

		# check if the new vector is better
		mean = sum(results, 0.0) / len(results)
		median = statistics.median(results)

		if mean < opt_mean:
			opt_vector = vector
			opt_mean = mean
			print ("new: {!s} with mean: {!s} and median: {!s}".format(vector, mean, median))
			complete = False
			break
