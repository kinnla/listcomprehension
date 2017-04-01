import random
import statistics
import bisect

data = []

# the optimal vector found so far
# initial value is the equal vector
opt_vector = None

# difference of completions in the so far optimal vector
# initially zero, to be evaluated in the first round
opt_mean = float("inf")


# generates the differences
differences = []
def gen_differences():
	counter = 0
	while True:
		if counter >= len(differences):
			differences.append(abs(random.randint(1, 6) - random.randint(1, 6)))
		yield differences[counter]
		counter += 1

# generates new vectors by altering the given one in two coordinates
def gen_vectors():
	
	# start with the default vector
	vector = [3, 3, 3, 3, 3, 3]
	if data == []:
		yield vector

	# init modifiers 
	modifiers = [(a, b) for a in range(6) for b in range(6) if a != b]
	random.shuffle(modifiers)

	# loop while still vectors to be tried
	counter = 0
	while counter < len(modifiers):

		# if we just found a better vector, reset the counter
		if vector != data[0][2]:
			vector = data[0][2]
			counter = 0

		# create the modified vector		
		v = list(vector)
		v[modifiers[counter][0]] -= 1
		v[modifiers[counter][1]] += 1

		# assert all values to be nonegative
		if all(n >= 0 for n in v):
			yield v

		# adjust counter
		counter += 1

complete = False
while not complete:

	# try to find a better vector
	for vector in gen_vectors():
		complete = True

		results = []
		generator = gen_differences()
		for _ in range(1000):
			v = list(vector)
			while any(n > 0 for n in v):
				v[next(generator)] -= 1

			# one set completed. Add counter to results.
			results.append(sum(vector) - sum(v))

		# check if the new vector is better
		mean = sum(results, 0.0) / len(results)
		median = statistics.median(results)

		# append results to the data
		bisect.insort(data,(mean, median, vector))

		if mean < opt_mean:
			opt_vector = vector
			opt_mean = mean
			print ("new: {!s} with mean: {!s} and median: {!s}".format(vector, mean, median))
			complete = False
			break

# print data
for d in data:
	print(str(d))