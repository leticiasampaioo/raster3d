import numpy as np
from skimage.measure import marching_cubes
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from test import create_open_box, create_cone, create_frustum, create_line


# Funções de transformação geométrica
def rotate_x(vertices, degrees):
    theta = np.radians(degrees)
    rot = np.array([
        [1, 0, 0],
        [0, np.cos(theta), -np.sin(theta)],
        [0, np.sin(theta), np.cos(theta)]
    ])
    return np.dot(vertices, rot.T)

def rotate_y(vertices, degrees):
    theta = np.radians(degrees)
    rot = np.array([
        [np.cos(theta), 0, np.sin(theta)],
        [0, 1, 0],
        [-np.sin(theta), 0, np.cos(theta)]
    ])
    return np.dot(vertices, rot.T)

def rotate_z(vertices, degrees):
    theta = np.radians(degrees)
    rot = np.array([
        [np.cos(theta), -np.sin(theta), 0],
        [np.sin(theta), np.cos(theta), 0],
        [0, 0, 1]
    ])
    return np.dot(vertices, rot.T)

def apply_transformations(vertices, scale=1, rotation=(0,0,0), translation=(0,0,0)):
    """Aplica escala, rotação e translação aos vértices"""
    # Escala
    vert = vertices * scale

    # Rotação (ordem XYZ)
    vert = rotate_x(vert, rotation[0])
    vert = rotate_y(vert, rotation[1])
    vert = rotate_z(vert, rotation[2])

    # Translação
    vert += np.array(translation)

    return vert

# Função para criar e transformar todos os objetos
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

# Função de visualização da cena completa
def plot_scene(scene):
    fig = plt.figure(figsize=(12, 10))
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

# Execução principal
if __name__ == "__main__":
    scene = create_scene()

    # Verificar limites máximos
    all_verts = np.concatenate([v for v, _ in scene])
    print(f"Valor máximo em qualquer eixo: {np.max(np.abs(all_verts)):.2f}")

    plot_scene(scene)