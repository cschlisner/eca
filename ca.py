import sys
import time
import random as r

# 1 <= r <= 256
def getrule(r):
	b = bin(r)[2:]
	for _ in range(8-len(b)):
		b = '0'+b
	return {
		(1,1,1): int(b[0]),
		(1,1,0): int(b[1]),
		(1,0,1): int(b[2]),
		(1,0,0): int(b[3]),
		(0,1,1): int(b[4]),
		(0,1,0): int(b[5]),
		(0,0,1): int(b[6]),
		(0,0,0): int(b[7]),
	}

# c = length of automaton
# rule = hashmap: (a,b,c) -> d for all 8 combonations of binary digits abc
def iterate(c, rule):
	k = len(c)-1
	triplets = [(c[k], c[0], c[1])] + [(c[i-1], c[i], c[i+1]) for i in range(1, len(c)-1)] + [(c[k-1], c[k], c[0])]
	return list(map(lambda x: rule.get(x), triplets))

class colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    CYAN = '\033[36m'
    UNDERLINE = '\033[4m'

"""
	Handle Command Line Input
"""

if (len(sys.argv) < 3):
	print("USAGE: $ python3 %s <width> <rule> [-r] [-s0 <sym>] [-s1 <sym>] [-eth] [-d <delay>] [-p <pattern>] [-i <iterations> [-o] [-evolve <r1,r2,...>]]" % sys.argv[0])
	print("\t<width>				int >= 1 (width of automaton)")
	print("\t<rule>				int 1-255 (cellular automaton to simulate)")
	print("\t-r				randomize initial state (default sets all cells to 0 except rightmost)")
	print("\t-s0 <sym>			display 0 cells as <sym> (default = ' ')")
	print("\t-s1 <sym>           		display 1 cells as <sym> (default = █)")
	print("\t-eth        	    		show rule 110 background ether as different color (mostly-accurate)")
	print("\t-d <delay>    			set delay between steps to <delay> seconds (default = 0.01)")
	print("\t-p <pattern>  			supply initial state via string pattern. --help -p for info.")
	print("\t-i <iterations>  		number of applications of the rule to simulate (i.e. a timer.)")
	print("\t\t-o			output result of iterations as binary without displaying transformations. Can be used for piping.")
	print("\t\t-evolve <r1,r2,..>	use rule r1 after <i> iterations, r2 after 2<i> iterations, etc..")
	print("\t\t-evolver <r1,r2,..>	randomly use rules r1,r2... while evaluating <rule>..")
	print("\t\t--evolve-all 		evaluate <i> iterations of every rule (0-255)")
	exit(0)

stream_input = ""
if (not sys.stdin.isatty()):
	stream_input=sys.stdin.readline()

# get rule,width specified by user
RULE = getrule(int(sys.argv[2]))
WIDTH = int(sys.argv[1])

# I the number of rule applications to do. inf if negative. 
I = -1 if ("-i" not in sys.argv) else int(sys.argv[sys.argv.index("-i")+1]) 

# Compute final state in background and output in binary if I is finite
silent_mode = ("-o" in sys.argv) if I>0 else False

evolutions = []
evolutionsr = []
if (I>0 and "-evolve" in sys.argv):
	evolutions.extend(list(map(lambda x: getrule(int(x)), sys.argv[sys.argv.index("-evolve")+1].split(","))))
if (I>0 and "-evolver" in sys.argv):
	evolutionsr.extend(list(map(lambda x: getrule(int(x)), sys.argv[sys.argv.index("-evolver")+1].split(","))))

# s:= current state -- initialize randomly if user specified -r, otherwise set to 000...0001
s = []
if (stream_input!=""):
	for c in stream_input:
		if (c!="\n"):
			s.extend(list(map(lambda x: int(x), bin(int(c))[2:])))
elif ("-p" in sys.argv): 
	for p in sys.argv[sys.argv.index("-p")+1]:
		s.extend(patterns.get(p))
elif ("-r" in sys.argv):
	s = [r.choice([0,1]) for _ in range(WIDTH)]
else: s = [0] * WIDTH + [1]

# set symbols for output according to user -- defaults to block and space
s1 = "█" if ("-s1" not in sys.argv) else sys.argv[sys.argv.index("-s1")+1]
_s0 = s0 = " " if ("-s0" not in sys.argv) else sys.argv[sys.argv.index("-s0")+1]
filter_r110_eth = "-eth" in sys.argv
step_delay = 0.01 if ("-d" not in sys.argv) else float(sys.argv[sys.argv.index("-d")+1])

# patterns 
ether = [[1,0,0,0,1,0,0],
		 [1,0,0,1,1,0,1],
		 [1,0,1,1,1,1,1]]
patterns = { 
	"." : [0,0,0,1,0,0,1,1,0,1,1,1,1,1],
	"a" : [0,0,0,1,1,1,0,1,1,1],
	"b" : [0,1,0,1,1,1,0],
	"c" : [1,1,1],
	"e" : [1,0,0,1,1,1,1],
	"x" : [1,0,0,0,1],
	"0" : [0] * WIDTH,
	"1" : [1] * WIDTH,
	"E" : [1] + [0] * (WIDTH-2) + [1],
	"S" : [0] * (WIDTH-2) + [1],
	"I" : [0,1] + [0] * (WIDTH-4) + [1,0],
}

def run(rule, state, iterations, s0=" ", s1="█"):
	I = iterations
	if (filter_r110_eth):
		print(colors.ENDC)
		while(I<0 or I>0):
			I -= 1
			eth=0
			for _ in range(len(state)):
				if (eth == 0):
					pe=state[_-1:_+6]
					if (pe in ether):
						eth=4-ether.index(pe)
						print(colors.CYAN,end='')
						s0="█"
				if (eth>0):
					eth -= 1
					if (eth==0): 
						print(colors.ENDC,end='')
						s0 = _s0
				if (state[_]==0):
					print(s0,end='')
				else: print(s1,end='')
			print()
			state = iterate(state, rule)
			time.sleep(step_delay)
		print(colors.ENDC)
	else:
		while(I!=0):
			if (I>0): I -= 1
			if (not silent_mode):
				for x in state:
					if x == 0:
						print(s0,end='')
					else: print(s1,end='')
				print()
				time.sleep(step_delay)
			state = iterate(state, rule)
		if (silent_mode):
			for x in state:
				print(x,end='');
	# print(colors.ENDC)	
	return state

if (not silent_mode):
	print(RULE.values())

if (evolutions!=[]):
	evolutions.insert(0,RULE)
	for r in evolutions:
		s = run(r, s, I, s0, s1)
elif (evolutionsr != []):
	while(True):
		s = run(RULE, s, I)
		run(r.choice(evolutionsr), s, r.randint(0,I))

elif ("--evolve-all" in sys.argv):
	for i in range(256):
		# print(i)
		if sum(s) == 0:
			s = patterns['S']
		elif sum(s) == WIDTH:
			s = patterns['I']
		rle = getrule(i)
		s = run(rle, s, I)

else:
	run(RULE, s, I, s0, s1)





