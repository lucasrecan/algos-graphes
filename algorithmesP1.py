import numpy as np
import matplotlib.pyplot as plt
import generation_graphes as gr
import time
import random

def pl(M,s):
    """Parcours en largeur d'une matrice orientée M pondérée à partir d'un sommet de départ s."""
    file = [s]
    parcours = [s]
    while file!=[]:
        for i in range(len(M)):
            if M[file[0]][i] != float('inf'):
                if i not in parcours:
                    file.append(i)
                    parcours.append(i)
        file.pop(0)
    return parcours

def pp(M, s): 
    """Parcours en profondeur d'une matrice orientée M pondérée à partir d'un sommet de départ s."""
    pile = [s]
    parcours = [s]
    while pile != []:
        non_visite = []
        for i in range(len(M)):
            if M[pile[-1]][i] != float('inf') and i not in parcours: # si il y a un chemin vers un sommet non visité
                non_visite.append(i)
        if non_visite != []:
            sommet = non_visite[0] # prend le premier dans l'ordre alphabetique
            pile.append(sommet)
            parcours.append(sommet)
        else:
            pile.pop()
    return parcours

def Dijsktra(M,d):
    """
    Mesure les chemins les plus courts entre un sommet de départ et 
    tous les autres sommets d'une matrice avec des poids de signe positif
    Paramètres : 
    M : graphe sous forme d'une matrice
    d : sommet de départ
    """
    infini = float("inf")
    # L'algorithme ne fonctionne que pour les graphes pondérés à poids positif, donc on renvoit
    # None en cas de chemin à poids négatif.
    for i in range(len(M)):
        for j in range(len(M)):
            if M[i][j] < 0:
                return "Présence d'un poids négatif, l'algorithme ne peut pas fonctionner."
    # dictionnaire resultat qui stocke le chemin le plus court du sommet d vers chaque sommet
    # du graphe
    resultat = {}
    resultat[d] = (0, [d])
    # On remplit deux listes pour les couples de dist(s) et pred(s) pour chaque sommet,
    # dist(s) étant la distance minimale entre s et l'origine et pred(s) le sommet qui précède.
    dist = {}
    pred = {}
    for sommet in range(len(M)):
        dist[sommet], pred[sommet] = infini, None
    # Initialisation :
    # dist(d) prend la valeur 0 et pred(d) prend d (d étant le sommet de départ)
    dist[d], pred[d] = 0, d
    # On initialise une variable choix qui constitue la colonne choix de l'algorithme
    # Ici, elle prend (dist(d), pred(d), d)
    choix = dist[d], pred[d], d
    # On initialise une liste sommets_choisis qui garde en mémoire les sommets choisis
    # pour éviter de les sélectionner à nouveau et pour détecter quand le sommet d'arrivée
    # est choisi par l'algorithme
    sommets_choisis = [d]
    # On récupère les sommets accessibles à l'aide d'un parcours en largeur,
    # pour vérifier que chaque sommet d'arrivée est joignable depuis le sommet de départ.
    sommets_accessibles = pl(M, d)
    # On applique l'algorithme pour chaque sommet de la matrice
    # Ici, sommet_arrivee est le sommet d'arrivée
    for sommet_arrivee in range(len(M)):
        if sommet_arrivee in sommets_accessibles:
            # tant que le sommet d'arrivée n'est pas choisi
            while sommet_arrivee not in sommets_choisis:
                # on itère parmi tous les sommets de M
                for sommet in range(len(M)):
                    # l'itération se fait parmi les sommets qui n'ont pas été choisi
                    # (on ne "regarde" pas les sommets dont la colonne a été fermée)
                    if sommet not in sommets_choisis:
                        # si dist(s) + poids(s,t) < dist(t)
                        if choix[0] + M[choix[2]][sommet] < dist[sommet]:
                            # dist(t), pred(t) est remplacé par (dist(s) + poids(s,t), s)
                            dist[sommet], pred[sommet] = choix[0] + M[choix[2]][sommet], choix[2]
                # definition du nouveau choix qui sera le sommet jamais choisi dont la distance est la plus basse :
                minimum = infini
                sommet_choisi = d
                for sommet in range(len(M)):
                    if sommet not in sommets_choisis:
                        if dist[sommet] < minimum:
                            minimum = dist[sommet]
                            sommet_choisi = sommet
                # choix prend les nouvelles données du sommet choisi
                choix = dist[sommet_choisi], pred[sommet_choisi], sommet_choisi
                # on ajoute le sommet choisi à la liste des sommets déjà choisis, "fermant" sa colonne
                sommets_choisis.append(sommet_choisi)
            # Quand le sommet d'arrivée est choisi on a donc un chemin de poids dist[sommet_arrivee] et
            # de chemin [d, ..., pred[[pred[sommet_choisi]], pred[sommet_choisi], sommet_choisi]
            chemin = [sommet_arrivee]
            sommet = sommet_arrivee
            while sommet != d:
                sommet = pred[sommet]
                chemin.append(sommet)
            # on réécrit le chemin dans le bon ordre
            chemin.reverse()
            resultat[sommet_arrivee] = dist[sommet_arrivee], chemin
        else:
            resultat[sommet_arrivee] = f"Sommet non joignable depuis {d}" 
    return resultat
    
