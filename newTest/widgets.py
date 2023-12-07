import pygame
from constantes import *
from utils import *
import textwrap

# Inicializa o Pygame
pygame.init()

# Configurações da tela
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Lista com Caixa de Scroll')

# Fonte
font = pygame.font.SysFont(None, 20)



class TextBox:
	def __init__(self, x, y, width, height, text='',invisibleText=""):
		self.rect = pygame.Rect(x, y, width, height)
		self.text = text
		self.active = False
		self.border_color = GRAY
		self.invisibleText=invisibleText

	def handle_event(self, event):
		if event.type == pygame.MOUSEBUTTONDOWN:
			if self.rect.collidepoint(event.pos):
				self.active = not self.active
				self.border_color = BLUE if self.active else GRAY
			else:
				self.active = False
				self.border_color=GRAY
		elif event.type == pygame.KEYDOWN:
			if self.active:
				if event.key == pygame.K_BACKSPACE:
					self.text = self.text[:-1]
				else:
					self.text += event.unicode

	def draw(self, screen):
		pygame.draw.rect(screen, WHITE, self.rect)
		pygame.draw.rect(screen, self.border_color, self.rect,2)
		if self.text=="":
			text_surface = font.render(self.invisibleText, True, GRAY)
		else:
			text_surface = font.render(self.text, True, BLACK)
		screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))


class Button:
	def __init__(self, x, y, width, height, func,param=None,text=''):
		self.rect = pygame.Rect(x, y, width, height)
		self.text = text
		self.border_color = GRAY
		self.func=func
		self.param=param

	def draw(self, screen):
		pygame.draw.rect(screen, self.border_color, self.rect)
		text_surface = font.render(self.text, True, BLACK)
		screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))

	def is_clicked(self, event):
		if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
			self.border_color=BLUE
			if self.param==None:
				self.func()
			else:
				self.func(self.param)
		else:
			self.border_color=GRAY


class CascadeMenu:
	def __init__(self, x, y, width, height, item_height,  items,func):
		self.rect = pygame.Rect(x, y, width, height)
		self.item_height = item_height
		self.items = items
		self.filtered_items = items[:]
		self.search_box = TextBox(x, y - 50, width, 25,"","Digite algo...")
		self.scroll_y = 0
		self.max_scroll = 0
		self.func=func
		self.visible = False
		self.marked=-1
		self.filter_items("")



	def update_buttons(self):
		self.buttons = [[pygame.Rect(5, i * self.item_height - 5 + self.scroll_y, self.rect.width - 10, 30),GRAY] for i in range(len(self.filtered_items))]
		self.max_scroll = max(0, len(self.filtered_items) * self.item_height - self.rect.height)

	def filter_items(self, query):
		self.filtered_items = [item for item in self.items if query.lower() in item.lower()]
		self.scroll_y = 0
		self.update_buttons()

	def handle_event(self, event):
		self.search_box.handle_event(event)
		if event.type == pygame.KEYDOWN:
			self.filter_items(self.search_box.text)

		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 4:  # Scroll up
				self.scroll_y = min(self.scroll_y + 20, 0)
			elif event.button == 5:  # Scroll down
				self.scroll_y = max(self.scroll_y - 20, -self.max_scroll)
			for i, button in enumerate(self.buttons):
				if  event.button ==1 and button[0].collidepoint(event.pos[0], event.pos[1] - self.scroll_y-self.rect.y):
						self.buttons[i][1]=BLUE
						self.marked=i
						
					

		if event.type==pygame.MOUSEBUTTONUP:
			a=len(self.items)
			if self.marked!=-1 and a>0:
				self.buttons[self.marked][1]=GRAY
				self.func(self.filtered_items[self.marked].replace(" / ","."),self)
				self.marked=-1
			if a<1:
				self.marked=-1


				




	def draw(self, screen):
		if self.visible:

			# Desenha a barra de pesquisa
			self.search_box.draw(screen)

			# Desenha a caixa de itens
			category_box=pygame.draw.rect(screen, LIGHT_GRAY, self.rect)

			for i, button in enumerate(self.buttons):
				button_rect = pygame.Rect(button[0].x + self.rect.x, self.scroll_y +button[0].y + self.rect.y, button[0].width, button[0].height)
				if category_box.collidepoint(button_rect.topleft) or category_box.collidepoint(button_rect.bottomright):
					pygame.draw.rect(screen,button[1], button_rect)
					dText = adjust_text_to_fit(self.filtered_items[i],button_rect.width - 10, font)
					text = font.render(dText, True, BLACK)
					screen.blit(text, (button_rect.x + 5, button_rect.y + 5))



