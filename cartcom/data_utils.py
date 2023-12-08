from cartcom import models as cc_models
import pandas as pd
import json

df = json.filter(items=['sku', 'name', 'price', 'description', 'image' ])

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

