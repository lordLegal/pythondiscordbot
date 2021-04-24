import time
s = time.strftime('%S')
x = time.strftime('%M')
int_x2 = int(x)
min_x = int_x2*60
int_s = int(s)
m = min_x + int_s

t = int(m)
g = t+120
print(g)
