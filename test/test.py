import numpy as np
from skimage.measure import marching_cubes
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def create_open_box(side=2, height=1, wall_thickness=0.1, resolution=50):
    """
    Caixa aberta sem tampa com base quadrada
    :param side: Lado da base quadrada
    :param height: Altura da caixa
    :param wall_thickness: Espessura das paredes
    :param resolution: Resolução da grade 3D
    """
    # Cria grade 3D centralizada na base
    x = np.linspace(-side/2, side/2, resolution)
    y = np.linspace(-side/2, side/2, resolution)
    z = np.linspace(0, height, resolution)

    X, Y, Z = np.meshgrid(x, y, z, indexing='ij')

    # Define as paredes e fundo
    outer = (np.abs(X) <= side/2) & (np.abs(Y) <= side/2) & (Z <= height)
    inner = (np.abs(X) <= side/2 - wall_thickness) & \
            (np.abs(Y) <= side/2 - wall_thickness) & \
            (Z >= wall_thickness)

    volume = outer & ~inner

    vertices, faces, _, _ = marching_cubes(
        volume,
        level=0.5,
        spacing=(x[1]-x[0], y[1]-y[0], z[1]-z[0])
    )

    return vertices, faces

def create_cone(radius=1, height=2, resolution=50):
    """
    Cone completo
    """
    x = np.linspace(-radius, radius, resolution)
    y = np.linspace(-radius, radius, resolution)
    z = np.linspace(0, height, resolution)

    X, Y, Z = np.meshgrid(x, y, z, indexing='ij')

    cone_radius = radius * (1 - Z/height)
    volume = (np.sqrt(X**2 + Y**2) <= cone_radius) & (Z >= 0)

    vertices, faces, _, _ = marching_cubes(
        volume,
        level=0.5,
        spacing=(x[1]-x[0], y[1]-y[0], z[1]-z[0])
    )

    return vertices, faces

def create_frustum(r_lower=1, r_upper=0.5, height=2, resolution=50):
    """
    Tronco de cone (frustum)
    """
    max_radius = max(r_lower, r_upper)
    x = np.linspace(-max_radius, max_radius, resolution)
    y = np.linspace(-max_radius, max_radius, resolution)
    z = np.linspace(0, height, resolution)

    X, Y, Z = np.meshgrid(x, y, z, indexing='ij')

    current_radius = r_lower + (r_upper - r_lower) * (Z / height)
    volume = (np.sqrt(X**2 + Y**2) <= current_radius) & (Z >= 0)

    vertices, faces, _, _ = marching_cubes(
        volume,
        level=0.5,
        spacing=(x[1]-x[0], y[1]-y[0], z[1]-z[0])
    )

    return vertices, faces

def create_line(length=3, radius=0.05, resolution=50):
    """
    Linha reta representada como cilindro fino
    """
    x = np.linspace(-radius, radius, resolution)
    y = np.linspace(-radius, radius, resolution)
    z = np.linspace(0, length, resolution)

    X, Y, Z = np.meshgrid(x, y, z, indexing='ij')

    volume = (np.sqrt(X**2 + Y**2) <= radius) & (Z >= 0)

    vertices, faces, _, _ = marching_cubes(
        volume,
        level=0.5,
        spacing=(x[1]-x[0], y[1]-y[0], z[1]-z[0])
    )

    return vertices, faces

# def create_line(length=3):
#     """
#     Linha reta de tamanho 3
#     """
#     # Define os pontos inicial e final da linha
#     vertices = np.array([[0, 0, 0], [0, 0, length]])  # Linha ao longo do eixo Z
#     faces = np.array([[0, 1]])  # Apenas uma aresta conectando os dois pontos
#     return vertices, faces

def plot_mesh(vertices, faces, title='Malha 3D', facecolor='skyblue', linewidth=2):
    """Função de visualização genérica"""
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')

    mesh = Poly3DCollection(vertices[faces], alpha=0.8)
    mesh.set_facecolor(facecolor)
    mesh.set_edgecolor('k')
    ax.add_collection3d(mesh)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(title)

    # Ajuste automático dos limites
    max_dim = max(vertices.max(axis=0) - vertices.min(axis=0))
    ax.set_xlim(vertices[:,0].min(), vertices[:,0].max())
    ax.set_ylim(vertices[:,1].min(), vertices[:,1].max())
    ax.set_zlim(vertices[:,2].min(), vertices[:,2].max())

    plt.show()

# Exemplo de uso para todos os objetos
if __name__ == "__main__":
    # Caixa aberta
    vertices, faces = create_open_box(side=2, height=1.5, wall_thickness=0.15)
    plot_mesh(vertices, faces, 'Caixa Aberta', facecolor='blue')

    # Cone
    vertices, faces = create_cone(radius=1, height=3)
    plot_mesh(vertices, faces, 'Cone', facecolor='green')

    # Tronco de cone
    vertices, faces = create_frustum(r_lower=1.5, r_upper=0.5, height=2)
    plot_mesh(vertices, faces, 'Tronco de Cone', facecolor='red')

    # Linha
    vertices, faces = create_line(length=3, radius=0.08)
    plot_mesh(vertices, faces, 'Linha Reta',facecolor='purple')