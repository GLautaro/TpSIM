import pandas as pd
import numpy as np

def euler(h, a0, t0):
    r = []
    a = a0
    a1 = a0
    t1 = 0
    t = t0
    while (a > 0):
        a = a1
        t = t1
        da = -68 - ((a * a) / a0)
        a1 = a + h * da
        t1 = t + h
        r.append([t, a, da, t1, a1])

    df2 = pd.DataFrame(np.array(r), columns=['t', 'A', 'dA/dt', 't(i+1)', 'A(i+1)'])
    return df2

def calcularTiempo(h, a0, t0):
    df = euler(h, a0, t0)
    df_aux = df.loc[df["A"] <= 0]
    tiempo = round(df_aux.iloc[0]["t"])
    return df, tiempo

def main():
    z = euler(0.1, 1000, 0)
    print(z)

if __name__ == "__main__":
    main()