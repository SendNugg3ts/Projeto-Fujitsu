import numpy as np

# Matriz de distâncias
d = np.array([[0, 23, 23, 24],
              [23, 0, 40, 20],
              [23, 40, 0, 23],
              [24, 20, 23, 0]])

n = len(d)

def tradutor(row, col):
    matrix_index = row * 4 + col
    return matrix_index

# Criar o primeiro QUBO
Q1 = np.zeros((17, 17))

for i in range(n):
    for j in range(n):
        for t in range(n):
            linha = tradutor(t, i)
            if t == n-1: #para considerar que quando t=3 então t+1=0
                coluna = tradutor(0, j)
            else:
                coluna = tradutor(t+1, j)
            Q1[linha][coluna] = d[i][j]


# criar o segundo Qubo
Q2 = np.zeros((17, 17))
N=len(Q2)
P2= 100
for i in range(n):
    for t in range(n):
        linha = tradutor(t, i)
        for tt in range(n):
            coluna = tradutor(tt, i)
            if t == tt:
                Q2[linha][coluna] += P2*1
            else:
                Q2[linha][coluna] -= P2*2
        Q2[linha][linha] += P2*1
Q2[N-1][N-1]=P2*1

# Criar o terceiro QUBO
Q3 = np.zeros((17, 17))
P3=100
for t in range(n):
    for i in range(n):
        linha = tradutor(t, i)
        for j in range(n):
            coluna = tradutor(t, j)
            if i == j:
                Q3[linha][coluna] += P3*1
            else:
                Q3[linha][coluna] -= P3*2
        Q3[linha][linha] += P3*1
Q3[N-1][N-1]=P3*1

Q= Q1+Q2+Q3

from tabu import TabuSampler
sampler = TabuSampler()
response = sampler.sample_qubo(Q)

# Encontrar a solução com menor energia
sample = response.first.sample

# Criar uma lista com as cidades visitadas
cities_visited = [i for i in range(n) if sample[tradutor(t, i)] == 1]
cities_visited.append(cities_visited[0])  # Adicionar a última cidade visitada (primeira da lista)

# Mostrar a lista de cidades visitadas
print(cities_visited)

