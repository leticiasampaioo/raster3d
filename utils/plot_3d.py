from skimage import measure
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def plot_3d_matrix(matriz, cor_arestas='k', cor_face='skyblue', titulo="Caixa 3D"):

    # Extrai a superfície usando Marching Cubes
    verts, faces, normals, values = measure.marching_cubes(matriz,0.5 )

    verts_corrigidos = verts[:, [1, 0, 2]]

    # Configuração do plot
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Cria a malha poligonal com os vértices corrigidos
    mesh = Poly3DCollection(verts_corrigidos[faces])
    mesh.set_edgecolor(cor_arestas)
    mesh.set_facecolor(cor_face)
    ax.add_collection3d(mesh)

    # Configuração dos eixos com limites corretos
    ax.set_xlim(0, matriz.shape[1])  # X: largura (dimensão 1)
    ax.set_ylim(0, matriz.shape[0])  # Y: altura (dimensão 0)
    ax.set_zlim(0, matriz.shape[2])  # Z: profundidade (dimensão 2)

    # Rótulos dos eixos
    ax.set_xlabel("Largura (X)")
    ax.set_ylabel("Altura (Y)")
    ax.set_zlabel("Profundidade (Z)")

    ax.set_title(titulo, fontsize=14)
    plt.tight_layout()
    plt.show()