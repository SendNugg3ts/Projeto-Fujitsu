import numpy as np
import pandas as pd

# Matriz de distâncias
d = np.array([[0, 23, 23, 24],
              [23, 0, 40, 20],
              [23, 40, 0, 23],
              [24, 20, 23, 0]])

n = len(d)

def tradutor(row, col):
    ind_matriz = row * 4 + col
    return ind_matriz

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

df = pd.DataFrame(Q1)
df.to_excel("Q1.xlsx")

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
                Q2[linha][coluna] += 1
            else:
                Q2[linha][coluna] -= 2
        Q2[linha][linha] += 2
Q2[N-1][N-1]=1
Q2 = P2*Q2


df = pd.DataFrame(Q2)

# Criar o terceiro QUBO
Q3 = np.zeros((17, 17))
P3=100
for t in range(n):
    for i in range(n):
        linha = tradutor(t, i)
        for j in range(n):
            coluna = tradutor(t, j)
            if i == j:
                Q3[linha][coluna] += 1
            else:
                Q3[linha][coluna] -= 2
        Q3[linha][linha] += 2
Q3[N-1][N-1]=1
Q3= P3*Q3

Q= Q1+Q2+Q3

from tabu import TabuSampler
sampler = TabuSampler()
response = sampler.sample_qubo(Q)

# Encontrar a solução com menor energia
sample = response.first.sample

# Criar uma lista com as cidades visitadas
cidades_visitadas= [i for i in range(n) if sample[tradutor(t, i)] == 1]
cidades_visitadas.append(cidades_visitadas[0])  # Adicionar a última cidade visitada (primeira da lista)

# Mostrar a lista de cidades visitadas
print(cidades_visitadas)

