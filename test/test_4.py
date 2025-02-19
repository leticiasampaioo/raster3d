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

