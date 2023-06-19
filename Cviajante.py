import itertools
import random
import time
cidades = ['Braga', 'Guimarães', 'Famalicão']
distancias = {
    ('Braga', 'Guimarães'): 24,
    ('Braga', 'Famalicão'): 27,
    ('Guimarães', 'Famalicão'): 32
}
city_count = 3
while True:
    start_time = time.time()
    #Adiciona uma nova cidade com distancia entre 20 e 400
    city_count += 1
    new_city = f"City{city_count}"
    cidades.append(new_city)
    for city in cidades[:-1]:
        dist = random.randint(20, 400)
        distancias[(city, new_city)] = dist
        distancias[(new_city, city)] = dist
    # Gera todas as permutações das cidades
    permutacoes = itertools.permutations(cidades)
    # Inicializa a menor distância como infinito
    menor_distancia = float('inf')
    # Itera sobre todas as permutações e calcula a distância total
    for permutacao in permutacoes:
        distancia_total = 0
        for i in range(len(permutacao) - 1):
            distancia = distancias.get((permutacao[i], permutacao[i+1]), 0)
            if distancia == 0:
                distancia = distancias.get((permutacao[i+1], permutacao[i]), 0)
            distancia_total += distancia
        distancia_total += distancias.get((permutacao[-1], permutacao[0]), 0)
        # Atualiza a menor distância
        if distancia_total < menor_distancia:
            menor_distancia = distancia_total
            melhor_rota = permutacao
    #Calcula o temo até chegar a mais de 1 minuto
    elapsed_time = time.time() - start_time
    print(elapsed_time)
    if elapsed_time > 60:
        break

print(f"Menor distância: {menor_distancia}")
print(f"Melhor rota: {melhor_rota}")
print(f"Número de Cidades: {city_count}")
