from itertools import product

# სიმრავლე X = {0, 1, 2} (პროგრამირებაში 0-დან ვიწყებთ ათვლას)
X = (0, 1, 2)
 
# ყველა შესაძლო ფუნქცია X -> X (სულ 3^3 = 27)
all_functions = list(product(X, repeat=len(X)))
 
# გავფილტროთ: არაბიექციური და არამუდმივი
# რანგი უნდა იყოს ზუსტად 2
test_functions = [f for f in all_functions if len(set(f)) == 2]

def compose(f, g):
    # f o g ნიშნავს f(g(x))
    return tuple(f[g[x]] for x in X)

def get_rank(f):
    return len(set(f))

i =0

# ჩავატაროთ ექსპერიმენტი ყველა წყვილისთვის
results = []
results_isomorphic = [] 
results_same_rank = []
for f in test_functions:
    for g in test_functions:
       
        fog = compose(f, g)
        gof = compose(g, f)
        # print(f"წყვილი {i}:")
        # i += 1
        # print(f"f: {f}, g: {g}")
        # print(f"f o g: {fog}, g o f: {gof}")    
        
        # ჩვენი ჰიპოთეზა: არაიზომორფულია თუ რანგები განსხვავდება
        is_isomorphic = get_rank(fog) == get_rank(gof)
        
        if not is_isomorphic:
            results.append((f, g, fog, gof))

        if is_isomorphic:
            results_isomorphic.append((f, g, fog, gof))
        if is_isomorphic and get_rank(fog) ==2 and get_rank(gof) ==2:
            results_same_rank.append((f, g, fog, gof))



# print(f"ნაპოვნია {len(results)} არაიზომორფული შემთხვევა.")
# print("მაგალითები:" )
# for f, g, fog, gof in results:
#     print(f"f: {f}, g: {g}")
#     print(f"f o g: {fog}, g o f: {gof}")
#     print()

# print("-----------------------------------------------------------------------")

# print(f"ნაპოვნია {len(results_isomorphic)} იზომორფული შემთხვევა.")
# print("მაგალითები:" )
# for f, g, fog, gof in results_isomorphic:
#     print(f"f: {f}, g: {g}")
#     print(f"f o g: {fog}, g o f: {gof}")
#     print()

print(f"ნაპოვნია {len(results_same_rank)} შემთხვევა, სადაც რანგები ტოლია.")
print("მაგალითები:" )
for f, g, fog, gof in results_same_rank:
    print(f"f: {f}, g: {g}")
    print(f"f o g: {fog}, g o f: {gof}")
    print()
