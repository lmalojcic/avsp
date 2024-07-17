from math import floor

numBaskets = int(input())
s = float(input())
threshold = floor(s * numBaskets)

numBuckets = int(input())

items = {}

baskets = []

for i in range(numBaskets):
    basket = list(map(int, input().split()))
    baskets.append(basket)

for basket in baskets:
    for item in basket:
        if item in items:
            items[item] += 1
        else:
            items[item] = 1
len_items = len(items)

m = 0
for key, value in items.items():
    if value > threshold:
        m += 1
A = (m * (m - 1)) / 2

buckets = [0] * numBuckets

for basket in baskets:
    for i in range(len(basket)):
        for j in range(i + 1, len(basket)):
            if (items[basket[i]] >= threshold) and (items[basket[j]] >= threshold):
                buckets[(basket[i] * len_items + basket[j]) % numBuckets] += 1

pairs = {}

for basket in baskets:
    for i in range(len(basket)):
        for j in range(i + 1, len(basket)):
            if (items[basket[i]] >= threshold) and (items[basket[j]] >= threshold):
                if buckets[(basket[i] * len_items + basket[j]) % numBuckets] >= threshold:
                    if (basket[i], basket[j]) in pairs:
                        pairs[(basket[i], basket[j])] += 1
                    else:
                        pairs[(basket[i], basket[j])] = 1

print(int(A))
print(len(pairs))
for key, value in sorted(pairs.items(), key=lambda item: item[1], reverse=True):
    print(value)