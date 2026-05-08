import networkx as nx
import random
from collections import defaultdict

def get_point_depths(func, n):
    depths = {}
    for i in range(1, n + 1):
        path, curr = [], i
        while curr not in path:
            path.append(curr)
            curr = func[curr]
        cycle = set(path[path.index(curr):])
        curr, d = i, 0
        while curr not in cycle:
            d += 1
            curr = func[curr]
        depths[i] = d
    return depths

def calculate_trimmed_vector(f, g, n):
    """ითვლის V ვექტორს და აჭრის ბოლო ნულებს (სტანდარტიზაცია)."""
    f_depths = get_point_depths(f, n)
    max_d = max(f_depths.values()) if f_depths else 0
    v_vector = [0] * (max_d + 1)
    for i in range(1, n + 1):
        v_vector[f_depths[g[i]]] += 1
    
    # ნულების მოჭრა (Trimming)
    while v_vector and v_vector[-1] == 0:
        v_vector.pop()
    return tuple(v_vector)

def get_tree_function(n):
    f = {i: random.randint(1, n) for i in range(1, n + 1)}
    f[1] = 1
    for i in range(2, n + 1):
        visited, curr, path = {i}, f[i], [i]
        while curr != 1 and curr not in visited:
            visited.add(curr); path.append(curr); curr = f[curr]
        if curr != 1: f[path[-1]] = 1
    return f

def run_diagnostic_test(n_size, iterations, mode="tree"):
    false_positives = 0  # ვექტორები ტოლია, გრაფები - არა (გაეპარა არაიზომორფული)
    false_negatives = 0  # ვექტორები სხვადასხვაა, გრაფები - იზომორფულია (დაიწუნა სწორი)
    true_matches = 0     # ვექტორებიც ტოლია და გრაფებიც იზომორფულია
    
    print(f"\n--- დიაგნოსტიკური ტესტი: n={n_size}, რეჟიმი: {mode}, იტერაცია: {iterations} ---")
    
    for i in range(1, iterations + 1):
        if mode == "tree":
            f, g = get_tree_function(n_size), get_tree_function(n_size)
        else:
            f = {j: random.randint(1, n_size) for j in range(1, n_size + 1)}
            g = {j: random.randint(1, n_size) for j in range(1, n_size + 1)}
        
        # 1. ვექტორების შედარება (Trimmed)
        v1 = calculate_trimmed_vector(f, g, n_size)
        v2 = calculate_trimmed_vector(g, f, n_size)
        vectors_equal = (v1 == v2)
        
        # 2. რეალური იზომორფიზმის შემოწმება
        fog = {j: f[g[j]] for j in range(1, n_size + 1)}
        gof = {j: g[f[j]] for j in range(1, n_size + 1)}
        G1 = nx.DiGraph([(j, fog[j]) for j in range(1, n_size + 1)])
        G2 = nx.DiGraph([(j, gof[j]) for j in range(1, n_size + 1)])
        are_isomorphic = nx.is_isomorphic(G1, G2)
        
        # 3. შედეგების აღრიცხვა
        if vectors_equal and not are_isomorphic:
            false_positives += 1
        elif not vectors_equal and are_isomorphic:
            false_negatives += 1
        elif vectors_equal and are_isomorphic:
            true_matches += 1
            
        if i % 1000 == 0:
            print(f"დამუშავდა {i} წყვილი...")

    print("-" * 60)
    print(f"სტატისტიკა {iterations} მცდელობიდან:")
    print(f"✅ True Matches (ვექტორი მუშაობს): {true_matches}")
    print(f"❌ False Positives (ვექტორმა ვერ დაიჭირა სხვაობა): {false_positives}")
    print(f"⚠️ False Negatives (ვექტორმა არასწორად დაიწუნა იზომორფული): {false_negatives}")
    print("-" * 60)

# გაშვება
run_diagnostic_test(n_size=15, iterations=5000, mode="tree")