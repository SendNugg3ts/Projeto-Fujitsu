import numpy as np
import pandas as pd
from tabu import TabuSampler

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
Q1 = np.zeros((16, 16))
for i in range(n):
    for j in range(n):
        for t in range(n-1):
            linha = tradutor(t, i)
            coluna = tradutor(t+1, j)
            Q1[linha][coluna] = d[i][j]/2
            Q1[coluna][linha] = d[i][j]/2

df = pd.DataFrame(Q1)
df.to_excel("Q1.xlsx")



# criar o segundo Qubo
Q2 = np.zeros((16, 16))
P2= 110
for i in range(n):
    for t in range(n):
        linha = tradutor(t, i)
        for tt in range(n):
            coluna = tradutor(tt, i)
            if t == tt:
                Q2[linha][coluna] -= 1
            else:
                Q2[linha][coluna] += 2/2


Q2 = P2*Q2
df2 = pd.DataFrame(Q2)
df2.to_excel("Q2.xlsx")


# Criar o terceiro QUBO
Q3 = np.zeros((16, 16))
P3=110
for t in range(n):
    for i in range(n):
        linha = tradutor(t, i)
        for j in range(n):
            coluna = tradutor(t, j)
            if i == j:
                Q3[linha][coluna] -= 1
            else:
                Q3[linha][coluna] += 2/2

Q3= P3*Q3
df3 = pd.DataFrame(Q3)
df3.to_excel("Q3.xlsx")


Q= Q1+Q2+Q3


b = Q.transpose()
# Comparing both arrays using array_equal() method
if np.array_equal(Q, b):
    print("The array is Symmetric")
else:
    print("The array is Not Symmetric")



sampler = TabuSampler()
response = sampler.sample_qubo()
print(response)
# Encontrar a solução com menor energia
sample = response.first.sample

# Criar uma lista com as cidades visitadas
cidades_visitadas= [i for i in range(n) if sample[tradutor(t, i)] == 1]
cidades_visitadas.append(cidades_visitadas[0])  # Adicionar a última cidade visitada (primeira da lista)

# Mostrar a lista de cidades visitadas
print(cidades_visitadas)

