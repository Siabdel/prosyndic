class Container:
    pass


def revert(obj):
    if isinstance(obj, Container):
        return revert_container(obj)
    elif isinstance(obj, dict):
        return revert_dict(obj)
    elif isinstance(obj, list):
        return revert_list(obj)
    elif isinstance(obj, tuple):
        return revert_tuple(obj)
    elif isinstance(obj, set):
        return revert_set(obj)
    else:
        return obj


def revert_container(obj_container: Container):
    return dict([key, revert(value)]
                for key, value in obj_container.__dict__.items())


def revert_dict(obj_dict: dict):
    return dict([key, revert(value)] for key, value in obj_dict.items())


def revert_list(obj_list: list):
    return list(revert(element) for element in obj_list)


def revert_tuple(obj_tuple: tuple):
    return tuple(revert(element) for element in obj_tuple)


def revert_set(obj_set: set):
    return set(revert(element) for element in obj_set)


def convert(obj):
    if isinstance(obj, dict):
        return convert_dict(obj)
    elif isinstance(obj, list):
        return convert_list(obj)
    elif isinstance(obj, tuple):
        return convert_tuple(obj)
    elif isinstance(obj, set):
        return convert_set(obj)
    else:
        return obj


def convert_dict(obj_dict: dict):
    converted = Container()

    for key, value in obj_dict.items():
        setattr(converted, key, convert(value))

    return converted


def convert_list(obj_list: list):
    return list(convert(element) for element in obj_list)


def convert_tuple(obj_tuple: tuple):
    return tuple(convert(element) for element in obj_tuple)


def convert_set(obj_set: set):
    return set(convert(element) for element in obj_set)
## 
class Dict2Obj(object):
    """
    Turns a dictionary into a class
    allow object-like access to dicts, it does so via getattr
    """
    def __init__(self, d):
        for k, v in d.items():
            if isinstance(k, (list, tuple)):
                setattr(self, k, [obj(x) if isinstance(x, dict) else x for x in v])
            else:
                setattr(self, k, obj(v) if isinstance(v, dict) else v)

        """
        Dict2obj: transform dict to simpler object. 
        # pip install dict2obj

        """
        
import collections as co
import pandas as pd

df = pd.read_excel('file.xlsx')
df = df.where(pd.notnull(df), None)
od = co.OrderedDict((k.strip().encode('utf8'),v.strip().encode('utf8')) 
                    for (k,v) in df.values)



## import data 
import pandas as pd
from copro import models as pro_models

def import_data(request):

    df = pd.read_excel("tmp/Candidats Syndic-2023.xls", )
    df.head(3)

    """
    societe                 contact  ...                  Comment ajouter
    0  Energy Real Estate          Mr Nabil Rafki  ...  - 20 ans d'experience dans la gestion immobili...     YES
    1        Salam Gestion            Mr Mohammed  ...  - Base a Marrakech, gere plusieurs immeubles e...     YES
    2              Gestsyn  Mme Chaimaa Bouaanani  ...  - Equipe jeune et dynamique\n- Dans le domaine...     YES
    3            ViaSyndic      Mr Yassine Alaoui  ...  - Base a Marrakech, dans le domaine depuis 200...     YES
    4            PacoClean  Mr Youness El Gazouir  ...  - Base a Marrakech, gere uniquement une reside...   50/50

    [5 rows x 7 columns]

    ##
    f.name for f in pro_models.LigneDeCandidature._meta.get_fields()
    ['pjointe', 'id', 'title', 'created_at', 'etude', 'societe', 'status', 'notation', 
     'adresse', 'site_web', 'contacte', 'role', 'reference', 'telephone', 'recommande_par',
     'visite', 'candidat', 'offre', 'remuneration', 'budget_global', 'author', 'description', 'comment']
    ## columns = ['societe', 'contact', 'rôle', 'tel', 'recommende', 'Comment',
       'ajouter']

    """ 
    ett = pro_models.Etude.objects.all().first()
    auteur = acc_models.CustomUser.objects.get(pk=1)

    
    for elem in df.values :
        # print(elem)
        for elem in df.values :
            print(elem)
            pro_models.LigneDeCandidature(
            etude=et,
            author=auteur,
            societe=elem[0],
            contacte=elem[1],
            role=elem[2],
            telephone=elem[3],
            recommande_par=elem[4],
            description=elem[5],
            candidat=False,
            ).save()


    list_total  = [ f.name for f in pro_models.Ticket._meta.get_fields()]
    