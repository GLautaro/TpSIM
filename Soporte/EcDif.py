import pandas as pd
import numpy as np

def euler(h, a0, t0):
    r = []
    a = a0
    a1=0
    t=t0
    while (a > 0):
        da = -68-((a*a)/a0)
        a1 = a + h*da
        t = t + h
        r.append([t-h,a,da,t,a1])
        a=a1
    df2 = pd.DataFrame(np.array(r),
                   columns=['t', 'a', 'da/dt', 't+1', 'D+1'])
    return df2
    
z = euler(0.1, 1000, 0)
print(z)