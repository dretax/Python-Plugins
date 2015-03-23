__author__ = 'DreTaX'
import time
import math

def Calc1():
    s = time.time()
    for i in xrange(750000):
        fct = i**.5
    print "Took %f seconds" % (time.time() - s)

def Calc2():
    s = time.time()
    for i in xrange(750000):
        fct = math.sqrt(i)
    print "Took %f seconds" % (time.time() - s)

def Calc3(arg=math.sqrt):
    s = time.time()
    for i in xrange(750000):
        fct = arg(i)
    print "Took %f seconds" % (time.time() - s)

Calc1()
Calc2()
Calc3()