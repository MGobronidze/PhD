import itertools
import networkx as nx

def get_block_graph(h1, h2, n):
    """
    აგებს W(h1, h2) ბლოკების გრაფს.
    წვეროები: h2-ის კერნელური ბლოკები.
    ატრიბუტები: აქტიური წონა (a) და ტოტალური წონა (t).
    """
    elements = list(range(1, n + 1))
    im_h1 = set(h1.values())
    
    # 1. h2-ის კერნელური ბლოკების პოვნა
    ker_h2_dict = {}
    for x in elements:
        val = h2[x]
        ker_h2_dict.setdefault(val, []).append(x)
    
    # ბლოკებს მივანიჭოთ ინდექსები (0, 1, 2...) სტაბილურობისთვის
    blocks = list(ker_h2_dict.values())
    block_to_id = {}
    for i, block in enumerate(blocks):
        for x in block:
            block_to_id[x] = i # რომელი ელემენტი რომელ ბლოკშია
            
    # 2. შეწონილი ორიენტირებული გრაფის აგება
    W = nx.DiGraph()
    
    for i, block in enumerate(blocks):
        active_weight = len(set(block).intersection(im_h1))
        total_weight = len(block)
        
        # დავამატოთ კვანძი ატრიბუტებით
        W.add_node(i, a=active_weight, t=total_weight)
        
        # 3. გადასვლის პოვნა: h1(h2(B_i)) სად ხვდება?
        # ავიღოთ ბლოკის ნებისმიერი წარმომადგენელი, მაგ. block[0]
        rep = block[0]
        destination_element = h1[h2[rep]]
        
        # ვიპოვოთ რომელი h2-ის ბლოკის წარმომადგენელია h1-ის მიერ მიღებული მნიშვნელობა
        # რადგან h1(h2(x)) შეიძლება არ იყოს h2-ის იმიჯში, 
        # უნდა ვიპოვოთ h2-ის რომელი ბლოკი შეიცავს h1(h2(rep))-ს
        
        # მნიშვნელოვანია: h1(h2(rep)) ყოველთვის არის A-ს წევრი
        dest_block_id = None
        for b_id, b_cont in enumerate(blocks):
            if destination_element in b_cont:
                dest_block_id = b_id
                break
        
        W.add_edge(i, dest_block_id)
        
    return W

def are_block_graphs_isomorphic(W1, W2):
    # networkx ამოწმებს იზომორფიზმს კვანძების ატრიბუტების (a და t) გათვალისწინებით
    nm = nx.algorithms.isomorphism.categorical_node_match(['a', 't'], [0, 0])
    return nx.is_isomorphic(W1, W2, node_match=nm)

def solve(n):
    elements = list(range(1, n + 1))
    all_funcs_raw = list(itertools.product(elements, repeat=n))
    all_funcs = []
    for f_tuple in all_funcs_raw:
        all_funcs.append({i+1: val for i, val in enumerate(f_tuple)})
    
    print(f"Checking n={n} with Block Graph Theorem...")
    
    found_counterexample = False
    
    for f, g in itertools.product(all_funcs, repeat=2):
        # ვაგებთ W(f, g) და W(g, f)
        W_fg = get_block_graph(f, g, n)
        W_gf = get_block_graph(g, f, n)
        
        # ვამოწმებთ ბლოკების გრაფების იზომორფიზმს
        if are_block_graphs_isomorphic(W_fg, W_gf):
            # კომპოზიციები
            fog = {x: f[g[x]] for x in elements}
            gof = {x: g[f[x]] for x in elements}
            
            # ვამოწმებთ რეალურ იზომორფიზმს
            G1 = nx.DiGraph([(x, fog[x]) for x in elements])
            G2 = nx.DiGraph([(x, gof[x]) for x in elements])
            
            if not nx.is_isomorphic(G1, G2):
                print("\n!!! თეორიული შეცდომა (კონტრმაგალითი) !!!")
                print(f"f: {f}")
                print(f"g: {g}")
                found_counterexample = True
                break
                
    if not found_counterexample:
        print(f"\nთეორემა დადასტურდა n={n}-ისთვის!")

solve(5)