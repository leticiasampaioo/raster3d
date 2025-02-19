import numpy as np
import matplotlib.pyplot as plt
from test_3 import transform_to_camera, look_at
from test_3 import create_scene

def projetar_xy(vertices):
    return vertices[:, [0, 1]]  # Seleciona apenas as coordenadas X e Y

def projetar_yz(vertices):
    return vertices[:, [1, 2]]  # Seleciona apenas as coordenadas Y e Z

def projetar_zx(vertices):
    return vertices[:, [2, 0]]  # Seleciona apenas as coordenadas Z e X

def perspective_projection(vertices, d=4):

    x = vertices[:, 0] / (vertices[:, 2] + d)  # Divide X por (Z + d)
    y = vertices[:, 1] / (vertices[:, 2] + d)  # Divide Y por (Z + d)
    return np.column_stack((x, y))

def plot_2d_edges(vertices_2d, faces, color='b'):

    for face in faces:
        face_cycle = np.append(face, face[0])  # Fechar o ciclo da face
        plt.plot(vertices_2d[face_cycle, 0], vertices_2d[face_cycle, 1], color=color, linewidth=1)

def plot_projection(scene, transformation_matrix, projection_func, title, xlabel, ylabel):

    colors = ['blue', 'green', 'red', 'purple']
    plt.figure(figsize=(6, 5))
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)

    # Para cada objeto na cena, aplica a transformação e projeção
    for idx, (verts, faces) in enumerate(scene):
        cam_verts = transform_to_camera(verts, transformation_matrix)  # Converte para as coordenadas da câmera
        verts_2d = projection_func(cam_verts)  # Aplica a projeção no plano 2D
        plot_2d_edges(verts_2d, faces, color=colors[idx % len(colors)])  # Desenha as arestas do objeto

    plt.show()

def menu():
    print("Escolha o tipo de projeção:")
    print("1 - Projeção Ortogonal")
    print("2 - Projeção em Perspectiva")
    print("3 - Ambos")
    choice = input("Digite o número da opção desejada: ")

    if choice == "1":
        # Projeção Ortogonal
        plot_projection(scene, transformation_matrix, projetar_xy, "Projeção Ortogonal XY", "X", "Y")
        plot_projection(scene, transformation_matrix, projetar_yz, "Projeção Ortogonal YZ", "Y", "Z")
        plot_projection(scene, transformation_matrix, projetar_zx, "Projeção Ortogonal ZX", "Z", "X")
    elif choice == "2":
        # Projeção em Perspectiva
        plot_projection(scene, transformation_matrix, perspective_projection, "Projeção em Perspectiva", "X", "Y")
    elif choice == "3":
        # Ambos
        plot_projection(scene, transformation_matrix, projetar_xy, "Projeção Ortogonal XY", "X", "Y")
        plot_projection(scene, transformation_matrix, projetar_yz, "Projeção Ortogonal YZ", "Y", "Z")
        plot_projection(scene, transformation_matrix, projetar_zx, "Projeção Ortogonal ZX", "Z", "X")
        plot_projection(scene, transformation_matrix, perspective_projection, "Projeção em Perspectiva", "X", "Y")
    else:
        print("Opção inválida. Por favor, execute o programa novamente e escolha uma opção válida.")

    return choice

if __name__ == "__main__":

    scene = create_scene()

    # Definir parâmetros da câmera
    camera_eye = np.array([10, 10, 10])  # Posição da câmera
    camera_target = np.array([0, 0, 0])  # Ponto de foco
    camera_up = np.array([0, 0, 1])      # Vetor para cima

    # Calcula a matriz de transformação homogênea (rotação + translação)
    transformation_matrix = look_at(camera_eye, camera_target, camera_up)

    choice = menu()


