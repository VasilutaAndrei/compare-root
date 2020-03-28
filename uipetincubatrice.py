import os
import ui
import player
import mouseModule
import net
import app
import snd
import item
import player
import chat
import grp
import uiScriptLocale
import localeInfo
import constInfo
import ime
import wndMgr


class PetSystemIncubator(ui.ScriptWindow):
	
	def __init__(self, new_pet):
		ui.ScriptWindow.__init__(self)
		self.__LoadWindow()
		self.LoadPetIncubatorImg(new_pet)

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Show(self):
		ui.ScriptWindow.Show(self)

	def Close(self):
		self.Hide()
	
	def __LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/PetHatchingWindow.py")
		except:
			import exception
			exception.Abort("PetHatchingWindow.LoadWindow.LoadObject")
			
		try:
			self.board = self.GetChild("board")
			self.boardtitle = self.GetChild("PetHatching_TitleBar")
			
			self.petimg = self.GetChild("HatchingItemSlot")
			self.petname = self.GetChild("pet_name")
			self.HatchingButton = self.GetChild("HatchingButton")
			
			
			#Event
			self.boardtitle.SetCloseEvent(ui.__mem_func__(self.Close))
			self.HatchingButton.SetEvent(ui.__mem_func__(self.RequestHatching,))
			
			
		except:
			import exception
			exception.Abort("PetHatchingWindow.LoadWindow.BindObject")
			
	def LoadPetIncubatorImg(self, new_pet):
		petarryname = ["Ou de Maimutica", "Ou de Paianjen", "Ou de Razador", "Ou de Nemere", "Ou Dragon", "Ou Regina Meley", "Ou Azrael", "Oul Raului"]
		petarryimg = [55701, 55702, 55703, 55704, 55705, 55706, 55707, 55708]
		chat.AppendChat(chat.CHAT_TYPE_INFO, "[Incubator] "+petarryname[int(new_pet)]+".")
		self.petimg.SetItemSlot(0,petarryimg[int(new_pet)], 0)
		self.petimg.SetAlwaysRenderCoverButton(0, True)		
			
	def RequestHatching(self):
		if self.petname.GetText() == "" or len(self.petname.GetText()) < 4:
			chat.AppendChat(chat.CHAT_TYPE_INFO, "[Incubator] Nu poti folosii aceste charactere in numele petului, sau numele are mai putin de 4 caractere.")
			return
			
		if player.GetElk() < 100000:
			chat.AppendChat(chat.CHAT_TYPE_INFO, "[Incubator]Ai nevoie de  "+str(localeInfo.NumberToMoneyString(100000)) +".")
			return
			
		chat.AppendChat(chat.CHAT_TYPE_INFO, "[Incubator]Insotitorul a eclozat cu suces.")
		import chr
		chr.RequestPetName(self.petname.GetText())
		self.Close()
