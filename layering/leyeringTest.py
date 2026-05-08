import networkx as nx
import random

def get_point_depths(func, n):
    """ითვლის თითოეული წერტილის მანძილს ციკლამდე."""
    depths = {}
    for i in range(1, n + 1):
        path = []
        curr = i
        while curr not in path:
            path.append(curr)
            curr = func[curr]
        cycle_start_idx = path.index(curr)
        cycle = set(path[cycle_start_idx:])
        curr = i
        d = 0
        while curr not in cycle:
            d += 1
            curr = func[curr]
        depths[i] = d
    return depths

def get_influence_vector(f, g, n):
    """ითვლის V_{g -> f} ვექტორს."""
    f_depths = get_point_depths(f, n)
    g_values = [g[i] for i in range(1, n + 1)]
    max_d = max(f_depths.values())
    vector = [0] * (max_d + 1)
    for val in g_images: # შესწორება: g_values
        vector[f_depths[val]] += 1
    return vector

def calculate_influence_vector(f, g, n): # ოპტიმიზებული ვერსია
    f_depths = get_point_depths(f, n)
    v_vector = [0] * (max(f_depths.values()) + 1)
    for i in range(1, n + 1):
        v_vector[f_depths[g[i]]] += 1
    # ვაბრუნებთ ტუპლს შედარებისთვის და ვასუფთავებთ ბოლო ნულებს
    while v_vector and v_vector[-1] == 0:
        v_vector.pop()
    return tuple(v_vector)

def run_deep_test(n, iterations=10000):
    print(f"--- შრეობრივი თეორემის ტესტირება: n={n}, მცდელობა: {iterations} ---")
    
    for i in range(iterations):
        # შემთხვევითი ფუნქციების გენერაცია
        f = {j: random.randint(1, n) for j in range(1, n + 1)}
        g = {j: random.randint(1, n) for j in range(1, n + 1)}
        
        # 1. კომპოზიციების აწყობა
        fog = {j: f[g[j]] for j in range(1, n + 1)}
        gof = {j: g[f[j]] for j in range(1, n + 1)}
        
        # 2. ჩვენი ახალი პირობის შემოწმება (შრეობრივი ვექტორები)
        v_g_to_f = calculate_influence_vector(f, g, n)
        v_f_to_g = calculate_influence_vector(g, f, n)
        
        # 3. თუ ვექტორები ტოლია, ვამოწმებთ რეალურ იზომორფიზმს
        if v_g_to_f == v_f_to_g:
            G1 = nx.DiGraph([(j, fog[j]) for j in range(1, n + 1)])
            G2 = nx.DiGraph([(j, gof[j]) for j in range(1, n + 1)])
            
            if not nx.is_isomorphic(G1, G2):
                print(f"\n[!!!] ნაპოვნია კონტრმაგალითი {i+1} მცდელობაზე!")
                print(f"f = {f}")
                print(f"g = {g}")
                print(f"V-Vector: {v_g_to_f}")
                return f, g
        
        if (i + 1) % 1000 == 0:
            print(f"შემოწმდა {i + 1} წყვილი...")

    print("\nკონტრმაგალითი ვერ მოიძებნა. პირობა საკმარისია ამ შერჩევისთვის!")
    return None

# გაუშვით n=20 ან n=30-ისთვის
run_deep_test(n=100, iterations=2000)