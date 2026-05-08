import networkx as nx
import random
from collections import Counter

def get_point_depths(func, n):
    """ითვლის თითოეული წერტილის მანძილს უახლოეს ციკლამდე (შრეებს)."""
    depths = {}
    for i in range(1, n + 1):
        path = []
        curr = i
        # ციკლის პოვნის ალგორითმი
        while curr not in path:
            path.append(curr)
            curr = func[curr]
        
        cycle_start_idx = path.index(curr)
        cycle = set(path[cycle_start_idx:])
        
        # მანძილის დათვლა ციკლამდე
        curr = i
        d = 0
        while curr not in cycle:
            d += 1
            curr = func[curr]
        depths[i] = d
    return depths

def calculate_influence_vector(f, g, n):
    """
    ითვლის V_{g -> f} ვექტორს.
    აღწერს, თუ როგორ ნაწილდება g-ს მნიშვნელობები f-ის შრეებში.
    """
    f_depths = get_point_depths(f, n)
    # g-ს მნიშვნელობათა სიმრავლე (Im(g))
    g_images = [g[i] for i in range(1, n + 1)]
    
    max_d = max(f_depths.values()) if f_depths else 0
    v_vector = [0] * (max_d + 1)
    
    for val in g_images:
        d = f_depths[val]
        v_vector[d] += 1
    
    # ვაშორებთ ბოლო ნულებს ვექტორის სტანდარტიზაციისთვის
    while v_vector and v_vector[-1] == 0:
        v_vector.pop()
    return tuple(v_vector)

def get_tree_function(n):
    """
    აგენერირებს ფუნქციას, რომელსაც აქვს მხოლოდ 1 ფიქსირებული წერტილი (ხე).
    ეს ქმნის ყველაზე რთულ სტრუქტურებს იზომორფიზმისთვის.
    """
    f = {i: random.randint(1, n) for i in range(1, n + 1)}
    f[1] = 1 # წერტილი 1 ხდება ფესვი (ციკლი)
    
    for i in range(2, n + 1):
        visited = {i}
        curr = f[i]
        path = [i]
        # ვწყვეტთ ნებისმიერ ციკლს, რომელიც არ არის 1
        while curr != 1 and curr not in visited:
            visited.add(curr)
            path.append(curr)
            curr = f[curr]
        
        if curr != 1: # თუ ვიპოვეთ ციკლი, გადავამისამართებთ 1-ისკენ
            f[path[-1]] = 1
    return f

def run_comprehensive_test(n_size, iterations, mode="random"):
    """
    მთავარი ტესტირების ფუნქცია.
    mode: "random" (ნებისმიერი ფუნქცია) ან "tree" (მხოლოდ ღრმა ხეები)
    """
    print(f"\n--- ტესტირება: n={n_size}, რეჟიმი: {mode}, მცდელობა: {iterations} ---")
    
    for i in range(1, iterations + 1):
        if mode == "tree":
            f = get_tree_function(n_size)
            g = get_tree_function(n_size)
        else:
            f = {j: random.randint(1, n_size) for j in range(1, n_size + 1)}
            g = {j: random.randint(1, n_size) for j in range(1, n_size + 1)}
        
        # 1. შრეობრივი ვექტორების გამოთვლა
        v_g_to_f = calculate_influence_vector(f, g, n_size)
        v_f_to_g = calculate_influence_vector(g, f, n_size)
        
        # 2. თუ ვექტორები ტოლია, ვამოწმებთ რეალურ იზომორფიზმს
        if v_g_to_f == v_f_to_g:
            # კომპოზიციების აწყობა
            fog = {j: f[g[j]] for j in range(1, n_size + 1)}
            gof = {j: g[f[j]] for j in range(1, n_size + 1)}
            
            G1 = nx.DiGraph([(j, fog[j]) for j in range(1, n_size + 1)])
            G2 = nx.DiGraph([(j, gof[j]) for j in range(1, n_size + 1)])
            
            if not nx.is_isomorphic(G1, G2):
                print(f"\n[!!!] კონტრმაგალითი ნაპოვნია {i}-ე მცდელობაზე!")
                print(f"f = {f}")
                print(f"g = {g}")
                print(f"V-ვექტორი: {v_g_to_f}")
                return f, g
        
        if i % 1000 == 0:
            print(f"გაიარა {i} წყვილმა...")

    print(f"\nდასრულდა წარმატებით! კონტრმაგალითი ვერ მოიძებნა.")
    return None

# --- გაშვება ---

# 1. ტესტი შემთხვევით ფუნქციებზე
run_comprehensive_test(n_size=20, iterations=5000, mode="random")

# 2. სტრეს-ტესტი ღრმა ხეებზე (უფრო მკაცრი შემოწმება)
run_comprehensive_test(n_size=15, iterations=5000, mode="tree")