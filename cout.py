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

dict_usines_f = gen_usines_from_list(table_usines_f[-1])

dict_usines_i = gen_usines_from_list(table_usines_f[-1])

### Recherche des chemins les moins couteux
dict_usines_i_cost = min_fourn_usine_i(dict_usines_i, dict_fourn, dict_affretement, dict_camion)

print('Arborescence usine intermediaire :')
for usine in dict_usines_i_cost.keys():
    dict_usine = dict_usines_i_cost[usine]
    print('\t', usine)
    for matiere in dict_usine.keys():
        print('\t\t', matiere, dict_usine[matiere])
        

dict_usines_f_cost = min_fourn_usine_f(dict_usines_f, dict_usines_i_cost, dict_fourn, dict_affretement, dict_camion)

print('\nArborescence usine intermediaire :')
for usine in dict_usines_f_cost.keys():
    dict_usine = dict_usines_f_cost[usine]
    print('\t',usine)
    for matiere in dict_usine.keys():
        print('\t\t', matiere, dict_usine[matiere])

            
dict_vente_cost = min_fourn_vente(dict_usines_f_cost, dict_affretement, dict_camion, dict_previsions)

print('\nArborescence point de vente :')
for point_vente in dict_vente_cost.keys():
    dict_point_vente = dict_vente_cost[point_vente]
    print('\t',point_vente)
    for matiere in dict_point_vente.keys():
        print('\t\t', matiere, dict_point_vente[matiere])

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

for point_vente in dict_vente_cost.keys():
    dict_usines_f_cost[dict_vente_cost[point_vente]['Usine_f']]['Volume'] += dict_vente_cost[point_vente]['Volume']

for usine_f in dict_usines_f_cost.keys():
    dict_usines_i_cost[dict_usines_f_cost[usine_f]['Usine_i'][0]]['Volume'] += dict_usines_f_cost[usine_f]['Volume']


import networkx as nx
import matplotlib.pyplot as plt
dict_colors = {}
color_index = 0
G = nx.Graph()

## Creation noeud fournisseur
for matiere in dict_fourn.keys():
    dict_colors['Fournisseur : '+matiere] = color_index
    color_index += 1
    for ville in dict_fourn[matiere]:
        if matiere=='Tube':
            subset = 9
        else:
            subset = 10
        volume = 0
        if matiere != 'Tube':
            for usine in dict_usines_i_cost.keys():
                if dict_usines_i_cost[usine][matiere][0] == ville:
                    volume += dict_usines_i_cost[usine]['Volume']
        else:
            for usine in dict_usines_f_cost.keys():
                if dict_usines_f_cost[usine][matiere][0] == ville:
                    volume += dict_usines_f_cost[usine]['Volume']
        G.add_node(matiere+ville, node_type='Fournisseur : '+matiere, place=ville, cout_unitaire = 0, subset=subset, volume=volume)


## Création noeud usine intermédiaire
dict_colors['Usine intermédiaire'] = color_index
color_index += 1
for usine in dict_usines_i_cost.keys():
    G.add_node('Usine_i'+usine, node_type='Usine intermédiaire', place=usine, cout_unitaire = dict_usines_i_cost[usine]['totalCost'], subset=9, volume=dict_usines_i_cost[usine]['Volume'])
    i = 0
    for matiere in dict_usines_i_cost[usine].keys():
        if i<3:
            i+=1
            G.add_edge('Usine_i'+usine, matiere+dict_usines_i_cost[usine][matiere][0], volume=0)



## Création noeud usine finale
dict_colors['Usine finale'] = color_index
color_index += 1
for usine in dict_usines_f_cost.keys():
    G.add_node('Usine_f'+usine, node_type='Usine finale', place=usine, cout_unitaire = dict_usines_f_cost[usine]['totalCost'], subset=8, volume=dict_usines_f_cost[usine]['Volume'])
    G.add_edge('Usine_f'+usine, 'Tube'+dict_usines_f_cost[usine]['Tube'][0], volume=0)
    G.add_edge('Usine_f'+usine, 'Usine_i'+dict_usines_f_cost[usine]['Usine_i'][0], volume=0)

## Création noeud point de vente
dict_colors['Point de vente'] = color_index
color_index += 1
for site in dict_vente_cost.keys():
    G.add_node('Point de vente'+site, node_type='Point de vente', place=site, cout_unitaire = dict_vente_cost[site]['totalCost'], subset=7, volume=dict_vente_cost[site]['Volume'])
    G.add_edge('Point de vente'+site, 'Usine_f'+dict_vente_cost[site]['Usine_f'], volume=dict_vente_cost[site]['Volume'])

    
## Création de la liste des labels et répartition des couleurs
labels = {n : G.nodes[n]['node_type']+'\n'+G.nodes[n]['place']+'\nVolume : '+str(G.nodes[n]['volume'])+f"\nCoût unitaire : {G.nodes[n]['cout_unitaire']:.2f}" for n in G.nodes}
colors = [dict_colors[G.nodes[n]['node_type']] for n in G.nodes]
sizes = []
for n in list(G):
    sizes.append(G.nodes[n]['volume'])


## Affichage
pos = nx.multipartite_layout(G)
nx.draw(G, with_labels=True, labels=labels, node_color = colors, pos=pos, node_size = sizes)
plt.show()