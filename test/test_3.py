import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from test_2 import apply_transformations, create_scene

def normalize(v):

    return v / np.linalg.norm(v)

def look_at(eye, target, up):

    # Vetor forward (direção da câmera, apontando de eye para target)
    forward = normalize(target - eye)

    # Vetor right (direita da câmera, ortogonal a forward e up)
    right = normalize(np.cross(forward, up))

    # Vetor up corrigido (ortogonal a forward e right)
    up = normalize(np.cross(right, forward))

    # Matriz de rotação (mundo -> câmera)
    rotation = np.array([right, up, -forward])

    # Matriz de translação (mundo -> câmera)
    translation = -np.dot(rotation, eye)

    # Criar matriz homogênea 4x4 para a transformação
    transformation_matrix = np.eye(4)
    transformation_matrix[:3, :3] = rotation  # Matriz de rotação
    transformation_matrix[:3, 3] = translation  # Vetor de translação

    return transformation_matrix

def transform_to_camera(vertices, transformation_matrix):

    # Adicionar a coordenada homogênea (1) para cada vértice
    vertices_homogeneous = np.hstack([vertices, np.ones((vertices.shape[0], 1))])

    # Aplicar a multiplicação da matriz de transformação
    transformed_vertices_homogeneous = vertices_homogeneous @ transformation_matrix.T

    # Retornar apenas as coordenadas (x, y, z) dos pontos transformados
    return transformed_vertices_homogeneous[:, :3]

def plot_camera_scene(scene, transformation_matrix, camera_eye, camera_target, title="Cena no Sistema da Câmera"):
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')

    colors = ['blue', 'green', 'red', 'purple']

    for idx, (verts, faces) in enumerate(scene):
        # Transformar para o sistema da câmera
        cam_verts = transform_to_camera(verts, transformation_matrix)

        # Plotar
        mesh = Poly3DCollection(cam_verts[faces],
                                alpha=0.8,
                                edgecolor='k',
                                facecolor=colors[idx])
        ax.add_collection3d(mesh)

    # Plotar pontos importantes
    # Origem do sistema de coordenadas do mundo
    ax.scatter(0, 0, 0, color='black', s=100, label='Origem')

    # Posição da câmera (eye)
    cam_eye_cam = transform_to_camera(np.array([camera_eye]), transformation_matrix)
    ax.scatter(cam_eye_cam[0][0], cam_eye_cam[0][1], cam_eye_cam[0][2], color='orange', s=100, label='Eye')

    # Ponto de foco (target)
    cam_target_cam = transform_to_camera(np.array([camera_target]), transformation_matrix)
    ax.scatter(cam_target_cam[0][0], cam_target_cam[0][1], cam_target_cam[0][2], color='cyan', s=100, label='at')

    # Configurar limites
    ax.set_xlim(-15, 15)
    ax.set_ylim(-15, 15)
    ax.set_zlim(-15, 15)

    # Configurar eixos
    ax.set_xlabel('X (Câmera)', fontsize=12)
    ax.set_ylabel('Y (Câmera)', fontsize=12)
    ax.set_zlabel('Z (Câmera)', fontsize=12)
    ax.set_title(title, fontsize=14)

    # Adicionar legenda apenas para os pontos importantes
    ax.legend(loc='upper right')

    plt.tight_layout()
    plt.show()

def plot_scene_from_camera(scene, camera_eye, camera_target, camera_up):
    # Calcular a matriz de transformação baseada nos parâmetros da câmera
    transformation_matrix = look_at(camera_eye, camera_target, camera_up)

    # Visualizar a cena a partir da perspectiva da câmera
    plot_camera_scene(scene, transformation_matrix, camera_eye, camera_target, title="Cena na Perspectiva da Câmera")

def plot_scene_from_world(scene, camera_eye, camera_target, camera_up):
    # Calcular a matriz de transformação baseada nos parâmetros da câmera
    transformation_matrix = look_at(camera_eye, camera_target, camera_up)

    # Visualizar a cena no sistema de coordenadas do mundo
    plot_camera_scene(scene, np.eye(4), camera_eye, camera_target, title="Cena no Sistema de Coordenadas do Mundo")

if __name__ == "__main__":

    scene = create_scene()

    # Definir parâmetros da câmera
    camera_eye = np.array([1, 1, 5])  # Posição da câmera
    camera_target = np.array([-9, -9, -9])  # Ponto de foco
    camera_up = np.array([0, 0, 1])  # Vetor "para cima"

    # Plotar a cena no sistema de coordenadas do mundo
    plot_scene_from_world(scene, camera_eye, camera_target, camera_up)

    # Plotar a cena a partir da perspectiva da câmera (considerando a transformação da câmera)
    plot_scene_from_camera(scene, camera_eye, camera_target, camera_up)

