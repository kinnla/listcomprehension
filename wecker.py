"""Computes possible equations for the wecker problem"""

def evalx(f):
	try: return eval(f)
	except: return False

def gen_formulas2(a, b):
	return [a + o + b for o in '+-*/']

def gen_formulas3(a, b, c):
	return [a + o1 + b + o2 + c for o1 in '+-*/' for o2 in '+-*/'] 

def gen_formulas4(a, b, c, d):
	l = [a + '==' + f for f in gen_formulas3(b, c, d)]
	l += [f1 + '==' + f2 for f1 in gen_formulas2(a, b) for f2 in gen_formulas2(c, d)]
	return l + [f + '==' + d for f in gen_formulas3(a, b, c)]


times = [('2.', '1.', str(a)+'.', str(b)+'.') for a in range(6) for b in range(10)]
for t in times:
	l = gen_formulas4(t[0], t[1], t[2], t[3])
	print (filter(lambda x : evalx(x), l))

