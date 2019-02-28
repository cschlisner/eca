
# Usage
`$python3 eca.py <width> <rule> [-r] [-s0 <sym>] [-s1 <sym>] [-eth] [-d <delay>] [-p <pattern>]`

`<width>`       int >= 1 (width of automaton)

`<rule>`        int 1-256 (cellular automaton to simulate)

`-r`            randomize initial state (default sets all cells to 0 except rightmost)

`-s0 <sym>`     display 0 cells as `<sym>` (default = ' ')

`-s1 <sym>`     display 1 cells as `<sym>` (default = █)

`-eth`          show rule 110 background ether as different color (mostly-accurate)

`-d <delay>`    set delay between steps to `<delay>` seconds (default = 0.01)

`-p <pattern>`  supply initial state via string pattern. {0,1,a,b,c,B,E,x}* (see eca.py for pattern defs)

# Examples

600 cell Rule 110 with default parameters: 

`$python3 eca.py 600 110`

600 cell Rule 90 with randomized initial state:

`$python3 eca.py 600 90 -r`


![img](https://i.imgur.com/4NlddlB.png)
