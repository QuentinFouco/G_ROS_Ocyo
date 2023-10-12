import pandas as pd

list_csv = [
    'nom.csv'
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
        data = pd.read_csv(list_csv)
    return (data)

print (list_csv)