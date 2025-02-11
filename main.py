from polygon.cone import generate_cone
from polygon.line import plotar_solid, generate_line
from polygon.open_box import generate_open_box
from utils.plot_3d import plot_3d_matrix
from polygon.truncked_cone import generate_truncked_cone

if __name__ == "__main__":

    #Tronco de Cone
    tronco_cone = generate_truncked_cone(
        altura=20,
        raio_base_maior=10,
        raio_base_menor=5,
        padding=5
    )

    # Plota o tronco de cone
    plot_3d_matrix(
        matriz=tronco_cone,
        cor_face='lightblue',
        cor_arestas='darkblue',
        titulo="Tronco de Cone 3D"
    )

    # # Gera uma caixa com 15x20x25 de dimensões internas
    # caixa = generate_open_box(
    #     altura=15,  # Altura (Y)
    #     largura=20,  # Largura (X)
    #     profundidade=25,  # Profundidade (Z)
    #     espessura=2,
    #     padding=5
    # )
    #
    # # Plota a caixa gerada
    # plot_3d_matrix(
    #     matriz=caixa,
    #     cor_face='lightgreen',
    #     cor_arestas='darkgreen',
    #     titulo="Caixa Aberta no Topo 15x20x25"
    # )

    # # Gera um cone com altura 20, raio da base 10 e padding 5
    # cone = generate_cone(
    #     altura=20,
    #     raio_base=10,
    #     padding=5
    # )
    #
    # # Plota o cone
    # plot_3d_matrix(
    #     matriz=cone,
    #     cor_face='orange',
    #     cor_arestas='brown',
    #     titulo="Cone 3D"
    # )


    #Linha
    # vertices, arestas = generate_line(3)
    # plotar_solid(vertices, arestas)