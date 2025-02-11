import numpy as np

def generate_truncked_cone(altura=10, raio_base_maior=8, raio_base_menor=4, padding=5):
    # Dimensões totais da matriz
    diametro_base_maior = 2 * raio_base_maior
    matriz = np.zeros((
        altura + 2 * padding,
        diametro_base_maior + 2 * padding,
        diametro_base_maior + 2 * padding
    ))

    # Centro da base do tronco de cone
    centro_x = padding + raio_base_maior
    centro_z = padding + raio_base_maior

    # Gera o tronco de cone
    for y in range(altura):
        # Calcula o raio atual (interpola linearmente entre raio_base_maior e raio_base_menor)
        raio_atual = raio_base_maior - (raio_base_maior - raio_base_menor) * (y / altura)

        # Percorre os pontos no plano XZ para o nível y
        for x in range(matriz.shape[1]):
            for z in range(matriz.shape[2]):
                # Verifica se o ponto está dentro do círculo atual
                if (x - centro_x) ** 2 + (z - centro_z) ** 2 <= raio_atual ** 2:
                    matriz[padding + y, x, z] = 1

    return matriz