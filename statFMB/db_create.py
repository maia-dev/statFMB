from statFMB.views import db
from statFMB.models import *
import csv
from collections import defaultdict
from operator import itemgetter

#create the Database and db tables
def create_tables():
    db.create_all()
    insert_countries()
    insert_municipalities_and_alias()
    insert_gates()
    insert_vehicle_types()
    insert_roles()

    db.session.commit()
    return

#insert
def insert_roles():
    db.session.add(Role(name="Administrador",
                        description = "Acesso a todas a funcionalidades"))
    db.session.add(Role(name="Portageiro",
                        description = "Acesso unicamente para carregamento \
                        de ficheiros"))
    db.session.add(Role(name="Visualizador",
                        description = "Acesso à analise de dados"))

def insert_vehicle_types():
   db.session.add(Vehicle_type("Moto"))
   db.session.add(Vehicle_type("Ligeiro"))
   db.session.add(Vehicle_type("Ligeiro XL"))
   db.session.add(Vehicle_type("Caravana"))
   db.session.add(Vehicle_type("Autocarro"))


def insert_countries():
    country_list = []
    with open('statFMB/static/resources/country_list.csv','rt',
              encoding ="ISO-8859-1") as country_csv:
        reader = csv.reader(country_csv)
        for row in reader:
            country_list.append(row[0])

    country_list.sort()
    country_list.append("N/A")

    country_obj_list = []
    for country in country_list:
        country_obj = Country(country)
        country_obj_list.append(country_obj)

    db.session.add_all(country_obj_list)

    return


def insert_municipalities_and_alias():
    read_list = []
    #read table from file
    with open('statFMB/static/resources/municipality_list.csv', 'rt',
              encoding = "ISO-8859-1") as f:
        reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE)
        for row in reader:
            read_list.append(row)

    municipalities_dict = defaultdict(list)
    for entry in sorted(read_list, key=itemgetter(3)):
        municipality = entry[3]
        parish = entry[5]
        municipalities_dict[municipality].append(parish)
    municipalities_dict["N/A"].append("N/A")

    municipality_obj_list = []
    parish_obj_list = []
    for municipality, parish_list in municipalities_dict.items():
        municipality_obj = Municipality(municipality)
        municipality_obj_list.append(municipality_obj)
        for parish in parish_list:
            parish_obj = Municipality_alias(parish,municipality_obj)
            parish_obj_list.append(parish_obj)

    db.session.add_all(municipality_obj_list)
    db.session.add_all(parish_obj_list)

    return



def insert_gates():
   db.session.add(Gate("Ameias"))
   db.session.add(Gate("Serpa"))
   db.session.add(Gate("Rainha"))


def insert_country_alias():
    pass

