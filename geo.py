import requests

import pandas as pd


def get_pois(lat, lon, api_key, categories,radious):
    """ Retorna pontos de interesse próximos à localização fornecida. """
    pois_url = f"https://api.geoapify.com/v2/places?categories={categories}&filter=circle:{lon},{lat},{radious}&bias=proximity:{lon},{lat}&apiKey={api_key}"
    response = requests.get(pois_url)
    return response.json()

def verify(name,typ):
    while True:
        obj=input(name+">:")
        try:
            return typ(obj)
        except:
            print("INVALID")

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




f = open("categories.txt","r")
all_categories = [i.strip() for i in f]  # Exemplo com 50 categorias
f.close()

# Exemplo de uso
api_key = "21b87e0e53674c85a76c2a2d2a400632"


latitude =verify(" Sua Latitude",float)
longitude = verify("Sua Longitude",float)
radious=verify("Raio de procura em km",float)*1000
categorias = inCategorie(verify("Categorias",str),all_categories)



pois_proximos = get_pois(latitude, longitude, api_key, categorias,radious)


dic = {"name":[],"distance":[],"country":[],"district":[],"street":[],"lat":[],"lon":[],"entidade":[]}
for i in pois_proximos["features"]:
    i=i["properties"]
    name = i.get("name","NONAME")
    distance = float(i.get("distance",0))/1000
    country = i.get("country")
    distrito=i.get("district")
    codigo=i.get("postcode")
    rua=i.get("street")
    latEnt=i.get("lat")
    lonEnt=i.get("lon")


    entidade = i["datasource"]["raw"].get("shop",'')+i["datasource"]["raw"].get("amenity",0)+i["datasource"]["raw"].get("tourism","")

    dic["name"].append(name)
    dic["distance"].append(distance)
    dic["country"].append(country)
    dic["district"].append(distrito)
    dic["street"].append(rua)
    dic["lat"].append(latEnt)
    dic["lon"].append(lonEnt)
    dic["entidade"].append(entidade)
	

# Chaves que você deseja salvar
chaves_desejadas = list(dic.keys())
# Criando um DataFrame com apenas as chaves desejadas
organiza = inCategorie(verify("Escolha o metodo de organizar: "+str(chaves_desejadas),str),chaves_desejadas).split(",")


df = pd.DataFrame(dic)
df.sort_values(by=organiza)

print(df.to_string(index=False))
# Salvando o DataFrame em um arquivo Excel
df.to_excel(verify("Nome do arquivo",str)+".xlsx", index=False)
