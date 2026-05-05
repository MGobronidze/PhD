from itertools import product

# 1. განვსაზღვროთ სიმრავლე X = {0, 1, 2, 3}
X = (0, 1, 2, 3)
n = len(X)

# 2. შევქმნათ ყველა შესაძლო ასახვა (4^4 = 256)
all_functions = list(product(X, repeat=n))

# 3. გავფილტროთ: გამოვრიცხოთ ბიექციები (რანგი 4) და მუდმივები (რანგი 1)
# დავიტოვოთ მხოლოდ შუალედური ფუნქციები (რანგი 2 და 3)
test_functions = [f for f in all_functions if 1 < len(set(f)) < n]

def get_kernel_blocks(f):
    blocks = {}
    for x, y in enumerate(f):
        blocks.setdefault(y, set()).add(x)
    return list(blocks.values())    

def is_im_in_ker_block(img, kerf_blocks):
    img_set = set(img)
    return any(img_set.issubset(block) for block in kerf_blocks)

def compose(f, g):
    # f o g ნიშნავს f(g(x))
    return tuple(f[g[x]] for x in X)

def get_rank(f):
    return len(set(f))
# ---------------------------------------§---------------------------------------

# # მონაცემთა შესანახი ჯგუფები
# same_rank_results = []
# different_rank_results = []

# # 4. ექსპერიმენტის გაშვება ყველა წყვილისთვის
# # for f in test_functions:
# #     for g in test_functions:
# #         fog = compose(f, g)
# #         gof = compose(g, f)
        
# #         rank_fog = get_rank(fog)
# #         rank_gof = get_rank(gof)
        
# #         if rank_fog == rank_gof:
# #             same_rank_results.append((f, g, fog, gof, rank_fog))
# #         else:
# #             different_rank_results.append((f, g, fog, gof, rank_fog, rank_gof))

# # # 5. შედეგების ანალიზისთვის გამოსატანი ბლოკი
# # print(f"სულ შემოწმდა {len(test_functions)} ფუნქცია.")
# # print(f"წყვილების ჯამური რაოდენობა: {len(test_functions)**2}")
# # print("-" * 50)
# # print(f"კომპოზიციები ტოლი რანგით: {len(same_rank_results)}")
# # print(f"კომპოზიციები განსხვავებული რანგით: {len(different_rank_results)}")
# # print("-" * 50)

# # # მაგალითების ჩვენება გასააზრებლად
# # print("\n[მაგალითები, სადაც რანგები განსხვავებულია]:")
# # # გამოვიტანოთ მხოლოდ პირველი 5 მაგალითი, რომ ეკრანი არ გადაიტვირთოს
# # for f, g, fog, gof, r1, r2 in different_rank_results[:5]:
# #     print(f"f: {f}, g: {g}")
# #     print(f"f o g: {fog} (Rank {r1})")
# #     print(f"g o f: {gof} (Rank {r2})")
# #     print("---")

# # print("\n[მაგალითები, სადაც რანგები ტოლია (მაგრამ ფუნქციები სხვადასხვაა)]:")
# # for f, g, fog, gof, r in same_rank_results[:5]:
# #     if fog != gof: # დავიტოვოთ მხოლოდ ისეთები, სადაც კომპოზიცია სხვადასხვაა
# #         print(f"f: {f}, g: {g}")
# #         print(f"f o g: {fog} (Rank {r})")
# #         print(f"g o f: {gof} (Rank {r})")
# #         print("---")

# print(test_functions)
# -----------------------------------------------------------------------   

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
# print_group("ჯგუფი 1: ორივე პირობა სრულდება (A AND B)", cond_A_AND_B)
# print_group("ჯგუფი 2: მხოლოდ ერთი პირობა სრულდება (A XOR B)", cond_A_XOR_B)
# print_group("ჯგუფი 3: არცერთი პირობა არ სრულდება (NOT A AND NOT B)", cond_NOT_A_NOT_B)

print(len(cond_A_AND_B))
print(len(cond_A_XOR_B))
print(len(cond_NOT_A_NOT_B))    