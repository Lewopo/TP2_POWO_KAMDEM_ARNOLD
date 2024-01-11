from flask import Flask, render_template,url_for
import pandas as pd
from matplotlib import pyplot as plt
import base64
from io import BytesIO
import numpy as np


app = Flask(__name__)

import mysql.connector

# Définissez les informations de connexion à la base de données
db_user = "ossute5_master2"
db_password = "ISJ_datascience+2023"
db_host = "192.145.239.38"
db_database = "ossute5_pointsinterest"

# Connectez-vous à la base de données
cnx = mysql.connector.connect(
    user=db_user,
    password=db_password,
    host=db_host,
    database=db_database,
)
req1="select avg(p.amount) pr_moyen, ca.name category, t.name ville  from ossute5_pointsinterest.prices p inner join ossute5_pointsinterest.point_interests c on c.id = p.pointinteret_id inner join  ossute5_pointsinterest.categories ca on ca.id = c.category_id inner join ossute5_pointsinterest.quartiers q on q.id = c.quartier_id inner join ossute5_pointsinterest.towns t on t.id = q.town_id where  c.langue = 'fr'  and  p.langue = 'fr' and  ca.langue = 'fr' and  t.langue = 'fr' and  q.langue = 'fr' and lower(ca.name) in ('hôtel', 'restaurant') and lower(t.name) in ('yaoundé', 'douala','garoua','bafoussam') group by ca.name,t.name"
req2="select count(*) as nb ,t.name ville from point_interests c inner join categories ca on ca.id = c.category_id inner join quartiers q on q.id = c.quartier_id inner join towns t on t.id = q.town_id where c.etoile  >= 3  and c.etoile  >= 3  and c.langue  ='fr'  and ca.langue  ='fr'  and t.langue  ='fr'  and q.langue  ='fr'  and lower(ca.name)  in ('hôtel')  and lower(t.name)  in ('yaoundé', 'douala','garoua','bafoussam')  group by t.name"
req3="select count(*) nom_interet,t.name ville from point_interests c inner join categories ca on ca.id = c.category_id inner join quartiers q on q.id = c.quartier_id inner join towns t on t.id = q.town_id where c.is_verify  = 1  and c.is_verify  = 1  and c.langue  ='fr'  and ca.langue  ='fr'  and t.langue  ='fr'  and q.langue  ='fr'  and lower(t.name)   in ('yaoundé', 'douala','garoua','bafoussam')  group by t.name"
req4="select count(*) number,t.name ville from point_interests c inner join categories ca on ca.id = c.category_id inner join quartiers q on q.id = c.quartier_id inner join towns t on t.id = q.town_id where c.langue  ='fr'  and c.langue  ='fr'  and ca.langue  ='fr'  and t.langue  ='fr'  and q.langue  ='fr'  and lower(ca.name)  like '%banque%'  and lower(t.name)   in ('yaoundé', 'douala','garoua','bafoussam')  group by t.name,ca.name"
req5="select count(*) nombre,t.name ville,q.name quartier from prices p inner join point_interests c on c.id = p.pointinteret_id inner join categories ca  on ca.id = c.category_id inner join quartiers q on q.id = c.quartier_id inner join towns t on t.id = q.town_id where c.etoile  >=3  and p.amount  >= 20000 and c.langue ='fr'  and p.langue ='fr'  and ca.langue  ='fr'  and t.langue  ='fr'  and q.langue  ='fr'  and lower(ca.name)  in ('hôtel')  and lower(t.name) in ('yaoundé', 'douala','garoua','bafoussam')  group by t.name,q.name"
req6="select count(*) nombre,t.name ville,q.name quartier from point_interests c inner join categories ca on ca.id = c.category_id inner join quartiers q on q.id = c.quartier_id inner join towns t on t.id = q.town_id where c.langue ='fr'  and c.langue ='fr'  and ca.langue  ='fr'  and t.langue  ='fr'  and q.langue  ='fr'  and lower(ca.name)  in ('coins chauds')  and lower(t.name)  in ('yaoundé', 'douala','garoua','bafoussam')  group by t.name,q.name"

def get_results(powo):
    # Connexion à la base de données et execution requete
    cursor = cnx.cursor(cursor_class=mysql.connector.cursor.MySQLCursorDict)
    cursor.execute(powo)
    # Stockez les résultats de la requête dans une liste
    results = cursor.fetchall()
    df=pd.DataFrame(results)
    # Fermeture de la connexion
    #cnx.close()
    return df


