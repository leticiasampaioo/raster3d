import numpy as np
import matplotlib.pyplot as plt
from test import create_line, create_open_box, create_cone, create_frustum

def bresenham_line(x0, y0, x1, y1, image):

    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    while True:
        if 0 <= x0 < image.shape[1] and 0 <= y0 < image.shape[0]:
            image[y0, x0] = 0  # Desenha o pixel (0 para cor preta em imagem binária)

        if x0 == x1 and y0 == y1:
            break

        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

def rasterize_objects(vertices_2d, faces, resolution):
    """ Rasteriza os objetos desenhando linhas entre os vértices manualmente. """
    # Cria uma imagem em branco (branco representado por 255)
    image = np.ones((resolution[1], resolution[0])) * 255

    # Escala os vértices para o tamanho da imagem
    scale_x = resolution[0] / (vertices_2d[:, 0].max() - vertices_2d[:, 0].min())
    scale_y = resolution[1] / (vertices_2d[:, 1].max() - vertices_2d[:, 1].min())
    scale = min(scale_x, scale_y)

    # Centraliza os vértices na imagem
    vertices_scaled = (vertices_2d - vertices_2d.min(axis=0)) * scale
    vertices_scaled[:, 1] = resolution[1] - vertices_scaled[:, 1]  # Inverte Y para coordenadas de imagem

    # Desenha as faces ou arestas
    for face in faces:
        for i in range(len(face)):
            start = vertices_scaled[face[i]].astype(int)
            end = vertices_scaled[face[(i + 1) % len(face)]].astype(int)
            bresenham_line(start[0], start[1], end[0], end[1], image)

    return image

def perspective_projection(vertices, focal_length=5, plane="xy"):
    if plane == "xy":
        vertices_2d = vertices[:, :2] / (vertices[:, 2:3] + focal_length)
    elif plane == "yz":
        vertices_2d = vertices[:, 1:] / (vertices[:, 0:1] + focal_length)
    elif plane == "zx":
        vertices_2d = vertices[:, [2, 0]] / (vertices[:, 1:2] + focal_length)
    else:
        raise ValueError("Plano de projeção inválido! Escolha entre 'xy', 'yz' ou 'zx'.")

    return vertices_2d

def rasterize_scene(object_index, resolutions):
    object_names = ["Caixa Aberta", "Cone", "Tronco de Cone", "Linha"]

    # Verifica se o índice do objeto é válido
    if object_index < 0 or object_index >= len(object_names):
        print("Índice de objeto inválido!")
        return

    # Cria o objeto selecionado
    if object_index == 0:
        vertices, faces = create_open_box()
    elif object_index == 1:
        vertices, faces = create_cone()
    elif object_index == 2:
        vertices, faces = create_frustum()
    elif object_index == 3:
        vertices, faces = create_line()
    else:
        print("Índice de objeto inválido!")
        return

    # Define os planos de projeção
    if object_index == 3:  # Se for a linha, projeta apenas no plano YZ
        planes = ["yz"]
    else:  # Para outros objetos, projeta apenas nos planos XY e YZ
        planes = ["xy", "yz"]

    # Rasteriza o objeto em cada resolução e plano
    for plane in planes:
        for idx, resolution in enumerate(resolutions):
            print(f"Rasterizando {object_names[object_index]} no plano {plane.upper()} em resolução {resolution}...")

            # Projeta os vértices em 2D no plano selecionado
            verts_2d = perspective_projection(vertices, focal_length=5, plane=plane)

            # Rasteriza o objeto na imagem
            img = rasterize_objects(verts_2d, faces, resolution)

            # Exibe a imagem usando matplotlib
            plt.figure(figsize=(8, 6))
            plt.title(f"{object_names[object_index]} ({plane.upper()} - {resolution[0]}x{resolution[1]})")
            plt.imshow(img, cmap="gray")
            plt.axis("off")  # Desativa os eixos
            plt.show()

if __name__ == "__main__":
    # Definir resoluções
    resolutions = [
        (320, 240),  # Resolução baixa
        (640, 480),  # Resolução média
        (1280, 720)  # Resolução alta
    ]

    while True:
        print("\nEscolha o objeto para rasterizar:")
        print("1 - Caixa Aberta")
        print("2 - Cone")
        print("3 - Tronco de Cone")
        print("4 - Linha")
        print("0 - Sair")
        escolha = input("Digite o número da opção desejada: ")

        # Verifica se o usuário quer sair
        if escolha == "0":
            print("Saindo...")
            break

        # Converte a escolha para inteiro e ajusta o índice
        try:
            object_index = int(escolha) - 1  # Subtrai 1 para corresponder aos índices dos objetos
        except ValueError:
            print("Entrada inválida! Digite um número válido.")
            continue

        # Verifica se o índice do objeto é válido
        if object_index < 0 or object_index >= 4:
            print("Índice de objeto inválido! Escolha um número entre 1 e 4.")
            continue

        # Rasteriza o objeto escolhido nas três resoluções
        rasterize_scene(object_index, resolutions)
