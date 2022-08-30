import time
import pandas as pd

def wait(seconds):
    time.sleep(seconds)

# cross up
def cross_up(a,b):
    old_short = a[len(a) - 3]
    short = a[len(a) - 2]
    now_short = a[len(a) - 1]

    old_long = b[len(b) - 3]
    long = b[len(b) - 2]
    now_long = b[len(b) - 1]

    if old_short < old_long and short > long and now_short > now_long: return True
    else: return False  

# cross down
def cross_down(a,b):
    old_short = a[len(a) - 3]
    short = a[len(a) - 2]
    now_short = a[len(a) - 1]

    old_long = b[len(b) - 3]
    long = b[len(b) - 2]
    now_long = b[len(b) - 1]

    if old_short > old_long and short < long and now_short < now_long: return True
    else: return False 

# controling the deep point
def is_deep(a):
    two_past = a[len(a) - 3]
    one_past = a[len(a) - 2]
    past = a[len(a) - 1]

    if two_past > one_past and past > one_past: return True
    else: return False

# controling the peak point
def is_peak(a):
    two_past = a[len(a) - 3]
    one_past = a[len(a) - 2]
    past = a[len(a) - 1]

    if two_past < one_past and past < one_past: return True
    else: return False

# retest Up
def retest_up(a,b):
    k3 = a[len(a) - 4]
    k2 = a[len(a) - 3]
    k1 = a[len(a) - 2]
    k0 = a[len(a) - 1]
    
    u3 = b[len(b) - 4]
    u2 = b[len(b) - 3]
    u1 = b[len(b) - 2]
    u0 = b[len(b) - 1]

    if k3 > k2 and k2 < k1 < k3 and k3 > u3 and k2 < u2 * 1.0008 and k1 > u1 * 1.0008 and k0 > u0: return True
    else: return False

# retest Down
def retest_down(a,b):
    k3 = a[len(a) - 4]
    k2 = a[len(a) - 3]
    k1 = a[len(a) - 2]
    k0 = a[len(a) - 1]
    
    u3 = b[len(b) - 4]
    u2 = b[len(b) - 3]
    u1 = b[len(b) - 2]
    u0 = b[len(b) - 1]

    if k3 < k2 and k2 > k1 > k3 and k3 < u3 and k2 > u2 * 1.0008 and k1 < u1 * 1.0008 and k0 < u0: return True
    else: return False

# highest and lowest candle functions
def highest(a, candles): return max(a.tail(candles))
def lowest(a, candles): return min(a.tail(candles))

# distance between two point
def distance(l,el):
    for i in l.index:
        if l[i] == el: return len(l) - i - 1
        else: None
    
