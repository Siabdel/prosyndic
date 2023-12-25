from cartcom import models as cc_models
from copro import models as pro_models
import pandas as pd
import json
from django_pandas.io import read_frame


## convert dict to Obj
class Dict2Obj(object):
    """
    Turns a dictionary into a class
    """
    #----------------------------------------------------------------------
    def __init__(self, dictionary):
        """Constructor"""
        for key in dictionary:
            setattr(self, key, dictionary[key])


## df = json.filter(items=['sku', 'name', 'price', 'description', 'image' ])

json = pd.read_json('./data_set/open-data-set/products.json')

# on prend 100 premieres elem
data_100  = df[:100]
# on converti data en dict 
data_dict = data_100.to_dict('index')

## insert en base 
for i,  elem in data_100.items() :
    cc_models.Product.objects.create(
    name=elem['name'], 
    description=elem['description'], 
    unit_price=elem['price'],
    quantity_instock=100)
    print(elem['name'])

##------------------
#-
##------------------

queryset = pro_models.LigneDeCandidature.objects.filter(status='OP')# Convert the QuerySet to a Pandas DataFrame
df = read_frame(queryset)

# pivote table
dpivot = df.pivot_table(values=['budget_securite', 'budget_jardinage',] ,  columns=['societe'])

"""_summary_
   societe           Energy Real Estate  HONA Protect  PacoClean  Salam Gestion  VALOR Syndic  ViaSyndic
budget_jardinage            541200.0      129600.0   388800.0       334728.0      436800.0   544320.0
budget_securite             703200.0      374400.0   506880.0       557208.0      624000.0   777600.0

"""



soc = [ (elem.societe, elem.telephone, elem.email) for elem in queryset]
with open("sundic_list", "w") as pf:
    for name, tel, email in soc:
        ligne = "|{} \t| {} |\t {} |".format(name, tel, email)
        pf.write(ligne + "\n")
