import pandas as pd
import numpy as np
from data_reader import affretement, gen_dict_fourn, gen_camion_cap, gen_previsions_vente

### Récupération des données des tableaux
dict_affretement = affretement()
dict_fourn = gen_dict_fourn(dict_affretement)
dict_camion = gen_camion_cap()
dict_previsions = gen_previsions_vente()

def gen_usine(index : int) -> tuple:
    """Genere le dictionnaire des usines a partir de la décomposition bianaire 
    d'un incrément

    Args:
        index (int): incrément permettant d'identifier de façon unique une répartition d'usine

    Returns:
        tuple (dict, int) : 
            - dict : dictionnaire des usines
            - int : nombre d'usine 
    """
    villes = ['Madrid','Marseille','Turin','Munich','Bruxelles']
    dict_usine = {}
    nb_usine_f = 0
    for ville in villes:
        mod_index = index%2
        nb_usine_f = nb_usine_f + mod_index
        index = index//2
        dict_usine_f[ville] = mod_index
    return(dict_usine, nb_usine_f)

table_usines_f = [
    [0,0,0,0,1],
    [0,0,0,1,0],
    [0,0,1,0,0],
    [0,1,0,0,0],
    [1,0,0,0,0],
    [0,0,0,1,1],
    [0,0,1,0,1],
    [0,1,0,0,1],
    [1,0,0,0,1],
    [0,0,1,1,0],
    [0,1,0,1,0],
    [1,0,0,1,0],
    [0,1,1,0,0],
    [1,0,1,0,0],
    [1,1,0,0,0],
    [0,0,1,1,1],
    [0,1,0,1,1],
    [1,0,0,1,1],
    [0,1,1,0,1],
    [1,0,1,0,1],
    [0,1,1,1,0],
    [1,0,1,1,0],
    [1,1,1,0,0],
    [0,1,1,1,1],
    [1,0,1,1,1],
    [1,1,0,1,1],
    [1,1,1,0,1],
    [1,1,1,1,0],
    [1,1,1,1,1]
]

def gen_usines_from_list(liste_usines : list) -> dict:
    """Génère le dictionnaire des usines et de leur présence en fonction d'une liste de binaire

    Args:
        liste_usines (list): Liste de 0 ou 1 décrivant si il y a une usine ou non a la ville du même index dans la liste "villes"

    Returns:
        dict:  Dictionnaire des usines
            dict : ('<ville>': int)
    """
    villes = ['Madrid','Marseille','Turin','Munich','Bruxelles']
    dict_usine = {}
    for i, ville in enumerate(villes):
        dict_usine[ville] = liste_usines[i]
    return (dict_usine)    

# dict_usine_test, nb_usine = gen_usine(2**5-1)
# villes = ['Madrid','Marseille','Turin','Munich','Bruxelles']
# print(dict_usine_test.keys())
# for ville in villes:
#     print(dict_usine_test[ville])
# print(nb_usine)
    
    
dict_usine_f = {
    'Madrid':0,
    'Marseille':1,
    'Turin':1,
    'Munich':1,
    'Bruxelles':1,
}

dict_usine_i = {
    'Madrid':0,
    'Marseille':1,
    'Turin':1,
    'Munich':1,
    'Bruxelles':1,
}



def min_fourn_usine_i (dict_usine_i : dict, dict_fourn : dict, dict_affretement : dict, dict_camion : dict) -> dict:
    """Calcul le chemin optimal entre les usines intermédiaires et leurs fournisseurs

    Args:
        dict_usine_i (dict): Dictionnaire des usines intermédiaires
            dict : ('<ville>': int) 
        dict_fourn (dict): Dictionnaire des matières premières et de la localisation de leur fournisseur
            dict : ('<produit>' : list['<ville>','<ville>'])
        dict_affretement (dict): Dictionnaire des couts d'affretement
            dict : ('<depart>' : dict ('<arrivée>' : int(<cout>)))
        dict_camion (dict): Dictionnaire de la capacité des camions pour chaque matière
            dict : ('<matière>' : int(<capacité>))

    Returns:
        dict: ('<usine>' : dict ('<matière>' : tuple('<fournisseur>', <cout>)
                                'totalCost' : float(Somme des couts)
                                'Volume' : int(nb equivalants chaises produits)))
    """
    dict_usine_i_cost = {}
    for usine in dict_usine_i.keys():
        if dict_usine_i[usine]>0:
            dict_cost_mat = {}
            totalCost = 0
            for matiere in ['Tissus', 'Mousse', 'Plastique']:
                aff_cost = []
                for fourn in dict_fourn[matiere]:
                    aff_cost.append(2*dict_affretement[usine][fourn]/dict_camion[matiere]) #On multiplie par 2 car pour chaque chaise on a besoin de 2 fois chaque ressource
                id_min = np.argmin(aff_cost)
                dict_cost_mat[matiere] = (dict_fourn[matiere][id_min], aff_cost[id_min])
                totalCost = totalCost + aff_cost[id_min]
            dict_cost_mat['totalCost']= totalCost
            dict_cost_mat['Volume']= 0
            dict_usine_i_cost[usine] = dict_cost_mat
    return(dict_usine_i_cost)

