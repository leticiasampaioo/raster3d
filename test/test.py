import numpy as np
from skimage.measure import marching_cubes
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def create_open_box(side=2, height=1, wall_thickness=0.1, resolution=50):

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

def create_cone(radius=1, height=2, resolution=50, pad=0.1):

    # Define os intervalos de x, y e z
    x = np.linspace(-radius, radius, resolution)
    y = np.linspace(-radius, radius, resolution)
    # O eixo z é estendido de -pad a height+pad para garantir que as superfícies
    # (base e ápice) não estejam exatamente na borda do grid.
    z = np.linspace(-pad, height + pad, resolution)

    X, Y, Z = np.meshgrid(x, y, z, indexing='ij')

    # Define o volume do cone:
    # - Apenas para 0 <= z <= height
    # - Para cada z, o raio máximo é dado por: radius * (1 - z/height)
    volume = ((Z >= 0) & (Z <= height)) & (np.sqrt(X ** 2 + Y ** 2) <= radius * (1 - Z / height))

    # Converte o volume para float para garantir transição suave (0 para 1)
    volume = volume.astype(float)

    # Executa o marching cubes para extrair a malha
    vertices, faces, _, _ = marching_cubes(volume, level=0.5,
                                           spacing=(x[1] - x[0], y[1] - y[0], z[1] - z[0]))
    return vertices, faces

def create_frustum(r_lower=1, r_upper=0.5, height=2, resolution=50, pad=0.1):

    # Para x e y usamos o máximo dos raios
    max_radius = max(r_lower, r_upper)
    x = np.linspace(-max_radius, max_radius, resolution)
    y = np.linspace(-max_radius, max_radius, resolution)
    # O eixo z é estendido um pouco além do intervalo [0, height]
    z = np.linspace(-pad, height + pad, resolution)

    X, Y, Z = np.meshgrid(x, y, z, indexing='ij')

    # Definindo o volume:
    # A região interior é onde Z está entre 0 e height e o raio no plano XY é menor ou igual
    # a uma interpolação linear entre r_lower e r_upper.
    # Fora desse intervalo de z o volume é False, fazendo com que as transições ocorram no interior do grid.
    volume = ((Z >= 0) & (Z <= height)) & (np.sqrt(X ** 2 + Y ** 2) <= (r_lower + (r_upper - r_lower) * (Z / height)))

    # Executa o marching cubes. Convertendo o volume para float garante que a transição de 0 para 1 seja bem interpretada.
    vertices, faces, _, _ = marching_cubes(volume.astype(float), level=0.5,
                                           spacing=(x[1] - x[0], y[1] - y[0], z[1] - z[0]))
    return vertices, faces

def create_line(length=3):

    # Define os pontos inicial e final da linha
    vertices = np.array([[0, 0, 0], [0, 2, length]])  # Linha ao longo do eixo Z
    faces = np.array([[0, 1]])  # Apenas uma aresta conectando os dois pontos
    return vertices, faces

def plot_mesh(vertices, faces, title='Malha 3D', facecolor='skyblue', linewidth=2):

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

    ax.auto_scale_xyz(vertices[:, 0], vertices[:, 1], vertices[:, 2])

    plt.show()

def menu():
    while True:
        print("\nEscolha o sólido para visualizar:")
        print("1 - Caixa Aberta")
        print("2 - Cone")
        print("3 - Tronco de Cone")
        print("4 - Linha")
        print("5 - Todos os sólidos")
        print("0 - Sair")

        choice = input("Digite o número da opção desejada:")

        if choice == "1":
            vertices, faces = create_open_box(side=10, height=10, wall_thickness=2, resolution=20)
            plot_mesh(vertices, faces, 'Caixa Aberta', facecolor='blue')
        elif choice == "2":
            vertices, faces = create_cone(radius=1, height=3, resolution=20, pad=0.1)
            plot_mesh(vertices, faces, 'Cone', facecolor='green')
        elif choice == "3":
            vertices, faces = create_frustum(r_lower=1.5, r_upper=0.5, height=3, resolution=20, pad=0.1)
            plot_mesh(vertices, faces, 'Tronco de Cone', facecolor='red')
        elif choice == "4":
            vertices, faces = create_line(length=3)
            plot_mesh(vertices, faces, 'Linha Reta', facecolor='purple')
        elif choice == "5":
            vertices, faces = create_open_box(side=9, height=10, wall_thickness=0.9)
            plot_mesh(vertices, faces, 'Caixa Aberta', facecolor='blue')

            vertices, faces = create_cone(radius=1, height=3, resolution=70, pad=0.1)
            plot_mesh(vertices, faces, 'Cone', facecolor='green')

            vertices, faces = create_frustum(r_lower=1.5, r_upper=0.5, height=3, resolution=70, pad=0.1)
            plot_mesh(vertices, faces, 'Tronco de Cone', facecolor='red')

            vertices, faces = create_line(length=3)
            plot_mesh(vertices, faces, 'Linha Reta', facecolor='purple')
        elif choice == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()

