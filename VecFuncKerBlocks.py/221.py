from itertools import product

n = 5
X = tuple(range(n))
target_profile = (2, 2, 1)

def get_v_profile_no_zeros(f, g):
    """V(g, f) გამოთვლა: f-ის ბლოკები და g-ს იმიჯი"""
    img_g = set(g)
    # f-ის კერნელური ბლოკები
    blocks_dict = {}
    for x, y in enumerate(f):
        blocks_dict.setdefault(y, set()).add(x)
    
    # მხოლოდ არაცარიელი თანაკვეთების ზომები
    v = sorted([len(b.intersection(img_g)) for b in blocks_dict.values() if b.intersection(img_g)], reverse=True)
    return tuple(v)

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

def find_specific_profile_pairs():
    print(f"ვეძებთ წყვილებს პროფილით {target_profile}...")
    
    # რადგან (2,2,1) ნიშნავს, რომ იმიჯში 5-ივე ელემენტი მონაწილეობს (2+2+1=5),
    # f და g უნდა იყვნენ მაღალი რანგის.
    all_f = list(product(X, repeat=n))
    # ვფილტრავთ მხოლოდ იმ ფუნქციებს, რომელთა რანგი მინიმუმ 3-ია
    filtered_f = [f for f in all_f if len(set(f)) >= 3]
    
    found_count = 0
    for i, f in enumerate(filtered_f):
        if i % 100 == 0:
            print(f"დამუშავდა {i} ფუნქცია...")
            
        for g in filtered_f:
            # ვამოწმებთ ორივე მიმართულებას
            v_gf = get_v_profile_no_zeros(f, g) # V(g, f)
            if v_gf != target_profile:
                continue
                
            v_fg = get_v_profile_no_zeros(g, f) # V(f, g)
            if v_fg == target_profile:
                # თუ ორივე პროფილი (2,2,1)-ია, ვამოწმებთ იზომორფიზმს
                fog = tuple(f[g[x]] for x in X)
                gof = tuple(g[f[x]] for x in X)
                
                cycles_fog = get_cycles(fog)
                cycles_gof = get_cycles(gof)
                
                found_count += 1
                print("-" * 40)
                print(f"წყვილი #{found_count}:")
                print(f"f: {f}")
                print(f"g: {g}")
                print(f"Cycles(f ∘ g): {cycles_fog}")
                print(f"Cycles(g ∘ f): {cycles_gof}")
                
                if cycles_fog != cycles_gof:
                    print("!!! კონტრმაგალითი ნაპოვნია !!!")
                    return # ვჩერდებით პირველივე შეცდომაზე
    
    print(f"\nძებნა დასრულდა. სულ ნაპოვნია {found_count} წყვილი {target_profile} პროფილით.")
    print("ყველა მათგანი აკმაყოფილებს იზომორფიზმის პირობას.")

if __name__ == "__main__":
    find_specific_profile_pairs()