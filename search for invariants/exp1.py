from itertools import product
from collections import defaultdict

# ============================================================
#   MONO-UNARY ALGEBRA EXPERIMENT (OPTIMIZED)
#
#   იგნორირდება შემთხვევები:
#       • f ბიექცია
#       • g ბიექცია
#       • f მუდმივი
#       • g მუდმივი
#       • f = g
#       • fg = gf
#
#   მიზანი:
#       ვიპოვოთ არატრივიალური შემთხვევები,
#       სადაც (A,fg) ≅ (A,gf)
#       ან არა.
#
# ============================================================


# ------------------------------------------------------------
# კომპოზიცია
# ------------------------------------------------------------

def compose(f, g):
    n = len(f)
    return tuple(f[g[x]] for x in range(n))


# ------------------------------------------------------------
# ფუნქციის ტიპები
# ------------------------------------------------------------

def is_bijective(f):
    return len(set(f)) == len(f)


def is_constant(f):
    return len(set(f)) == 1


# ------------------------------------------------------------
# შვილების სია
# ------------------------------------------------------------

def children_map(f):

    ch = defaultdict(list)

    for x, y in enumerate(f):
        ch[y].append(x)

    return ch


# ------------------------------------------------------------
# ციკლების პოვნა
# ------------------------------------------------------------

def find_cycles(f):

    n = len(f)

    used = [False] * n

    cycles = []

    for s in range(n):

        if used[s]:
            continue

        pos = {}
        x = s
        step = 0

        while True:

            if used[x]:
                break

            if x in pos:

                cyc = []

                y = x

                while True:
                    cyc.append(y)
                    y = f[y]

                    if y == x:
                        break

                cycles.append(tuple(sorted(cyc)))
                break

            pos[x] = step
            step += 1
            x = f[x]

        for z in pos:
            used[z] = True

    return sorted(set(cycles))


# ------------------------------------------------------------
# rooted tree canonical type
# ------------------------------------------------------------

def rooted_type(f, root):

    ch = children_map(f)

    cycle_vertices = set()

    for cyc in find_cycles(f):
        cycle_vertices.update(cyc)

    memo = {}

    def dfs(x):

        if x in memo:
            return memo[x]

        sub = []

        for y in ch[x]:

            if y == x:
                continue

            # სხვა cycle-ში არ შევიდეთ
            if y in cycle_vertices and y != root:
                continue

            sub.append(dfs(y))

        sub.sort()

        typ = tuple(sub)

        memo[x] = typ

        return typ

    return dfs(root)


# ------------------------------------------------------------
# canonical signature
# ------------------------------------------------------------

def algebra_signature(f):

    sig = []

    for cyc in find_cycles(f):

        k = len(cyc)

        cyc_types = []

        for c in cyc:
            cyc_types.append(rooted_type(f, c))

        cyc_types.sort()

        sig.append((k, tuple(cyc_types)))

    sig.sort()

    return tuple(sig)


# ------------------------------------------------------------
# იზომორფიზმი
# ------------------------------------------------------------

def are_isomorphic(f, g):

    return algebra_signature(f) == algebra_signature(g)


# ------------------------------------------------------------
# ფუნქციის ბეჭდვა
# ------------------------------------------------------------

def print_function(name, f):

    print(name)

    for i, v in enumerate(f):
        print(f"  {i} -> {v}")

    print()


# ------------------------------------------------------------
# ყველა არასაინტერესო ფუნქციის გაფილტვრა
# ------------------------------------------------------------

def generate_nontrivial_functions(n):

    A = range(n)

    good = []

    for f in product(A, repeat=n):

        if is_bijective(f):
            continue

        if is_constant(f):
            continue

        good.append(tuple(f))

    return good


# ------------------------------------------------------------
# მთავარი ექსპერიმენტი
# ------------------------------------------------------------

def experiment(n=5, max_examples=15):

    funcs = generate_nontrivial_functions(n)

    total = 0
    iso_count = 0
    noniso_count = 0

    iso_examples = []
    noniso_examples = []

    for f in funcs:

        for g in funcs:

            # ----------------------------------------
            # ზედმეტი შემთხვევების გამოტოვება
            # ----------------------------------------

            if f == g:
                continue

            fg = compose(f, g)
            gf = compose(g, f)

            if fg == gf:
                continue

            total += 1

            iso = are_isomorphic(fg, gf)

            if iso:

                iso_count += 1

                if len(iso_examples) < max_examples:
                    iso_examples.append((f, g, fg, gf))

            else:

                noniso_count += 1

                if len(noniso_examples) < max_examples:
                    noniso_examples.append((f, g, fg, gf))

    # ========================================================
    # RESULTS
    # ========================================================

    print("=" * 70)
    print("RESULTS")
    print("=" * 70)

    print(f"n = {n}")
    print(f"tested pairs        = {total}")
    print(f"isomorphic pairs    = {iso_count}")
    print(f"non-isomorphic      = {noniso_count}")

    print()

    # ========================================================
    # ISOMORPHIC
    # ========================================================

    print("=" * 70)
    print("ISOMORPHIC EXAMPLES")
    print("=" * 70)

    for i, (f, g, fg, gf) in enumerate(iso_examples):

        print(f"\nExample #{i+1}\n")

        print_function("f", f)
        print_function("g", g)

        print_function("fg", fg)
        print_function("gf", gf)

        print("signature(fg) =", algebra_signature(fg))
        print("signature(gf) =", algebra_signature(gf))

        print("-" * 50)

    # ========================================================
    # NON-ISOMORPHIC
    # ========================================================

    print("=" * 70)
    print("NON-ISOMORPHIC EXAMPLES")
    print("=" * 70)

    for i, (f, g, fg, gf) in enumerate(noniso_examples):

        print(f"\nExample #{i+1}\n")

        print_function("f", f)
        print_function("g", g)

        print_function("fg", fg)
        print_function("gf", gf)

        print("signature(fg) =", algebra_signature(fg))
        print("signature(gf) =", algebra_signature(gf))

        print("-" * 50)


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    # n=5 რეკომენდებულია
    # n=6 უკვე საკმაოდ მძიმეა
    # n=7 brute force პრაქტიკულად შეუძლებელია

    experiment(n=5)
    print("\nExperiment completed.")