def BellmanFord(M, d, afficher_compteur=False) :
    """
    Mesure les chemins les plus courts entre un sommet de départ et 
    tous les autres sommets d'une matrice avec des poids de signe quelconque
    Prend en paramètre une matrice M et un sommet de départ d
    Chaque sommet de sortie s est associé à un poids et à une liste de sommet (chemin)
    """
    NB_TOUR_MAX = len(M) - 1 # Nombre maximum de tours
    infini = float("inf")
    # Initialisation du tableau des distances et prédécesseurs
    dist = {}
    pred = {}
    # On initialise les distances et prédécesseurs antérieurs
    # On assigne des valeurs infinies à tous les sommets sauf le sommet de départ
    for i in range(len(M)):
        dist[i] = (infini)
        pred[i] = None
    pred[d] = d
    dist[d] = 0
    # dist_ancien et pred_ancien permettent de comparer le tour n et le tour n-1
    # pour détecter la présence d'un cycle à poids négatif
    dist_ancien = {}
    pred_ancien = {}
    
    # On crée l'ordre des flèches
    liste_fleches = []
    for i in range(len(M)):
        for j in range(len(M)):
            if M[i][j] != infini:
                liste_fleches.append((i,j))
    compteur = 0
    # on fait (n-1 sommets) tours
    for sommet in range(NB_TOUR_MAX):
        compteur += 1
        dist_ancien, pred_ancien = dist, pred
        # On parcourt chaque coefficient de la matrice qui correspond à chaque flèche du graphe
        # dans l'ordre alphabétique ou numérique du graphe
        for (depart, arrivee) in liste_fleches:
            # si dist(s) + poids(s,t) < dist(t)
            if dist[depart] + M[depart][arrivee] < dist[arrivee]:
                # dist(t), pred(t) = dist(s) + poids(s, t), s
                dist[arrivee] = dist[depart] + M[depart][arrivee]
                pred[arrivee] = depart 
     
    resultat = {}      
    for sommet in range(len(M)):
        # Si il y a une différence entre le tour n et le tour n-1,
        # un cycle de poids négatif est présent
        if dist[sommet] != dist_ancien[sommet] or pred[sommet] != pred_ancien[sommet]:
            resultat[sommet] = "Présence d'un cycle de poids négatif"
        #Si dist(s) est infini alors le sommet s n'est pas joignable depuis le sommet d
        elif dist[sommet] == infini:
            resultat[sommet] = f"sommet non joignable depuis {d} par un chemin dans le graphe."
        else:
            predecesseur = sommet
            chemin = [sommet]
            # On initialise une variable cycle et compteur pour vérifier la présence d'un cycle
            cycle = False
            compteur = 0
            # Si en remontant les prédecesseurs on atteint le sommet de départ alors
            # on obtient le chemin.
            # Si le compteur dépasse le nombre de sommet du graphe alors le chemin 
            # passe par plusieurs sommets et il y a donc un cycle
            while predecesseur != d and compteur < NB_TOUR_MAX+1:
                compteur += 1
                if predecesseur != pred[predecesseur]:
                    predecesseur_sommet = pred[predecesseur]
                    chemin.append(predecesseur_sommet)
                    predecesseur = predecesseur_sommet
                else:
                    cycle = True
                    break
            # Si il n'y a pas de cycle alors on retourne les éléments de la liste
            # et on ajoute le résultat au dictionnaire resultat
            if not cycle and compteur != NB_TOUR_MAX+1:
                chemin.reverse()
                resultat[sommet] = (dist[sommet], chemin)
            else:
                resultat[sommet] = "Présence d'un cycle de poids négatif"
    if afficher_compteur:
        print(f"Nombre de tours effectués : {compteur}")
    return resultat
                