class Table:
    def __init__(self, data, x, y, column_width, row_height):
        self.data = data
        self.x = x
        self.y = y
        self.column_width = column_width
        self.row_height = row_height
        self.columns = list(data.keys())
        self.rows = len(data[self.columns[0]])
        self.sort_orders = {column: True for column in self.columns}  # True para ascendente, False para descendente

    def draw(self, screen):
        # Desenhar cabeçalho
        for i, column in enumerate(self.columns):
            pygame.draw.rect(screen, (180, 180, 180), (self.x + i * self.column_width, self.y, self.column_width, self.row_height))
            column_text = font.render(column, True, (0, 0, 0))
            screen.blit(column_text, (self.x + i * self.column_width + 5, self.y + 5))

        # Desenhar células da tabela
        for row in range(self.rows):
            for col, column in enumerate(self.columns):
                pygame.draw.rect(screen, (255, 255, 255), (self.x + col * self.column_width, self.y + (row + 1) * self.row_height, self.column_width, self.row_height))
                cell_text = font.render(str(self.data[column][row]), True, (0, 0, 0))
                screen.blit(cell_text, (self.x + col * self.column_width + 5, self.y + (row + 1) * self.row_height + 5))

        # Desenhar linhas de divisão
        for i in range(1, len(self.columns)):
            pygame.draw.line(screen, (0, 0, 0), (self.x + i * self.column_width, self.y), (self.x + i * self.column_width, self.y + self.row_height * (self.rows + 1)))
        pygame.draw.line(screen, (0, 0, 0), (self.x, self.y + self.row_height * (self.rows + 1)), (self.x + self.column_width * len(self.columns), self.y + self.row_height * (self.rows + 1)))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Verificar clique no cabeçalho
            for i, column in enumerate(self.columns):
                header_rect = pygame.Rect(self.x + i * self.column_width, self.y, self.column_width, self.row_height)
                if header_rect.collidepoint(event.pos):
                    self.sort_by_column(column)

    def sort_by_column(self, column):
        # Alternar a ordem de classificação
        self.sort_orders[column] = not self.sort_orders[column]

        # Reorganizar os dados
        zipped_data = zip(*(self.data[col] for col in self.columns))
        sorted_data = sorted(zipped_data, key=lambda row: row[self.columns.index(column)], reverse=self.sort_orders[column])

        # Atualizar os dados
        for i, col in enumerate(self.columns):
            self.data[col] = [row[i] for row in sorted_data]

        # Atualizar número de linhas
        self.rows = len(self.data[self.columns[0]])

    def updateDada(self,dic):
    	self.data=dic
    	self.columns = list(dic.keys())
    	self.rows=len(dic[self.columns[0]])



class Popup:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.visible = False
        self.font = pygame.font.Font(None, 36)
        self.close_button = pygame.Rect(x + width - 30, y, 30, 30)
        self.background_color = (200, 200, 200)
        self.text_color = (0, 0, 0)
        self.text_lines=[]
        self.close_button_color = (255, 0, 0)

    def draw(self, screen):
        if not self.visible:
            return

        # Draw the popup background
        pygame.draw.rect(screen, self.background_color, self.rect)

        # Draw the close button
        pygame.draw.rect(screen, self.close_button_color, self.close_button)

        # Render the text
        for i, line in enumerate(self.text_lines):
            text_surf = self.font.render(line, True, self.text_color)
            screen.blit(text_surf, (self.rect.x + 10, self.rect.y + 10 + i * 30))



    def handle_event(self, event):
        if not self.visible:
            return False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.close_button.collidepoint(event.pos):
                self.visible = False
                return True

        return False



    def update_text(self, new_text):
        self.text_lines = textwrap.wrap(new_text, width=25)  # Assuming 25 characters fit in the width
