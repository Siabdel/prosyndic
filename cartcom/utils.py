# -*- coding: utf-8 -*-
import re, time
from datetime import datetime, timedelta, date
import io
import matplotlib.pyplot as plt
import numpy as np
from ofschedule.models import Blob



def bissextile(a):
    """Dit si l'année donnée est bissextile ou non"""
    return (a%4==0 and a%100!=0) or a%400==0



def nbjoursan(a):
    """Donne le nombre de jours de l'année"""
    if (a%4==0 and a%100!=0) or a%400==0: # bissextile?
        return 366
    else:
        return 365


def nbjoursmois(m,a):
    """Donne le nombre de jours du mois m de l'année a"""
    nj = (0,31,28,31,30,31,30,31,31,30,31,30,31)[m]
    if m==2 and ((a%4==0 and a%100!=0) or a%400==0): # m=février et a=bissextile?
        return nj + 1
    return nj


def dt2DT(dt):
     "Converts Python datetime to Zope DateTime"
     try:
         # convert dt to local timezone
         ltz = dt.astimezone(LocalTimezone())
         return DateTime(*ltz.timetuple()[:6])
     except:
         return DateTime(dt.year, dt.month, dt.day, 0, 0, 0)


def DT2dt(DT):
     """
     Converts Zope DateTime to Python datetime, Zope DateTime is allways utc
     """
     return datetime.fromtimestamp(DT.timeTime(), LocalTimezone())



def datetimeIterator(from_date=None, to_date=None, delta=timedelta(days=1)):
    from_date = from_date or datetime.now()
    while to_date is None or from_date <= to_date:
        yield from_date
        from_date = from_date + delta
    return

def get_dates_semaine( sem, annee=datetime(2018, 1, 1).year):
    """
    in : sem numero de semaine en int
    return ; tableau des jours semaines en datetime
    """
    nb = 0
    jours_semaine  = []

    date_ref = date(annee, 1, 1) # Le 4 janvier est toujours en semaine 1

    for courant in datetimeIterator(datetime(annee, 1, 1), datetime(annee, 12, 31)):
        #courant += timedelta(days=1)) :
        sem_courante = courant.isocalendar()[1]

        if sem_courante == sem :
            nb += 1
            jours_semaine.append(courant)

    return jours_semaine


def  get_numero_semaine(date_in):

    """

    in : date_in  format datetime

    return ; numero de la semaine

    """

    #return date_in.isocalendar()[1]
    return datetime.isocalendar(date_in)[1]



def  get_num_semaine_from_date(annee, mois, jour):

    """
    annee : year
    mois : month
    jour : day
    return : numero de la semaine
    """

    date_in = datetime(int(annee), int(mois), int(jour))
    return datetime.isocalendar(date_in)[1]


def get_delta_week(annee, semaine,  v_week=1):
    """
    annee : year
    mois : month
    jour : day
    week : semaine
    return : (annee,  semaine, jour)
    """
    date_in = get_dates_semaine(semaine,  annee  )
    semaine_precedante = date_in[0] + timedelta(weeks = v_week)
    semaine_precedante = semaine_precedante.isocalendar()
    return semaine_precedante

def get_timedelta(*args):
    """
    week : semaine
    return :
    """
    for v_days, v_weeks in args :
        if v_days :
            return timedelta(days=v_days)
        if v_weeks :
            return timedelta(weeks=v_weeks)



def lire_doc():
    return eval(symbole + ".__doc__")


def verif_date():
   pass


def test_date(chaine):
    pattern_fr = re.compile("\d{2}/\d{2}/\d{4}")
    pattern_en = re.compile("\d{4}[/-]\d{2}[/-]\d{2}")


    if pattern_fr.match(chaine):
                an=int(chaine[6:])
                mois=int(chaine[3:5])
                jour=int(chaine[:2])

    elif pattern_en.match(chaine):
                an=int(chaine[:4])
                mois=int(chaine[5:7])
                jour=int(chaine[8:])

    else:
        return False


    if an>2200:
        return False

    try:
        datetime.date(an, mois, jour)
        return True

    except:
        return False



def valider_heure(heure):
    try:
        heure == time.strptime(heure, "%H:%M:%S")
        valid = True
    except ValueError:
        try :
            heure == time.strptime(heure, "%H:%M")
            valid = True
        except ValueError:
            valid = False
    return valid



class Article :
    def __init__(self, titre, prix):
        self.titre = titre
        self.prix = prix

    def show_article(self):
        return "Article %s" % self.titre

    def modifier_prix(self, new_prix):
        self.prix = new_prix


def charger_base():
    tab_article = []
    for elem in ['Chemise', 'Pantalon', 'Chaussure']:
        a1 = Article(elem, 35 + 10)
        print a1.show_article()
        tab_article.append(elem)


    return tab_article


