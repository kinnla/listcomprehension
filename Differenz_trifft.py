# http://www.schulentwicklung.nrw.de/angebote/materialdatenbank/upload/4674/143093_E_S1_AB1_Differenz_trifft.pdf

import random
import statistics
import bisect

"""Start vector from which the script starts improving."""
START_VECTOR = [3, 3, 3, 3, 3, 3]

"""The number of sets to be computed in one series."""
SETS_PER_SERIES = 1000

# all results that we generate 
results = []

# an unlimited series of throws
# each throw is a difference of 2 dices
throws = []

def gen_throws():
	"""Generates the throws. Every vector gets the same throws."""
	i = 0
	while True:
		if i >= len(throws):
			throws.append(abs(random.randint(1, 6) - random.randint(1, 6)))
		yield throws[i]
		i += 1

def gen_vectors():
	"""Generates new vectors by altering two coordinates of the best one we found so far."""	
	
	# if we are at the start, return the start vector
	vector = START_VECTOR
	if results == []:
		yield vector

	# init modifiers 
	modifiers = [(a, b) for a in range(6) for b in range(6) if a != b]
	random.shuffle(modifiers)

	# loop while still vectors to be tried
	counter = 0
	while counter < len(modifiers):

		# if we just found a better vector, reset the counter
		if vector != results[0][2]:
			vector = results[0][2]
			counter = 0

		# create the modified vector		
		v = list(vector)
		v[modifiers[counter][0]] -= 1
		v[modifiers[counter][1]] += 1

		# assert all values to be nonegative
		# assert that we did not yet try this vector
		if all(n >= 0 for n in v) and all(d[2] != v for d in results):
			yield v

		# adjust counter
		counter += 1

def main():
	""" generates series and stores them in the results list."""
	print("Running the script with start vector {!s} and {!s} sets per series.".format(START_VECTOR, SETS_PER_SERIES))

	# repeat while still vectors to be checked
	for vector in gen_vectors():

		# prepare for the new series
		series = []
		generator = gen_throws()

		# create the sets for this series
		for _ in range(SETS_PER_SERIES):
			copy_of_vector = list(vector)
			while any(n > 0 for n in copy_of_vector):
				copy_of_vector[next(generator)] -= 1

			# one set completed. Add number of throws to series.
			series.append(sum(vector) - sum(copy_of_vector))

		# append series to the results
		mean = sum(series, 0.0) / len(series)
		median = statistics.median(series)
		standard_deviation = statistics.stdev(series)
		bisect.insort(results, (mean, median, vector, standard_deviation))
		print('.', end = '', flush = True)

	# print results
	print("\nResults in ascending order, sorted by average number of throws per set")
	for d in results:
		print("Vector: {!s}, Means: {!s}, Median: {!s}, Standard Deviation: {!s}".format(d[2], d[0], d[1], d[3]))

if __name__ == "__main__":
	main()

