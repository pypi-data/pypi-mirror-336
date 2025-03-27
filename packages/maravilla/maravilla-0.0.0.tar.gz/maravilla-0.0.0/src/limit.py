import math
import cmath
def sum(func,a,b):
    total = 0
    for i in range(a,b+1):
        total += func(i)
    return total

def integral(func,a,b,delta=0.001):
    total = 0
    x = a
    while x < b:
        total += func(x)*delta
        x += delta
    return total

def fourier_transform(func,delta=0.001,n=1000):
    def t1(e):
        def t2(x):
            return func(x) * cmath.exp(-cmath.sqrt(-1)*2*math.pi*e*x)
        return t2
    def transform(freq):
        return integral(t1(freq),-n,n,delta)
    return transform

