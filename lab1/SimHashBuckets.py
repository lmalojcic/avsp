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
    #ne prebacujem u bytes zbog lakseg uporedjivanja
    simhashes.append(sh)

candidates = {}
for i in range(0, 128, 16):
    bands = {}
    for j in range(n):
        sh = simhashes[j][i:i+16]
        sh = int(sh, 2)
        texts_in_band = []
        if (bands.get(sh) != None):
            texts_in_band = bands[sh]
            for text_id in texts_in_band:
                if (text_id == j):
                    continue
                if (candidates.get(j) == None):
                    candidates[j] = set()
                if (candidates.get(text_id) == None):
                    candidates[text_id] = set()
                candidates[j].add(text_id)
                candidates[text_id].add(j)
        else:
            texts_in_band = []
        texts_in_band.append(j)
        bands[sh] = texts_in_band

for query in all_queries:
    similar = 0
    hash_ind = int(query[0])
    hash = int(simhashes[hash_ind], 2)
    max_dist = int(query[1])
    for candidate in candidates[hash_ind]:
        xor = int(simhashes[candidate], 2) ^ hash
        hamming = bin(xor).count('1')
        if hamming <= max_dist:
            similar += 1
    print(similar)
        