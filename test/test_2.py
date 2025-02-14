from test import *


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

    vert = vertices * scale

    vert = rotate_x(vert, rotation[0])
    vert = rotate_y(vert, rotation[1])
    vert = rotate_z(vert, rotation[2])

    vert += np.array(translation)

    return vert

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

def plot_scene(scene):
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')

    colors = ['#4e79a7', '#59a14f', '#e15759', '#f28e2b']
    labels = ['Caixa Aberta', 'Cone', 'Tronco de Cone', 'Linha']

    for idx, (verts, faces) in enumerate(scene):
        mesh = Poly3DCollection(verts[faces],
                                alpha=0.8,
                                edgecolor='k',
                                facecolor=colors[idx])
        ax.add_collection3d(mesh)

    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.set_zlim(-10, 10)

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

    all_verts = np.concatenate([v for v, _ in scene])
    print(f"Valor máximo em qualquer eixo: {np.max(np.abs(all_verts)):.2f}")

    plot_scene(scene)