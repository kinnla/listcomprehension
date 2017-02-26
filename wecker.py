"""Computes possible equations for the wecker problem"""

def evalx(f):
	try: return eval(f)
	except: return False

def gen_formulas2(a, b):
	return [a + o + b for o in '+-*/']

def gen_formulas3(a, b, c):
	l1 = ['(' + f1 + ')' + o + c for f1 in gen_formulas2(a, b) for o in '+-*/']
	l2 = [a + o + '(' + f2 + ')' for o in '+-*/' for f2 in gen_formulas2(b, c)]
	return l1 + l2

def check_eval(l1, l2):
	l = [f1 + '==' + f2 for f1 in l1 for f2 in l2]
	return filter(lambda x : evalx(x), l)		

times = [('2.', '1.', str(a)+'.', str(b)+'.') for a in range(6) for b in range(10)]
for t in times:
	l = check_eval([t[0]] , gen_formulas3(t[1], t[2], t[3]))
	l += check_eval(gen_formulas2(t[0], t[1]) , gen_formulas2(t[2], t[3]))
	l += check_eval(gen_formulas3(t[0], t[1], t[2]) , [t[3]])
	print l
