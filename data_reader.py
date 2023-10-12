import pandas as pd

list_csv = [
    'Previsions_vente.csv'
    ]

def read_data (list_csv : list[str]) -> pd.DataFrame:
    """
    La fonction lit un tableau csv et renvoi les données dans un data frame
    
    INPUT : 
        - nom_csv : string du nom du fichier
    
    OUTPUT :
        - data frame du fichier
    """
    for csv in list_csv:
        data = pd.read_csv(csv)
    return (data)

def affretement () -> dict[dict]:
    data = pd.read_csv('Affretement.csv')
    dict_affretement = {}
    for i, nom1 in enumerate(data.Sites):
        dict_longueurs = {}
        for j, nom2 in enumerate(data.Sites):
            print(data[nom1][j])
            dict_longueurs[nom2] = data[nom1][j]
        dict_affretement[nom1] = dict_longueurs    
    return (dict_affretement)
data = read_data(list_csv)

print (data.Sites)
print (data.Chaises)
dict_affretement = affretement()
print (dict_affretement)
print (dict_affretement.keys())