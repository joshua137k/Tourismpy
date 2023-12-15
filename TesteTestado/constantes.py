# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (220, 220, 220)
BLUE=(0,0,255)


f = open("../categories.txt","r")
all_categories = [i.strip().replace("."," / ") for i in f]  # Exemplo com 50 categorias
f.close()