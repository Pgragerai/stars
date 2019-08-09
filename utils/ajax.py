from django.http import HttpResponse

import json
import requests
import re


def get_character(request):
    total_results = [] 
    data = {}

    #Realizamos la peticion
    response = requests.get("https://swapi.co/api/people/")
    data = response.json()
    
    #Guardamos la primera pagina de resultados
    total_results = total_results + data['results']

    #Cargamos todas las paginas disponibles
    while data['next'] is not None:
        response = requests.get(data['next'])
        data = response.json()
        total_results = total_results + data['results']

    # Generamos una lista con los ids y el nombre
    list_ids = [re.sub("\D", "", i['url']) for i in total_results]
    list_name = [i['name'] for i in total_results]

    #Guardamos los datos obtenidos
    data['characters_ids'] = list_ids
    data['characters'] = list_name

    return HttpResponse(json.dumps(data), content_type="application/json")