def is_exist_semaine53(v_annee):
    date_in = datetime(int(v_annee), 12, 30)
    return datetime.isocalendar(date_in)[1]



def week_start_date(year, week):
    d = date(year, 1, 1)
    delta_days = d.isoweekday() - 1
    delta_weeks = week
    if year == d.isocalendar()[0]:
        delta_weeks -= 1
    delta = timedelta(days=-delta_days, weeks=delta_weeks)
    return d + deltas


def test_get_all_permissions_mixed_user_and_group(self):
        permissions = Permission.objects.filter(content_type__app_label='auth',
                                                codename__in=[
                                                    'add_user', 'change_user',
                                                    'add_group', 'change_group'
                                                ])
        user = User.objects.create_user(username='testuser', password='test123.')
        group = Group.objects.create(name='group')
        group.user_set.add(user)

        user.user_permissions.add(*permissions.filter(content_type__model='user'))
        group.permissions.add(*permissions.filter(content_type__model='group'))

        backend = ChemoPermissionsBackend()

        self.assertEqual(
            set(permissions.filter(content_type__model='group').values_list('codename', flat=True)),
            set(backend.get_all_permissions(user, group))
        )
        self.assertEqual(
            set(permissions.filter(content_type__model='user').values_list('codename', flat=True)),
            set(backend.get_all_permissions(user, user))
        )


def test_user_has_perm_multiple_relation_types(self):
        # Set up a bookstore graph
        store = StoreFixture(Store).create_one()
        get_nodeset_for_queryset(Store.objects.filter(pk=store.pk), sync=True)
        permissions = Permission.objects.filter(codename__in=['add_store', 'change_store', 'delete_store'])

        user = get_user_model().objects.latest('pk')
        user.user_permissions.add(*list(permissions))

        # Create an access rule which allows 'add_store' and 'change_store',
        # but not 'delete_store'
        access_rule = AccessRule.objects.create(
            ctype_source=ContentType.objects.get_for_model(user),
            ctype_target=ContentType.objects.get_for_model(Store),
            relation_types=[{'AUTHOR': None}, {'BOOK': None}, {'STORE': None}]
        )
        access_rule.permissions.add(*list(permissions.exclude(codename='delete_store')))

        self.assertTrue(user.has_perm('testapp.add_store', store))
        self.assertTrue(user.has_perm('testapp.change_store', store))
        self.assertFalse(user.has_perm('testapp.delete_store', store))



#To generate and save the image:

# Any old code to generate a plot - NOTE THIS MATPLOTLIB CODE IS NOT THREADSAFE, see http://stackoverflow.com/questions/31719138/matplotlib-cant-render-multiple-contour-plots-on-django
def plotImage(request):
    gui_val_in = 480
    t = np.arange(0.0, gui_val_in, gui_val_in/200)
    s = np.sin(2*np.pi*t)
    plt.figure(figsize=(7, 6), dpi=300, facecolor='w')
    plt.plot(t, s)
    plt.xlabel('time (n)')
    plt.ylabel('temp (c)')
    plt.title('A sample matplotlib graph')
    plt.grid(True)

    # Save it into a BytesIO type then use BytesIO.getvalue()
    f = io.BytesIO()  # StringIO if Python <3
    plt.savefig(f)
    b = Blob(blob=f.getvalue())
    b.save()
    # To display it, I create the following in myapp/views.py:

def image(request, blob_id):
    b = Blob.objects.get(id=blob_id)
    response = HttpResponse(b.blob)
    response['Content-Type'] = "image/png"
    response['Cache-Control'] = "max-age=0"
    return response

"""
Add to myapp/urls.py:

url(r'^image/(?P<blob_id>\d+)/$', views.image, name='image'),
And in the template:

<img src="{% url 'myapp:image' item.blob_id %}" alt="{{ item.name }}" />
"""



def mplimage(request):

    # 1-
    ofs = DjangoOf.objects.filter(semaine='38', annee='18' )

    df = read_frame(ofs, fieldnames = ['machine_travail', 'quantite_commandee'])
    df.plot(kind="bar", stacked=True)

    # 2 --
    plt.title('Plan de charge machine semaine 37')
    plt.xlim(0, 10)
    plt.ylim(0, 8)
    plt.xlabel('x label')
    plt.ylabel('y label')
    bar1 = plt.bar(x, h,
                   width = 1.0,
                   bottom = 0,
                   color = 'Green',
                   alpha = 0.65,
                   label = 'Legend')
    plt.legend()

    # 3 --
    fig = matplotlib.figure.Figure()
    buf = io.BytesIO()
    canvas = FigureCanvasAgg(fig)
    canvas.print_png(buf)
    plt.savefig(fig)

    response=HttpResponse(buf.getvalue(),content_type='image/png')
    # if required clear the figure for reuse
    fig.clear()
    # I recommend to add Content-Length for Django
    response['Content-Length'] = str(len(response.content))
    #
    return response