# Exécutez une requête SQL pour récupérer les données
# nom_Ville=['Bafoussam','Yaounde','Douala','Maroua']
# Prix_moy_res=[]

def powo(x,y):
    
    fig = plt.figure(figsize=(6, 6))
    p = plt.bar(x=x, height=y) 
    plt.ylabel(y, size=10)
    plt.xlabel(x, size=10)
   
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # return
    return base64.b64encode(buf.getbuffer()).decode("utf-8")


@app.route("/")
def index():
    return render_template("index.html")
@app.route("/question1")
def hello():
    kl=get_results(req1)
    
    bh=kl["pr_moyen"][0]
    dh=kl['pr_moyen'][1]
    yh=kl['pr_moyen'][2]
    br=kl["pr_moyen"][3]
    dr=kl['pr_moyen'][4]
    yr=kl['pr_moyen'][5]
    gh=0
    gr=0
    X=['Yaounde','Bafoussam','Garoua','Douala']
    Y_hot=[yh,bh,gh,dh]
    Y_RESt=[yr,br,gr,dr]
    g=powo(X,Y_hot)
    h=powo(X,Y_RESt)
    return render_template("table.html",yh=yh,bh=bh,dh=dh,br=br,dr=dr,yr=yr,g=g,h=h)

@app.route("/question2")
def table1():
    kl=get_results(req2)
    
    bh=kl["nb"][0]
    dh=kl['nb'][1]
    gh=kl['nb'][2]
    yh=kl['nb'][3]
    
    X=['Yaounde','Bafoussam','Garoua','Douala']
    Y_hot=[yh,bh,gh,dh]
    
    g=powo(X,Y_hot)
    
    return render_template("table2.html",yh=yh,bh=bh,dh=dh,gh=gh,g=g)

@app.route("/question3")
def table3():
    kl=get_results(req3)
    
    bh=kl["nom_interet"][0]
    dh=kl['nom_interet'][1]
    gh=kl['nom_interet'][2]
    yh=kl['nom_interet'][3]
    
    X=['Yaounde','Bafoussam','Garoua','Douala']
    Y_int=[yh,bh,gh,dh]
    
    g=powo(X,Y_int)
    
    return render_template("table3.html",yh=yh,bh=bh,dh=dh,gh=gh,g=g)


@app.route("/question4")
def table4():
    kl=get_results(req4)
    
    bh=kl["number"][0]
    dh=kl['number'][1]
    gh=kl['number'][2]
    yh=kl['number'][3]
    
    X=['Yaounde','Bafoussam','Garoua','Douala']
    Y_int=[yh,bh,gh,dh]
    
    g=powo(X,Y_int)
    
    return render_template("table4.html",yh=yh,bh=bh,dh=dh,gh=gh,g=g)


@app.route("/question5")
def table5():
    kl=get_results(req5)
    
    # bh=kl["number"][0]
    # dh=kl['number'][1]
    # gh=kl['number'][2]
    # yh=kl['number'][3]
    
    # X=['Yaounde','Bafoussam','Garoua','Douala']
    # Y_int=[yh,bh,gh,dh]
    
    # g=powo(X,Y_int)
    
    return render_template("table5.html",kl=kl)


@app.route('/question6')
def table6():

    villes = ["Yaoundé", "Douala", "Garoua", "Bafoussam"]
    cursor = cnx.cursor(cursor_class=mysql.connector.cursor.MySQLCursorDict)

    distractions = {}

    for ville in villes:
        cursor.execute("""
                SELECT t.name AS town_name, q.name AS quartier_name, COUNT(pi.id) AS distraction_count
                FROM towns AS t
                JOIN quartiers AS q ON t.id = q.town_id
                LEFT JOIN point_interests AS pi ON pi.quartier_id = q.id
                LEFT JOIN categories AS c ON pi.category_id = c.id
                WHERE t.name = %s
                AND c.name = 'Coins chauds'
                GROUP BY t.name, q.name
                ORDER BY distraction_count DESC
                LIMIT 5;
                """
                    , (ville,))

        towns = cursor.fetchall()

        distractions[ville] = towns

    print(distractions)

    return render_template("table6.html", distractions=distractions)
