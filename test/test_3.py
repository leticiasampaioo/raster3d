from test import *
from test_2 import apply_transformations


# Funções de transformação geométrica
def normalize(v):
    return v / np.linalg.norm(v)

def look_at(eye, target, up):

    forward = normalize(target - eye)

    right = normalize(np.cross(forward, up))

    up = normalize(np.cross(right, forward))

    rotation = np.array([right, up, -forward])

    translation = -np.dot(rotation, eye)

    return rotation, translation

def transform_to_camera(vertices, rotation, translation):
    return np.dot(vertices, rotation.T) + translation

# Função para criar e transformar a cena
def create_scene():
    box_verts, box_faces = create_open_box(side=2, height=1.5, wall_thickness=0.15, resolution=10)
    cone_verts, cone_faces = create_cone(radius=1, height=3, resolution=10)
    frustum_verts, frustum_faces = create_frustum(r_lower=1.5, r_upper=0.5, height=2, resolution=10)
    line_verts, line_faces = create_line(length=3, radius=0.08, resolution=10)

    objects = [
        {
            'verts': box_verts,
            'faces': box_faces,
            'scale': 4,
            'rot': (0, 30, 0),
            'trans': (-8, 0, 0)
        },
        {
            'verts': cone_verts,
            'faces': cone_faces,
            'scale': 3,
            'rot': (45, 0, 0),
            'trans': (6, 6, 0)
        },
        {
            'verts': frustum_verts,
            'faces': frustum_faces,
            'scale': 2.4,
            'rot': (0, 0, -30),
            'trans': (-5, -7, 5)
        },
        {
            'verts': line_verts,
            'faces': line_faces,
            'scale': 6,
            'rot': (0, 90, 0),
            'trans': (5, -5, 5)
        }
    ]

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

def plot_camera_scene(scene, camera_rotation, camera_translation):
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')

    colors = ['#4e79a7', '#59a14f', '#e15759', '#f28e2b']
    labels = ['Caixa Aberta', 'Cone', 'Tronco de Cone', 'Linha']

    for idx, (verts, faces) in enumerate(scene):
        cam_verts = transform_to_camera(verts, camera_rotation, camera_translation)

        mesh = Poly3DCollection(cam_verts[faces],
                                alpha=0.8,
                                edgecolor='k',
                                facecolor=colors[idx])
        ax.add_collection3d(mesh)

    ax.set_xlim(-15, 15)
    ax.set_ylim(-15, 15)
    ax.set_zlim(-15, 15)

    ax.set_xlabel('X (Câmera)', fontsize=12)
    ax.set_ylabel('Y (Câmera)', fontsize=12)
    ax.set_zlabel('Z (Câmera)', fontsize=12)
    ax.set_title('Cena no Sistema de Coordenadas da Câmera', fontsize=14)

    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=c, label=l)
                       for c, l in zip(colors, labels)]
    ax.legend(handles=legend_elements, loc='upper right')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    scene = create_scene()

    camera_eye = np.array([0, 0, 0])
    camera_target = np.array([10, 10, 10])
    camera_up = np.array([0, 0, 1])

    camera_rotation, camera_translation = look_at(camera_eye, camera_target, camera_up)

    plot_camera_scene(scene, camera_rotation, camera_translation)