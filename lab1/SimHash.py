import hashlib

n = int(input())
all_texts = []
for i in range(n):
    all_texts.append(input().split())

q = int(input())
all_queries = []
for i in range(q):
    all_queries.append(input().split())

simhashes = []
for text in all_texts:
    sh = [0] * 128
    for word in text:
        h = hashlib.md5(word.encode()).digest()
        b = ''.join(format(byte, '08b') for byte in h)
        for i in range(128):
            if b[i] == '1':
                sh[i] += 1
            else:
                sh[i] -= 1
    sh = [1 if x >= 0 else 0 for x in sh]
    sh = ''.join(str(x) for x in sh)
    bytes([int(sh[i:i+8], 2) for i in range(0, len(sh), 8)])
    simhashes.append(sh)

for query in all_queries:
    similar = 0
    hash_ind = int(query[0])
    hash = int(simhashes[hash_ind], 2)
    max_dist = int(query[1])
    for i in range(n):
        if i == hash_ind:
            continue
        xor = int(simhashes[i], 2) ^ hash
        hamming = bin(xor).count('1')
        if hamming <= max_dist:
            similar += 1
    print(similar)