def GraphsViewBar(request):
    f = plt.figure()
    x = np.arange(10)
    h = [0,1,2,3,5,6,4,2,1,0]
    plt.title('Title')
    plt.xlim(0, 10)
    plt.ylim(0, 8)
    plt.xlabel('x label')
    plt.ylabel('y label')
    bar1 = plt.bar(x,h,width=1.0,bottom=0,color='Green',alpha=0.65,label='Legend')
    plt.legend()

    canvas = FigureCanvasAgg(f)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    matplotlib.pyplot.close(f)
    return response



def plot_of_test(request):



    # ex donne en 4 :   df2 = pd.DataFrame(np.random.rand(10, 4), columns=['a', 'b', 'c', 'd'])
    # df2.plot.bar()

    # 1-
    fig = matplotlib.figure.Figure()
    canvas = FigureCanvasAgg(fig)

    # 2- canvas
    #buf = io.BytesIO()
    #canvas.print_png(buf)

    ofs = DjangoOf.objects.filter(semaine='38', annee='18' )

    # df = pd.DataFrame(ofs, columns = ['code_of', 'quantite_commandee'] )
    df = read_frame(ofs, fieldnames = ['machine_travail', 'quantite_commandee'])
    #df.plot(ax=ax)
    df.plot(kind="bar", stacked=True)
    #plt.show()


    base_dir_media = PROJECT_PATH + '/media/'
    """

    with open(os.path.join(base_dir_media, "testPlot.png"), "wb") as fd_image :
        fd_image.write(buf.getvalue())
        #

        with open(os.path.join(base_dir_media, "testPlot.png"), "rb") as fd :
            response = HttpResponse(fd, content_type = 'image/png')
            #pylab.savefig(response, format="png")
    """

    output = StringIO.StringIO()
    fig.savefig(output, format="png")
    contents = output.getvalue()

    #
    plt.close(fig)
    response = HttpResponse(contents, content_type = 'image/png')
    #canvas.print_png(response)

    # 3 print
    #df.plot(kind="bar", stacked=True)
    #canvas.print_png(response)
    # plot  df.plot(kind='bar')
    # df.plot.hist(alpha=0.5)

    # hitogramme des ofs
    #plt.axhline(0, color='k')
    #plt.show()
    return response

def my_view(request):
    # sql ORM
    lignes_pdc = models.DjangoPDC.objects.all()
    #cc = models.DjangoMachine.objects.all()
    #output = _("Welcome to my site. date liv = %s date_debut %s" % (ofs.first().date_livraison_prevue, ofs.first().date_debut_reelle ))
    output = _("Welcome to my site. date liv = %s date_debut %s" %
               (lignes_pdc.first()))
    return HttpResponse("mesg = %s calendrier slug = %s count of = %s" % (output, lignes_pdc.first().code_of, lignes_pdc.count()))


def my_view(request):
    # sql ORM
    ofs = models.DjangoOf.objects.all()
    form = CalendarForm
    # je  cree mon calendrier
    #calendar = Calendar(name = 'ofCalendar')
    #calendar.save()
    #cc = models.DjangoMachine.objects.all()
    #output = _("Welcome to my site. date liv = %s date_debut %s" % (ofs.first().date_livraison_prevue, ofs.first().date_debut_reelle ))
    output = _("Welcome to my site. date liv = %s date_debut %s" %
               (cc.first()))
    return HttpResponse("mesg = %s calendrier slug = %s count of = %s" % (output, cc.first().slug, ofs.count()))


def api_test(request):
    queryset = models.DjangoOf.objects.filter(semaine=38, annee=18)
    response = HttpResponse(content_type="application/json")
    serializers.serialize("json", queryset, stream=response)
    return response



def export_as_json(request, ct, ids):
    queryset = models.DjangoOf.objects.filter(id__in=ids.split(","))
    response = HttpResponse(content_type="application/json")
    serializers.serialize("json", queryset, stream=response)
    return response

from django.utils.encoding import smart_str

def export_as_cvs(request, ct, ids):
    queryset = models.DjangoOf.objects.filter(id__in=ids.split(","))
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=mymodel.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
    # response['Content-Disposition'] = 'attachment; filename="%s"'% os.path.join('export', 'export_of.csv')
    writer = csv.writer(response)
    for obj in queryset:
        writer.writerow([
            smart_str(obj.pk),
            smart_str(obj.code_of),
            smart_str(obj.client),
        ])
    return response
