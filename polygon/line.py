import numpy as np
from matplotlib import pyplot as plt


def generate_line(comprimento):

    vertices = np.array([[0, 0, 0], [comprimento, 0, 0]])
    arestas = np.array([[0, 1]])
    return vertices, arestas

# Função para plotar os vértices e arestas
def plotar_solid(vertices, arestas):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plotando as arestas
    for aresta in arestas:
        x_vals = [vertices[aresta[0], 0], vertices[aresta[1], 0]]
        y_vals = [vertices[aresta[0], 1], vertices[aresta[1], 1]]
        z_vals = [vertices[aresta[0], 2], vertices[aresta[1], 2]]
        ax.plot(x_vals, y_vals, z_vals, color='b')

    # Ajuste automático de limites para garantir que o objeto caiba
    ax.set_xlim([vertices[:, 0].min() - 1, vertices[:, 0].max() + 1])
    ax.set_ylim([vertices[:, 1].min() - 1, vertices[:, 1].max() + 1])
    ax.set_zlim([vertices[:, 2].min() - 1, vertices[:, 2].max() + 1])

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plt.show()
