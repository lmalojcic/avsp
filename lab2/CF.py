import numpy as np
from decimal import Decimal, ROUND_HALF_UP
#Decimal(Decimal(x).quantize(Decimal('.001'), rounding=ROUND_HALF_UP))

def cf(ratings, i, j, k):
    ratings_f = []
    for l in range(len(ratings)):
        if l == i:
            og_user = ratings[l]
        elif l != i and ratings[l][j] != 0:
            ratings_f.append(np.array(ratings[l]))
    og_user = np.array(og_user)

    mean_of_non_zero_values = np.mean(og_user[og_user != 0])
    og_user = np.where(og_user != 0, og_user - mean_of_non_zero_values, og_user)

    similarities = []
    for l in range(len(ratings_f)):
        mean_of_non_zero_values = np.mean(ratings_f[l][ratings_f[l] != 0])
        temp = np.where(ratings_f[l] != 0, ratings_f[l] - mean_of_non_zero_values, ratings_f[l])
        similarities.append((l, np.corrcoef(og_user, temp)[0, 1], ratings_f[l][j]))

    top_k_similarities = sorted(similarities, key=lambda x: x[1], reverse=True)[:k]
    top_k_similarities = [similarity for similarity in top_k_similarities if similarity[1] > 0]

    weighted_sum = 0
    total_similarity = 0
    for similar_user, similarity, rating_other in top_k_similarities:
        weighted_sum += similarity * rating_other
        total_similarity += similarity

    print(Decimal(Decimal(weighted_sum / total_similarity).quantize(Decimal('.001'), rounding=ROUND_HALF_UP)))

temp = input()
n, m = temp.split()
n = int(n)
m = int(m)

ratings = [[0 for i in range(m)] for j in range(n)]

for i in range(n):
    temp = input()
    ratings[i] = [int(element) if element != 'X' else 0 for element in temp.split()]
ratings_t = [[ratings[j][i] for j in range(n)] for i in range(m)] #transponirana matrica za item_item

q = int(input())
for i in range(q):
    temp = input()
    temp = temp.split()
    if temp[2] == "0":
        cf(ratings, int(temp[0]) - 1, int(temp[1]) - 1, int(temp[3]))
    elif temp[2] == "1":
        cf(ratings_t, int(temp[1]) - 1, int(temp[0]) - 1, int(temp[3]))