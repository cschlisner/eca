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

# patterns 
ether = [[1,0,0,0,1,0,0],
		 [1,0,0,1,1,0,1],
		 [1,0,1,1,1,1,1]]
patterns = { 
	"0" : [0,0,0,0,0,0,0,0,0,0,0,0,0],
	"1" : [1,1,1,1,1,1,1,1,1,1,1,1,1],
	"a" : [0,0,0,1,1,1,0,1,1,1],
	"b" : [0,1,0,1,1,1,0],
	"B" : [0,0,0,1,0,0,1,1,0,1,1,1,1,1],
	"E" : [1,0,0,1,1,1,1],
	"c" : [1,1,1],
	"x" : [1,0,0,0,1]
}


"""
	Handle Command Line Input
"""

if (len(sys.argv) < 3):
	print("USAGE: $ python3 %s <width> <rule> [-r] [-s0 <sym>] [-s1 <sym>] [-eth] [-d <delay>] [-p <pattern>]" % sys.argv[0])
	print("\t<width>       int >= 1 (width of automaton)")
	print("\t<rule>        int 1-256 (cellular automaton to simulate)")
	print("\t-r            randomize initial state (default sets all cells to 0 except rightmost)")
	print("\t-s0 <sym>     display 0 cells as <sym> (default = ' ')")
	print("\t-s1 <sym>     display 1 cells as <sym> (default = █)")
	print("\t-eth          show rule 110 background ether as different color (mostly-accurate)")
	print("\t-d <delay>    set delay between steps to <delay> seconds (default = 0.01)")
	print("\t-p <pattern>  supply initial state via string pattern. {b,c}*")
	exit(0)

# s:= current state -- initialize randomly if user specified -r, otherwise set to 000...0001
s = []

if ("-p" in sys.argv): 
	for p in sys.argv[sys.argv.index("-p")+1]:
		s.extend(patterns.get(p))
elif ("-r" in sys.argv):
	s = [r.choice([0,1]) for _ in range(int(sys.argv[1]))]
else: s = [0] * int(sys.argv[1]) + [1]

# get rule specified by user
rule = getrule(int(sys.argv[2]))

# set symbols for output according to user -- defaults to block and space
s1 = "█" if ("-s1" not in sys.argv) else sys.argv[sys.argv.index("-s1")+1]
_s0 = s0 = " " if ("-s0" not in sys.argv) else sys.argv[sys.argv.index("-s0")+1]
filter_r110_eth = "-eth" in sys.argv
step_delay = 0.01 if ("-d" not in sys.argv) else float(sys.argv[sys.argv.index("-d")+1])

print(rule)
print(colors.ENDC)
print(s)
if (filter_r110_eth):
	while(True):
		eth=0
		for _ in range(len(s)):
			if (eth == 0):
				pe=s[_-1:_+6]
				if (pe in ether):
					eth=4-ether.index(pe)
					print(colors.CYAN,end='')
					s0="█"
			if (eth>0):
				eth -= 1
				if (eth==0): 
					print(colors.ENDC,end='')
					s0 = _s0
			if (s[_]==0):
				print(s0,end='')
			else: print(s1,end='')
		print()
		s = iterate(s, rule)
		time.sleep(step_delay)
else:
	while(True):
		for x in s:
			if x == 0:
				print(s0,end='')
			else: print(s1,end='')
		print()
		s = iterate(s, rule)
		time.sleep(step_delay)
print(colors.ENDC)