"""
Running the script with start vector [3, 3, 3, 3, 3, 3] and 1000 sets per series.
..................................................................................
Results in ascending order, sorted by average number of throws per set
Vector: [3, 6, 5, 3, 1, 0], Means: 31.445, Median: 30.0, Standard Deviation: 8.013188265989148
Vector: [2, 6, 5, 3, 2, 0], Means: 31.978, Median: 30.0, Standard Deviation: 8.086959559371799
Vector: [3, 6, 4, 3, 2, 0], Means: 31.978, Median: 30.0, Standard Deviation: 8.591468403557645
Vector: [2, 7, 5, 3, 1, 0], Means: 31.978, Median: 31.0, Standard Deviation: 7.7407645252543
Vector: [3, 6, 5, 2, 2, 0], Means: 32.09, Median: 30.0, Standard Deviation: 8.520240283847311
Vector: [3, 5, 5, 3, 2, 0], Means: 32.22, Median: 30.0, Standard Deviation: 8.639690054871428
Vector: [2, 6, 6, 3, 1, 0], Means: 32.297, Median: 31.0, Standard Deviation: 8.16587242567948
Vector: [3, 6, 4, 4, 1, 0], Means: 32.327, Median: 30.0, Standard Deviation: 8.848184071399135
Vector: [2, 6, 5, 4, 1, 0], Means: 32.347, Median: 31.0, Standard Deviation: 8.62966175826504
Vector: [2, 7, 4, 3, 2, 0], Means: 32.409, Median: 31.0, Standard Deviation: 8.234532562721853
Vector: [2, 7, 5, 2, 2, 0], Means: 32.488, Median: 31.0, Standard Deviation: 7.919885136829989
Vector: [2, 6, 4, 4, 2, 0], Means: 32.645, Median: 31.0, Standard Deviation: 8.914058303345083
Vector: [2, 6, 6, 2, 2, 0], Means: 32.727, Median: 31.0, Standard Deviation: 8.384077991273921
Vector: [3, 7, 3, 3, 2, 0], Means: 32.763, Median: 31.0, Standard Deviation: 8.267356299336576
Vector: [3, 5, 4, 4, 2, 0], Means: 32.847, Median: 31.0, Standard Deviation: 9.323117049115682
Vector: [1, 7, 5, 3, 2, 0], Means: 33.014, Median: 31.0, Standard Deviation: 8.247898631277655
Vector: [2, 5, 6, 3, 2, 0], Means: 33.075, Median: 31.0, Standard Deviation: 8.959109366485077
Vector: [3, 6, 3, 4, 2, 0], Means: 33.099, Median: 31.0, Standard Deviation: 9.194113917650288
Vector: [2, 5, 5, 4, 2, 0], Means: 33.171, Median: 31.0, Standard Deviation: 9.452465715785914
Vector: [1, 6, 6, 3, 2, 0], Means: 33.274, Median: 32.0, Standard Deviation: 8.584207162726946
Vector: [1, 6, 5, 4, 2, 0], Means: 33.407, Median: 31.0, Standard Deviation: 9.099678849011934
Vector: [2, 6, 4, 3, 3, 0], Means: 34.318, Median: 32.0, Standard Deviation: 10.446722452999794
Vector: [3, 6, 4, 3, 1, 1], Means: 34.652, Median: 31.0, Standard Deviation: 13.973122204580626
Vector: [2, 6, 5, 2, 3, 0], Means: 34.685, Median: 32.0, Standard Deviation: 10.46868513082557
Vector: [2, 5, 5, 3, 3, 0], Means: 34.77, Median: 32.0, Standard Deviation: 10.816658453519743
Vector: [2, 6, 5, 3, 1, 1], Means: 34.846, Median: 31.0, Standard Deviation: 13.677403092522912
Vector: [3, 5, 4, 5, 1, 0], Means: 34.884, Median: 33.0, Standard Deviation: 10.59380822805344
Vector: [2, 6, 5, 2, 2, 1], Means: 34.996, Median: 31.0, Standard Deviation: 13.9012671807008
Vector: [2, 6, 4, 3, 2, 1], Means: 35.044, Median: 31.0, Standard Deviation: 14.264415078703282
Vector: [1, 6, 5, 3, 3, 0], Means: 35.048, Median: 32.0, Standard Deviation: 10.642883395347662
Vector: [2, 5, 4, 5, 2, 0], Means: 35.129, Median: 33.0, Standard Deviation: 10.40310451661347
Vector: [2, 5, 4, 4, 3, 0], Means: 35.252, Median: 33.0, Standard Deviation: 11.09448437664336
Vector: [2, 5, 5, 3, 2, 1], Means: 35.278, Median: 31.0, Standard Deviation: 14.12962711335166
Vector: [3, 5, 3, 5, 2, 0], Means: 35.494, Median: 33.0, Standard Deviation: 10.576759041967055
Vector: [3, 4, 4, 5, 2, 0], Means: 35.576, Median: 34.0, Standard Deviation: 10.628319960613963
Vector: [3, 5, 4, 4, 1, 1], Means: 35.597, Median: 32.0, Standard Deviation: 14.45931058739187
Vector: [3, 4, 4, 4, 3, 0], Means: 35.619, Median: 33.0, Standard Deviation: 11.248215919040733
Vector: [3, 5, 3, 4, 3, 0], Means: 35.619, Median: 33.0, Standard Deviation: 11.380833113720733
Vector: [1, 6, 5, 3, 2, 1], Means: 35.627, Median: 32.0, Standard Deviation: 13.930826929473316
Vector: [3, 6, 2, 5, 2, 0], Means: 35.834, Median: 33.0, Standard Deviation: 10.440088095386908
Vector: [2, 5, 3, 5, 3, 0], Means: 37.742, Median: 35.0, Standard Deviation: 11.960036725632513
Vector: [3, 5, 3, 5, 1, 1], Means: 37.896, Median: 34.0, Standard Deviation: 14.23452864712442
Vector: [3, 4, 3, 5, 3, 0], Means: 38.187, Median: 36.0, Standard Deviation: 12.17588942473129
Vector: [3, 5, 2, 5, 3, 0], Means: 38.277, Median: 36.0, Standard Deviation: 11.971950492655681
Vector: [3, 5, 3, 6, 1, 0], Means: 38.734, Median: 37.0, Standard Deviation: 12.019638751464859
Vector: [3, 4, 3, 5, 2, 1], Means: 38.814, Median: 35.0, Standard Deviation: 14.353725420023661
Vector: [2, 5, 3, 6, 2, 0], Means: 39.117, Median: 36.0, Standard Deviation: 12.128743439343475
Vector: [3, 4, 3, 6, 2, 0], Means: 39.543, Median: 37.0, Standard Deviation: 12.128695571093218
Vector: [3, 5, 2, 6, 2, 0], Means: 39.606, Median: 37.0, Standard Deviation: 12.0142043059499
Vector: [2, 4, 3, 6, 3, 0], Means: 41.198, Median: 39.0, Standard Deviation: 12.99514023278201
Vector: [3, 4, 2, 6, 3, 0], Means: 41.715, Median: 39.0, Standard Deviation: 12.76937084714168
Vector: [3, 5, 1, 6, 3, 0], Means: 41.875, Median: 39.0, Standard Deviation: 12.484840657623398
Vector: [2, 4, 3, 5, 4, 0], Means: 42.302, Median: 40.0, Standard Deviation: 14.161049796230904
Vector: [3, 4, 2, 6, 2, 1], Means: 42.48, Median: 40.0, Standard Deviation: 14.363074110297486
Vector: [3, 5, 1, 6, 2, 1], Means: 42.718, Median: 40.0, Standard Deviation: 14.423054478871682
Vector: [2, 4, 2, 6, 3, 1], Means: 43.921, Median: 41.0, Standard Deviation: 15.196041546359323
Vector: [3, 4, 2, 7, 2, 0], Means: 44.328, Median: 42.0, Standard Deviation: 13.485929196250671
Vector: [2, 4, 2, 6, 4, 0], Means: 45.041, Median: 43.0, Standard Deviation: 14.29894327489898
Vector: [2, 4, 2, 7, 3, 0], Means: 45.509, Median: 43.0, Standard Deviation: 13.899680576190235
Vector: [3, 4, 1, 7, 3, 0], Means: 46.03, Median: 44.0, Standard Deviation: 13.798967769783054
Vector: [3, 4, 2, 5, 2, 2], Means: 46.342, Median: 40.0, Standard Deviation: 20.627567295552147
Vector: [2, 4, 2, 7, 2, 1], Means: 46.441, Median: 44.0, Standard Deviation: 16.21201247064498
Vector: [3, 3, 3, 5, 2, 2], Means: 46.449, Median: 41.0, Standard Deviation: 20.659676212884392
Vector: [3, 4, 2, 7, 1, 1], Means: 46.473, Median: 43.0, Standard Deviation: 15.845641525522257
Vector: [3, 5, 1, 5, 2, 2], Means: 46.604, Median: 40.0, Standard Deviation: 20.614561458933444
Vector: [3, 4, 1, 7, 2, 1], Means: 46.78, Median: 44.0, Standard Deviation: 15.811565564662015
Vector: [2, 4, 2, 5, 3, 2], Means: 47.836, Median: 42.0, Standard Deviation: 21.350619498107143
Vector: [3, 4, 2, 6, 1, 2], Means: 48.748, Median: 43.0, Standard Deviation: 20.434482231367255
Vector: [2, 4, 2, 6, 2, 2], Means: 49.064, Median: 43.0, Standard Deviation: 20.50146858676749
Vector: [3, 3, 2, 6, 2, 2], Means: 49.324, Median: 43.5, Standard Deviation: 20.175978144667337
Vector: [3, 4, 1, 6, 2, 2], Means: 49.363, Median: 44.0, Standard Deviation: 20.102072637524827
Vector: [3, 3, 3, 4, 2, 3], Means: 57.523, Median: 49.0, Standard Deviation: 28.334790123297743
Vector: [3, 4, 2, 4, 2, 3], Means: 57.599, Median: 49.0, Standard Deviation: 28.48743113607706
Vector: [3, 3, 3, 3, 3, 3], Means: 58.066, Median: 50.0, Standard Deviation: 28.365158667390286
Vector: [3, 4, 2, 3, 3, 3], Means: 58.066, Median: 50.0, Standard Deviation: 28.577899508892187
Vector: [2, 3, 3, 4, 3, 3], Means: 58.425, Median: 51.0, Standard Deviation: 28.08425003627656
Vector: [2, 3, 3, 5, 2, 3], Means: 58.739, Median: 51.0, Standard Deviation: 28.09958123291992
Vector: [3, 3, 2, 4, 3, 3], Means: 58.739, Median: 51.0, Standard Deviation: 28.225406153898874
Vector: [3, 3, 3, 5, 1, 3], Means: 58.849, Median: 51.0, Standard Deviation: 28.194736071510622
Vector: [3, 4, 2, 5, 1, 3], Means: 58.852, Median: 51.0, Standard Deviation: 28.16763233769412
Vector: [3, 3, 2, 5, 2, 3], Means: 58.898, Median: 51.0, Standard Deviation: 27.903802934693655
Vector: [3, 3, 3, 4, 1, 4], Means: 74.05, Median: 67.0, Standard Deviation: 35.73931726822434
[Finished in 6.0s]
"""
