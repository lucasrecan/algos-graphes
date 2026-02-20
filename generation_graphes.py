import numpy as np
import random
import networkx as nx
import matplotlib.pyplot as plt
alphabet = "abcdefghijklmnopqrstuvwxyz".upper()

def graphe(n, a, b) :
    """
    Crée un graphe orienté avec n sommets et des poids de chemins entre a et b.
    Elle prend en paramètres un nombre de sommets n, et deux entiers a et b qui représentent 
    l'intervalle des valeurs possibles pour les poids des chemins
    """
    # On genère une matrice de taille n x n
    M = np.zeros((n, n)) 
    infini = float('inf')
    # Pour chaque coefficient de la matrice
    for i in range (len(M)):
        for j in range(len(M)):
            # random.randint(0, 1) renvoie environ 50% du temps 1, le reste du temps 0
            if (random.randint(0, 1) == 1):
                # Le coefficient reçoit un nombre entier dans l'intervalle [a, b[
                M[i][j] = random.randint(a, b-1) 
            else :
                # Le coefficient reçoit inf 
                M[i][j] = infini
    return M

def graphe2(n, p, a, b) :
    """
    Crée un graphe orienté avec n sommets, des pondérations de flèches dans l'intervalle entre a et b et
    des flèches présentes dans une proportion p
    Elle prend en paramètres un nombre de sommets n, deux entiers a et b qui représentent 
    l'intervalle des valeurs possibles pour les poids des chemins et la proportion de flèches p.
    """
    # On genère une matrice de taille n x n
    M = np.zeros((n, n)) 
    infini = float('inf')
    # Pour chaque coefficient de la matrice
    for i in range (len(M)):
        for j in range(len(M)):
            # random.random() renvoie un flottant entre 0 et 1 
            if (random.random() < p):
                # Le coefficient reçoit un nombre entier dans l'intervalle [a, b[
                M[i][j] = random.randint(a, b-1) 
            else :
                # Le coefficient reçoit inf 
                M[i][j] = infini
    return M

def parcours_rouge(graphe, parcours):
    """
    Met en surbrillance le chemin rouge dans le graphe en utilisant le parcours donné.
    Prend en argument le graphe et le parcours souhaité.
    """
    for sommet in range(len(parcours) - 1):
        src = parcours[sommet]
        dest = parcours[sommet + 1]
        #print("arête :", src, " -> ", dest)
        # Vérifie si l'arête existe avant de la colorier
        if graphe.has_edge(src, dest):
            graphe.edges[src, dest]['color'] = 'red'
        else:
            print(f"Aucune arête entre {src} et {dest}")

def generer_graphe(m):
    """
    Génère un graphe à partir d'une matrice m.
    Chaque élément m[i][j] représente le poids de l'arc de i à j.
    """
    g = nx.DiGraph()
    for i in range(len(m)):
        g.add_node(i)
    for i in range(len(m)):
        for j in range(len(m)):
            if m[i][j] != float("inf"):
                g.add_edges_from([(i,j)], weight=m[i][j], color='black')
    return g

def afficher_graphe(g):
    """
    Affiche le graphe g avec les poids des arêtes.
    """
    # Récupération des couleurs
    edge_colors = [g.edges[u, v]['color'] for u, v in g.edges]
    layout = nx.circular_layout(g)
    labels = nx.get_edge_attributes(g, "weight")
    nx.draw(g, pos=layout, node_size=500, with_labels=True, connectionstyle="arc3,rad=0.05", edge_color=edge_colors)
    nx.draw_networkx_edge_labels(g, pos=layout, edge_labels=labels, label_pos=0.6)
    plt.show()

if __name__ == "__main__":
    m = graphe2(5, 0,-3,20)
    print(m)
