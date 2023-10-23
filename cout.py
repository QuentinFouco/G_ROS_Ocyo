import pandas as pd
import numpy as np
from data_reader import affretement, gen_dict_fourn, gen_camion_cap, gen_previsions_vente, gen_amortissement
from pfut import gen_usines_from_list, min_fourn_usine_i, min_fourn_usine_f, min_fourn_vente

### Récupération des données des tableaux
dict_affretement = affretement()
dict_fourn = gen_dict_fourn(dict_affretement)
dict_camion = gen_camion_cap()
dict_previsions = gen_previsions_vente()
dict_amortissement = gen_amortissement()

### Set up d'une architecture
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

dict_usines_f = gen_usines_from_list(table_usines_f[6])

dict_usines_i = gen_usines_from_list(table_usines_f[1])

### Recherche des chemins les moins couteux
dict_usines_i_cost = min_fourn_usine_i(dict_usines_i, dict_fourn, dict_affretement, dict_camion)

dict_usines_f_cost = min_fourn_usine_f(dict_usines_f, dict_usines_i_cost, dict_fourn, dict_affretement, dict_camion)

dict_vente_cost = min_fourn_vente(dict_usines_f_cost, dict_affretement, dict_camion, dict_previsions)

### Calcul du cout 
def cout_affretement(dict_vente_cost : dict, dict_previsions : dict) -> float:
    cout = 0
    for point_vente in dict_previsions.keys():
        cout += dict_previsions[point_vente]*dict_vente_cost[point_vente]['totalCost']
    return(cout)

def cout_amortissement(dict_usines_f : dict, dict_usines_i : dict, dict_amortissement : dict) -> float:
    cout_machine_usine_f = dict_amortissement['Perceuse'] + dict_amortissement['Plieuse']
    cout_machine_usine_i = dict_amortissement['Colleuse'] + dict_amortissement['Presse'] + dict_amortissement['MoulSieg'] + dict_amortissement['MoulDos'] + dict_amortissement['Decoupeuse']
    cout = len(dict_usines_f.keys())*cout_machine_usine_f + len(dict_usines_i.keys())*cout_machine_usine_i
    return(cout)

cout_aff = cout_affretement(dict_vente_cost, dict_previsions)
print('cout_aff = ',cout_aff)
cout_amo = cout_amortissement(dict_usines_f, dict_usines_i, dict_amortissement)
print('cout_amo = ',cout_amo)