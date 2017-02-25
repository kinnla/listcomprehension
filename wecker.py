

operators = ['+', '-', '*', '/']
signs = ['', '-']

def evalx(f):
	try:
		return eval(f)
	except:
		return False

def gen_formulas1(a):
	return [str(a), '-' + str(a)]

def gen_formulas2(a, b):
	global operators, signs
	return [s1 + str(a) + o + s2 + str(b) for s1 in signs for s2 in signs for o in operators]

def gen_formulas3(a, b, c):
	global operators, signs
	l1 = [s1 + '(' + f1 + ')' + o + f2 for s1 in signs for f1 in gen_formulas2(a, b) for o in operators for f2 in gen_formulas1(c)]
	l2 = [f1 + o + s2 + '(' + f2 + ')' for s2 in signs for f1 in gen_formulas1(a) for o in operators for f2 in gen_formulas2(b, c)]
	return l1 + l2

def check_eval(l1, l2):
	"""Returns a valid formula or False"""
	ll1 = [evalx(f) for f in l1]
	ll2 = [evalx(f) for f in l2]
	for i1 in range(len(l1)):
		for i2 in range(len(l2)):
			if ll1[i1] == ll2[i2]:
				return l1[i1] + '=' + l2[i2]
	return False


times = [(2.0,1.0,float(a),float(b)) for a in range(6) for b in range(10)]
for t in times:
	print check_eval(gen_formulas1(t[0]) , gen_formulas3(t[1], t[2], t[3])) or check_eval(gen_formulas2(t[0], t[1]) , gen_formulas2(t[2], t[3])) or check_eval(gen_formulas3(t[0], t[1], t[2]) , gen_formulas1(t[3]))

