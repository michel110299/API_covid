from django.shortcuts import render
import requests
import json
from django.utils import timezone

def index(request):
    total_mortes = 0 
    lista_atualizada = []
    lista_estados = []

    req = requests.get('https://api.covid19api.com/countries')
    todos_paises = json.loads(req.text)

    req = requests.get('https://api.covid19api.com/live/country/Brazil')
    dicionario = json.loads(req.text)


    if request.POST:
        country = request.POST.get('select_pais', None)  
        if country:
            req = requests.get('https://api.covid19api.com/live/country/' + country)
            dicionario = json.loads(req.text)

            if not dicionario:
                req = requests.get('https://api.covid19api.com/live/country/brazil')
                dicionario = json.loads(req.text)
        else:
            req = requests.get('https://api.covid19api.com/live/country/brazil')
            dicionario = json.loads(req.text) 

    for x in dicionario:
        if lista_estados:
            valida = None
            for q in lista_estados:                
                if q['nome_estado'] == x['Province']:                                                      
                    q['dados'].append(x)
                    valida = 1
                             
            if not valida: 
                listAux = []
                listAux.append(x)
                obj = {
                    "nome_estado": x['Province'],
                    "dados":listAux,
                }
                lista_estados.append(obj)
        else:
            listAux = []
            listAux.append(x)
            obj = {
                "nome_estado": x['Province'],
                "dados":listAux,
            }
            lista_estados.append(obj)
    

    for x in lista_estados:        
        total_mortes += x['dados'][len(x['dados'])-1]['Deaths']
        obj = x['dados'][len(x['dados'])-1]
        lista_atualizada.append(obj)

    titulo = lista_atualizada[0]['Country']
    print(titulo)

    
    context = {
        "dicionario" : lista_atualizada,
        "total_mortes": total_mortes,
        "todos_paises": todos_paises,
        "titulo" : titulo,
    }

    return render(request,'index.html',context)
