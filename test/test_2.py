import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from test import create_open_box, create_cone, create_frustum, create_line

def get_scale_matrix(scale):

    return np.array([
        [scale, 0, 0, 0],
        [0, scale, 0, 0],
        [0, 0, scale, 0],
        [0, 0, 0, 1]
    ])

def get_translation_matrix(translation):

    tx, ty, tz = translation
    return np.array([
        [1, 0, 0, tx],
        [0, 1, 0, ty],
        [0, 0, 1, tz],
        [0, 0, 0, 1]
    ])

def get_rotation_matrix_x(degrees):

    theta = np.radians(degrees)
    return np.array([
        [1, 0, 0, 0],
        [0, np.cos(theta), -np.sin(theta), 0],
        [0, np.sin(theta), np.cos(theta), 0],
        [0, 0, 0, 1]
    ])

def get_rotation_matrix_y(degrees):

    theta = np.radians(degrees)
    return np.array([
        [np.cos(theta), 0, np.sin(theta), 0],
        [0, 1, 0, 0],
        [-np.sin(theta), 0, np.cos(theta), 0],
        [0, 0, 0, 1]
    ])

def get_rotation_matrix_z(degrees):

    theta = np.radians(degrees)
    return np.array([
        [np.cos(theta), -np.sin(theta), 0, 0],
        [np.sin(theta), np.cos(theta), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])

def apply_transformations(vertices, scale=1, rotation=(0,0,0), translation=(0,0,0)):

    # Criar matriz de transformação combinada
    transformation_matrix = (
        get_translation_matrix(translation) @
        get_rotation_matrix_z(rotation[2]) @
        get_rotation_matrix_y(rotation[1]) @
        get_rotation_matrix_x(rotation[0]) @
        get_scale_matrix(scale)
    )

    # Converter vértices para coordenadas homogêneas (adicionar uma dimensão extra de 1)
    homogeneous_vertices = np.hstack([vertices, np.ones((vertices.shape[0], 1))])

    # Aplicar a transformação usando multiplicação de matrizes
    transformed_vertices = homogeneous_vertices @ transformation_matrix.T

    # Remover a dimensão homogênea e retornar os vértices transformados
    return transformed_vertices[:, :3]

def create_scene():
    # Gerar objetos base
    box_verts, box_faces = create_open_box(side=4, height=3, wall_thickness=0.15, resolution=20)
    cone_verts, cone_faces = create_cone(radius=2, height=6, resolution=20)
    frustum_verts, frustum_faces = create_frustum(r_lower=3, r_upper=1, height=4, resolution=20)
    line_verts, line_faces = create_line(length=3)

    # Aplicar transformações
    objects = [
        {
            'verts': box_verts,
            'faces': box_faces,
            'scale': 2,
            'rot': (0, 30, 0),
            'trans': (-7, 7, 0)
        },
        {
            'verts': cone_verts,
            'faces': cone_faces,
            'scale': 1,
            'rot': (45, 0, 0),
            'trans': (5, 5, -4)
        },
        {
            'verts': frustum_verts,
            'faces': frustum_faces,
            'scale': 1.5,
            'rot': (0, 0, -30),
            'trans': (-8, -8, 4)
        },
        {
            'verts': line_verts,
            'faces': line_faces,
            'scale': 2,
            'rot': (0, 60, 0),
            'trans': (5, -5, -8)
        }
    ]

    # Processar transformações
    scene = []
    for obj in objects:
        transformed_verts = apply_transformations(
            obj['verts'],
            scale=obj['scale'],
            rotation=obj['rot'],
            translation=obj['trans']
        )
        scene.append((transformed_verts, obj['faces']))

    return scene

def plot_scene(scene):

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')

    colors = ['blue', 'green', 'red', 'purple']
    labels = ['Caixa Aberta', 'Cone', 'Tronco de Cone', 'Linha']

    for idx, (verts, faces) in enumerate(scene):
        mesh = Poly3DCollection(verts[faces],
                                alpha=0.8,
                                edgecolor='k',
                                facecolor=colors[idx])
        ax.add_collection3d(mesh)

    # Configurar limites fixos
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.set_zlim(-10, 10)

    # Configurar eixos
    ax.set_xlabel('X', fontsize=12)
    ax.set_ylabel('Y', fontsize=12)
    ax.set_zlabel('Z', fontsize=12)
    ax.set_title('Cena 3D com Objetos Transformados', fontsize=14)

    # Adicionar legenda
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=c, label=l)
                       for c, l in zip(colors, labels)]
    ax.legend(handles=legend_elements, loc='upper right')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    scene = create_scene()

    # Verificar limites máximos
    all_verts = np.concatenate([v for v, _ in scene])
    print(f"Valor máximo em qualquer eixo: {np.max(np.abs(all_verts)):.2f}")

    plot_scene(scene)


# import numpy as np
# from skimage.measure import marching_cubes
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d.art3d import Poly3DCollection
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
#     box_verts, box_faces, box_edges = create_open_box(side=4, height=3, wall_thickness=0.15, resolution=20)
#     cone_verts, cone_faces, cone_edges = create_cone(radius=2, height=6, resolution=20)
#     frustum_verts, frustum_faces, frustum_edges = create_frustum(r_lower=3, r_upper=1, height=4, resolution=20)
#     line_verts, line_faces, line_edges = create_line(length=3, radius=0.01, resolution=20)
#
#     # Aplicar transformações
#
#     # Aplicar transformações
#     objects = [
#         {
#             'verts': box_verts,
#             'faces': box_faces,
#             'edges': box_edges,
#             'scale': 1,
#             'rot': (0, 30, 0),
#             'trans': (7, 0, 2)
#         },
#         {
#             'verts': cone_verts,
#             'faces': cone_faces,
#             'edges': cone_edges,
#             'scale': 1,
#             'rot': (45, 0, 0),
#             'trans': (-2, 2, -4)
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
# # Função de visualização da cena completa
# def plot_scene(scene):
#     fig = plt.figure(figsize=(12, 10))
#     ax = fig.add_subplot(111, projection='3d')
#
#     colors = ['blue', 'green', 'red', 'purple']
#     labels = ['Caixa Aberta', 'Cone', 'Tronco de Cone', 'Linha']
#
#     for idx, (verts, faces, edges) in enumerate(scene):
#         mesh = Poly3DCollection(verts[faces],
#                                 alpha=0.8,
#                                 edgecolor='k',
#                                 facecolor=colors[idx])
#         ax.add_collection3d(mesh)
#
#     # Configurar limites fixos
#     ax.set_xlim(-10, 10)
#     ax.set_ylim(-10, 10)
#     ax.set_zlim(-10, 10)
#
#     # Configurar eixos
#     ax.set_xlabel('X', fontsize=12)
#     ax.set_ylabel('Y', fontsize=12)
#     ax.set_zlabel('Z', fontsize=12)
#     ax.set_title('Cena 3D com Objetos Transformados', fontsize=14)
#
#     # Adicionar legenda
#     from matplotlib.patches import Patch
#     legend_elements = [Patch(facecolor=c, label=l)
#                        for c, l in zip(colors, labels)]
#     ax.legend(handles=legend_elements, loc='upper right')
#
#     plt.tight_layout()
#     plt.show()
#
# # Execução principal
# if __name__ == "__main__":
#     scene = create_scene()
#
#     # Verificar limites máximos
#     all_verts = np.concatenate([v for v, _, _ in scene])
#     print(f"Valor máximo em qualquer eixo: {np.max(np.abs(all_verts)):.2f}")
#
#     plot_scene(scene)