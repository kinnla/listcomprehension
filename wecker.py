"""
Python 3.6
Computes possible equations for the wecker problem
"""

# start time as 'hh:mm'
START_TIME = '21:00'

# time span in minutes
TIME_SPAN = 60

# recursive computation of solutions (2 numbers and 1 operator)
def solutions2(a, b):
	return [a + o + b for o in '+-*/']

# recursive computation of solutions (3 numbers and 2 operators)
def solutions3(a, b, c):
	return [a + o1 + b + o2 + c for o1 in '+-*/' for o2 in '+-*/'] 

# recursive computation of solutions (4 numbers, 2 operators and 1 equality sign)
def solutions4(a, b, c, d):
	l = [a + '==' + f for f in solutions3(b, c, d)]
	l += [f1 + '==' + f2 for f1 in solutions2(a, b) for f2 in solutions2(c, d)]
	return l + [f + '==' + d for f in solutions3(a, b, c)]

# customized variant of eval() mapping an arithmetic-error to False
def evalx(f):
	try: return eval(f)
	except: return False

# ----------------------------- main program ---------------------------- #

# compute minutes of the day as variable for the iterations
minutesOfDay = int(START_TIME[:2]) * 60 + int(START_TIME[3:])

# count the minutes given by the time span
for i in range (TIME_SPAN):

	# compute hour and minutes
	hour, minutes = divmod(minutesOfDay, 60)
	
	# get digits of the hour
	if hour < 10: 
		a, b = '0', str(hour)
	else: 
		a, b = str(hour)[0], str(hour)[1]

	# get digits of minutes
	if minutes < 10: 
		c, d = '0', str(minutes)
	else: 
		c, d = str(minutes)[0], str(minutes)[1]

	# compute and print solutions
	print (list(filter(lambda x : evalx(x), solutions4(a, b, c, d))))

	# icrement minutes of the day
	minutesOfDay = (minutesOfDay + 1) % (24 * 60)
