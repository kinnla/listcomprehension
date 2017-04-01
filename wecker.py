"""
Python 3.6
Computes possible equations for the wecker problem
"""

# start time as 'hh:mm'
START_TIME = '20:42'

# time span in minutes
TIME_SPAN = 60

# list of operators that can be inserted between the numbers
OPS = ['+', '-', '*', '/', '==']

# customized variant of eval() mapping an arithmetic-error to False
def evalx(f):
	try: return eval(f)
	except: return False

# ----------------------------- main program ---------------------------- #

# compute minutes of the day as loop variable
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

	# compute solutions
	l = [a + o1 + b + o2 + c + o3 + d for o1 in OPS for o2 in OPS for o3 in OPS]
	l = list(filter(lambda x : evalx(x) and x.count('=') == 2, l))

	# print solutions
	print (l)

	# icrement minutes of the day
	minutesOfDay = (minutesOfDay + 1) % (24 * 60)