# import numpy as np
# import matplotlib.pyplot as plt
# from skimage.measure import marching_cubes
#
# # Funções para criar objetos (com arestas)
# def create_open_box(side=2, height=1, wall_thickness=0.1, resolution=50):
#     """
#     Caixa aberta sem tampa com base quadrada
#     :return: vertices (Nx3), faces (Mx3), edges (Kx2)
#     """
#     x = np.linspace(-side/2, side/2, resolution)
#     y = np.linspace(-side/2, side/2, resolution)
#     z = np.linspace(0, height, resolution)
#
#     X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
#
#     outer = (np.abs(X) <= side/2) & (np.abs(Y) <= side/2) & (Z <= height)
#     inner = (np.abs(X) <= side/2 - wall_thickness) & \
#             (np.abs(Y) <= side/2 - wall_thickness) & \
#             (Z >= wall_thickness)
#
#     volume = outer & ~inner
#
#     vertices, faces, _, _ = marching_cubes(
#         volume,
#         level=0.5,
#         spacing=(x[1]-x[0], y[1]-y[0], z[1]-z[0])
#     )
#
#     edges = extract_edges(faces)  # Extrai as arestas
#     return vertices, faces, edges
#
# def create_cone(radius=1, height=2, resolution=50):
#     """
#     Cone completo
#     :return: vertices (Nx3), faces (Mx3), edges (Kx2)
#     """
#     x = np.linspace(-radius, radius, resolution)
#     y = np.linspace(-radius, radius, resolution)
#     z = np.linspace(0, height, resolution)
#
#     X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
#
#     cone_radius = radius * (1 - Z/height)
#     volume = (np.sqrt(X**2 + Y**2) <= cone_radius) & (Z >= 0)
#
#     vertices, faces, _, _ = marching_cubes(
#         volume,
#         level=0.5,
#         spacing=(x[1]-x[0], y[1]-y[0], z[1]-z[0])
#     )
#
#     edges = extract_edges(faces)  # Extrai as arestas
#     return vertices, faces, edges
#
# def create_frustum(r_lower=1, r_upper=0.5, height=2, resolution=50):
#     """
#     Tronco de cone (frustum)
#     :return: vertices (Nx3), faces (Mx3), edges (Kx2)
#     """
#     max_radius = max(r_lower, r_upper)
#     x = np.linspace(-max_radius, max_radius, resolution)
#     y = np.linspace(-max_radius, max_radius, resolution)
#     z = np.linspace(0, height, resolution)
#
#     X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
#
#     current_radius = r_lower + (r_upper - r_lower) * (Z / height)
#     volume = (np.sqrt(X**2 + Y**2) <= current_radius) & (Z >= 0)
#
#     vertices, faces, _, _ = marching_cubes(
#         volume,
#         level=0.5,
#         spacing=(x[1]-x[0], y[1]-y[0], z[1]-z[0])
#     )
#
#     edges = extract_edges(faces)  # Extrai as arestas
#     return vertices, faces, edges
#
# def create_line(length=3, radius=0.05, resolution=50):
#     """
#     Linha reta representada como cilindro fino
#     :return: vertices (Nx3), faces (Mx3), edges (Kx2)
#     """
#     x = np.linspace(-radius, radius, resolution)
#     y = np.linspace(-radius, radius, resolution)
#     z = np.linspace(0, length, resolution)
#
#     X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
#
#     volume = (np.sqrt(X**2 + Y**2) <= radius) & (Z >= 0)
#
#     vertices, faces, _, _ = marching_cubes(
#         volume,
#         level=0.5,
#         spacing=(x[1]-x[0], y[1]-y[0], z[1]-z[0])
#     )
#
#     edges = extract_edges(faces)  # Extrai as arestas
#     return vertices, faces, edges
#
# def extract_edges(faces):
#     """
#     Extrai as arestas a partir das faces.
#     :param faces: Matriz de faces (Mx3)
#     :return: Arestas únicas (Kx2)
#     """
#     edges = set()
#     for face in faces:
#         edges.add(tuple(sorted((face[0], face[1]))))
#         edges.add(tuple(sorted((face[1], face[2]))))
#         edges.add(tuple(sorted((face[2], face[0]))))
#     return np.array(list(edges))
#
# # Funções de transformação geométrica
# def rotate_x(vertices, degrees):
#     theta = np.radians(degrees)
#     rot = np.array([
#         [1, 0, 0],
#         [0, np.cos(theta), -np.sin(theta)],
#         [0, np.sin(theta), np.cos(theta)]
#     ])
#     return np.dot(vertices, rot.T)
#
# def rotate_y(vertices, degrees):
#     theta = np.radians(degrees)
#     rot = np.array([
#         [np.cos(theta), 0, np.sin(theta)],
#         [0, 1, 0],
#         [-np.sin(theta), 0, np.cos(theta)]
#     ])
#     return np.dot(vertices, rot.T)
#
# def rotate_z(vertices, degrees):
#     theta = np.radians(degrees)
#     rot = np.array([
#         [np.cos(theta), -np.sin(theta), 0],
#         [np.sin(theta), np.cos(theta), 0],
#         [0, 0, 1]
#     ])
#     return np.dot(vertices, rot.T)
#
# def apply_transformations(vertices, scale=1, rotation=(0,0,0), translation=(0,0,0)):
#     """Aplica escala, rotação e translação aos vértices"""
#     # Escala
#     vert = vertices * scale
#
#     # Rotação (ordem XYZ)
#     vert = rotate_x(vert, rotation[0])
#     vert = rotate_y(vert, rotation[1])
#     vert = rotate_z(vert, rotation[2])
#
#     # Translação
#     vert += np.array(translation)
#
#     return vert
#
# # Função para criar e transformar todos os objetos
# def create_scene():
#     # Gerar objetos base
#     box_verts, box_faces, box_edges = create_open_box(side=4, height=3, wall_thickness=0.5)
#     cone_verts, cone_faces, cone_edges = create_cone(radius=1, height=4)
#     frustum_verts, frustum_faces, frustum_edges = create_frustum(r_lower=1.5, r_upper=0.5, height=3)
#     line_verts, line_faces, line_edges = create_line(length=5, radius=0.1)
#
#     # Aplicar transformações
#     objects = [
#         {
#             'verts': box_verts,
#             'faces': box_faces,
#             'edges': box_edges,
#             'scale': 1,
#             'rot': (0, 30, 0),
#             'trans': (7, 0, 0)
#         },
#         {
#             'verts': cone_verts,
#             'faces': cone_faces,
#             'edges': cone_edges,
#             'scale': 1,
#             'rot': (45, 0, 0),
#             'trans': (2, 2, -4)
#         },
#         {
#             'verts': frustum_verts,
#             'faces': frustum_faces,
#             'edges': frustum_edges,
#             'scale': 1.5,
#             'rot': (0, 0, -30),
#             'trans': (-8, -8, 4)
#         },
#         {
#             'verts': line_verts,
#             'faces': line_faces,
#             'edges': line_edges,
#             'scale': 2,
#             'rot': (0, 60, 0),
#             'trans': (5, -5, -8)
#         }
#     ]
#
#     # Processar transformações
#     scene = []
#     for obj in objects:
#         transformed_verts = apply_transformations(
#             obj['verts'],
#             scale=obj['scale'],
#             rotation=obj['rot'],
#             translation=obj['trans']
#         )
#         scene.append((transformed_verts, obj['faces'], obj['edges']))
#
#     return scene
#
# # Função de projeção em perspectiva
# def perspective_projection(vertices, focal_length=5):
#     """
#     Projeta vértices 3D em 2D usando projeção em perspectiva.
#     :param vertices: Vértices no sistema de coordenadas da câmera (shape: Nx3)
#     :param focal_length: Distância focal da câmera
#     :return: Vértices projetados em 2D (shape: Nx2)
#     """
#     # Coordenadas z devem ser positivas (na frente da câmera)
#     z = vertices[:, 2]
#     if np.any(z <= 0):
#         # Filtra apenas os vértices na frente da câmera
#         valid_indices = z > 0
#         vertices = vertices[valid_indices]
#         z = z[valid_indices]
#
#     # Projeção em perspectiva
#     x_proj = (focal_length * vertices[:, 0]) / z
#     y_proj = (focal_length * vertices[:, 1]) / z
#     return np.column_stack((x_proj, y_proj))
#
# # Função para desenhar arestas em 2D
# def plot_2d_edges(vertices_2d, edges, color='b'):
#     """
#     Desenha as arestas de um objeto em 2D.
#     :param vertices_2d: Vértices projetados em 2D (shape: Nx2)
#     :param edges: Arestas do objeto (shape: Kx2)
#     :param color: Cor das arestas
#     """
#     for edge in edges:
#         v0, v1 = edge
#         # Verifica se os índices são válidos
#         if v0 < len(vertices_2d) and v1 < len(vertices_2d):
#             plt.plot([vertices_2d[v0, 0], vertices_2d[v1, 0]],
#                      [vertices_2d[v0, 1], vertices_2d[v1, 1]],
#                      color=color, linewidth=1)
#
# # Função para projetar e exibir a cena em 2D
# def plot_perspective_scene(scene, focal_length=5, resolution=(800, 600)):
#     """
#     Projeta a cena em 2D usando projeção em perspectiva e exibe.
#     :param scene: Lista de objetos (vértices, faces, edges) no sistema do mundo
#     :param focal_length: Distância focal da câmera
#     :param resolution: Resolução da janela de visualização (largura, altura)
#     """
#     # Cores para cada objeto
#     colors = ['blue', 'green', 'red', 'purple']
#     labels = ['Caixa Aberta', 'Cone', 'Tronco de Cone', 'Linha']
#
#     # Configurar o plot 2D
#     plt.figure(figsize=(10, 8))
#     plt.title("Projeção em Perspectiva 2D")
#     plt.xlabel("X (2D)")
#     plt.ylabel("Y (2D)")
#     plt.grid(True)
#
#     # Projetar e desenhar cada objeto
#     for idx, (vertices, _, edges) in enumerate(scene):
#         # Projetar em 2D
#         verts_2d = perspective_projection(vertices, focal_length)
#
#         # Desenhar arestas
#         plot_2d_edges(verts_2d, edges, color=colors[idx % len(colors)])
#
#     # Adicionar legenda
#     from matplotlib.patches import Patch
#     legend_elements = [Patch(facecolor=c, label=l)
#                        for c, l in zip(colors, labels)]
#     plt.legend(handles=legend_elements, loc='upper right')
#
#     plt.tight_layout()
#     plt.show()
#
# # Execução principal
# if __name__ == "__main__":
#     # Criar cena
#     scene = create_scene()
#
#     # Projetar e exibir a cena em 2D
#     plot_perspective_scene(scene, focal_length=5, resolution=(800, 600))