import pandas as pd

list_csv = [
    'Previsions_vente.csv'
    ]

def read_data (list_csv : list) -> pd.DataFrame:
    """La fonction lit un tableau csv et renvoi les données dans un data frame

    Args:
        list_csv (list[str]): liste des noms de fichier

    Returns:
        pd.DataFrame: _description_
    """
    
    for csv in list_csv:
        data = pd.read_csv(csv)
    return (data)

def affretement () -> dict:
    """_summary_

    Returns:
        dict: Dictionnaire des couts d'affretement
            dict : ('<depart>' : dict ('<arrivée>' : int(<cout>)))
    """
    data = pd.read_csv('Affretement.csv')
    dict_affretement = {}
    for i, nom1 in enumerate(data.Sites):
        dict_longueurs = {}
        for j, nom2 in enumerate(data.Sites):
            # print(data[nom1][j])
            dict_longueurs[nom2] = data[nom1][j]
        dict_affretement[nom1] = dict_longueurs    
    return (dict_affretement)
data = read_data(list_csv)

# print (data.Sites)
# print (data.Chaises)
dict_affretement = affretement()
# print (dict_affretement)
# print (dict_affretement.keys())


def gen_dict_fourn (dict_affretement : dict) -> dict:
    """Génere le dictionnaire des fournisseurs à partir du tableau

    Args:
        dict_affretement (dict): Dictionnaire des couts d'affretement
            dict : ('<depart>' : dict ('<arrivée>' : int(<cout>)))
        
    Returns:
        dict: ('<produit>' : list['<ville>','<ville>'])
    """
    villes = dict_affretement.keys()
    df_fourn = pd.read_csv('Fournisseur.csv')
    dict_fournisseur = {}
    matieres = ['Tissus', 'Mousse', 'Plastique', 'Tube']
    for matiere in matieres:
        fourn = []
        for i, ville in enumerate(villes):
            if df_fourn[matiere][i]==1:
                fourn.append(ville)
        print(matiere, fourn)
        dict_fournisseur[matiere]=fourn
    return(dict_fournisseur)
        

    
gen_dict_fourn(dict_affretement)

def gen_camion_cap() -> dict:
    """Génere le dictionnaire des capacités des camions à partir du tableau

    Returns:
        dict ('<Produit>':int(capacité))
    """
    data = pd.read_csv('Camion.csv')
    dict_affretement = {}
    for i, Produit in enumerate(data.Produits):
        dict_affretement[Produit]= data.Unit_camion[i]
    return dict_affretement

dict_camion = gen_camion_cap()
# for prod in dict_camion.keys():
#     print (prod, dict_camion[prod])

def gen_previsions_vente() -> dict:
    """Génere le dictionnaire des capacités des camions à partir du tableau

    Returns:
        dict ('<Produit>':int(capacité))
    """
    data = pd.read_csv('Previsions_vente.csv')
    dict_previsions = {}
    for i, Site in enumerate(data.Sites):
        dict_previsions[Site]= data.Chaises[i]
    return dict_previsions

dict_previsions = gen_previsions_vente()
for prod in dict_previsions.keys():
    print (prod, dict_previsions[prod])
    
def gen_amortissement() -> dict:
    """Génere le dictionnaire des capacités des camions à partir du tableau

    Returns:
        dict ('<Produit>':int(capacité))
    """
    data = pd.read_csv('Cout_machine.csv')
    dict_amortissement = {}
    for i, Machine in enumerate(data.Machines):
        dict_amortissement[Machine]= data.Amortissement[i]
    return dict_amortissement