def BellmanFord_aleatoire(M, d, afficher_compteur=False) :
    """
    Mesure les chemins les plus courts entre un sommet de départ et 
    tous les autres sommets d'une matrice avec des poids de signe quelconque
    Prend en paramètre une matrice M et un sommet de départ d
    Chaque sommet de sortie s est associé à un poids et à une liste de sommet (chemin)
    """
    NB_TOUR_MAX = len(M) - 1 # Nombre maximum de tours
    infini = float("inf")
    # Initialisation du tableau des distances et prédécesseurs
    dist = {}
    pred = {}
    # On initialise les distances et prédécesseurs antérieurs
    # On assigne des valeurs infinies à tous les sommets sauf le sommet de départ
    for i in range(len(M)):
        dist[i] = (infini)
        pred[i] = None
    pred[d] = d
    dist[d] = 0
    # dist_ancien et pred_ancien permettent de comparer le tour n et le tour n-1
    # pour détecter la présence d'un cycle à poids négatif
    dist_ancien = {}
    pred_ancien = {}
    
    # On crée l'ordre des flèches
    liste_fleches = []
    for i in range(len(M)):
        for j in range(len(M)):
            if M[i][j] != infini:
                liste_fleches.append((i,j))
    # ordre aléatoire grâce à la méthode shuffle()
    random.shuffle(liste_fleches)
    # on fait (n-1 sommets) tours
    for compteur_tours in range(NB_TOUR_MAX):
        dist_ancien, pred_ancien = dist.copy(), pred.copy()
        # On parcourt chaque coefficient de la matrice qui correspond à chaque flèche du graphe
        # dans l'ordre alphabétique ou numérique du graphe
        for (depart, arrivee) in liste_fleches:
            # si dist(s) + poids(s,t) < dist(t)
            if dist[depart] + M[depart][arrivee] < dist[arrivee]:
                # dist(t), pred(t) = dist(s) + poids(s, t), s
                dist[arrivee] = dist[depart] + M[depart][arrivee]
                pred[arrivee] = depart
        if dist==dist_ancien and pred==pred_ancien:
            break
     
    resultat = {}      
    for sommet in range(len(M)):
        # Si il y a une différence entre le tour n et le tour n-1,
        # un cycle de poids négatif est présent
        if dist[sommet] != dist_ancien[sommet] or pred[sommet] != pred_ancien[sommet]:
            resultat[sommet] = "Présence d'un cycle de poids négatif"
        #Si dist(s) est infini alors le sommet s n'est pas joignable depuis le sommet d
        elif dist[sommet] == infini:
            resultat[sommet] = f"sommet non joignable depuis {d} par un chemin dans le graphe."
        else:
            predecesseur = sommet
            chemin = [sommet]
            # On initialise une variable cycle et compteur pour vérifier la présence d'un cycle
            cycle = False
            compteur = 0
            # Si en remontant les prédecesseurs on atteint le sommet de départ alors
            # on obtient le chemin.
            # Si le compteur dépasse le nombre de sommet du graphe alors le chemin 
            # passe par plusieurs sommets et il y a donc un cycle
            while predecesseur != d and compteur < NB_TOUR_MAX+1:
                compteur += 1
                if predecesseur != pred[predecesseur]:
                    predecesseur_sommet = pred[predecesseur]
                    chemin.append(predecesseur_sommet)
                    predecesseur = predecesseur_sommet
                else:
                    cycle = True
                    break
            # Si il n'y a pas de cycle alors on retourne les éléments de la liste
            # et on ajoute le résultat au dictionnaire resultat
            if not cycle and compteur != NB_TOUR_MAX+1:
                chemin.reverse()
                resultat[sommet] = (dist[sommet], chemin)
            else:
                resultat[sommet] = "Présence d'un cycle de poids négatif"
    if afficher_compteur:
        print(f"Nombre de tours effectués : {compteur_tours+1}")
    return resultat

