import numpy as np
from skimage.measure import marching_cubes
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def create_open_box(side=2, height=1, wall_thickness=0.1, resolution=20):

    x = np.linspace(-side/2, side/2, resolution)
    y = np.linspace(-side/2, side/2, resolution)
    z = np.linspace(0, height, resolution)

    X, Y, Z = np.meshgrid(x, y, z, indexing='ij')

    left_wall = X <= (-side/2 + wall_thickness)
    right_wall = X >= (side/2 - wall_thickness)
    front_wall = Y <= (-side/2 + wall_thickness)
    back_wall = Y >= (side/2 - wall_thickness)
    bottom = Z <= wall_thickness

    volume = left_wall | right_wall | front_wall | back_wall | bottom

    vertices, faces, _, _ = marching_cubes(
        volume,
        level=0.5,
        spacing=(x[1]-x[0], y[1]-y[0], z[1]-z[0])
    )

    return vertices, faces

def create_cone(radius=1, height=2, resolution=20):

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

def create_frustum(r_lower=1, r_upper=0.5, height=2, resolution=20):

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

def create_line(length=3, radius=0.05, resolution=20):

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

def plot_mesh(vertices, faces, title='Malha 3D'):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    mesh = Poly3DCollection(vertices[faces], alpha=0.8)
    mesh.set_facecolor('skyblue')
    mesh.set_edgecolor('k')
    ax.add_collection3d(mesh)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(title)

    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_zlim(-2, 2)

    plt.show()

if __name__ == "__main__":
    # Caixa aberta
    vertices, faces = create_open_box(side=3, height=2, wall_thickness=0.6, resolution=30)
    plot_mesh(vertices, faces, 'Caixa Aberta')

    # Cone
    vertices, faces = create_cone(radius=1, height=3)
    plot_mesh(vertices, faces, 'Cone')

    # Tronco de cone
    vertices, faces = create_frustum(r_lower=1.5, r_upper=0.5, height=2)
    plot_mesh(vertices, faces, 'Tronco de Cone')

    # Linha
    vertices, faces = create_line(length=3, radius=0.08)
    plot_mesh(vertices, faces, 'Linha Reta')