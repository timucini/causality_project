from numpy import random

def act_name():
    k = 70
    i = 600
    f = 1000
    g_z = random.normal()*f+i
    g_k = 70*(g_z)
    return g_k, g_z
for i in range(0, 100):
    print(act_name())