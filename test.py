import time
import random
import string

t0 = time.time()
b = []
for i in range(10**7):
    a = random.choice(string.ascii_lowercase)
    b.append(a)
open("bla.txt", "w").write(''.join(b))
d = time.time() - t0
print ("duration: %.2f s." % d)