def BellmanFord_largeur(M, d, afficher_compteur=False) :
    """
    Mesure les chemins les plus courts entre un sommet de départ et 
    tous les autres sommets d'une matrice avec des poids de signe quelconque
    Prend en paramètre une matrice M et un sommet de départ d
    Chaque sommet de sortie s est associé à un poids et à une liste de sommet (chemin)
    """
    NB_TOUR_MAX = len(M) - 1 # Nombre maximum de tours
    infini = float("inf")
    # Initialisation du tableau des distances et prédécesseurs
    dist = {}
    pred = {}
    # On initialise les distances et prédécesseurs antérieurs
    # On assigne des valeurs infinies à tous les sommets sauf le sommet de départ
    for i in range(len(M)):
        dist[i] = (infini)
        pred[i] = None
    pred[d] = d
    dist[d] = 0
    # dist_ancien et pred_ancien permettent de comparer le tour n et le tour n-1
    # pour détecter la présence d'un cycle à poids négatif
    dist_ancien = {}
    pred_ancien = {}
    
    # On crée l'ordre des flèches
    liste_fleches = []
    parcours = pl(M,d)
    for s in parcours:
        for t in range(len(M)):
            if M[s][t] != infini:
                liste_fleches.append((s,t))
    # on fait (n-1 sommets) tours
    for compteur_tours in range(NB_TOUR_MAX):
        dist_ancien, pred_ancien = dist.copy(), pred.copy()
        # On parcourt chaque coefficient de la matrice qui correspond à chaque flèche du graphe
        for (depart, arrivee) in liste_fleches:
            # si dist(s) + poids(s,t) < dist(t)
            if dist[depart] + M[depart][arrivee] < dist[arrivee]:
                # dist(t), pred(t) = dist(s) + poids(s, t), s
                dist[arrivee] = dist[depart] + M[depart][arrivee]
                pred[arrivee] = depart 
        if dist==dist_ancien and pred==pred_ancien:
            break
     
    resultat = {}      
    for sommet in range(len(M)):
        # Si il y a une différence entre le tour n et le tour n-1,
        # un cycle de poids négatif est présent
        if dist[sommet] != dist_ancien[sommet] or pred[sommet] != pred_ancien[sommet]:
            resultat[sommet] = "Présence d'un cycle de poids négatif"
        #Si dist(s) est infini alors le sommet s n'est pas joignable depuis le sommet d
        elif dist[sommet] == infini:
            resultat[sommet] = f"sommet non joignable depuis {d} par un chemin dans le graphe."
        else:
            predecesseur = sommet
            chemin = [sommet]
            # On initialise une variable cycle et compteur pour vérifier la présence d'un cycle
            cycle = False
            compteur = 0
            # Si en remontant les prédecesseurs on atteint le sommet de départ alors
            # on obtient le chemin.
            # Si le compteur dépasse le nombre de sommet du graphe alors le chemin 
            # passe par plusieurs sommets et il y a donc un cycle
            while predecesseur != d and compteur < NB_TOUR_MAX+1:
                compteur += 1
                if predecesseur != pred[predecesseur]:
                    predecesseur_sommet = pred[predecesseur]
                    chemin.append(predecesseur_sommet)
                    predecesseur = predecesseur_sommet
                else:
                    cycle = True
                    break
            # Si il n'y a pas de cycle alors on retourne les éléments de la liste
            # et on ajoute le résultat au dictionnaire resultat
            if not cycle and compteur != NB_TOUR_MAX+1:
                chemin.reverse()
                resultat[sommet] = (dist[sommet], chemin)
            else:
                resultat[sommet] = "Présence d'un cycle de poids négatif"
    if afficher_compteur:
        print(f"Nombre de tours effectués : {compteur_tours+1}")
    return resultat

