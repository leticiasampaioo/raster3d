import numpy as np
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt  # Adicionado para exibir as imagens

from test_2 import create_scene

from test_4 import perspective_projection


# Função para rasterizar os objetos em uma imagem
def rasterize_objects(vertices_2d, faces, resolution):
    """
    Rasteriza os objetos em uma imagem com a resolução especificada.
    :param vertices_2d: Vértices projetados em 2D (shape: Nx2)
    :param faces: Faces do objeto (shape: Mx3)
    :param resolution: Resolução da imagem (largura, altura)
    :return: Imagem rasterizada
    """
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

    # Desenha as arestas
    for face in faces:
        face_cycle = np.append(face, face[0])  # Fecha o ciclo da face
        points = vertices_scaled[face_cycle].tolist()
        # Converte os pontos para uma lista de tuplas (x, y)
        points = [(int(p[0]), int(p[1])) for p in points]
        draw.line(points, fill="black", width=1)  # Desenha as arestas

    return img

# Função principal para rasterizar a cena em diferentes resoluções
def rasterize_scene(scene, resolutions):
    """
    Rasteriza a cena em diferentes resoluções.
    :param scene: Lista de objetos (vértices e faces) no sistema do mundo
    :param resolutions: Lista de resoluções (largura, altura)
    """
    for idx, resolution in enumerate(resolutions):
        print(f"Rasterizando em resolução {resolution}...")

        # Cria uma imagem para cada resolução
        img = Image.new("RGB", resolution, "white")
        draw = ImageDraw.Draw(img)

        # Rasteriza cada objeto na cena
        for verts, faces in scene:
            # Projeta os vértices em 2D (usando a função perspective_projection do código anterior)
            verts_2d = perspective_projection(verts, focal_length=5)

            # Rasteriza o objeto na imagem
            obj_img = rasterize_objects(verts_2d, faces, resolution)

            # Cola o objeto na imagem principal
            img.paste(obj_img, (0, 0))  # Removido o parâmetro mask

        # Salva a imagem
        img.save(f"rasterized_scene_{idx + 1}.png")

        # Exibe a imagem usando matplotlib
        plt.figure(figsize=(8, 6))
        plt.title(f"Resolução: {resolution[0]}x{resolution[1]}")
        plt.imshow(img)
        plt.axis("off")  # Desativa os eixos
        plt.show()

# Execução principal
if __name__ == "__main__":
    # Criar cena no sistema do mundo
    scene = create_scene()

    # Definir resoluções
    resolutions = [
        (320, 240),  # Resolução baixa
        (640, 480),  # Resolução média
        (1280, 720)  # Resolução alta
    ]

    # Rasterizar a cena em diferentes resoluções
    rasterize_scene(scene, resolutions)