def min_fourn_usine_f (dict_usine_f : dict, dict_usine_i_cost : dict, dict_fourn : dict, dict_affretement : dict, dict_camion : dict) -> dict:
    """Calcul le chemin optimal entre les usines finales et leurs fournisseurs

    Args:
        dict_usine_f (dict): Dictionnaire des usines finales
            dict : ('<ville>': int) 
        dict_usine_i_cost (dict): Dictionnaire des usines intermédiaires avec leur fournisseur et leurs couts d'affretement
            dict: ('<usine>' : dict ('<matière>' : tuple('<fournisseur>', <cout>)
                            'totalCost' : float(Somme des couts)
                            'Volume' : int(nb equivalants chaises produits)))
        dict_fourn (dict): Dictionnaire des matières premières et de la localisation de leur fournisseur
            dict : ('<produit>' : list['<ville>','<ville>'])
        dict_affretement (dict): Dictionnaire des couts d'affretement
            dict : ('<depart>' : dict ('<arrivée>' : int(<cout>)))
        dict_camion (dict): Dictionnaire de la capacité des camions pour chaque matière
            dict : ('<matière>' : int(<capacité>))

    Returns:
        dict: ('<usine>' : dict ('Tube' : tuple('<fournisseur>', <cout>)
                                'Usine_i' : tuple('<fournisseur>', <cout_affretement>)
                                'totalCost' : float(Somme des couts)
                                'Volume' : int(nb equivalants chaises produits)))
    """
    dict_usine_f_cost = {}
    for usine_f in dict_usine_f.keys():
        if dict_usine_f[usine_f]>0:
            dict_cost_mat = {}
            totalCost = 0
            ### Recherche du meilleur fournisseur de tube
            aff_cost=[]
            matiere = 'Tube'
            for fourn in dict_fourn[matiere]:
                aff_cost.append(dict_affretement[usine_f][fourn]/dict_camion[matiere])
            id_min = np.argmin(aff_cost)
            dict_cost_mat[matiere] = (dict_fourn[matiere][id_min], aff_cost[id_min])
            totalCost = totalCost + aff_cost[id_min]
            ### Recherche du meilleur fournisseur de dossier et assise
            aff_cost=[]
            keys = []
            for usine_i in dict_usine_i_cost.keys():
                cout_unitaire_usine_i = dict_usine_i_cost[usine_i]['totalCost']
                cout_unitaire_affretement = dict_affretement[usine_f][usine_i]/dict_camion['Dossier']+dict_affretement[usine_f][usine_i]/dict_camion['Assise']
                aff_cost.append(cout_unitaire_usine_i + cout_unitaire_affretement)
                keys.append(usine_i)
            id_min = np.argmin(aff_cost)
            dict_cost_mat['Usine_i'] = (keys[id_min], cout_unitaire_affretement)
            totalCost = totalCost + aff_cost[id_min]
            dict_cost_mat['totalCost'] = totalCost
            dict_cost_mat['Volume'] = 0
            dict_usine_f_cost[usine_f] = dict_cost_mat
    return(dict_usine_f_cost)

def min_fourn_vente (dict_usine_f_cost : dict, dict_affretement : dict, dict_camion : dict, dict_previsions : dict) -> dict:
    """Calcul le chemin optimal entre les points de ventes et leurs fournisseurs

    Args:
        dict_usine_f_cost (dict): Dictionnaire des usines finales avec leur fournisseur et leurs couts d'affretement
            dict: ('<usine>' : dict ('Tube' : tuple('<fournisseur>', <cout>)
                                'Usine_i' : tuple('<fournisseur>', <cout_affretement>)
                                'totalCost' : float(Somme des couts)
                                'Volume' : int(nb equivalants chaises produits)))
        dict_affretement (dict): Dictionnaire des couts d'affretement
            dict : ('<depart>' : dict ('<arrivée>' : int(<cout>)))
        dict_camion (dict): Dictionnaire de la capacité des camions pour chaque matière
            dict : ('<matière>' : int(<capacité>))
        dict_previsions (dict): Dictionnaire des prévisions de vente par point de vente
            dict ('<Ville>':int(NbChaise))

    Returns:
        dict: ('<ville>' : dict ('Usine_f' : '<fournisseur>'
                                'totalCost' : float(Somme des couts)
                                'Volume' : int(nb equivalants chaises produits)))
    """
    dict_vente_cost = {}
    for point_vente in dict_previsions.keys():
        dict_cost = {}
        totalCost = 0
        aff_cost = []
        keys = []
        for usine_f in dict_usine_f_cost.keys():
            aff_cost.append(dict_usine_f_cost[usine_f]['totalCost'] + dict_affretement[point_vente][usine_f]/dict_camion['Chaise'])
            keys.append(usine_f)
        id_min = np.argmin(aff_cost)
        dict_cost['Usine_f'] = keys[id_min]
        totalCost = totalCost + aff_cost[id_min]
        dict_cost['totalCost'] = totalCost
        dict_vente_cost[point_vente] = dict_cost 
        dict_cost['Volume'] = dict_previsions[point_vente]
    return(dict_vente_cost)