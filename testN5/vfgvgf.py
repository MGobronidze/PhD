from itertools import product
from collections import defaultdict, Counter

# ============================================================
# საბაზისო მონაცემები
# ============================================================

X = (0, 1, 2, 3, 4)
n = len(X)

all_functions = list(product(X, repeat=n))

# გამოვრიცხოთ:
# - მუდმივები
# - ბიექციები
test_functions = [
    f for f in all_functions
    if 1 < len(set(f)) < n
]

# ============================================================
# კომპოზიცია
# ============================================================

def compose(f, g):
    return tuple(f[g[x]] for x in X)

# ============================================================
# kernel კლასები
# ============================================================

def get_kernel_blocks_sorted(f):

    blocks_dict = defaultdict(set)

    for x, y in enumerate(f):
        blocks_dict[y].add(x)

    blocks = list(blocks_dict.values())

    # სტაბილური დალაგება
    blocks.sort(
        key=lambda b: (len(b), sorted(list(b))),
        reverse=True
    )

    return blocks

# ============================================================
# V(f,g)
# ============================================================

def get_v_sizes(g, f):

    img = set(g)

    blocks = get_kernel_blocks_sorted(f)

    vec = []

    for block in blocks:
        vec.append(len(block.intersection(img)))

    vec.sort(reverse=True)

    return tuple(vec)

# ============================================================
# ფუნქციური გრაფის სრული კანონიკური აღწერა
# ============================================================

def indegrees(f):

    deg = [0] * n

    for x in X:
        deg[f[x]] += 1

    return deg

# ------------------------------------------------------------

def find_cycles(f):

    visited = [0] * n
    cycles = []

    for start in X:

        if visited[start]:
            continue

        cur = start
        path = {}

        step = 0

        while True:

            if visited[cur]:
                break

            if cur in path:

                cyc = []

                keys = list(path.keys())
                idx = path[cur]

                cyc = keys[idx:]

                cycles.append(tuple(cyc))

                break

            path[cur] = step
            step += 1

            cur = f[cur]

        for v in path:
            visited[v] = 1

    return cycles

# ------------------------------------------------------------

def reverse_graph(f):

    rev = defaultdict(list)

    for x in X:
        rev[f[x]].append(x)

    return rev

# ------------------------------------------------------------

def rooted_tree_code(root, rev, forbidden):

    children = []

    for ch in rev[root]:

        if ch in forbidden:
            continue

        children.append(
            rooted_tree_code(ch, rev, forbidden)
        )

    children.sort()

    return "(" + "".join(children) + ")"

# ------------------------------------------------------------

def component_signature(f, cycle):

    rev = reverse_graph(f)

    cycset = set(cycle)

    tree_codes = []

    for v in cycle:

        code = rooted_tree_code(v, rev, cycset)

        tree_codes.append(code)

    # ციკლის როტაციების ნორმალიზაცია
    k = len(tree_codes)

    rotations = []

    for i in range(k):
        rot = tuple(tree_codes[i:] + tree_codes[:i])
        rotations.append(rot)

    return min(rotations)

# ------------------------------------------------------------

def graph_signature(f):

    cycles = find_cycles(f)

    sigs = []

    for cyc in cycles:

        sigs.append(component_signature(f, cyc))

    sigs.sort()

    return tuple(sigs)

# ============================================================
# მთავარი ძებნა
# ============================================================

counterexamples = []

checked = 0

for f in test_functions:

    for g in test_functions:

        # ------------------------------------
        # შენი კანდიდატი:
        # V(f,g)=V(g,f)
        # ------------------------------------

        if get_v_sizes(g, f) != get_v_sizes(f, g):
            continue

        fg = compose(f, g)
        gf = compose(g, f)

        sig_fg = graph_signature(fg)
        sig_gf = graph_signature(gf)

        # ------------------------------------
        # თუ არაიზომორფულია
        # ------------------------------------

        if sig_fg != sig_gf:

            counterexamples.append({
                "f": f,
                "g": g,
                "fg": fg,
                "gf": gf,
                "V(g,f)": get_v_sizes(g, f),
                "V(f,g)": get_v_sizes(f, g),
                "sig_fg": sig_fg,
                "sig_gf": sig_gf
            })

            print("\n===================================")
            print("ნაპოვნია კონტრმაგალითი!")
            print("===================================")

            print("\nf =", f)
            print("g =", g)

            print("\nfg =", fg)
            print("gf =", gf)

            print("\nV(g,f) =", get_v_sizes(g, f))
            print("V(f,g) =", get_v_sizes(f, g))

            print("\nSignature(fg) =", sig_fg)
            print("Signature(gf) =", sig_gf)

            raise SystemExit

        checked += 1

        if checked % 100000 == 0:
            print("შემოწმებულია:", checked)

# ============================================================

print("\n===================================")
print("კონტრმაგალითი ვერ მოიძებნა")
print("===================================")
print("შემოწმებული კანდიდატები:", checked)