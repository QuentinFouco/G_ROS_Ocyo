import pandas as pd

nom_csv = 'nom.csv'

def read_data (nom_csv : str) -> pd.DataFrame:
    """
    La fonction lit un tableau csv et renvoi les données dans un data frame
    
    INPUT : 
        - nom_csv : string du nom du fichier
    
    OUTPUT :
        - data frame du fichier
    """
    data = pd.read_csv(nom_csv)
    return (data)

print (nom_csv)