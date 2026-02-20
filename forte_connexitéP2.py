import numpy as np
from generation_graphes import graphe2
import matplotlib.pyplot as plt

def Trans2(matrice):
    """Algorithme de fermeture transitive à l'aide de l'algorithme de Roy-Marshall.
    Prend en paramètre la matrice d'un graphe orienté non pondéré et renvoie
    la matrice de fermeture transitive associée."""
    n = len(matrice)
    nouvelle_matrice = matrice
    for s in range(n):
        for r in range(n):
            if nouvelle_matrice[r,s]==1:
                for t in range(n):
                    if nouvelle_matrice[s,t]==1:
                        nouvelle_matrice[r,t] = 1
    return nouvelle_matrice

def fc(M):
    """prend en entrée la matrice d’un graphe orienté
    (non pondéré) et qui retourne True ou False à la question : "le graphe G donné
    par la matrice M (après numérotation de ses sommets) est-il fortement connexe ?"
    """
    # on retire la pondération
    for i in range(len(M)):
        for j in range(len(M)):
            if M[i][j] != float("inf"):
                M[i][j] = 1
            else:
                M[i][j] = 0
    # le graphe est fortement connexe si et seulement si la matrice de sa fermeture transitive
    # n'est composée que de 1 (np.ones(n) renvoie une matrice de taille n qui ne contient que
    # des 1) 
    matrice_fermeture_transitive = Trans2(M)
    return (matrice_fermeture_transitive == np.ones(len(matrice_fermeture_transitive))).all()

def test_stat_fc(n, nb_graphes=200):
    """Fonction qui retourne le pourcentage de graphes de taille n fortement connexe pour un test
    pourtant sur nb_graphes graphes (par défaut : 200), avec 50% de 1 (donc de flèches)
    """
    # on définit le nombre de graphes
    resultats = []
    for i in range(nb_graphes):
        # on récupère le resultat de fc pour chaque graphe
        resultats.append(fc(graphe2(n,0.5,1,2)))
    # pour connaître le taux de graphes fortement connexes on récupère le nombre
    # de fois où un graphe est fortement connexe et on divise par le nombre de graphes
    return resultats.count(True) / nb_graphes * 100

def test_stat_fc2(n,p, nb_graphes=200):
    """Fonction qui retourne le pourcentage de graphes de taille n fortement connexe pour un test
    pourtant sur nb_graphes graphes (par défaut : 200), avec p% de 1 (donc de flèches)
    """
    resultats = []
    for i in range(nb_graphes):
        # on récupère le resultat de fc pour chaque graphe
        resultats.append(fc(graphe2(n,p,1,2)))
    # pour connaître le taux de graphes fortement connexes on récupère le nombre
    # de fois où un graphe est fortement connexe et on divise par le nombre de graphes
    return resultats.count(True) / nb_graphes * 100

def seuil(n, pas=0.05):
    """Fonction qui détermine le seuil de proportion de flèches en dessous duquel les graphes
    ne sont pas presque toujours connexes. Prend en paramètre la taille des graphes n et le pas
    de diminution du seuil (défaut : pas=0.05). Fonction qui prend du temps avec n élevé et/ou un
    pas bas."""
    p = 1
    seuil = p
    # on réexécute le test jusqu'à ce que le pourcentage de graphe fortement connexe
    # soit en dessous de 99%
    while test_stat_fc2(n,p) >= 99.0 and p > 0:
        seuil = p
        # on enlève 0.05 au pourcentage de 1 dans les graphes
        # (on enlevait 0.01 avant mais cela prend beaucoup trop de temps avec n élevé)
        p -= pas
    return round(seuil, 4)

    
if __name__ == '__main__':
    m = np.array([[1,1,1,1],
                  [1,1,1,1],
                  [1,1,1,1],
                  [1,1,1,1],])
    m2 = np.array([[1,1,1,1],
                  [float('inf'),1,1,1],
                  [float('inf'),1,1,1],
                  [float('inf'),1,1,1],])
    # print(fc(m))
    # print(fc(m2))
    ### TEST DE TEST_STAT_FC AVEC DES GRAPHES ALLANT DE 1 A 20 SOMMETS ###
    # for i in range(1,21):
    #     print(f"Pourcentage de graphes fortement connexes avec {i} sommets : ")
    #     print(test_stat_fc(i))
    
    # print(seuil(15))
    ### TEST DE SEUIL AVEC DES GRAPHES ALLANT DE 10 A 40 SOMMETS ###
    resultats_seuil = []
    for i in range(10,41):
        # print("Seuil de proportion de flèche p en dessous duquel le graphe n'est pas "
        #        + f"presque toujours fortement connexe, avec des graphes à {i} sommets")
        resultats_seuil.append(seuil(i))
        
    x = [i for i in range(10,41)]
    plt.plot(x, resultats_seuil)
    plt.xlabel("Nombre de sommets n des graphes")
    plt.ylabel("Seuil de p")
    plt.title("Seuil de proportion de flèche p en dessous duquel le graphe n'est pas "
               + f"presque toujours fortement connexe, avec des graphes à n sommets")
    plt.legend()
    plt.show()
    