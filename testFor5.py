from itertools import product
from collections import defaultdict

# 1. სიმრავლე X = {0, 1, 2, 3, 4}
n = 5
X = tuple(range(n))
all_functions = list(product(X, repeat=n))

# 2. ვფილტრავთ შუალედურ ფუნქციებს (რანგი 2, 3, 4)
test_functions = [f for f in all_functions if 1 < len(set(f)) < n]
print(f"შემოწმდება {len(test_functions)} ფუნქცია.")
print(f"წყვილების მაქსიმალური რაოდენობა: {len(test_functions)**2:,}")

def get_kernel_blocks_sorted(f):
    blocks_dict = {}
    for x, y in enumerate(f):
        blocks_dict.setdefault(y, set()).add(x)
    blocks = list(blocks_dict.values())
    blocks.sort(key=lambda b: (len(b), sorted(list(b))), reverse=True)
    return blocks

def get_v_profile_sizes(g, f):
    img = set(g)
    sorted_blocks = get_kernel_blocks_sorted(f)
    # ვაბრუნებთ მხოლოდ ზომებს დალაგებულად
    v_sizes = tuple(sorted([len(block.intersection(img)) for block in sorted_blocks], reverse=True))
    return v_sizes

def compose(f, g):
    return tuple(f[g[x]] for x in X)

def get_cycles(h):
    visited = [False] * n
    cycle_lengths = []
    for i in range(n):
        if not visited[i]:
            path = []
            curr = i
            while not visited[curr]:
                visited[curr] = True
                path.append(curr)
                curr = h[curr]
            if curr in path:
                cycle_start_idx = path.index(curr)
                cycle_lengths.append(len(path) - cycle_start_idx)
    return tuple(sorted(cycle_lengths))

# -----------------------------------------------------------------------
# ოპტიმიზებული ძიება
# -----------------------------------------------------------------------

print("მიმდინარეობს ანალიზი...")
counter_examples = []
checked_pairs = 0

# რადგან 9 მილიონი წყვილი ბევრია, ვიყენებთ ოპტიმიზაციას:
# ჩვენ გვაინტერესებს მხოლოდ ისეთი (f,g), სადაც V(g,f) == V(f,g)
for i, f in enumerate(test_functions):
    if i % 100 == 0: print(f"დამუშავდა {i} ფუნქცია...")
    for g in test_functions:
        v_gf = get_v_profile_sizes(g, f)
        v_fg = get_v_profile_sizes(f, g)
        
        if v_gf == v_fg:
            fog = compose(f, g)
            gof = compose(g, f)
            
            cycles_fog = get_cycles(fog)
            cycles_gof = get_cycles(gof)
            
            if cycles_fog != cycles_gof:
                counter_examples.append({
                    'f': f, 'g': g,
                    'v_profile': v_gf,
                    'cycles_fog': cycles_fog,
                    'cycles_gof': cycles_gof
                })
                # თუ ერთი მაინც ვიპოვეთ, შეგვიძლია გამოვიტანოთ
                if len(counter_examples) == 1:
                    print("\n!!! პირველი საეჭვო წყვილი !!!")

# -----------------------------------------------------------------------
# შედეგები
# -----------------------------------------------------------------------
print(f"\nანალიზი დასრულდა. სულ ნაპოვნია {len(counter_examples)} საეჭვო წყვილი.")

for ce in counter_examples[:5]:
    print("-" * 50)
    print(f"f: {ce['f']}, g: {ce['g']}")
    print(f"საერთო V-პროფილი: {ce['v_profile']}")
    print(f"Cycles(f o g): {ce['cycles_fog']} | Cycles(g o f): {ce['cycles_gof']}")