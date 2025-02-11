import numpy as np

def generate_cone(altura=10, raio_base=5, padding=5):
    # Dimensões totais da matriz
    diametro_base = 2 * raio_base
    matriz = np.zeros((
        altura + 2 * padding,
        diametro_base + 2 * padding,
        diametro_base + 2 * padding
    ))

    # Centro da base do cone
    centro_x = padding + raio_base
    centro_z = padding + raio_base

    # Gera o cone
    for y in range(altura):
        # Calcula o raio atual (decresce linearmente com a altura)
        raio_atual = raio_base * (1 - y / altura)

        # Percorre os pontos no plano XZ para o nível y
        for x in range(matriz.shape[1]):
            for z in range(matriz.shape[2]):
                # Verifica se o ponto está dentro do círculo atual
                if (x - centro_x) ** 2 + (z - centro_z) ** 2 <= raio_atual ** 2:
                    matriz[padding + y, x, z] = 1

    return matriz