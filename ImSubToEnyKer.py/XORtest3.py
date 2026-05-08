from itertools import product

# 1. სიმრავლე X 
X = (0, 1, 2)
all_functions = list(product(X, repeat=len(X)))
test_functions = [f for f in all_functions if len(set(f)) == 2]

def get_kernel_blocks(f):
    blocks = {}
    for x, y in enumerate(f):
        blocks.setdefault(y, set()).add(x)
    return list(blocks.values())

def is_im_in_ker_block(img, kerf_blocks):
    img_set = set(img)
    return any(img_set.issubset(block) for block in kerf_blocks)

def compose(f, g):
    return tuple(f[g[x]] for x in X)

def get_rank(f):
    return len(set(f))

# სიები შედეგების დასახარისხებლად
cond_A_AND_B = []
cond_A_XOR_B = []
cond_NOT_A_NOT_B = []

for f in test_functions:
    for g in test_functions:
        fog = compose(f, g)
        gof = compose(g, f)
        
        # რანგები
        rf = get_rank(fog)
        rg = get_rank(gof)
        
        # ჰიპოთეზის პირობები
        cond_A = is_im_in_ker_block(set(g), get_kernel_blocks(f))
        cond_B = is_im_in_ker_block(set(f), get_kernel_blocks(g))
        
        # მონაცემების შენახვა: (f, g, fog, gof, rank_fog, rank_gof, ranks_equal)
        data = (f, g, fog, gof, rf, rg, rf == rg)
        
        if cond_A and cond_B:
            cond_A_AND_B.append(data)
        elif cond_A ^ cond_B:
            cond_A_XOR_B.append(data)
        elif not cond_A and not cond_B:
            cond_NOT_A_NOT_B.append(data)

def print_group(title, data_list):
    print(f"\n{'='*110}")
    print(f" {title} (სულ: {len(data_list)} შემთხვევა)")
    print(f"{'='*110}")
    # დავამატე სვეტი "რანგები ტოლია?"
    print(f"{'№':<4} | {'f':<10} | {'g':<10} | {'f o g':<10} | {'g o f':<10} | {'R(fog)':<6} | {'R(gof)':<6} | {'რანგები ტოლია?'}")
    print("-" * 110)
    for i, (f, g, fog, gof, rf, rg, eq) in enumerate(data_list, 1):
        print(f"{i:<4} | {str(f):<10} | {str(g):<10} | {str(fog):<10} | {str(gof):<10} | {rf:<6} | {rg:<6} | {str(eq):<15}")

# შედეგების გამოტანა
print_group("ჯგუფი 1: ორივე პირობა სრულდება (A AND B)", cond_A_AND_B)
print_group("ჯგუფი 2: მხოლოდ ერთი პირობა სრულდება (A XOR B)", cond_A_XOR_B)
print_group("ჯგუფი 3: არცერთი პირობა არ სრულდება (NOT A AND NOT B)", cond_NOT_A_NOT_B)

# # -------------------
# # უნიკალური კომპოზიციების ამოკრება მე-3 ჯგუფიდან
# unique_fog = set()
# unique_gof = set()

# for item in cond_NOT_A_NOT_B:
#     unique_fog.add(item[2]) # fog არის მე-3 ინდექსზე (data სიაში)
#     unique_gof.add(item[3]) # gof არის მე-4 ინდექსზე

# # ყველა უნიკალური კომპოზიციის გაერთიანება (რადგან fog და gof სიმეტრიულია ამ ჯგუფში)
# all_unique_results = unique_fog.union(unique_gof)

# print(f"\n{'='*60}")
# print(f" უნიკალური კომპოზიციები ჯგუფიდან (NOT A AND NOT B)")
# print(f"{'='*60}")
# print(f"სულ ნაპოვნია {len(all_unique_results)} უნიკალური ფუნქცია:")
# print("-" * 60)

# for i, func in enumerate(sorted(all_unique_results), 1):
#     print(f"{i}. {func} (Rank: {get_rank(func)})")

# -------------------------
# # უნიკალური წყვილების შესანახი სიმრავლე
# unique_pairs = set()

# for item in cond_NOT_A_NOT_B:
#     # item[2] არის fog, item[3] არის gof
#     # ვინახავთ როგორც tuple-ს, რადგან set-ს სჭირდება hashable ობიექტები
#     unique_pairs.add((item[2], item[3]))

# print(f"\n{'='*70}")
# print(f" ჯგუფი 3: (NOT A AND NOT B) - უნიკალური კომპოზიციური წყვილები")
# print(f"{'='*70}")
# print(f"ამ ჯგუფში არსებული 144 შემთხვევიდან, რეალურად გვაქვს {len(unique_pairs)} უნიკალური წყვილი.")
# print("-" * 70)
# print(f"{'№':<4} | {'f o g':<12} | {'g o f':<12} | {'შენიშვნა'}")
# print("-" * 70)

# for i, (fog, gof) in enumerate(sorted(unique_pairs), 1):
#     note = "fog == gof" if fog == gof else "fog != gof"
#     print(f"{i:<4} | {str(fog):<12} | {str(gof):<12} | {note}")

# print(f"\nდასკვნა: სულ {len(unique_pairs)} უნიკალური კომბინაცია.")


# --- ახალი ნაწილი: უნიკალური წყვილების ანალიზი კლასების მიხედვით ---

# თქვენ მიერ განსაზღვრული ეკვივალენტობის კლასები
# class_1 = {
#     (0, 0, 2), (0, 1, 0), (0, 1, 1), 
#     (0, 2, 2), (1, 1, 2), (2, 1, 2)
# }
# class_2 = {
#     (1, 0, 0), (1, 0, 1), (1, 2, 1), 
#     (2, 0, 0), (2, 2, 0), (2, 2, 1)
# }

# def get_class(func):
#     if func in class_1:
#         return "ტიპი 1"
#     if func in class_2:
#         return "ტიპი 2"
#     return "უცნობი"

# # უნიკალური წყვილების შესანახი სიმრავლე
# unique_pairs = set()
# for item in cond_NOT_A_NOT_B:
#     unique_pairs.add((item[2], item[3]))

# print(f"\n{'='*95}")
# print(f" ჯგუფი 3: უნიკალური წყვილები და სტრუქტურული იზომორფიზმი")
# print(f"{'='*95}")
# print(f"{'№':<4}|f | {'f o g':<10} | {'g o f':<10} | {'f o g ტიპი':<12} | {'g o f ტიპი':<12} | {'იზომორფულია?'}")
# print("-" * 95)

# for i, (fog, gof) in enumerate(sorted(unique_pairs), 1):
#     type_fog = get_class(fog)
#     type_gof = get_class(gof)
    
#     # იზომორფულია, თუ ორივე ერთსადაიმავე კლასშია
#     is_iso = "დიახ" if type_fog == type_gof else "არა"
    
#     print(f"{i:<4} | {str(fog):<10} | {str(gof):<10} | {type_fog:<12} | {type_gof:<12} | {is_iso}")

# print(f"\n[შენიშვნა]: 'დიახ' ნიშნავს, რომ წყვილის ორივე წევრი ვარდება ერთსა და იმავე ეკვივალენტობის კლასში.")