def BellmanFord_profondeur(M, d, afficher_compteur=False) :
    """
    Mesure les chemins les plus courts entre un sommet de départ et 
    tous les autres sommets d'une matrice avec des poids de signe quelconque
    Prend en paramètre une matrice M et un sommet de départ d
    Chaque sommet de sortie s est associé à un poids et à une liste de sommet (chemin)
    """
    NB_TOUR_MAX = len(M) - 1 # Nombre maximum de tours
    infini = float("inf")
    # Initialisation du tableau des distances et prédécesseurs
    dist = {}
    pred = {}
    # On initialise les distances et prédécesseurs antérieurs
    # On assigne des valeurs infinies à tous les sommets sauf le sommet de départ
    for i in range(len(M)):
        dist[i] = (infini)
        pred[i] = None
    pred[d] = d
    dist[d] = 0
    # dist_ancien et pred_ancien permettent de comparer le tour n et le tour n-1
    # pour détecter la présence d'un cycle à poids négatif
    dist_ancien = {}
    pred_ancien = {}
    # On crée l'ordre des flèches
    liste_fleches = []
    parcours = pp(M,d)
    for s in parcours:
        for t in range(len(M)):
            if M[s][t] != infini:
                liste_fleches.append((s,t))
    # on fait (n-1 sommets) tours
    for compteur_tours in range(NB_TOUR_MAX):
        dist_ancien, pred_ancien = dist.copy(), pred.copy()
        # On parcourt chaque coefficient de la matrice qui correspond à chaque flèche du graphe
        for (depart, arrivee) in liste_fleches:
            # si dist(s) + poids(s,t) < dist(t)
            if dist[depart] + M[depart][arrivee] < dist[arrivee]:
                # dist(t), pred(t) = dist(s) + poids(s, t), s
                dist[arrivee] = dist[depart] + M[depart][arrivee]
                pred[arrivee] = depart 
        if dist==dist_ancien and pred==pred_ancien:
            break
     
    resultat = {}      
    for sommet in range(len(M)):
        # Si il y a une différence entre le tour n et le tour n-1,
        # un cycle de poids négatif est présent
        if dist[sommet] != dist_ancien[sommet] or pred[sommet] != pred_ancien[sommet]:
            resultat[sommet] = "Présence d'un cycle de poids négatif"
        #Si dist(s) est infini alors le sommet s n'est pas joignable depuis le sommet d
        elif dist[sommet] == infini:
            resultat[sommet] = f"sommet non joignable depuis {d} par un chemin dans le graphe."
        else:
            predecesseur = sommet
            chemin = [sommet]
            # On initialise une variable cycle et compteur pour vérifier la présence d'un cycle
            cycle = False
            compteur = 0
            # Si en remontant les prédecesseurs on atteint le sommet de départ alors
            # on obtient le chemin.
            # Si le compteur dépasse le nombre de sommet du graphe alors le chemin 
            # passe par plusieurs sommets et il y a donc un cycle
            while predecesseur != d and compteur < NB_TOUR_MAX+1:
                compteur += 1
                if predecesseur != pred[predecesseur]:
                    predecesseur_sommet = pred[predecesseur]
                    chemin.append(predecesseur_sommet)
                    predecesseur = predecesseur_sommet
                else:
                    cycle = True
                    break
            # Si il n'y a pas de cycle alors on retourne les éléments de la liste
            # et on ajoute le résultat au dictionnaire resultat
            if not cycle and compteur != NB_TOUR_MAX+1:
                chemin.reverse()
                resultat[sommet] = (dist[sommet], chemin)
            else:
                resultat[sommet] = "Présence d'un cycle de poids négatif"
    if afficher_compteur:
        print(f"Nombre de tours effectués : {compteur_tours+1}")
    return resultat

def TempsDij(n):
    """Mesure et renvoie le temps d'exécution de l'algorithme de Dijsktra sur un graphe de taille n."""
    matrice = gr.graphe2(n, 0.25, 1, 50)
    # on récupère l'heure actuelle en secondes
    t1 = time.time()
    Dijsktra(matrice, 0)
    #on retourne la différence entre l'heure actuelle et l'heure relevée avant l'exécution
    # de Dijsktra
    return time.time() - t1
    
