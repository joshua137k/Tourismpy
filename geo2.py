import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd
import requests

f = open("categories.txt","r")
all_categories = [i.strip() for i in f]  # Exemplo com 50 categorias
f.close()
def adicionar_a_lista(nome):
    items = [lista_box.get(i) for i in range(lista_box.size())]
    if nome in all_categories and nome not in items:
        lista_box.insert(tk.END, nome)


def remover_da_lista(event):
    selecionado = lista_box.curselection()
    if selecionado:
        item = lista_box.get(selecionado)
        lista_box.delete(selecionado)

def atualizar_sugestoes(event):
    valor_digitado = menu_botao.get()
    if valor_digitado == '':
        sugestoes = botoes
    else:
        sugestoes = [botao for botao in botoes if valor_digitado.lower() in botao.lower()]
    menu_botao['values'] = sugestoes

def validar_float(entrada):
    try:
        float(entrada)
        return True
    except ValueError:
        return False

def ordenar_por_coluna(tree, col, reverse):
    # Obtém uma lista dos itens no Treeview
    l = [(tree.set(k, col), k) for k in tree.get_children('')]
    
    # Ordena a lista de forma crescente ou decrescente
    l.sort(reverse=reverse)

    # Reordena os itens no Treeview
    for index, (val, k) in enumerate(l):
        tree.move(k, '', index)

    # Alterna entre ordenação crescente e decrescente
    tree.heading(col, command=lambda: ordenar_por_coluna(tree, col, not reverse))


# Função para buscar POIs
def get_pois(lat, lon, api_key, categories, radius):
    pois_url = f"https://api.geoapify.com/v2/places?categories={categories}&filter=circle:{lon},{lat},{radius}&bias=proximity:{lon},{lat}&apiKey={api_key}"
    response = requests.get(pois_url)
    return response.json()

# Função para salvar os dados como CSV
def salvar_como_csv():
    data = [tree.item(item)['values'] for item in tree.get_children()]
    df = pd.DataFrame(data, columns=columns)
    filepath = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if filepath:
        df.to_csv(filepath, index=False, encoding='utf-8-sig')


# Função chamada quando o botão 'Buscar' é pressionado
def buscar_pois():
    lat_str = lat_entry.get()
    lon_str = lon_entry.get()
    radius_str = radius_entry.get()

    if not (validar_float(lat_str) and validar_float(lon_str) and validar_float(radius_str)):
        messagebox.showerror("Erro de entrada", "Por favor, insira números válidos para latitude, longitude e raio.")
        return

    lat = float(lat_str)
    lon = float(lon_str)
    radius = float(radius_str) * 1000
    categories = ','.join([lista_box.get(i) for i in range(lista_box.size())])

    pois = get_pois(lat, lon, api_key, categories, radius)

    # Processando os dados recebidos
    data = []
    for feature in pois['features']:
        properties = feature['properties']
        data.append([
            properties.get('name', 'NONAME'),
            float(properties.get('distance', 0)) / 1000,
            properties.get('country', ''),
            properties.get('district', ''),
            properties.get('street', ''),
            properties["datasource"]["raw"].get("shop","")+properties["datasource"]["raw"].get("amenity","")+properties["datasource"]["raw"].get("tourism",""),
            properties.get('lat', ''),
            properties.get('lon', ''),
        ])

    # Atualizando o Treeview
    for i in tree.get_children():
        tree.delete(i)
    for row in data:
        tree.insert('', 'end', values=row)

# Configuração da janela principal
root = tk.Tk()
root.title("Buscador de POIs")
root.geometry("800x600")  # Define um tamanho inicial

# Variáveis de configuração
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

# Menu de cascata para botões
menu_botao = ttk.Combobox(entry_frame, values=all_categories, width=47)
menu_botao.pack(side='left', padx=(0, 10))
menu_botao.bind('<KeyRelease>', atualizar_sugestoes)

# Botão para adicionar à lista
botao_adicionar = tk.Button(entry_frame, text="Adicionar à Lista", command=lambda: adicionar_a_lista(menu_botao.get()))
botao_adicionar.pack(side='left', padx=(0, 10))

# Lista na tela para mostrar os cliques
lista_box = tk.Listbox(entry_frame, width=100)
lista_box.pack(side="right",padx=(0,10))
lista_box.bind('<Double-1>', remover_da_lista)


# Tabela de resultados (Treeview)
tree_frame = tk.Frame(root)
tree_frame.pack(fill='both', expand=True, padx=10, pady=10)

columns = ("name", "distance", "country", "district", "street", "entity","lat", "lon")
tree = ttk.Treeview(tree_frame, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col, command=lambda _col=col: ordenar_por_coluna(tree, _col, False))
tree.pack(fill='both', expand=True)

# Botão de busca
search_button = tk.Button(root, text="Buscar", command=buscar_pois)
search_button.pack(side="left",pady=(0, 10))

# Botão para salvar como CSV
save_button = tk.Button(root, text="Salvar como CSV", command=salvar_como_csv)
save_button.pack(side="left",pady=(0, 10))



root.mainloop()
