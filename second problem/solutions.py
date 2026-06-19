import random
import networkx as nx
from itertools import permutations

n = 8  # თავისუფლად შეგიძლიათ შეცვალოთ 9 ან 10-ზეც, კოდი იფრენს!

def compose(f, g):
    # მათემატიკური (f o g)(x) = f(g(x))
    return [f[g[x]] for x in range(n)]

def inverse(p):
    q = [0] * n
    for i, v in enumerate(p):
        q[v] = i
    return q

def commute(f, g):
    return compose(f, g) == compose(g, f)

def random_function():
    return [random.randrange(n) for _ in range(n)]

def random_permutation():
    p = list(range(n))
    random.shuffle(p)
    return p

def to_graph(f):
    # ფუნქციას გარდაქმნის NetworkX გრაფად სწრაფი იზომორფიზმისთვის
    G = nx.DiGraph()
    for x in range(n):
        G.add_edge(x, f[x])
    return G

# ნამდვილი იზომორფიზმის შემოწმება NetworkX-ით (ძალიან სწრაფია)
def are_isomorphic_fast(f, g):
    G1 = to_graph(f)
    G2 = to_graph(g)
    return nx.is_isomorphic(G1, G2)

# თუ იზომორფულია, აღვადგინოთ კონკრეტული theta-ც ჩვენებისვის
def find_theta(f, g):
    for theta in permutations(range(n)):
        theta = list(theta)
        if all(theta[f[x]] == g[theta[x]] for x in range(n)):
            return theta
    return None

print(f"ვეძებთ მაგალითს n={n}-ისთვის...")

found = False
for trial in range(500000):  # გავზარდეთ ცდების რაოდენობა, რადგან კოდი სწრაფია
    f = random_function()
    g = random_function()
    delta = random_permutation()

    # პირობა 1: delta არ უნდა შედიოდეს f-ის და g-ს ცენტრალიზატორში
    if commute(delta, f) or commute(delta, g):
        continue

    # h1 = f o g
    h1 = compose(f, g)

    # h2 = f o delta o g o delta^(-1)
    del_inv = inverse(delta)
    # მათემატიკურად: delta o g o delta_inv
    # კოდში: del_g_delinv[x] = delta[g[del_inv[x]]]
    g_conjugated = [delta[g[del_inv[x]]] for x in range(n)]
    h2 = compose(f, g_conjugated)

    # პირობა 2: (A, h1) იზომორფულია (A, h2)-ის
    if are_isomorphic_fast(h1, h2):
        theta = find_theta(h1, h2)
        if theta is not None:
            print("\n--- მაგალითი მოიძებნა! ---")
            print(f"Trial: {trial}")
            print(f"f     = {f}")
            print(f"g     = {g}")
            print(f"delta = {delta}")
            print(f"theta = {theta}")
            print("\nშემოწმება:")
            print(f"f o g = {h1}")
            print(f"f o delta o g o delta^-1 = {h2}")
            found = True
            break

if not found:
    print("\nამ ცდებში მაგალითი ვერ მოიძებნა. შესაძლოა n უფრო დიდი უნდა იყოს.")