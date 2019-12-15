import time
import random
from random import random
import dithering

last_string = None
t0 = time.time()
# open('random.txt', 'w')
with open('random.txt', 'a') as file:
    for f in range(5301):
        t1 = time.time()
        string = ''
        for x in range(426):
            for y in range(160):
                char = dithering.getClosestChar(random())
                if last_string == None or char != last_string[y + x * 160]:
                    string = string+char
                else:
                    string = string+'t'
        last_string = string
        file.write(string)
        progress = 'frame '+str(f)+'/5301'
        speed = str(round(time.time()-t1, 2)) + 's/frame'
        print(progress+', '+speed, end='\r', flush=True)

d = time.time() - t0
print ('\nduration: %.2fs.' % d)