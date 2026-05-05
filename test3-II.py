from itertools import product

# 1. სიმრავლე X = {0, 1, 2}
X = (0, 1, 2)
all_functions = list(product(X, repeat=len(X)))

# 2. ვიტოვებთ მხოლოდ საწყის Rank 2 ფუნქციებს (18 ფუნქცია)
test_functions = [f for f in all_functions if len(set(f)) == 2]

def compose(f, g):
    return tuple(f[g[x]] for x in X)

def get_rank(f):
    return len(set(f))

# 3. შევქმნათ სეტი უნიკალური შედეგების შესანახად
unique_rank2_results = set()

# 4. ჩავატაროთ ექსპერიმენტი
for f in test_functions:
    for g in test_functions:
        fog = compose(f, g)
        gof = compose(g, f)
        
        # თუ რანგი 2-ია, ვამატებთ სეტში (სეტი დუბლიკატებს ავტომატურად დასკიპავს)
        if get_rank(fog) == 2:
            unique_rank2_results.add(fog)
        if get_rank(gof) == 2:
            unique_rank2_results.add(gof)

# 5. დავბეჭდოთ შედეგები
print(f"სულ ნაპოვნია {len(unique_rank2_results)} უნიკალური ფუნქცია, რომელთა რანგი 2-ია.\n")

for i, func in enumerate(sorted(unique_rank2_results), 1):
    print(f"ფუნქცია {i}: {func}")