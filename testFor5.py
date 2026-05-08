import random
from collections import Counter

# 1. პარამეტრები
n = 20  # სიმრავლის ზომა
max_attempts = 1_000_000  # რამდენი შემთხვევითი წყვილი შევამოწმოთ

def get_kernel_blocks_sorted(f):
    blocks_dict = {}
    for x, y in enumerate(f):
        blocks_dict.setdefault(y, set()).add(x)
    # ვიღებთ მხოლოდ ბლოკების ზომებს (უფრო სწრაფია)
    return sorted([len(b) for b in blocks_dict.values()], reverse=True)

def get_v_profile_sizes(g, f_kernel_blocks_indices, img_g):
    """ოპტიმიზებული პროფილი: მხოლოდ არანულოვანი ზომები"""
    v_sizes = []
    for block in f_kernel_blocks_indices:
        intersection_size = len(block.intersection(img_g))
        if intersection_size > 0:
            v_sizes.append(intersection_size)
    return tuple(sorted(v_sizes, reverse=True))

def get_f_data(f):
    """წინასწარ ამზადებს ფუნქციის კერნელურ ბლოკებს (ინდექსებს) და იმიჯს"""
    blocks_dict = {}
    for x, y in enumerate(f):
        blocks_dict.setdefault(y, set()).add(x)
    return list(blocks_dict.values()), set(f)

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

def compose(f, g):
    return tuple(f[x] for x in g) # უფრო სწრაფი ჩანაწერი პითონისთვის

print(f"დაიწყო n={n} შემთხვევების ძიება ({max_attempts:,} ცდა)...")

found = 0
for attempt in range(1, max_attempts + 1):
    # შემთხვევითი ფუნქციების გენერაცია (რანგი 2-დან n-1-მდე)
    f = tuple(random.randint(0, n-1) for _ in range(n))
    g = tuple(random.randint(0, n-1) for _ in range(n))
    
    # ვფილტრავთ რანგს (რომ არ იყოს ტრივიალური)
    rf, rg = len(set(f)), len(set(g))
    if rf < 2 or rf == n or rg < 2 or rg == n:
        continue

    # მონაცემების მომზადება
    f_blocks, f_img = get_f_data(f)
    g_blocks, g_img = get_f_data(g)

    # V-პროფილების შედარება
    v_gf = get_v_profile_sizes(g, f_blocks, g_img)
    v_fg = get_v_profile_sizes(f, g_blocks, f_img)

    if v_gf == v_fg:
        fog = compose(f, g)
        gof = compose(g, f)
        
        cycles_fog = get_cycles(fog)
        cycles_gof = get_cycles(gof)
        
        if cycles_fog != cycles_gof:
            print(f"\n[!] ნაპოვნია კონტრმაგალითი {attempt}-ე ცდაზე!")
            print(f"f: {f}")
            print(f"g: {g}")
            print(f"V-პროფილი: {v_gf}")
            print(f"Cycles(f o g): {cycles_fog} | Cycles(g o f): {cycles_gof}")
            found += 1
            break # პირველივეზე ვჩერდებით

    if attempt % 50000 == 0:
        print(f"შემოწმდა {attempt} წყვილი...")

if found == 0:
    print(f"\n{max_attempts} შემთხვევით წყვილში 'მოღალატე' ვერ მოიძებნა.")