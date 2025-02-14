import numpy as np
from skimage.measure import marching_cubes
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from test_2 import apply_transformations

from test import create_open_box, create_cone, create_frustum, create_line


# Funções de transformação geométrica
def normalize(v):
    """Normaliza um vetor"""
    return v / np.linalg.norm(v)

def look_at(eye, target, up):
    """
    Cria a matriz de transformação para o sistema de coordenadas da câmera
    :param eye: Posição da câmera (origem do sistema da câmera)
    :param target: Ponto para onde a câmera está olhando
    :param up: Vetor "para cima" da câmera
    """
    # Vetor forward (direção da câmera)
    forward = normalize(target - eye)

    # Vetor right (direita da câmera)
    right = normalize(np.cross(forward, up))

    # Vetor up corrigido (ortogonal a forward e right)
    up = normalize(np.cross(right, forward))

    # Matriz de rotação (mundo -> câmera)
    rotation = np.array([right, up, -forward])

    # Matriz de translação (mundo -> câmera)
    translation = -np.dot(rotation, eye)

    return rotation, translation

def transform_to_camera(vertices, rotation, translation):
    """Transforma vértices do sistema do mundo para o sistema da câmera"""
    return np.dot(vertices, rotation.T) + translation

# Função para criar e transformar a cena
def create_scene():
    # Gerar objetos base
    box_verts, box_faces = create_open_box(side=4, height=3, wall_thickness=0.15, resolution=20)
    cone_verts, cone_faces = create_cone(radius=2, height=6, resolution=20)
    frustum_verts, frustum_faces = create_frustum(r_lower=3, r_upper=1, height=4, resolution=20)
    line_verts, line_faces = create_line(length=3, radius=0.01, resolution=20)

    # Aplicar transformações
    objects = [
        {
            'verts': box_verts,
            'faces': box_faces,
            'scale': 2,
            'rot': (0, 30, 0),
            'trans': (-8, 0, 0)
        },
        {
            'verts': cone_verts,
            'faces': cone_faces,
            'scale': 1.5,
            'rot': (45, 0, 0),
            'trans': (6, 6, 0)
        },
        {
            'verts': frustum_verts,
            'faces': frustum_faces,
            'scale': 1.2,
            'rot': (0, 0, -30),
            'trans': (-5, -7, 5)
        },
        {
            'verts': line_verts,
            'faces': line_faces,
            'scale': 3,
            'rot': (0, 90, 0),
            'trans': (5, -5, 5)
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

# Função de visualização da cena no sistema da câmera
def plot_camera_scene(scene, camera_rotation, camera_translation):
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')

    colors = ['#4e79a7', '#59a14f', '#e15759', '#f28e2b']
    labels = ['Caixa Aberta', 'Cone', 'Tronco de Cone', 'Linha']

    for idx, (verts, faces) in enumerate(scene):
        # Transformar para o sistema da câmera
        cam_verts = transform_to_camera(verts, camera_rotation, camera_translation)

        # Plotar
        mesh = Poly3DCollection(cam_verts[faces],
                                alpha=0.8,
                                edgecolor='k',
                                facecolor=colors[idx])
        ax.add_collection3d(mesh)

    # Configurar limites
    ax.set_xlim(-15, 15)
    ax.set_ylim(-15, 15)
    ax.set_zlim(-15, 15)

    # Configurar eixos
    ax.set_xlabel('X (Câmera)', fontsize=12)
    ax.set_ylabel('Y (Câmera)', fontsize=12)
    ax.set_zlabel('Z (Câmera)', fontsize=12)
    ax.set_title('Cena no Sistema de Coordenadas da Câmera', fontsize=14)

    # Adicionar legenda
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=c, label=l)
                       for c, l in zip(colors, labels)]
    ax.legend(handles=legend_elements, loc='upper right')

    plt.tight_layout()
    plt.show()

# Execução principal
if __name__ == "__main__":
    # Criar cena no sistema do mundo
    scene = create_scene()

    # Definir parâmetros da câmera
    camera_eye = np.array([10, 10, 10])  # Posição da câmera
    camera_target = np.array([0, 0, 0])  # Ponto de foco
    camera_up = np.array([0, 0, 1])      # Vetor "para cima"

    # Calcular base vetorial da câmera
    camera_rotation, camera_translation = look_at(camera_eye, camera_target, camera_up)

    # Visualizar cena no sistema da câmera
    plot_camera_scene(scene, camera_rotation, camera_translation)