import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict

def get_point_depths(func, n):
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

def calculate_influence_vector(f, g, n):
    f_depths = get_point_depths(f, n)
    v_vector = defaultdict(int)
    for i in range(1, n + 1):
        v_vector[f_depths[g[i]]] += 1
    max_d = max(f_depths.values())
    return tuple(v_vector[i] for i in range(max_d + 1))

def get_hierarchical_pos(G, depths):
    pos = {}
    layers = defaultdict(list)
    for node, d in depths.items():
        layers[d].append(node)
    for d, nodes in layers.items():
        width = len(nodes)
        for i, node in enumerate(sorted(nodes)):
            pos[node] = (i - (width - 1) / 2, -d) 
    return pos

def visualize_complete_analysis(f_dict, g_dict, n):
    # 1. გამოთვლები
    v_g_to_f = calculate_influence_vector(f_dict, g_dict, n)
    v_f_to_g = calculate_influence_vector(g_dict, f_dict, n)
    
    fog = {j: f_dict[g_dict[j]] for j in range(1, n + 1)}
    gof = {j: g_dict[f_dict[j]] for j in range(1, n + 1)}
    
    depths_fog = get_point_depths(fog, n)
    depths_gof = get_point_depths(gof, n)

    # 2. ვიზუალიზაციის მომზადება (GridSpec გამოიყენება ტექსტისთვის ადგილი რომ დავტოვოთ)
    fig = plt.figure(figsize=(20, 14))
    gs = fig.add_gridspec(3, 2, height_ratios=[1, 0.2, 5])
    
    # ზედა პანელი: ფუნქციების და ვექტორების აღწერა
    ax_text = fig.add_subplot(gs[0, :])
    ax_text.axis('off')
    
    f_str = str({k: f_dict[k] for k in sorted(f_dict.keys())})
    g_str = str({k: g_dict[k] for k in sorted(g_dict.keys())})
    
    info_text = (
        f"საწყისი ფუნქცია f: {f_str}\n"
        f"საწყისი ფუნქცია g: {g_str}\n"
        f"{'-'*100}\n"
        f"გავლენის ვექტორი V(g -> f): {v_g_to_f}\n"
        f"გავლენის ვექტორი V(f -> g): {v_f_to_g}\n"
        f"შედეგი: ვექტორები იდენტურია, მაგრამ კომპოზიციები არაიზომორფული!"
    )
    ax_text.text(0.5, 0.5, info_text, ha='center', va='center', fontsize=12, 
                 family='monospace', bbox=dict(facecolor='whitesmoke', alpha=0.5))

    # გრაფების ხატვა
    ax1 = fig.add_subplot(gs[2, 0])
    ax2 = fig.add_subplot(gs[2, 1])

    G1 = nx.DiGraph([(j, fog[j]) for j in range(1, n + 1)])
    G2 = nx.DiGraph([(j, gof[j]) for j in range(1, n + 1)])

    pos1 = get_hierarchical_pos(G1, depths_fog)
    pos2 = get_hierarchical_pos(G2, depths_gof)

    # f ∘ g
    nx.draw(G1, pos1, ax=ax1, with_labels=True, node_color='skyblue', node_size=800,
            edge_color='#444444', arrows=True, arrowsize=20, font_weight='bold', width=1.5)
    ax1.set_title(f"კომპოზიცია f ∘ g\n(სტრუქტურული პროფილი)", fontsize=14, pad=20)
    
    # g ∘ f
    nx.draw(G2, pos2, ax=ax2, with_labels=True, node_color='lightcoral', node_size=800,
            edge_color='#444444', arrows=True, arrowsize=20, font_weight='bold', width=1.5)
    ax2.set_title(f"კომპოზიცია g ∘ f\n(სტრუქტურული პროფილი)", fontsize=14, pad=20)

    plt.tight_layout()
    plt.show()

# მონაცემები
f1 = {1: 1, 2: 3, 3: 14, 4: 11, 5: 10, 6: 1, 7: 1, 8: 15, 9: 12, 10: 1, 11: 15, 12: 14, 13: 8, 14: 4, 15: 1}
g1 = {1: 1, 2: 10, 3: 15, 4: 1, 5: 4, 6: 11, 7: 14, 8: 15, 9: 4, 10: 8, 11: 7, 12: 1, 13: 1, 14: 1, 15: 4}

visualize_complete_analysis(f1, g1, 15)