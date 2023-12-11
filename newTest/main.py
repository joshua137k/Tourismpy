from widgets import *
from web import push
import pandas  as pd
import sys


class App:
	def __init__(self):
		self.lst = []
		self.dic = {"name":[],"distance":[],"country":[],"city":[],"street":[],"lat":[],"lon":[],"entidade":[],"GMT":[],"Currency":[]}

		self.textboxes = [TextBox(55, 22, 290, 25, '',"Latitude:"),
							TextBox(405, 22, 290, 25,"",'Longitude:'),
							TextBox(55, 50, 290, 25,"",'Raio(Km):'),
							TextBox(405, 50, 290, 25,"",'Limite:'),
							TextBox(610, 85, 140, 25,"",'Nome do arquivo')]
		self.cascate_buttons =[CascadeMenu(50, 200, 300, 350, 40, all_categories,self.addLst),CascadeMenu(190, 200, 300, 350, 40,  self.lst,self.remLst)]
		self.cascate_buttonsON=0

		self.buttons = [Button(50, 80, 120, 40, self.switchVisible,0,'Categorias'), 
						Button(190, 80, 120, 40, self.switchVisible,1,'Cat. Escolhidas'),
						Button(340, 80, 120, 40, self.pushDados,None,'Buscar'),
						Button(480, 80, 120, 40, self.salvar,None,'Salvar CSV')]


		self.popUp=Popup(200, 150, 400, 200)
		self.PopUpText="oi"

		self.table = Table(self.dic, 0, 200, 80, 30)
		
	def salvar(self):


		if self.dic["name"]==[]:
			self.PopUpText="Erro. Sem dados para guardar"
			self.popUp.visible=True
			return


		if self.textboxes[4].text=="":
			self.PopUpText="Erro de entrada. Por favor, insira um nome."
			self.popUp.visible=True
			return
		df = pd.DataFrame(self.dic)
		df.to_excel(self.textboxes[4].text+".xlsx", index=False)


	def pushDados(self):

		if self.textboxes[0].text=="" or self.textboxes[1].text=="" or self.textboxes[2].text=="" or self.textboxes[3].text=="":
			self.PopUpText="Erro de entrada. Por favor, insira números válidos para latitude, longitude, limite e raio."
			self.popUp.visible=True
			return

		if self.lst==[]:
			self.PopUpText="Erro de entrada. Por favor, insira as categorias."
			self.popUp.visible=True
			return

		pygame.mouse.set_cursor(*pygame.cursors.diamond)

		push(self.textboxes[0].text,self.textboxes[1].text,self.lst,self.textboxes[2].text,self.textboxes[3].text,self.dic)
		self.table.updateDada(self.dic)
		pygame.mouse.set_cursor()
	        

	def switchVisible(self,n):

		if n!=self.cascate_buttonsON:
			self.cascate_buttons[self.cascate_buttonsON].visible=False
			self.cascate_buttonsON=n


		self.cascate_buttons[n].visible=not(self.cascate_buttons[n].visible)
		self.cascate_buttons[n].filter_items("")


	def addLst(self,n,i):
		if n not in self.lst:
			self.lst.append(n)


	def remLst(self,n,i):
		if n in self.lst:
			self.lst.remove(n)
			i.filter_items("")


	def printLst(self):
		print(self.lst)


	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

				self.table.handle_event(event)

				if self.popUp.visible:
					self.popUp.handle_event(event)

				for textbox in self.textboxes:
					textbox.handle_event(event)

				for button in self.buttons:
					button.is_clicked(event)

				for casbtn in self.cascate_buttons:
					if casbtn.visible:
						casbtn.handle_event(event)
			screen.fill(WHITE)
			self.table.draw(screen)
			for textbox in self.textboxes:
				textbox.draw(screen)

			for button in self.buttons:
				button.draw(screen)

			for casbtn in self.cascate_buttons:
				casbtn.draw(screen)

			self.popUp.update_text(self.PopUpText)
			self.popUp.draw(screen)
            # Desenhar outros elementos...

			

			pygame.display.flip()

# Executa a aplicação
if __name__ == '__main__':
	App().run()
