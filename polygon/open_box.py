import numpy as np

def generate_open_box(altura=10, largura=10, profundidade=10, espessura=1, padding=5):

    # Dimensões totais da matriz
    matriz = np.zeros((
        altura + 2 * padding,
        largura + 2 * padding + 2 * espessura,
        profundidade + 2 * padding + 2 * espessura
    ))

    # Coordenadas iniciais das paredes
    px = padding
    py = padding + espessura
    pz = padding + espessura

    # Parede frontal e traseira
    matriz[px:px + altura, py:py + largura, pz - espessura:pz] = 1  # Frente
    matriz[px:px + altura, py:py + largura, pz + profundidade:pz + profundidade + espessura] = 1  # Trás

    # Paredes laterais
    matriz[px:px + altura, py - espessura:py, pz - espessura:pz + profundidade + espessura] = 1  # Esquerda
    matriz[px:px + altura, py + largura:py + largura + espessura,
    pz - espessura:pz + profundidade + espessura] = 1  # Direita

    # Fundo da caixa
    matriz[px:px + espessura, py - espessura:py + largura + espessura, pz - espessura:pz + profundidade + espessura] = 1

    # Remove a tampa superior
    matriz[px + altura - espessura:px + altura, py:py + largura, pz:pz + profundidade] = 0

    return matriz