import ui
import net
import constInfo
import app
import localeInfo
import interfaceModule
import uimarbleshop
import uispecialstorage
import player
from _weakref import proxy
from switchbot import Bot
import switchbot

class InventoryMenueDialog(ui.ScriptWindow):

	def __init__(self): 
		self.isLoaded = False
		ui.ScriptWindow.__init__(self) 
		self.__LoadWindow()
		self.interface = None
		self.wndMarbleShop = uimarbleshop.MarbleShopWindow()
		self.wndSpecialStorage = uispecialstorage.SpecialStorageWindow()
		self.switchbot = Bot()

	def __del__(self): 
		ui.ScriptWindow.__del__(self) 

	def BindInterfaceClass(self, interface):
		self.interface = interface
		
	def Destroy(self):
		
		self.isLoaded = False
		self.cancelButton = None
		self.interface = None
		self.wndCofres = None
		

	def Show(self):
		self.__LoadWindow()
		ui.ScriptWindow.Show(self)

	def Close(self):
		self.Hide()

	def __LoadWindow(self):
		if self.isLoaded:
			return

		self.isLoaded = True

		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/InventoryMenue.py")
			
			self.NormalStorageButton = self.GetChild("normal_storage")
			self.ItemShopStorageButton = self.GetChild("itemshop_storage")
			self.GuildStorageButton = self.GetChild("guild_storage")
			self.SpecialStorageButton = self.GetChild("special_storage")
			
			self.NormalStorageButton.SetEvent(ui.__mem_func__(self.__OnClickNormalStorageButton))
			self.ItemShopStorageButton.SetEvent(ui.__mem_func__(self.__OnClickItemShopStorageButton))
			self.GuildStorageButton.SetEvent(ui.__mem_func__(self.__CofresShow))
			self.SpecialStorageButton.SetEvent(ui.__mem_func__(self.__SpecialStorage))

			self.Show()
		except:
			import exception
			exception.Abort("InventoryMenue.__LoadWindow - error") 
	
	def __OnClickNormalStorageButton(self):
		self.Close()
		print "click_safebox_button"
		net.SendChatPacket("/click_safebox")
 
	def __OnClickItemShopStorageButton(self):
		self.Close()
		print "click_mall_button"
		net.SendChatPacket("/click_mall")
	
	def __CofresShow(self):
		self.Close()
		self.wndMarbleShop.Show()	
	
	def __SpecialStorage(self):
		self.Close()
		self.switchbot.Show()		
		
	def OnPressEscapeKey(self):
		self.Close()