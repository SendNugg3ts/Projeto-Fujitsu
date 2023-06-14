import numpy as np
import pandas as pd
import math
import time
import folium
from tabu import TabuSampler

# Matriz de distâncias
d = np.array([[0, 23, 23, 24],
              [23, 0, 40, 20],
              [23, 40, 0, 23],
              [24, 20, 23, 0]])

n = len(d)

def tradutor(row, col, n):
    ind_matriz = row * n + col
    return ind_matriz

# Criar o primeiro QUBO
Q1 = np.zeros((16, 16))
for i in range(n):
    for j in range(n):
        for t in range(n):
            linha = tradutor(t, i,n)
            if t == 3:
                coluna = tradutor(0, j,n)
            else:
                coluna = tradutor(t+1, j,n)
            Q1[linha][coluna] = d[i][j]/2
            Q1[coluna][linha] = d[i][j]/2

df = pd.DataFrame(Q1)
df.to_excel("Q1.xlsx")



# criar o segundo Qubo
Q2 = np.zeros((16, 16))
P2= 50
for i in range(n):
    for t in range(n):
        linha = tradutor(t, i,n)
        for tt in range(n):
            coluna = tradutor(tt, i,n)
            if t == tt:
                Q2[linha][coluna] -= 1
            else:
                Q2[linha][coluna] += 2/2


Q2 = P2*Q2
df2 = pd.DataFrame(Q2)
df2.to_excel("Q2.xlsx")


# Criar o terceiro QUBO
Q3 = np.zeros((16, 16))
P3=50
for t in range(n):
    for i in range(n):
        linha = tradutor(t, i,n)
        for j in range(n):
            coluna = tradutor(t, j,n)
            if i == j:
                Q3[linha][coluna] -= 1
            else:
                Q3[linha][coluna] += 2/2

Q3= P3*Q3
df3 = pd.DataFrame(Q3)
df3.to_excel("Q3.xlsx")

Q = Q1+Q2+Q3

sampler = TabuSampler()
response = sampler.sample_qubo(Q)
print(response)

response = np.array([0 , 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  0,  0,  1 ])#sem restrições
response = np.array([0,  0,  0,  1,  0,  1,  0,  0,  1,  0,  0,  0,  0,  0,  1,  0 ])#3, 1, 0, 2, 3
response = np.array([ 0 , 1 , 0 , 0 , 1 , 0 , 0 , 0 , 0 , 0 , 1 , 0 , 0 , 0 , 0  ,1])#1, 0, 2, 3, 1
np.reshape(response,(4,4))
# Encontrar a solução com menor energia
sample = response

# Criar uma lista com as cidades visitadas
cidades_visitadas = []
for t in range(n):
    cidade = [i for i in range(n) if sample[tradutor(t, i,n)] == 1]
    if cidade:
        cidades_visitadas.append(cidade[0])

# Adicionar a primeira cidade no final da lista
cidades_visitadas.append(cidades_visitadas[0])

# Mostrar a lista de cidades visitadas
print(cidades_visitadas)


def gerar_matriz(dimensao):
    matriz = np.zeros((dimensao, dimensao))  # Cria uma matriz de zeros com a dimensão desejada
    for i in range(dimensao):
        for j in range(i + 1, dimensao):
            matriz[i, j] = matriz[j, i] = np.random.randint(40, 700)  # Preenche os elementos com valores aleatórios entre 1 e 50
    return matriz


def QubosCreator(dimensao, matriz,inicio):
    n=dimensao
    d=matriz
    Q1 = np.zeros((n**2, n**2))
    for i in range(n):
        for j in range(n):
            for t in range(n):
                linha = tradutor(t, i,n)
                if t == n-1:
                    coluna = tradutor(0, j,n)
                else:
                    coluna = tradutor(t+1, j,n)
                Q1[linha][coluna] = d[i][j]/2
                Q1[coluna][linha] = d[i][j]/2
    # criar o segundo Qubo
    Q2 = np.zeros((dimensao**2, dimensao**2))
    P2= 420
    for i in range(n):
        for t in range(n):
            linha = tradutor(t, i,n)
            for tt in range(n):
                coluna = tradutor(tt, i,n)
                if t == tt:
                    Q2[linha][coluna] -= 1
                else:
                    Q2[linha][coluna] += 2/2
    Q2 = P2*Q2
    # Criar o terceiro QUBO
    Q3 = np.zeros((dimensao**2, dimensao**2))
    P3=400
    for t in range(n):
        for i in range(n):
            linha = tradutor(t, i,n)
            for j in range(n):
                coluna = tradutor(t, j,n)
                if i == j:
                    Q3[linha][coluna] -= 1
                else:
                    Q3[linha][coluna] += 2/2
    Q3= P3*Q3
    Q4 = np.zeros((dimensao**2, dimensao**2))
    P4=400
    posicao=legenda[inicio]
    for i in range(n):
        linha = tradutor(0, i,n)
        for j in range(n):
            coluna = tradutor(0, j,n)
            if i == posicao or j == posicao:
                Q4[linha][coluna] -= 1
            else:
                Q4[linha][coluna] += 2/2
    Q4 = P4 * Q4
    print(Q4)
    return Q1, Q2, Q3,Q4

