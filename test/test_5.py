from PIL import Image, ImageDraw
import numpy as np
import matplotlib.pyplot as plt
from test import create_line, create_open_box, create_cone, create_frustum

def rasterize_objects(vertices_2d, faces, resolution):
    # Cria uma imagem em branco
    img = Image.new("RGB", resolution, "white")
    draw = ImageDraw.Draw(img)

    # Escala os vértices para o tamanho da imagem
    scale_x = resolution[0] / (vertices_2d[:, 0].max() - vertices_2d[:, 0].min())
    scale_y = resolution[1] / (vertices_2d[:, 1].max() - vertices_2d[:, 1].min())
    scale = min(scale_x, scale_y)

    # Centraliza os vértices na imagem
    vertices_scaled = (vertices_2d - vertices_2d.min(axis=0)) * scale
    vertices_scaled[:, 1] = resolution[1] - vertices_scaled[:, 1]  # Inverte Y para coordenadas de imagem

    # Desenha as faces ou arestas
    for face in faces:
        if len(face) == 2:  # Se for uma linha (dois vértices)
            start = tuple(vertices_scaled[face[0]])
            end = tuple(vertices_scaled[face[1]])
            draw.line([start, end], fill="black", width=1)
        else:  # Se for um polígono (mais de dois vértices)
            points = [tuple(vertices_scaled[v]) for v in face]
            draw.polygon(points, outline="black", fill=None)

    return img

def perspective_projection(vertices, focal_length=5, plane="xy"):
    if plane == "xy":
        vertices_2d = vertices[:, :2] / (vertices[:, 2:3] + focal_length)
    elif plane == "yz":
        vertices_2d = vertices[:, 1:] / (vertices[:, 0:1] + focal_length)
    elif plane == "zx":
        vertices_2d = vertices[:, [2, 0]] / (vertices[:, 1:2] + focal_length)
    else:
        raise ValueError("Plano de projeção inválido! Escolha entre 'xy', 'yz' ou 'zx'.")

    print("Vértices 2D projetados:", vertices_2d)  # Depuração
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

            # Salva a imagem
            img.save(f"rasterized_{object_names[object_index].replace(' ', '_')}_{plane}_{resolution[0]}x{resolution[1]}.png")

            # Exibe a imagem usando matplotlib
            plt.figure(figsize=(8, 6))
            plt.title(f"{object_names[object_index]} ({plane.upper()} - {resolution[0]}x{resolution[1]})")
            plt.imshow(img)
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


# #Só da linha
# import numpy as np
# from PIL import Image, ImageDraw
# import matplotlib.pyplot as plt  # Adicionado para exibir as imagens
#
# from test_2 import create_scene
#
# from test_4 import perspective_projection
#
# # Função para rasterizar os objetos em uma imagem
# def rasterize_objects(vertices_2d, faces, resolution):
#     """
#     Rasteriza os objetos em uma imagem com a resolução especificada.
#     :param vertices_2d: Vértices projetados em 2D (shape: Nx2)
#     :param faces: Faces do objeto (shape: Mx3)
#     :param resolution: Resolução da imagem (largura, altura)
#     :return: Imagem rasterizada
#     """
#     # Cria uma imagem em branco
#     img = Image.new("RGB", resolution, "white")
#     draw = ImageDraw.Draw(img)
#
#     # Escala os vértices para o tamanho da imagem
#     scale_x = resolution[0] / (vertices_2d[:, 0].max() - vertices_2d[:, 0].min())
#     scale_y = resolution[1] / (vertices_2d[:, 1].max() - vertices_2d[:, 1].min())
#     scale = min(scale_x, scale_y)
#
#     # Centraliza os vértices na imagem
#     vertices_scaled = (vertices_2d - vertices_2d.min(axis=0)) * scale
#     vertices_scaled[:, 1] = resolution[1] - vertices_scaled[:, 1]  # Inverte Y para coordenadas de imagem
#
#     # Desenha as arestas
#     for face in faces:
#         face_cycle = np.append(face, face[0])  # Fecha o ciclo da face
#         points = vertices_scaled[face_cycle].tolist()
#         # Converte os pontos para uma lista de tuplas (x, y)
#         points = [(int(p[0]), int(p[1])) for p in points]
#         draw.line(points, fill="black", width=1)  # Desenha as arestas
#
#     return img
#
# # Função principal para rasterizar a cena em diferentes resoluções
# def rasterize_scene(scene, resolutions):
#     """
#     Rasteriza a cena em diferentes resoluções.
#     :param scene: Lista de objetos (vértices e faces) no sistema do mundo
#     :param resolutions: Lista de resoluções (largura, altura)
#     """
#     for idx, resolution in enumerate(resolutions):
#         print(f"Rasterizando em resolução {resolution}...")
#
#         # Cria uma imagem para cada resolução
#         img = Image.new("RGB", resolution, "white")
#         draw = ImageDraw.Draw(img)
#
#         # Rasteriza cada objeto na cena
#         for verts, faces in scene:
#             # Projeta os vértices em 2D (usando a função perspective_projection do código anterior)
#             verts_2d = perspective_projection(verts, focal_length=5)
#
#             # Rasteriza o objeto na imagem
#             obj_img = rasterize_objects(verts_2d, faces, resolution)
#
#             # Cola o objeto na imagem principal
#             img.paste(obj_img, (0, 0))  # Removido o parâmetro mask
#
#         # Salva a imagem
#         img.save(f"rasterized_scene_{idx + 1}.png")
#
#         # Exibe a imagem usando matplotlib
#         plt.figure(figsize=(8, 6))
#         plt.title(f"Linha ({resolution[0]}x{resolution[1]})")
#         plt.imshow(img)
#         plt.axis("off")  # Desativa os eixos
#         plt.show()
#
# # Execução principal
# if __name__ == "__main__":
#     # Criar cena no sistema do mundo
#     scene = create_scene()
#
#     # Definir resoluções
#     resolutions = [
#         (320, 240),  # Resolução baixa
#         (640, 480),  # Resolução média
#         (1280, 720)  # Resolução alta
#     ]
#
#     # Rasterizar a cena em diferentes resoluções
#     rasterize_scene(scene, resolutions)
#

