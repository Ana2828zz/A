import random

# Lista de nomes
nomes = ["Nome1", "Nome2", "Nome3", "Nome4", "Nome5"]

# Inicializar um dicionário para armazenar os resultados
result = {}

# Sortear e armazenar os resultados em variáveis separadas
for i in range(1, 11):
    result[f"tiro{i}"] = random.choice(nomes)

# Exemplo de acesso aos resultados individuais
print(result["tiro1"])
print(result["tiro2"])
print(result["tiro3"])
# E assim por diante...