def CidadesMax():
    sampler = TabuSampler()
    TEMPO=0
    n=131 #tempo que o meu pc demorou a correr antes de demorar 1 minuto, 131 cidades, CPU- I5-8600K
    while TEMPO < 60:
        n += 1
        start = time.time()
        matriz=gerar_matriz(n)
        Q1,Q2,Q3,Q4 = QubosCreator(n,matriz,"Braga")
        Q = Q1+Q2+Q3+Q4
        response = sampler.sample_qubo(Q)
        end = time.time()
        TEMPO = end - start
        print(TEMPO)       
    print(n)
    print(TEMPO)

def CaminhoOptimo(d,inicio):
    sampler = TabuSampler()
    n = len(d)
    Q1,Q2,Q3,Q4 = QubosCreator(n,d,inicio)
    Q = Q1+Q2+Q3+Q4
    response = sampler.sample_qubo(Q)  
    list_response = list(response.samples())
    #Converter sampler em caminho
    cidades_visitadas = []
    # transformar dicionario em matrix
    caminhoBinario = np.array(list(list_response[0].values()))
    shape = int(math.sqrt(len(caminhoBinario)))
    matriz = np.reshape(caminhoBinario, (shape, shape))
    n = len(matriz)
    for t in range(n):
        cidade = [i for i in range(n) if caminhoBinario[tradutor(t, i,n)] == 1]
        if cidade:
            cidades_visitadas.append(cidade[0])

    cidades_visitadas.append(cidades_visitadas[0])
    print(f"Solução:{cidades_visitadas}")
    return cidades_visitadas

def custo(d,legenda,inicio):
    caminho= CaminhoOptimo(d,inicio)
    caminho_legendado=[]
    for i in caminho:
        for cidade, indx in legenda.items():
            if i ==indx:
                caminho_legendado.append(cidade)
    print(f"Caminho ótimo: {caminho_legendado}")
    custo=0
    counter = len(caminho)
    for i, j in enumerate(caminho):
        if i  == counter-1:
            break
        cidade1= j
        cidade2= caminho[i+1]
        custo+= d[cidade1,cidade2]
    return caminho_legendado,custo
        
##############################################CRIAR A MATRIZ DE DISTÂNCIAS PARA OS 18 DISTRITOS#######################################################
# Função para converter graus em radianos
def degrees_to_radians(degrees):
    return degrees * np.pi / 180.0

# Função para calcular a distância em quilômetros entre duas coordenadas geográficas
def calcular_distancia(coord1, coord2):
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    radius = 6371  # Raio médio da Terra em quilômetros
    dlat = degrees_to_radians(lat2 - lat1)
    dlon = degrees_to_radians(lon2 - lon1)
    a = np.sin(dlat/2) * np.sin(dlat/2) + np.cos(degrees_to_radians(lat1)) * np.cos(degrees_to_radians(lat2)) * np.sin(dlon/2) * np.sin(dlon/2)
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    distance = radius * c
    return distance

