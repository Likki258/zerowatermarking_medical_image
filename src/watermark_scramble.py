import numpy as np

def arnold_scramble(wm, iterations=5):
    N = wm.shape[0]
    scrambled = wm.copy()

    for _ in range(iterations):
        temp = np.zeros_like(scrambled)
        for x in range(N):
            for y in range(N):
                new_x = (x + y) % N
                new_y = (x + 2*y) % N
                temp[new_x, new_y] = scrambled[x, y]
        scrambled = temp

    return scrambled