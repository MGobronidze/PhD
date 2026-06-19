from itertools import permutations

def compose(f, g, n):
    return tuple(f[g[i]] for i in range(n))

def are_isomorphic_functional_graphs(f, g, n):
    # ფუნქციური გრაფები იზომორფულია ↔ ერთნაირი ციკლური სტრუქტურა
    # (სასრული პერმუტაციების შემთხვევაში)
    return cycle_type(f, n) == cycle_type(g, n)

def cycle_type(f, n):
    visited = [False]*n
    cycles = []
    for i in range(n):
        if not visited[i]:
            j, length = i, 0
            while not visited[j]:
                visited[j] = True
                j = f[j]
                length += 1
            cycles.append(length)
    return tuple(sorted(cycles))

def centralizer(h, n, sym):
    return [p for p in sym if compose(h, p, n) == compose(p, h, n)]

def N(f, g, n, sym):
    fg = compose(f, g, n)
    result = []
    for delta in sym:
        delta_inv = invert(delta, n)
        gdelta = compose(compose(delta, g, n), delta_inv, n)
        fgdelta = compose(f, gdelta, n)
        if are_isomorphic_functional_graphs(fg, fgdelta, n):
            result.append(delta)
    return result

def invert(p, n):
    inv = [0]*n
    for i in range(n): inv[p[i]] = i
    return tuple(inv)

n = 5
sym = list(permutations(range(n)))

for f in sym:
    for g in sym:
        fg = compose(f, g, n)
        Nfg = N(f, g, n, sym)
        Cfg = centralizer(fg, n, sym)
        Cfg_set = set(map(tuple, Cfg))
        for delta in Nfg:
            if tuple(delta) not in Cfg_set:
                print(f"კონტრმაგალითი!")
                print(f"f = {f}, g = {g}, delta = {delta}")
                break