# Coordenadas geográficas dos distritos (latitude, longitude)
coordenadas = {
    'Aveiro': (40.6405, -8.6538),
    'Beja': (38.0151, -7.8631),
    'Braga': (41.5454, -8.4265),
    'Bragança': (41.8071, -6.7583),
    'Castelo Branco': (39.8238, -7.4937),
    'Coimbra': (40.2110, -8.4293),
    'Évora': (38.5737, -7.9077),
    'Faro': (37.0179, -7.9307),
    'Guarda': (40.5370, -7.2673),
    'Leiria': (39.7442, -8.8070),
    'Lisboa': (38.7223, -9.1393),
    'Portalegre': (39.2938, -7.4313),
    'Porto': (41.1496, -8.6109),
    'Santarém': (39.2362, -8.6850),
    'Setúbal': (38.5244, -8.8945),
    'Viana do Castelo': (41.6918, -8.8349),
    'Vila Real': (41.3005, -7.7437),
    'Viseu': (40.6610, -7.9097)
}
legenda = {
    'Aveiro': 0,
    'Beja': 1,
    'Braga': 2,
    'Bragança': 3,
    'Castelo Branco': 4,
    'Coimbra': 5,
    'Évora': 6,
    'Faro': 7,
    'Guarda': 8,
    'Leiria': 9,
    'Lisboa': 10,
    'Portalegre': 11,
    'Porto': 12,
    'Santarém': 13,
    'Setúbal': 14,
    'Viana do Castelo': 15,
    'Vila Real': 16,
    'Viseu': 17
}

distritos = list(coordenadas.keys())
num_distritos = len(distritos)

# Criar uma matriz vazia para armazenar as distâncias
matriz_distancias = np.zeros((num_distritos, num_distritos))

# Calcular as distâncias em quilômetros entre os distritos
for i in range(num_distritos):
    for j in range(num_distritos):
        distancia = calcular_distancia(coordenadas[distritos[i]], coordenadas[distritos[j]])
        matriz_distancias[i, j] = distancia

ordem_distritos,custo_total=custo(matriz_distancias,legenda,"Braga")

print(f"Distância total:  {custo_total} km")
print(len(ordem_distritos))

guardar_resultados={}
for i in range(100):
    ordem_distritos,custo_total=custo(matriz_distancias,legenda,"Braga")
    guardar_resultados[i]= ordem_distritos, custo_total

melhor_custo = float('inf')  # inicializar com um valor infinito para encontrar o mínimo
melhor_ordem_distritos = None

for i in guardar_resultados:
    ordem_distritos, custo_total = guardar_resultados[i]
    if custo_total < melhor_custo:
        melhor_custo = custo_total
        melhor_ordem_distritos = ordem_distritos

print("Menor custo_total:", melhor_custo,"km")
print("Ordem distritos correspondente:", melhor_ordem_distritos)

 
def grafico_caminho(distritos):
    # Adiciona o primeiro distrito no final da lista para completar o ciclo
    distritos.append(distritos[0])
    # Extrai as coordenadas dos distritos
    coordenadas = grafico_coordenadas(distritos)
    # Cria um mapa centrado em Portugal continental
    mapa = folium.Map(location=[39.5, -8], zoom_start=7,tiles='CartoDB Positron')
    # Adiciona marcadores para cada distrito
    for i, coord in enumerate(coordenadas):
        distrito = distritos[i]
        folium.Marker(coord, popup=distrito, icon=folium.Icon(color="red")).add_to(mapa)
    # Adiciona uma linha para ligar os marcadores
    folium.PolyLine(coordenadas, color='black', weight=2.5, opacity=1).add_to(mapa)
    # Salva o mapa como um arquivo HTML
    mapa.save("mapa.html")



def grafico_coordenadas(distritos):
    coordenadas = {
        'Aveiro': (40.6405, -8.6538),
        'Beja': (38.0151, -7.8631),
        'Braga': (41.5454, -8.4265),
        'Bragança': (41.8071, -6.7583),
        'Castelo Branco': (39.8238, -7.4937),
        'Coimbra': (40.2110, -8.4293),
        'Évora': (38.5737, -7.9077),
        'Faro': (37.0179, -7.9307),
        'Guarda': (40.5370, -7.2673),
        'Leiria': (39.7442, -8.8070),
        'Lisboa': (38.7223, -9.1393),
        'Portalegre': (39.2938, -7.4313),
        'Porto': (41.1496, -8.6109),
        'Santarém': (39.2362, -8.6850),
        'Setúbal': (38.5244, -8.8945),
        'Viana do Castelo': (41.6918, -8.8349),
        'Vila Real': (41.3005, -7.7437),
        'Viseu': (40.6610, -7.9097)
    }

    return [coordenadas[distrito] for distrito in distritos]

grafico_caminho(melhor_ordem_distritos)
