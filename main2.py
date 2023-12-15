import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd
import requests


#Pegar as categorias
f = open("categories.txt","r")
all_categories = [i.strip() for i in f]
f.close()



#Pegar as moedas
f = open("moedas.txt","r")
teste = eval(f.read())
all_moedas = {i.lower():teste[i] for i in teste}
teste=0
f.close()


#Adicionar categoria a lista
def AddToList(nome):
    items = [lista_box.get(i) for i in range(lista_box.size())]
    if nome in all_categories and nome not in items:
        lista_box.insert(tk.END, nome)

#Remover categoria da lista
def RemToList(event):
    selecionado = lista_box.curselection()
    if selecionado:
        item = lista_box.get(selecionado)
        lista_box.delete(selecionado)

#Atualizar sujestão de categoria
def att_sugest(event):
    valor_digitado = menu_botao.get()
    sugestoes = [botao for botao in all_categories if valor_digitado.lower() in botao.lower()]
    menu_botao['values'] = sugestoes

#Validar se o elemento é um float
def validar_float(entrada):
    try:
        float(entrada)
        return True
    except ValueError:
        return False


#Ordernar a tabela
def SortedColumm(tree, col, reverse):
    # Obtém uma lista dos itens no Treeview
    l = [(tree.set(k, col), k) for k in tree.get_children('')]
    
    # Ordena a lista de forma crescente ou decrescente
    l.sort(reverse=reverse)

    # Reordena os itens no Treeview
    for index, (val, k) in enumerate(l):
        tree.move(k, '', index)

    # Alterna entre ordenação crescente e decrescente
    tree.heading(col, command=lambda: SortedColumm(tree, col, not reverse))


def get_moeda(nome):
    nome=nome.lower()
    return all_moedas.get(nome,"not find")

# Função para buscar as localizações
def get_locations(lat, lon, api_key, categories, radius,limit):
    pois_url = f"https://api.geoapify.com/v2/places?categories={categories}&filter=circle:{lon},{lat},{radius}&bias=proximity:{lon},{lat}&limit={limit}&apiKey={api_key}"
    response = requests.get(pois_url)
    return response.json()


def get_moreDetails(nome,key):
    response = requests.get(f"https://api.geoapify.com/v1/geocode/search?text={nome}&format=json&apiKey={key}")
    return response.json()


# Função para salvar os dados como CSV
def salvar_como_csv():
    data = [tree.item(item)['values'] for item in tree.get_children()]
    df = pd.DataFrame(data, columns=columns)
    df.sort_values(by="distance")
    filepath = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if filepath:
        df.to_csv(filepath, index=False, encoding='utf-8-sig')


# Função chamada quando o botão 'Buscar' é pressionado
def buscar_locations():
    lat_str = lat_entry.get()
    lon_str = lon_entry.get()
    radius_str = radius_entry.get()
    limit_str=Limit.get()

    #Validar se os elementos digitados são float
    if not (validar_float(lat_str) and validar_float(lon_str) and validar_float(radius_str) and validar_float(limit_str)):
        messagebox.showerror("Erro de entrada", "Por favor, insira números válidos para latitude, longitude, limite e raio.")
        return

    
    #Setar os valores
    lat = float(lat_str)
    lon = float(lon_str)
    limit = limit_str
    radius = float(radius_str) * 1000
    categories = ','.join([lista_box.get(i) for i in range(lista_box.size())])

    if categories=="":
        messagebox.showerror("Erro de entrada", "Por favor, insira as categorias.")
        return

    #Definir o mouse como icone de loading
    root.config(cursor="watch")
    root.update()

    locations = get_locations(lat, lon, api_key, categories, radius,limit)
    if locations["features"]==[]:
        messagebox.showerror("Não foi encontrado nada no raio dado.")
        return
    # Processando os dados recebidos
    data = []
    #Pegar as informações importantes
    for feature in locations['features']:
        properties = feature['properties']
        name = properties.get('name', 'NONAME')
        country=properties.get('country', '')
        city = properties.get('city', '')
        if name =="NONAME":
            continue
        data.append([
            name,
            float(properties.get('distance', 0)) / 1000,
            country,
            city,
            properties.get('street', ''),
            properties["datasource"]["raw"].get("shop","")+properties["datasource"]["raw"].get("amenity","")+properties["datasource"]["raw"].get("tourism",""),
            get_moreDetails(city,api_key)['results'][0].get("timezone").get("offset_STD"),
            get_moeda(country),
            properties.get('lat', ''),
            properties.get('lon', ''),
        ])
    # Atualizando o Treeview
    for i in tree.get_children():
        tree.delete(i)
    for row in data:
        tree.insert('', 'end', values=row)
    root.config(cursor="")
    root.update()

# Configuração da janela principal
root = tk.Tk()
root.title("JTurism")
root.geometry("800x600")  # Define um tamanho inicial
#root.attributes('-zoomed', True) não funciona no windows

# Minha api
api_key = "21b87e0e53674c85a76c2a2d2a400632"

# Campos de entrada
entry_frame = tk.Frame(root)
entry_frame.pack(fill='x', padx=10, pady=10)

tk.Label(entry_frame, text="Latitude:").pack(side='left')
lat_entry = tk.Entry(entry_frame)
lat_entry.pack(side='left', padx=(0, 10))

tk.Label(entry_frame, text="Longitude:").pack(side='left')
lon_entry = tk.Entry(entry_frame)
lon_entry.pack(side='left', padx=(0, 10))

tk.Label(entry_frame, text="Raio (km):").pack(side='left')
radius_entry = tk.Entry(entry_frame)
radius_entry.pack(side='left', padx=(0, 10))

tk.Label(entry_frame, text="Limite de pesquisas:").pack(side='left')
Limit = tk.Entry(entry_frame)
Limit.pack(side='left', padx=(0, 10))

# Menu de cascata para botões
menu_botao = ttk.Combobox(entry_frame, values=all_categories, width=47)
menu_botao.pack(side='left', padx=(0, 10))
menu_botao.bind('<KeyRelease>', att_sugest)

# Botão para adicionar à lista
botao_adicionar = tk.Button(entry_frame, text="Adicionar à Lista", command=lambda: AddToList(menu_botao.get()))
botao_adicionar.pack(side='left', padx=(0, 10))

# Lista na tela para mostrar os cliques
lista_box = tk.Listbox(entry_frame, width=100)
lista_box.pack(side="right",padx=(0,10))
lista_box.bind('<Double-1>', RemToList)


# Tabela de resultados (Treeview)
tree_frame = tk.Frame(root)
tree_frame.pack(fill='both', expand=True, padx=10, pady=10)

columns = ("name", "distance", "country", "city", "street", "entity","GMT","Currency","lat", "lon")
tree = ttk.Treeview(tree_frame, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col, command=lambda _col=col: SortedColumm(tree, _col, False))
tree.pack(fill='both', expand=True)

# Botão de busca
search_button = tk.Button(root, text="Buscar", command=buscar_locations)
search_button.pack(side="left",pady=(0, 10))

# Botão para salvar como CSV
save_button = tk.Button(root, text="Salvar como CSV", command=salvar_como_csv)
save_button.pack(side="left",pady=(0, 10))



root.mainloop()
