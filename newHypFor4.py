from itertools import product

# 1. სიმრავლე და შუალედური ფუნქციები
X = (0, 1, 2, 3)
n = len(X)
all_functions = list(product(X, repeat=n))
test_functions = [f for f in all_functions if 1 < len(set(f)) < n]

def get_kernel_blocks_sorted(f):
    blocks_dict = {}
    for x, y in enumerate(f):
        blocks_dict.setdefault(y, set()).add(x)
    blocks = list(blocks_dict.values())
    # დალაგება: ზომით (დიდიდან პატარასკენ), შემდეგ ელემენტებით (სტაბილურობისთვის)
    blocks.sort(key=lambda b: (len(b), sorted(list(b))), reverse=True)
    return blocks

def get_v_data(g, f):
    """აბრუნებს V_set-ს და V_sizes-ს (კარდინალურ პროფილს)"""
    img = set(g)
    sorted_blocks = get_kernel_blocks_sorted(f)
    v_set = tuple(block.intersection(img) for block in sorted_blocks)
    v_sizes = tuple(len(s) for s in v_set)
    return v_set, v_sizes

def compose(f, g):
    return tuple(f[g[x]] for x in X)

def get_rank(h):
    return len(set(h))

# -----------------------------------------------------------------------
# ანალიზი და ცხრილის მომზადება
# -----------------------------------------------------------------------

iso_candidates = []
non_iso_pairs = []

# ექსპერიმენტი (ავიღოთ პირველი 50 ფუნქცია საჩვენებლად)
for f in test_functions:
    for g in test_functions:
        v_set_gf, v_sizes_gf = get_v_data(g, f)
        v_set_fg, v_sizes_fg = get_v_data(f, g)
        
        # ახალი სიმეტრიული პირობა: ორივე მხრიდან შეკუმშვა უნდა იყოს იდენტური
        is_candidate = (v_sizes_gf == v_sizes_fg)
        
        data = {
            'f': f, 'g': g,
            'fog': compose(f, g),
            'gof': compose(g, f),
            'v_sizes_gf': v_sizes_gf,
            'v_sizes_fg': v_sizes_fg,
            'v_set_gf': v_set_gf,
            'v_set_fg': v_set_fg,
            'rank': get_rank(compose(f, g))
        }
        
        if is_candidate:
            iso_candidates.append(data)
        else:
            non_iso_pairs.append(data)

# def print_table(title, data_list, count=5):
#     print(f"\n{'='*145}")
#     print(f" {title} (სულ: {len(data_list)})")
#     print(f"{'='*145}")
#     header = f"{'f':<12} | {'g':<12} | {'R(comp)':<7} | {'V(g, f) ზომები':<15} | {'V(f, g) ზომები':<15} | {'V_set(g, f)':<35}"
#     print(header)
#     print("-" * 145)
    
#     for d in data_list[:count]:
#         print(f"{str(d['f']):<12} | {str(d['g']):<12} | {d['rank']:<7} | {str(d['v_sizes_gf']):<15} | {str(d['v_sizes_fg']):<15} | {str(d['v_set_gf']):<35}")
#         # სიმეტრიის საჩვენებლად მეორე ხაზზე გამოვიტანოთ საპირისპირო V_set
#         print(f"{'':<40} | {'V_set(f, g):':<15} | {str(d['v_set_fg']):<35}")
#         print("-" * 145)

# # ბეჭდვა
# print_table("ჯგუფი 1: იზომორფობის კანდიდატები (V(g, f) == V(f, g))", iso_candidates)
# print_table("ჯგუფი 2: არაიზომორფული წყვილები (V(g, f) != V(f, g))", non_iso_pairs)


def get_cycles(h):
    """აბრუნებს გრაფის ციკლურ სტრუქტურას (დალაგებულ სიგრძეებს)"""
    visited = [False] * n
    cycle_lengths = []
    
    # ვიპოვოთ ყველა ციკლი
    for i in range(n):
        if not visited[i]:
            path = []
            curr = i
            while not visited[curr]:
                visited[curr] = True
                path.append(curr)
                curr = h[curr]
            
            # შევამოწმოთ, ნამდვილად ციკლია თუ კუდი შევიდა არსებულ ციკლში
            if curr in path:
                cycle_start_idx = path.index(curr)
                cycle_lengths.append(len(path) - cycle_start_idx)
                
    return sorted(cycle_lengths)

# -----------------------------------------------------------------------
# კრიტიკული ანალიზი 524 კანდიდატისთვის
# -----------------------------------------------------------------------

counter_examples = []

for d in iso_candidates:
    # ვითვლით რეალურ ციკლურ სტრუქტურას
    cycles_fog = get_cycles(d['fog'])
    cycles_gof = get_cycles(d['gof'])
    
    # თუ პროფილები ტოლია, მაგრამ ციკლები სხვადასხვაა - ეს ჩვენი "ჩამჭრელი" მაგალითია!
    if cycles_fog != cycles_gof:
        d['cycles_fog'] = cycles_fog
        d['cycles_gof'] = cycles_gof
        counter_examples.append(d)

print(f"ნაპოვნია {len(counter_examples)} 'მოღალატე' წყვილი 524-დან.")

if counter_examples:
    print("\n[კრიტიკული მაგალითი - არაიზომორფული წყვილი იდენტური პროფილით]:")
    ce = counter_examples[0]
    print(f"f: {ce['f']}, g: {ce['g']}")
    print(f"V(g,f): {ce['v_sizes_gf']} | V(f,g): {ce['v_sizes_fg']}")
    print(f"fog ციკლები: {ce['cycles_fog']} | gof ციკლები: {ce['cycles_gof']}")