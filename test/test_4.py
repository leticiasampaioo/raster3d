import numpy as np
import matplotlib.pyplot as plt

from test_3 import transform_to_camera, look_at

from test_2 import create_scene


# Função para projeção em perspectiva
def perspective_projection(vertices, focal_length):
    """
    Projeta vértices 3D em 2D usando projeção em perspectiva.
    :param vertices: Vértices no sistema de coordenadas da câmera (shape: Nx3)
    :param focal_length: Distância focal da câmera
    :return: Vértices projetados em 2D (shape: Nx2)
    """
    # Coordenadas z devem ser positivas (na frente da câmera)
    z = vertices[:, 2]
    # if np.any(z <= 0):
    #     raise ValueError("Alguns vértices estão atrás da câmera (z <= 0).")

    # Projeção em perspectiva
    x_proj = (focal_length * vertices[:, 0]) / z
    y_proj = (focal_length * vertices[:, 1]) / z
    return np.column_stack((x_proj, y_proj))

# Função para desenhar arestas em 2D
def plot_2d_edges(vertices_2d, faces, color='b'):
    """
    Desenha as arestas de um objeto em 2D.
    :param vertices_2d: Vértices projetados em 2D (shape: Nx2)
    :param faces: Faces do objeto (shape: Mx3)
    :param color: Cor das arestas
    """
    for face in faces:
        # Fechar o ciclo da face
        face_cycle = np.append(face, face[0])
        # Desenhar as arestas
        plt.plot(vertices_2d[face_cycle, 0],
                 vertices_2d[face_cycle, 1],
                 color=color, linewidth=1)

# Função principal para projetar e exibir a cena em 2D
def plot_perspective_scene(scene, camera_rotation, camera_translation, focal_length=5):
    """
    Projeta a cena em 2D usando projeção em perspectiva e exibe.
    :param scene: Lista de objetos (vértices e faces) no sistema do mundo
    :param camera_rotation: Matriz de rotação da câmera
    :param camera_translation: Vetor de translação da câmera
    :param focal_length: Distância focal da câmera
    """
    # Cores para cada objeto
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

    # Configurar o plot 2D
    plt.figure(figsize=(10, 8))
    plt.title("Projeção em Perspectiva 2D")
    plt.xlabel("X (2D)")
    plt.ylabel("Y (2D)")
    plt.grid(True)

    # Projetar e desenhar cada objeto
    for idx, (verts, faces) in enumerate(scene):
        # Transformar para o sistema da câmera
        cam_verts = transform_to_camera(verts, camera_rotation, camera_translation)

        # Projetar em 2D
        verts_2d = perspective_projection(cam_verts, focal_length)

        # Desenhar arestas
        plot_2d_edges(verts_2d, faces, color=colors[idx % len(colors)])

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

    # Projetar e exibir a cena em 2D
    plot_perspective_scene(scene, camera_rotation, camera_translation, focal_length=5)