import requests
import pandas as pd

# Minha api
api_key = "21b87e0e53674c85a76c2a2d2a400632"

def get_moreDetails(nome,key):
    response = requests.get(f"https://api.geoapify.com/v1/geocode/search?text={nome}&format=json&apiKey={key}")
    return response.json()


def get_moeda(nome):
    return ".."

#Conseguir as localizações dos pontos perto de você
def get_locations(lat, lon, api_key, categories,radious,limit):
    pois_url = f"https://api.geoapify.com/v2/places?categories={categories}&filter=circle:{lon},{lat},{radious}&bias=proximity:{lon},{lat}&limit={limit}&apiKey={api_key}"
    response = requests.get(pois_url)
    return response.json()

#Verificar se oque você digitou "s" está dentro de uma lista "al"
def inCategorie(s,al):
    s=s.split(",")
    for k,i in enumerate(s):
        while True:
            if i in al:
                s[k]=i
                break
            else:
                print("INVALID")
            i=verify("Reescreva a categoria",str)

    return ",".join(s)


#Retirar as infomações importantes recolhidas
def organize(dic,locations):
    for i in locations["features"]:
        i=i["properties"]
        name = i.get("name","NONAME")
        if name =="NONAME":
            continue
        distance = float(i.get("distance",0))/1000
        country = i.get("country")
        city=i.get("city")
        codigo=i.get("postcode")
        rua=i.get("street")
        latEnt=i.get("lat")
        lonEnt=i.get("lon")
        entidade = i["datasource"]["raw"].get("shop",'')+i["datasource"]["raw"].get("amenity","")+i["datasource"]["raw"].get("tourism","")

        dic["name"].append(name)
        dic["distance"].append(distance)
        dic["country"].append(country)
        dic["city"].append(city)
        dic["street"].append(rua)
        dic["GMT"].append(get_moreDetails(country,api_key)['results'][0].get("timezone").get("offset_STD"))
        dic["lat"].append(latEnt)
        dic["lon"].append(lonEnt)
        dic["Currency"].append(get_moeda(country))
        dic["entidade"].append(entidade)
    

def push(latitude,longitude,categorias,radious,limit,dic):
    latitude=float(latitude)
    longitude=float(longitude)
    radious=float(radious)*1000
    limit=float(limit)
    categorias="".join(categorias)
    
    #Chamar as funções para receber o dicionario com as localizações
    locations = get_locations(latitude, longitude, api_key, categorias,radious,limit)
    
    print()
    #dic é o dicionario aonde seram guardadas as coisas importantes
    organize(dic,locations)


    #Organizar nossas tabela de acordo com os nomes dos titulos
    #chaves_desejadas = list(dic.keys())
    #organiza = inCategorie(verify("Escolha o metodo de organizar: "+str(chaves_desejadas),str),chaves_desejadas).split(",")

    #df.sort_values(by=organiza)

    #printar a tabela
    #print(df.to_string(index=False))


    # Salvando o DataFrame em um arquivo Excel
    #df.to_excel(verify("Nome do arquivo",str)+".xlsx", index=False)
