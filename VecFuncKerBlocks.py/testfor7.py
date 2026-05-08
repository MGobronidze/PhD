import numpy as np
import random
import networkx as nx

def get_adjacency_matrix(func, n):
    matrix = np.zeros((n, n), dtype=int)
    for i in range(1, n + 1):
        matrix[i-1, func[i]-1] = 1
    return matrix

def get_rank_sequence(matrix, n):
    ranks = []
    current_matrix = matrix.copy()
    # ფუნქციურ გრაფებში რანგი მაქსიმუმ n ნაბიჯში სტაბილურდება
    for k in range(1, n + 1):
        rank = np.linalg.matrix_rank(current_matrix)
        ranks.append(int(rank))
        if rank == 0: # უსაფრთხოებისთვის
            ranks.extend([0] * (n - k))
            break
        current_matrix = np.matmul(current_matrix, matrix)
    return tuple(ranks)

def get_random_function(n):
    return {i: random.randint(1, n) for i in range(1, n + 1)}

def run_experiment(n, iterations=1000):
    print(f"--- ექსპერიმენტი n={n}, {iterations} ტესტი ---")
    elements = list(range(1, n + 1))
    
    counter_example_found = False
    
    for i in range(iterations):
        f = get_random_function(n)
        g = get_random_function(n)
        
        # 1. კომპოზიციები
        fog = {x: f[g[x]] for x in elements}
        gof = {x: g[f[x]] for x in elements}
        
        # 2. რანგული მიმდევრობების შედარება (ჩვენი თეორემა)
        M_fog = get_adjacency_matrix(fog, n)
        M_gof = get_adjacency_matrix(gof, n)
        
        ranks_fog = get_rank_sequence(M_fog, n)
        ranks_gof = get_rank_sequence(M_gof, n)
        
        # 3. რეალური იზომორფიზმის შემოწმება (ვალიდაცია)
        if ranks_fog == ranks_gof:
            G_fog = nx.DiGraph([(x, fog[x]) for x in elements])
            G_gof = nx.DiGraph([(x, gof[x]) for x in elements])
            
            if not nx.is_isomorphic(G_fog, G_gof):
                print(f"\n[!] ნაპოვნია კონტრმაგალითი {i+1} მცდელობაზე!")
                print(f"f = {f}")
                print(f"g = {g}")
                print(f"Rank Sequence: {ranks_fog}")
                counter_example_found = True
                break
        
        if (i + 1) % 100 == 0:
            print(f"შემოწმდა {i + 1} წყვილი...")

    if not counter_example_found:
        print(f"\nთეორემა წარმატებით გატესტდა {iterations}-ჯერ n={n}-ისთვის. კონტრმაგალითი არ მოიძებნა.")

# გამოძახება n=20-ისთვის (შეგიძლიათ შეცვალოთ iterations რაოდენობა)
run_experiment(n=20, iterations=500)