def TempsBF(n, choix_liste="largeur"):
    """Mesure et renvoie le temps d'exécution de l'algorithme de Bellman-Ford sur un graphe de taille n."""
    matrice = gr.graphe2(n, 0.25, 1, 50)
    # on récupère l'heure actuelle en secondes
    t1 = time.time()
    match choix_liste:
        case "largeur":
            # print("Exécution Bellman Ford avec le choix des flèches obtenu avec un parcours en largeur")
            BellmanFord_largeur(matrice, 0)
        case "profondeur":
            # print("Exécution Bellman Ford avec le choix des flèches obtenu avec un parcours en profondeur")
            BellmanFord_profondeur(matrice, 0)
        case "aléatoire":
            # print("Exécution Bellman Ford avec le choix des flèches obtenu en aléatoire")
            BellmanFord_aleatoire(matrice, 0)
        case _:
            print("Valeur de choix_liste possibles : largeur, profondeur ou aléatoire. Algorithme non exécuté")
    #on retourne la différence entre l'heure actuelle et l'heure relevée avant l'exécution
    # de Dijsktra
    return time.time() - t1
    
def comparaison_temps(n):
    """Compare et affiche graphiquement la différence de temps de calcul des deux algorithmes
    de plus court chemin Dijsktra et Bellman-Ford sur des matrices de taille 2 à n. Prend en argument
    la taille n de la dernière matrice."""
    if n>2:
        # liste de nombre de sommets
        nb_sommets = [i for i in range(2,n)]
        # liste des temps effectués par Dijsktra
        temps_Dij = [TempsDij(i) for i in range(2,n)]
        #liste des temps effectués par Bellman-Ford
        temps_BF = [TempsBF(i) for i in range(2,n)]
        plt.plot(nb_sommets, temps_Dij, label="Temps Dijsktra")
        plt.plot(nb_sommets, temps_BF, label="Temps Bellman-Ford")
        plt.xlabel("Nombre de sommets")
        plt.ylabel("Temps d'exécution (en seconde)")
        plt.title("Comparaison des temps des algorithmes Dijsktra et Bellman-Ford")
        plt.legend()
        plt.show()
        
if __name__ == "__main__":
    infini = float("inf")
    g1 = np.array([[infini, 2, infini, infini],
         [infini, infini, infini, 3],
         [infini, 4, infini, infini],
         [infini, infini, 2, infini]])
    g2 = np.array([[infini, 2,  infini,  infini, 3,  infini,  infini],
                   [infini, infini, infini, 3, infini, infini,  infini],
                   [infini, -2, infini, infini, infini, infini, infini],
                   [infini, infini, -2, infini, infini, infini, infini],
                   [infini, infini, 3, infini, infini, infini, infini],
                   [infini, infini, infini, infini, 2, infini, infini],
                   [infini, infini, infini, 1, infini, 4, infini],])
    g3 = gr.graphe2(8, 0.3, 1, 20)
    parcours_Dij_g1 = Dijsktra(g1,3)
    parcours_Dij_g2 = Dijsktra(g2,0)
    parcours_Dij_g3 = Dijsktra(g3,0)
    print(parcours_Dij_g1)
    print(parcours_Dij_g2)
    print(parcours_Dij_g3)
    parcours_BF_g1 = BellmanFord(g1,3)
    parcours_BF_g2 = BellmanFord(g2,6)
    parcours_BF_g3 = BellmanFord(g3,0)
    print(parcours_BF_g1)
    print(parcours_BF_g2)
    print(parcours_BF_g3)
    graphe1 = gr.generer_graphe(g1)
    gr.parcours_rouge(graphe1, parcours_Dij_g1[1][1])
    gr.afficher_graphe(graphe1)
    graphe3 = gr.generer_graphe(g3)
    gr.parcours_rouge(graphe3, parcours_Dij_g3[5][1])
    gr.afficher_graphe(graphe3)
    graphe2 = gr.generer_graphe(g2)
    gr.parcours_rouge(graphe2, parcours_BF_g2[4][1])
    gr.afficher_graphe(graphe2)
    graphe3 = gr.generer_graphe(g3)
    gr.parcours_rouge(graphe3, parcours_BF_g3[5][1])
    gr.afficher_graphe(graphe3)
    # BellmanFord_aleatoire(g, 25, afficher_compteur=True)
    # BellmanFord_largeur(g, 25, afficher_compteur=True)
    # BellmanFord_profondeur(g, 25, afficher_compteur=True)
    # print(TempsDij(200))
    # print(TempsBF(200))
    # comparaison_temps(200)