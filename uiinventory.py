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
import uiRefine
import uiAttachMetin
import uiPickMoney
import uiCommon
import uiPrivateShopBuilder # 개인상점 열동안 ItemMove 방지
import localeInfo
import constInfo
import ime
import ui
import wndMgr
import exchange
import uiSearchShop
import uiNewShop
if app.ENABLE_SASH_SYSTEM:
	import sash
if app.ENABLE_BIOLOG_SYSTEM:
	import uiprofessionalbiolog, uiToolTip
if app.ENABLE_CHANGELOOK_SYSTEM:
	import changelook
from _weakref import proxy
from switchbot import Bot
import switchbot
import uiInventoryMenue
import interfaceModule

ITEM_MALL_BUTTON_ENABLE = True



ITEM_FLAG_APPLICABLE = 1 << 14

class CostumeWindow(ui.ScriptWindow):

	def __init__(self, wndInventory):
		import exception

		if not app.ENABLE_COSTUME_SYSTEM:
			exception.Abort("What do you do?")
			return

		if not wndInventory:
			exception.Abort("wndInventory parameter must be set to InventoryWindow")
			return

		ui.ScriptWindow.__init__(self)

		self.isLoaded = 0
		self.wndInventory = wndInventory;

		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Show(self):
		self.__LoadWindow()
		self.RefreshCostumeSlot()

		ui.ScriptWindow.Show(self)

	def Close(self):
		self.Hide()

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1

		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/costumewindow.py")
		except:
			import exception
			exception.Abort("CostumeWindow.LoadWindow.LoadObject")

		try:
			wndEquip = self.GetChild("CostumeSlot")
			self.GetChild("TitleBar").SetCloseEvent(ui.__mem_func__(self.Close))

		except:
			import exception
			exception.Abort("CostumeWindow.LoadWindow.BindObject")

		## Equipment
		wndEquip.SetOverInItemEvent(ui.__mem_func__(self.wndInventory.OverInItem))
		wndEquip.SetOverOutItemEvent(ui.__mem_func__(self.wndInventory.OverOutItem))
		wndEquip.SetUnselectItemSlotEvent(ui.__mem_func__(self.wndInventory.UseItemSlot))
		wndEquip.SetUseSlotEvent(ui.__mem_func__(self.wndInventory.UseItemSlot))
		wndEquip.SetSelectEmptySlotEvent(ui.__mem_func__(self.wndInventory.SelectEmptySlot))
		wndEquip.SetSelectItemSlotEvent(ui.__mem_func__(self.wndInventory.SelectItemSlot))

		self.wndEquip = wndEquip

	def RefreshCostumeSlot(self):
		getItemVNum=player.GetItemIndex
		for i in xrange(item.COSTUME_SLOT_COUNT):
			slotNumber = item.COSTUME_SLOT_START + i
			self.wndEquip.SetItemSlot(slotNumber, getItemVNum(slotNumber), 0)
			if app.ENABLE_CHANGELOOK_SYSTEM:
				itemTransmutedVnum = player.GetItemTransmutation(slotNumber)
				if itemTransmutedVnum:
					self.wndEquip.DisableCoverButton(slotNumber)
				else:
					self.wndEquip.EnableCoverButton(slotNumber)
		
		slotNumber = item.EQUIPMENT_BELT + 1
		self.wndEquip.SetItemSlot(slotNumber, getItemVNum(slotNumber), 0)
		if app.ENABLE_CHANGELOOK_SYSTEM:
			itemTransmutedVnum = player.GetItemTransmutation(slotNumber)
			if itemTransmutedVnum:
				self.wndEquip.DisableCoverButton(slotNumber)
			else:
				self.wndEquip.EnableCoverButton(slotNumber)
		
		self.wndEquip.RefreshSlot()
class BeltInventoryWindow(ui.ScriptWindow):

	def __init__(self, wndInventory):
		import exception

		if not app.ENABLE_NEW_EQUIPMENT_SYSTEM:
			exception.Abort("What do you do?")
			return

		if not wndInventory:
			exception.Abort("wndInventory parameter must be set to InventoryWindow")
			return

		ui.ScriptWindow.__init__(self)

		self.isLoaded = 0
		self.wndInventory = wndInventory;

		self.wndBeltInventoryLayer = None
		self.wndBeltInventorySlot = None
		self.expandBtn = None
		self.minBtn = None

		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Show(self, openBeltSlot = False):
		self.__LoadWindow()
		self.RefreshSlot()

		ui.ScriptWindow.Show(self)

		if openBeltSlot:
			self.OpenInventory()
		else:
			self.CloseInventory()

	def Close(self):
		self.Hide()

	def IsOpeningInventory(self):
		return self.wndBeltInventoryLayer.IsShow()

	def OpenInventory(self):
		self.wndBeltInventoryLayer.Show()
		self.expandBtn.Hide()

		if localeInfo.IsARABIC() == 0:
			self.AdjustPositionAndSize()

	def CloseInventory(self):
		self.wndBeltInventoryLayer.Hide()
		self.expandBtn.Show()

		if localeInfo.IsARABIC() == 0:
			self.AdjustPositionAndSize()

	## 현재 인벤토리 위치를 기준으로 BASE 위치를 계산, 리턴.. 숫자 하드코딩하기 정말 싫지만 방법이 없다..
	if app.ENABLE_BIOLOG_SYSTEM:
		def GetBasePosition(self):
			x, y = self.wndInventory.GetGlobalPosition()
			return x - 148, y + 385
	else:
		def GetBasePosition(self):
			x, y = self.wndInventory.GetGlobalPosition()
			return x - 148, y + 241	

	def AdjustPositionAndSize(self):
		bx, by = self.GetBasePosition()

		if self.IsOpeningInventory():
			self.SetPosition(bx, by)
			self.SetSize(self.ORIGINAL_WIDTH, self.GetHeight())

		else:
			self.SetPosition(bx + 138, by);
			self.SetSize(10, self.GetHeight())

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1

		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/BeltInventoryWindow.py")
		except:
			import exception
			exception.Abort("CostumeWindow.LoadWindow.LoadObject")

		try:
			self.ORIGINAL_WIDTH = self.GetWidth()
			wndBeltInventorySlot = self.GetChild("BeltInventorySlot")
			self.wndBeltInventoryLayer = self.GetChild("BeltInventoryLayer")
			self.expandBtn = self.GetChild("ExpandBtn")
			self.minBtn = self.GetChild("MinimizeBtn")

			self.expandBtn.SetEvent(ui.__mem_func__(self.OpenInventory))
			self.minBtn.SetEvent(ui.__mem_func__(self.CloseInventory))

			if localeInfo.IsARABIC() :
				self.expandBtn.SetPosition(self.expandBtn.GetWidth() - 2, 15)
				self.wndBeltInventoryLayer.SetPosition(self.wndBeltInventoryLayer.GetWidth() - 5, 0)
				self.minBtn.SetPosition(self.minBtn.GetWidth() + 3, 15)

			for i in xrange(item.BELT_INVENTORY_SLOT_COUNT):
				slotNumber = item.BELT_INVENTORY_SLOT_START + i
				wndBeltInventorySlot.SetCoverButton(slotNumber,	"d:/ymir work/ui/game/quest/slot_button_01.sub",\
												"d:/ymir work/ui/game/quest/slot_button_01.sub",\
												"d:/ymir work/ui/game/quest/slot_button_01.sub",\
												"d:/ymir work/ui/game/belt_inventory/slot_disabled.tga", False, False)

		except:
			import exception
			exception.Abort("CostumeWindow.LoadWindow.BindObject")

		## Equipment
		wndBeltInventorySlot.SetOverInItemEvent(ui.__mem_func__(self.wndInventory.OverInItem))
		wndBeltInventorySlot.SetOverOutItemEvent(ui.__mem_func__(self.wndInventory.OverOutItem))
		wndBeltInventorySlot.SetUnselectItemSlotEvent(ui.__mem_func__(self.wndInventory.UseItemSlot))
		wndBeltInventorySlot.SetUseSlotEvent(ui.__mem_func__(self.wndInventory.UseItemSlot))
		wndBeltInventorySlot.SetSelectEmptySlotEvent(ui.__mem_func__(self.wndInventory.SelectEmptySlot))
		wndBeltInventorySlot.SetSelectItemSlotEvent(ui.__mem_func__(self.wndInventory.SelectItemSlot))

		self.wndBeltInventorySlot = wndBeltInventorySlot

	def RefreshSlot(self):
		getItemVNum=player.GetItemIndex

		for i in xrange(item.BELT_INVENTORY_SLOT_COUNT):
			slotNumber = item.BELT_INVENTORY_SLOT_START + i
			self.wndBeltInventorySlot.SetItemSlot(slotNumber, getItemVNum(slotNumber), player.GetItemCount(slotNumber))
			self.wndBeltInventorySlot.SetAlwaysRenderCoverButton(slotNumber, True)

			avail = "0"

			if player.IsAvailableBeltInventoryCell(slotNumber):
				self.wndBeltInventorySlot.EnableCoverButton(slotNumber)
			else:
				self.wndBeltInventorySlot.DisableCoverButton(slotNumber)

		self.wndBeltInventorySlot.RefreshSlot()

if app.ENABLE_BIOLOG_SYSTEM:
###################################################################
# title_name		: Professional Biolog System
# date_created		: 2016.08.07
# filename			: uiInventory.py
# author			: VegaS
# version_actual	: Version 0.2.8
#
	class CollectInventoryWindow(ui.ScriptWindow):
		def __init__(self, wndInventory):
			import exception
			if not wndInventory:
				exception.Abort("wndInventory parameter must be set to CollectInventoryWindow")
				return
			ui.ScriptWindow.__init__(self)
			self.isLoaded = 0
			self.updated = 0
			self.wndInventory = wndInventory;
			self.tooltipItem = uiToolTip.ItemToolTip()
			self.tooltipItem.Hide()
			self.wndBeltInventoryLayer = None
			self.wndBeltInventorySlot = None
			self.expandBtn = None
			self.minBtn = None
			self.gameWindow = None
			self.__LoadWindow()

		def __del__(self):
			ui.ScriptWindow.__del__(self)

		def Show(self, openBeltSlot = False):
			self.__LoadWindow()
			ui.ScriptWindow.Show(self)

			if openBeltSlot:
				self.OpenInventory()
			else:
				self.CloseInventory()

		def Close(self):
			self.Hide()

		def IsOpeningInventory(self):
			return self.wndBeltInventoryLayer.IsShow()

		def OpenInventory(self):
			self.wndBeltInventoryLayer.Show()
			self.expandBtn.Hide()

			self.AdjustPositionAndSize()

		def CloseInventory(self):
			self.wndBeltInventoryLayer.Hide()
			self.expandBtn.Show()

			self.AdjustPositionAndSize()

		def GetBasePosition(self):
			x, y = self.wndInventory.GetGlobalPosition()
			return x - 148, y + 260
			
		def AdjustPositionAndSize(self):
			bx, by = self.GetBasePosition()

			if self.IsOpeningInventory():
				self.SetPosition(bx, by)
				self.SetSize(self.ORIGINAL_WIDTH, self.GetHeight())
			else:
				self.SetPosition(bx + 138, by);
				self.SetSize(10, self.GetHeight())

		def __LoadWindow(self):
			if self.isLoaded == 1:
				return

			self.isLoaded = 1

			try:
				pyScrLoader = ui.PythonScriptLoader()
				pyScrLoader.LoadScriptFile(self, "UIScript/biolog_collectinventorywindow.py")
			except:
				import exception
				exception.Abort("CollectInventoryWindow.LoadWindow.LoadObject")

			try:
				self.ORIGINAL_WIDTH = self.GetWidth()
				self.wndBeltInventoryLayer = self.GetChild("BeltInventoryLayer")
				self.wndItem = self.GetChild("BeltInventorySlot")
				self.time_value = self.GetChild("time_value")
				self.biolog_count = self.GetChild("count_value")
				self.expandBtn = self.GetChild("ExpandBtn")
				self.minBtn = self.GetChild("MinimizeBtn")
				self.sendBtn = self.GetChild("send_biolog")
				self.expandBtn.SetEvent(ui.__mem_func__(self.OpenInventory))
				self.minBtn.SetEvent(ui.__mem_func__(self.CloseInventory))
				self.wndItem.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
				self.wndItem.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
			except:
				import exception
				exception.Abort("CollectInventoryWindow.LoadWindow.BindObject")

			if self.sendBtn:
				self.sendBtn.SetEvent(ui.__mem_func__(self.AcceptBiolog))

		def SetItem(self, arg1, arg2, arg3):
			self.wndItem.SetItemSlot(0, int(uiprofessionalbiolog.BIOLOG_BINARY_LOADED["vnum"][0]), 0)
			
		def AcceptBiolog(self):
			net.SendChatPacket("/biolog")

		def SetTime(self, time):
			time_collect = time - app.GetGlobalTimeStamp()

			if time_collect < 0:
				time_collect = 0 

			if time_collect == 1:
				self.wndLeftTime = uiprofessionalbiolog.Biolog_TimeExpired()
				self.wndLeftTime.OpenWindow()
				self.wndLeftTime.Show()

			self.time_value.SetText(localeInfo.FormatTime(time_collect))

		def OnUpdate(self):
			self.SetTime(int(uiprofessionalbiolog.BIOLOG_BINARY_LOADED["time"][0]))
			self.SetItem(0, uiprofessionalbiolog.BIOLOG_BINARY_LOADED["vnum"][0], 0)
			self.biolog_count.SetText(uiprofessionalbiolog.BIOLOG_BINARY_LOADED['countActual'][0] + "/" + uiprofessionalbiolog.BIOLOG_BINARY_LOADED['countNeed'][0])

		def OverInItem(self):
			if uiprofessionalbiolog.BIOLOG_BINARY_LOADED["vnum"][0]:
				self.tooltipItem.SetItemToolTip(uiprofessionalbiolog.BIOLOG_BINARY_LOADED["vnum"][0])

		def OverOutItem(self):
			if self.tooltipItem:
				self.tooltipItem.HideToolTip()

class InventoryWindow(ui.ScriptWindow):

	if app.ENABLE_COSTUME_ATTR_SYSTEM:
		USE_TYPE_TUPLE = ("USE_CLEAN_SOCKET", "USE_CHANGE_ATTRIBUTE", "USE_ADD_ATTRIBUTE", "USE_ADD_ATTRIBUTE2", "USE_ADD_ACCESSORY_SOCKET", "USE_PUT_INTO_ACCESSORY_SOCKET", "USE_PUT_INTO_BELT_SOCKET", "USE_PUT_INTO_RING_SOCKET", "USE_COSTUME_ENCHANT", "USE_COSTUME_TRANSFORM", "USE_SPECIAL")
	else:
		USE_TYPE_TUPLE = ("USE_CLEAN_SOCKET", "USE_CHANGE_ATTRIBUTE", "USE_ADD_ATTRIBUTE", "USE_ADD_ATTRIBUTE2", "USE_ADD_ACCESSORY_SOCKET", "USE_PUT_INTO_ACCESSORY_SOCKET", "USE_PUT_INTO_BELT_SOCKET", "USE_PUT_INTO_RING_SOCKET", "USE_SPECIAL")

	questionDialog = None
	tooltipItem = None
	wndCostume = None
	wndBelt = None
	if app.ENABLE_BIOLOG_SYSTEM:
		wndCollect = None
	dlgPickMoney = None
	interface = None
	if app.WJ_ENABLE_TRADABLE_ICON:
		bindWnds = []
		
	sellingSlotNumber = -1
	isLoaded = 0
	isOpenedCostumeWindowWhenClosingInventory = 0		# 인벤토리 닫을 때 코스츔이 열려있었는지 여부-_-; 네이밍 ㅈㅅ
	if app.ENABLE_BIOLOG_SYSTEM:
		isOpenedCollectWindowWhenClosingInventory = 0
	isOpenedBeltWindowWhenClosingInventory = 0		# 인벤토리 닫을 때 벨트 인벤토리가 열려있었는지 여부-_-; 네이밍 ㅈㅅ

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.isOpenedBeltWindowWhenClosingInventory = 0		# 인벤토리 닫을 때 벨트 인벤토리가 열려있었는지 여부-_-; 네이밍 ㅈㅅ
		self.uiSearchShop=uiSearchShop.ShopSearch()
		self.switchbot = Bot()
		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Show(self):
		self.__LoadWindow()

		ui.ScriptWindow.Show(self)

		# 인벤토리를 닫을 때 코스츔이 열려있었다면 인벤토리를 열 때 코스츔도 같이 열도록 함.
		if self.isOpenedCostumeWindowWhenClosingInventory and self.wndCostume:
			self.wndCostume.Show()

		if app.ENABLE_BIOLOG_SYSTEM:
			if self.wndCollect:
				self.wndCollect.Show(self.isOpenedCollectWindowWhenClosingInventory)

		# Belt System
		if self.wndBelt:
			self.wndBelt.Show(self.isOpenedBeltWindowWhenClosingInventory)

	def BindInterfaceClass(self, interface):
		self.interface = interface

	if app.WJ_ENABLE_TRADABLE_ICON:
		def BindWindow(self, wnd):
			self.bindWnds.append(wnd)		
		
	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1

		try:
			pyScrLoader = ui.PythonScriptLoader()

			if ITEM_MALL_BUTTON_ENABLE:
				pyScrLoader.LoadScriptFile(self, uiScriptLocale.LOCALE_UISCRIPT_PATH + "InventoryWindow.py")
			else:
				pyScrLoader.LoadScriptFile(self, "UIScript/InventoryWindow.py")
		except:
			import exception
			exception.Abort("InventoryWindow.LoadWindow.LoadObject")

		try:
			wndItem = self.GetChild("ItemSlot")
			wndEquip = self.GetChild("EquipmentSlot")
			self.GetChild("TitleBar").SetCloseEvent(ui.__mem_func__(self.Close))
			#self.wndMoney = self.GetChild("Money")
			#self.wndMoneySlot = self.GetChild("Money_Slot")
			# self.mallButton = self.GetChild2("MallButton")
			self.OFFButton = self.GetChild2("OFFButton")
			self.SWITCHButton = self.GetChild2("SWITCHButton")
			self.INFOCHESTButton = self.GetChild2("INFOCHESTButton")
			self.costumeButton = self.GetChild2("CostumeButton")
				
			self.inventoryTab = []
			self.inventoryTab.append(self.GetChild("Inventory_Tab_01"))
			self.inventoryTab.append(self.GetChild("Inventory_Tab_02"))
			self.inventoryTab.append(self.GetChild("Inventory_Tab_03"))
			self.inventoryTab.append(self.GetChild("Inventory_Tab_04"))

			self.equipmentTab = []
			self.equipmentTab.append(self.GetChild("Equipment_Tab_01"))
			self.equipmentTab.append(self.GetChild("Equipment_Tab_02"))

			if self.costumeButton and not app.ENABLE_COSTUME_SYSTEM:
				self.costumeButton.Hide()
				self.costumeButton.Destroy()
				self.costumeButton = 0

			# Belt Inventory Window
			self.wndBelt = None

			if app.ENABLE_NEW_EQUIPMENT_SYSTEM:
				self.wndBelt = BeltInventoryWindow(self)
			if app.ENABLE_BIOLOG_SYSTEM:
				self.wndCollect = None
				self.wndCollect = CollectInventoryWindow(self)

		except:
			import exception
			exception.Abort("InventoryWindow.LoadWindow.BindObject")

		## Item
		wndItem.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySlot))
		wndItem.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectItemSlot))
		wndItem.SetUnselectItemSlotEvent(ui.__mem_func__(self.UseItemSlot))
		wndItem.SetUseSlotEvent(ui.__mem_func__(self.UseItemSlot))
		wndItem.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		wndItem.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))

		## Equipment
		wndEquip.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySlot))
		wndEquip.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectItemSlot))
		wndEquip.SetUnselectItemSlotEvent(ui.__mem_func__(self.UseItemSlot))
		wndEquip.SetUseSlotEvent(ui.__mem_func__(self.UseItemSlot))
		wndEquip.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		wndEquip.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))

		## PickMoneyDialog
		dlgPickMoney = uiPickMoney.PickMoneyDialog()
		dlgPickMoney.LoadDialog()
		dlgPickMoney.Hide()

		## RefineDialog
		self.refineDialog = uiRefine.RefineDialog()
		self.refineDialog.Hide()

		## AttachMetinDialog
		if app.WJ_ENABLE_TRADABLE_ICON:  
			self.attachMetinDialog = uiAttachMetin.AttachMetinDialog(self)
			self.BindWindow(self.attachMetinDialog)
		else:
			self.attachMetinDialog = uiAttachMetin.AttachMetinDialog()
		self.attachMetinDialog.Hide()

		## MoneySlot
		#self.wndMoneySlot.SetEvent(ui.__mem_func__(self.OpenPickMoneyDialog))

		self.inventoryTab[0].SetEvent(lambda arg=0: self.SetInventoryPage(arg))
		self.inventoryTab[1].SetEvent(lambda arg=1: self.SetInventoryPage(arg))
		self.inventoryTab[2].SetEvent(lambda arg=2: self.SetInventoryPage(arg))
		self.inventoryTab[3].SetEvent(lambda arg=3: self.SetInventoryPage(arg))
		self.inventoryTab[0].Down()
		self.inventoryPageIndex = 0

		self.equipmentTab[0].SetEvent(lambda arg=0: self.SetEquipmentPage(arg))
		self.equipmentTab[1].SetEvent(lambda arg=1: self.SetEquipmentPage(arg))
		self.equipmentTab[0].Down()
		self.equipmentTab[0].Hide()
		self.equipmentTab[1].Hide()

		self.wndItem = wndItem
		self.wndEquip = wndEquip
		self.dlgPickMoney = dlgPickMoney				
		
		# MallButton
		# if self.mallButton:
			# self.mallButton.SetEvent(ui.__mem_func__(self.ClickMallButton))

		if self.OFFButton:
			self.OFFButton.SetEvent(ui.__mem_func__(self.ClickOFFButton))

		if self.SWITCHButton:
			self.SWITCHButton.SetEvent(ui.__mem_func__(self.SwitchBot))

		if self.INFOCHESTButton:
			self.INFOCHESTButton.SetEvent(ui.__mem_func__(self.InfoChest))
							
		# Costume Button
		if self.costumeButton:
			self.costumeButton.SetEvent(ui.__mem_func__(self.ClickCostumeButton))

		self.wndCostume = None

 		#####

		## Refresh
		if app.ENABLE_SASH_SYSTEM:
			self.listAttachedSashs = []
		if app.ENABLE_CHANGELOOK_SYSTEM:
			self.listAttachedCl = []
		self.SetInventoryPage(0)
		self.SetEquipmentPage(0)
		self.RefreshItemSlot()
		self.RefreshStatus()

	def Destroy(self):
		self.ClearDictionary()

		self.dlgPickMoney.Destroy()
		self.dlgPickMoney = 0

		self.refineDialog.Destroy()
		self.refineDialog = 0

		self.attachMetinDialog.Destroy()
		self.attachMetinDialog = 0

		self.tooltipItem = None
		self.wndItem = 0
		self.wndEquip = 0
		self.dlgPickMoney = 0
		#self.wndMoney = 0
		#self.wndMoneySlot = 0
		self.questionDialog = None
		# self.mallButton = None
		self.DSSButton = None
		self.OFFButton = None
		self.SWITCHButton = None
		self.INFOCHESTButton = None
		self.interface = None
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.bindWnds = []

		if self.wndCostume:
			self.wndCostume.Destroy()
			self.wndCostume = 0

		if self.wndBelt:
			self.wndBelt.Destroy()
			self.wndBelt = None

		if app.ENABLE_BIOLOG_SYSTEM:
			if self.wndCollect:
				self.wndCollect.Destroy()
				self.wndCollect = None

		if self.uiSearchShop:
			self.uiSearchShop.Destroy()
			self.uiSearchShop = None
			
		self.inventoryTab = []
		self.equipmentTab = []

	def Hide(self):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS():
			self.OnCloseQuestionDialog()
			return
		if None != self.tooltipItem:
			self.tooltipItem.HideToolTip()

		if self.wndCostume:
			self.isOpenedCostumeWindowWhenClosingInventory = self.wndCostume.IsShow()			# 인벤토리 창이 닫힐 때 코스츔이 열려 있었는가?
			self.wndCostume.Close()

		if app.ENABLE_BIOLOG_SYSTEM:
			if self.wndCollect:
				self.isOpenedCollectWindowWhenClosingInventory = self.wndCollect.IsOpeningInventory()
				print "Is opening Biolog Inventory", self.isOpenedCollectWindowWhenClosingInventory
				self.wndCollect.Close()	

		if self.wndBelt:
			self.isOpenedBeltWindowWhenClosingInventory = self.wndBelt.IsOpeningInventory()		# 인벤토리 창이 닫힐 때 벨트 인벤토리도 열려 있었는가?
			print "Is Opening Belt Inven?? ", self.isOpenedBeltWindowWhenClosingInventory
			self.wndBelt.Close()

		if self.dlgPickMoney:
			self.dlgPickMoney.Close()

		self.OnCloseQuestionDialog()
		
		wndMgr.Hide(self.hWnd)


	def Close(self):
		self.Hide()

	def SetInventoryPage(self, page):
		self.inventoryTab[self.inventoryPageIndex].SetUp()
		self.inventoryPageIndex = page
		self.inventoryTab[self.inventoryPageIndex].Down()
		self.RefreshBagSlotWindow()		
		
	# def SetInventoryPage(self, page):
		# self.inventoryPageIndex = page
		# self.inventoryTab[(page+1)%4].SetUp()
		# self.inventoryTab[(page+2)%4].SetUp()
		# self.inventoryTab[(page+3)%4].SetUp()
		# self.RefreshBagSlotWindow()

	def SetEquipmentPage(self, page):
		self.equipmentPageIndex = page
		self.equipmentTab[1-page].SetUp()
		self.RefreshEquipSlotWindow()	

	# def ClickMallButton(self):
		# print "click_mall_button"
		# net.SendChatPacket("/click_mall")

	# DSSButton
	def ClickOFFButton(self):
		print "click_off_button"
		import uiNewShop
		net.SendChatPacket("/open_shop")
				
	def ClickDSSButton(self):
		print "click_dss_button"
		self.interface.ToggleDragonSoulWindow()
		
	def SwitchBot(self):
		self.interface.ToggleSpecialStorageWindow()

	def InfoChest(self):
		self.meniuinventar = uiInventoryMenue.InventoryMenueDialog()
		self.meniuinventar.Show()			

	def ClickCostumeButton(self):
		print "Click Costume Button"
		if self.wndCostume:
			if self.wndCostume.IsShow():
				self.wndCostume.Hide()
			else:
				self.wndCostume.Show()
		else:
			self.wndCostume = CostumeWindow(self)
			self.wndCostume.Show()

	def OpenPickMoneyDialog(self):

		if mouseModule.mouseController.isAttached():

			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			if player.SLOT_TYPE_SAFEBOX == mouseModule.mouseController.GetAttachedType():

				if player.ITEM_MONEY == mouseModule.mouseController.GetAttachedItemIndex():
					net.SendSafeboxWithdrawMoneyPacket(mouseModule.mouseController.GetAttachedItemCount())
					snd.PlaySound("sound/ui/money.wav")

			mouseModule.mouseController.DeattachObject()

		else:
			curMoney = player.GetElk()

			if curMoney <= 0:
				return

			self.dlgPickMoney.SetTitleName(localeInfo.PICK_MONEY_TITLE)
			self.dlgPickMoney.SetAcceptEvent(ui.__mem_func__(self.OnPickMoney))
			self.dlgPickMoney.Open(curMoney)
			self.dlgPickMoney.SetMax(7) # 인벤토리 990000 제한 버그 수정

	def OnPickMoney(self, money):
		mouseModule.mouseController.AttachMoney(self, player.SLOT_TYPE_INVENTORY, money)

	def OnPickItem(self, count):
		itemSlotIndex = self.dlgPickMoney.itemGlobalSlotIndex
		selectedItemVNum = player.GetItemIndex(itemSlotIndex)
		mouseModule.mouseController.AttachObject(self, player.SLOT_TYPE_INVENTORY, itemSlotIndex, selectedItemVNum, count)

	def __InventoryLocalSlotPosToGlobalSlotPos(self, local):
		if player.IsEquipmentSlot(local) or player.IsCostumeSlot(local) or (app.ENABLE_NEW_EQUIPMENT_SYSTEM and player.IsBeltInventorySlot(local)):
			return local

		return self.inventoryPageIndex*player.INVENTORY_PAGE_SIZE + local
		
	def GetInventoryPageIndex(self):
		return self.inventoryPageIndex

	if app.WJ_ENABLE_TRADABLE_ICON:
		def RefreshMarkSlots(self, localIndex=None):
			if not self.interface:
				return

			onTopWnd = self.interface.GetOnTopWindow()
			if localIndex:
				slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(localIndex)
				if onTopWnd == player.ON_TOP_WND_NONE:
					self.wndItem.SetUsableSlotOnTopWnd(localIndex)

				elif onTopWnd == player.ON_TOP_WND_SHOP:
					if player.IsAntiFlagBySlot(slotNumber, item.ANTIFLAG_SELL):
						self.wndItem.SetUnusableSlotOnTopWnd(localIndex)
					else:
						self.wndItem.SetUsableSlotOnTopWnd(localIndex)

				elif onTopWnd == player.ON_TOP_WND_EXCHANGE:
					if player.IsAntiFlagBySlot(slotNumber, item.ANTIFLAG_GIVE):
						self.wndItem.SetUnusableSlotOnTopWnd(localIndex)
					else:
						self.wndItem.SetUsableSlotOnTopWnd(localIndex)

				elif onTopWnd == player.ON_TOP_WND_PRIVATE_SHOP:
					if player.IsAntiFlagBySlot(slotNumber, item.ITEM_ANTIFLAG_MYSHOP):
						self.wndItem.SetUnusableSlotOnTopWnd(localIndex)
					else:
						self.wndItem.SetUsableSlotOnTopWnd(localIndex)

				elif onTopWnd == player.ON_TOP_WND_SAFEBOX:
					if player.IsAntiFlagBySlot(slotNumber, item.ANTIFLAG_SAFEBOX):
						self.wndItem.SetUnusableSlotOnTopWnd(localIndex)
					else:
						self.wndItem.SetUsableSlotOnTopWnd(localIndex)

				return

			for i in xrange(player.INVENTORY_PAGE_SIZE):
				slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(i)

				if onTopWnd == player.ON_TOP_WND_NONE:
					self.wndItem.SetUsableSlotOnTopWnd(i)

				elif onTopWnd == player.ON_TOP_WND_SHOP:
					if player.IsAntiFlagBySlot(slotNumber, item.ANTIFLAG_SELL):
						self.wndItem.SetUnusableSlotOnTopWnd(i)
					else:
						self.wndItem.SetUsableSlotOnTopWnd(i)

				elif onTopWnd == player.ON_TOP_WND_EXCHANGE:
					if player.IsAntiFlagBySlot(slotNumber, item.ANTIFLAG_GIVE):
						self.wndItem.SetUnusableSlotOnTopWnd(i)
					else:
						self.wndItem.SetUsableSlotOnTopWnd(i)

				elif onTopWnd == player.ON_TOP_WND_PRIVATE_SHOP:
					if player.IsAntiFlagBySlot(slotNumber, item.ITEM_ANTIFLAG_MYSHOP):
						self.wndItem.SetUnusableSlotOnTopWnd(i)
					else:
						self.wndItem.SetUsableSlotOnTopWnd(i)

				elif onTopWnd == player.ON_TOP_WND_SAFEBOX:
					if player.IsAntiFlagBySlot(slotNumber, item.ANTIFLAG_SAFEBOX):
						self.wndItem.SetUnusableSlotOnTopWnd(i)
					else:
						self.wndItem.SetUsableSlotOnTopWnd(i)
		
	def RefreshBagSlotWindow(self):
		is_activated = 0
		getItemVNum=player.GetItemIndex
		getItemCount=player.GetItemCount
		setItemVNum=self.wndItem.SetItemSlot
		for i in xrange(player.INVENTORY_PAGE_SIZE):
			slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(i)
			itemCount = getItemCount(slotNumber)
			if 0 == itemCount:
				self.wndItem.ClearSlot(i)
				continue
			elif 1 == itemCount:
				itemCount = 0

			itemVnum = getItemVNum(slotNumber)
			setItemVNum(i, itemVnum, itemCount)
			if app.ENABLE_CHANGELOOK_SYSTEM:
				itemTransmutedVnum = player.GetItemTransmutation(slotNumber)
				if itemTransmutedVnum:
					self.wndItem.DisableCoverButton(i)
				else:
					self.wndItem.EnableCoverButton(i)
					
			if constInfo.IS_AUTO_POTION(itemVnum):
				metinSocket = [player.GetItemMetinSocket(slotNumber, j) for j in xrange(player.METIN_SOCKET_MAX_NUM)]
				if slotNumber >= player.INVENTORY_PAGE_SIZE:
					slotNumber -= player.INVENTORY_PAGE_SIZE
				
				isActivated = 0 != metinSocket[0]
				if isActivated:
					self.wndItem.ActivateSlotOld(i)
					potionType = 0;
					if constInfo.IS_AUTO_POTION_HP(itemVnum):
						potionType = player.AUTO_POTION_TYPE_HP
					elif constInfo.IS_AUTO_POTION_SP(itemVnum):
						potionType = player.AUTO_POTION_TYPE_SP						

					usedAmount = int(metinSocket[1])
					totalAmount = int(metinSocket[2])					
					player.SetAutoPotionInfo(potionType, isActivated, (totalAmount - usedAmount), totalAmount, self.__InventoryLocalSlotPosToGlobalSlotPos(i))
				else:
					self.wndItem.DeactivateSlotOld(i)
			if app.WJ_ENABLE_TRADABLE_ICON:
				self.RefreshMarkSlots(i)
				
			if app.ENABLE_SASH_SYSTEM or app.ENABLE_CHANGELOOK_SYSTEM:
				if not constInfo.IS_AUTO_POTION(itemVnum):
					self.wndItem.DeactivateSlotOld(i)

			if app.ENABLE_SASH_SYSTEM:
				slotNumberChecked = 0
				for j in xrange(sash.WINDOW_MAX_MATERIALS):
					(isHere, iCell) = sash.GetAttachedItem(j)
					if isHere:
						if iCell == slotNumber:
							self.wndItem.ActivateSlot(i, (238.00 / 255.0), (11.00 / 255.0), (11.00 / 255.0), 1.0)
							if not slotNumber in self.listAttachedSashs:
								self.listAttachedSashs.append(slotNumber)

							slotNumberChecked = 1
					else:
						if slotNumber in self.listAttachedSashs and not slotNumberChecked:
							self.wndItem.DeactivateSlot(i)
							self.listAttachedSashs.remove(slotNumber)

			if app.ENABLE_CHANGELOOK_SYSTEM:
				slotClNumberChecked = 0
				for q in xrange(changelook.WINDOW_MAX_MATERIALS):
					(isHere, iCell) = changelook.GetAttachedItem(q)
					if isHere:
						if iCell == slotNumber:
							self.wndItem.ActivateSlot(i, (238.00 / 255.0), (11.00 / 255.0), (11.00 / 255.0), 1.0)
							if not slotNumber in self.listAttachedCl:
								self.listAttachedCl.append(slotNumber)

							slotClNumberChecked = 1
					else:
						if slotNumber in self.listAttachedCl and not slotClNumberChecked:
							self.wndItem.DeactivateSlot(i)
							self.listAttachedCl.remove(slotNumber)

			if self.IS_NEW_SPEED_POTION(itemVnum):
				metinSocket = [player.GetItemMetinSocket(slotNumber, j) for j in xrange(player.METIN_SOCKET_MAX_NUM)]
				if slotNumber >= player.INVENTORY_PAGE_SIZE * self.inventoryPageIndex:
					slotNumber -= player.INVENTORY_PAGE_SIZE * self.inventoryPageIndex

				isActivated = 0 != metinSocket[0]
	
				if isActivated:
					self.wndItem.ActivateSlotOld(i)
				else:
					self.wndItem.DeactivateSlotOld(i)
				
		self.wndItem.RefreshSlot()
		if self.wndBelt:
			self.wndBelt.RefreshSlot()
		if app.WJ_ENABLE_TRADABLE_ICON:
			map(lambda wnd:wnd.RefreshLockedSlot(), self.bindWnds)

	def IS_NEW_SPEED_POTION(self, itemVnum):
		if itemVnum == 20201:
			return 1
		if itemVnum == 20202:
			return 1
		if itemVnum == 20203:
			return 1
		if itemVnum == 20204:
			return 1
		if itemVnum == 20205:
			return 1
		if itemVnum == 20206:
			return 1
		if itemVnum == 20207:
			return 1
		if itemVnum == 20208:
			return 1
		if itemVnum == 20209:
			return 1
		if itemVnum == 20210:
			return 1
		if itemVnum == 20211:
			return 1
		if itemVnum == 20212:
			return 1
		if itemVnum == 20213:
			return 1
		if itemVnum == 20214:
			return 1

	def RefreshEquipSlotWindow(self):
		getItemVNum=player.GetItemIndex
		getItemCount=player.GetItemCount
		setItemVNum=self.wndEquip.SetItemSlot
		for i in xrange(player.EQUIPMENT_PAGE_COUNT):
			slotNumber = player.EQUIPMENT_SLOT_START + i
			itemCount = getItemCount(slotNumber)
			if itemCount <= 1:
				itemCount = 0
			
			setItemVNum(slotNumber, getItemVNum(slotNumber), itemCount)
			if app.ENABLE_CHANGELOOK_SYSTEM:
				itemTransmutedVnum = player.GetItemTransmutation(slotNumber)
				if itemTransmutedVnum:
					self.wndEquip.DisableCoverButton(slotNumber)
				else:
					self.wndEquip.EnableCoverButton(slotNumber)
		
		if app.ENABLE_NEW_EQUIPMENT_SYSTEM:
			for i in xrange(player.NEW_EQUIPMENT_SLOT_COUNT):
				slotNumber = player.NEW_EQUIPMENT_SLOT_START + i
				itemCount = getItemCount(slotNumber)
				if itemCount <= 1:
					itemCount = 0
				
				setItemVNum(slotNumber, getItemVNum(slotNumber), itemCount)
				if app.ENABLE_CHANGELOOK_SYSTEM:
					itemTransmutedVnum = player.GetItemTransmutation(slotNumber)
					if itemTransmutedVnum:
						self.wndEquip.DisableCoverButton(slotNumber)
					else:
						self.wndEquip.EnableCoverButton(slotNumber)
				
				print "ENABLE_NEW_EQUIPMENT_SYSTEM", slotNumber, itemCount, getItemVNum(slotNumber)
		
		self.wndEquip.RefreshSlot()
		
		if self.wndCostume:
			self.wndCostume.RefreshCostumeSlot()

	def RefreshItemSlot(self):
		self.RefreshBagSlotWindow()
		self.RefreshEquipSlotWindow()

	def RefreshStatus(self):
		money = player.GetElk()
		#self.wndMoney.SetText(localeInfo.NumberToMoneyString(money))

	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = tooltipItem

	def SellItem(self):
		if self.sellingSlotitemIndex == player.GetItemIndex(self.sellingSlotNumber):
			if self.sellingSlotitemCount == player.GetItemCount(self.sellingSlotNumber):
				## 용혼석도 팔리게 하는 기능 추가하면서 인자 type 추가
				net.SendShopSellPacketNew(self.sellingSlotNumber, self.questionDialog.count, player.INVENTORY)
				snd.PlaySound("sound/ui/money.wav")
		self.OnCloseQuestionDialog()

	def OnDetachMetinFromItem(self):
		if None == self.questionDialog:
			return

		#net.SendItemUseToItemPacket(self.questionDialog.sourcePos, self.questionDialog.targetPos)
		self.__SendUseItemToItemPacket(self.questionDialog.sourcePos, self.questionDialog.targetPos)
		self.OnCloseQuestionDialog()

	def OnCloseQuestionDialog(self):
		if not self.questionDialog:
			return

		self.questionDialog.Close()
		self.questionDialog = None
		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

	## Slot Event
	def SelectEmptySlot(self, selectedSlotPos):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			return

		selectedSlotPos = self.__InventoryLocalSlotPosToGlobalSlotPos(selectedSlotPos)

		if mouseModule.mouseController.isAttached():

			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			attachedItemCount = mouseModule.mouseController.GetAttachedItemCount()
			attachedItemIndex = mouseModule.mouseController.GetAttachedItemIndex()
			attachedCount = mouseModule.mouseController.GetAttachedItemCount()

			if player.SLOT_TYPE_INVENTORY == attachedSlotType:
				itemCount = player.GetItemCount(attachedSlotPos)
				self.__SendMoveItemPacket(attachedSlotPos, selectedSlotPos, attachedCount)

				if item.IsRefineScroll(attachedItemIndex):
					self.wndItem.SetUseMode(False)

			elif player.SLOT_TYPE_PRIVATE_SHOP == attachedSlotType:
				mouseModule.mouseController.RunCallBack("INVENTORY")

			elif player.SLOT_TYPE_SHOP == attachedSlotType:
				net.SendShopBuyPacket(attachedSlotPos)

			elif player.SLOT_TYPE_SAFEBOX == attachedSlotType:

				if player.ITEM_MONEY == attachedItemIndex:
					net.SendSafeboxWithdrawMoneyPacket(mouseModule.mouseController.GetAttachedItemCount())
					snd.PlaySound("sound/ui/money.wav")

				else:
					net.SendSafeboxCheckoutPacket(attachedSlotPos, selectedSlotPos)

			elif player.SLOT_TYPE_MALL == attachedSlotType:
				net.SendMallCheckoutPacket(attachedSlotPos, selectedSlotPos)
			
			elif app.ENABLE_SPECIAL_STORAGE and player.SLOT_TYPE_UPGRADE_INVENTORY == attachedSlotType:
				net.SendSpecialMovePacket(player.UPGRADE_INVENTORY, attachedSlotPos, selectedSlotPos, attachedCount)

			elif app.ENABLE_SPECIAL_STORAGE and player.SLOT_TYPE_BOOK_INVENTORY == attachedSlotType:
				net.SendSpecialMovePacket(player.BOOK_INVENTORY, attachedSlotPos, selectedSlotPos, attachedCount)

			elif app.ENABLE_SPECIAL_STORAGE and player.SLOT_TYPE_STONE_INVENTORY == attachedSlotType:
				net.SendSpecialMovePacket(player.STONE_INVENTORY, attachedSlotPos, selectedSlotPos, attachedCount)
			
			elif app.ENABLE_SPECIAL_STORAGE and player.SLOT_TYPE_INVENTORY == attachedSlotType:
				chat.AppendChat(1, "yes")
				net.SendSpecialMovePacket(player.BOOK_INVENTORY, attachedSlotPos, selectedSlotPos, attachedCount, "test")
			
			mouseModule.mouseController.DeattachObject()

	def SelectItemSlot(self, itemSlotIndex):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			return

		itemSlotIndex = self.__InventoryLocalSlotPosToGlobalSlotPos(itemSlotIndex)

		if mouseModule.mouseController.isAttached():
			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			attachedItemVID = mouseModule.mouseController.GetAttachedItemIndex()
			
			if app.ENABLE_SPECIAL_STORAGE:
				if player.SLOT_TYPE_INVENTORY == attachedSlotType or player.SLOT_TYPE_STONE_INVENTORY == attachedSlotType:
					self.__DropSrcItemToDestItemInInventory(attachedItemVID, attachedSlotPos, itemSlotIndex)
			else:
				if player.SLOT_TYPE_INVENTORY == attachedSlotType:
					self.__DropSrcItemToDestItemInInventory(attachedItemVID, attachedSlotPos, itemSlotIndex)

			mouseModule.mouseController.DeattachObject()

		else:

			curCursorNum = app.GetCursor()
			if app.SELL == curCursorNum:
				self.__SellItem(itemSlotIndex)

			elif app.BUY == curCursorNum:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SHOP_BUY_INFO)

			elif app.IsPressed(app.DIK_LALT):
				link = player.GetItemLink(itemSlotIndex)
				ime.PasteString(link)

			elif app.IsPressed(app.DIK_LSHIFT):
				itemCount = player.GetItemCount(itemSlotIndex)

				if itemCount > 1:
					self.dlgPickMoney.SetTitleName(localeInfo.PICK_ITEM_TITLE)
					self.dlgPickMoney.SetAcceptEvent(ui.__mem_func__(self.OnPickItem))
					self.dlgPickMoney.Open(itemCount)
					self.dlgPickMoney.itemGlobalSlotIndex = itemSlotIndex
				#else:
					#selectedItemVNum = player.GetItemIndex(itemSlotIndex)
					#mouseModule.mouseController.AttachObject(self, player.SLOT_TYPE_INVENTORY, itemSlotIndex, selectedItemVNum)

			elif app.IsPressed(app.DIK_LCONTROL):
				itemIndex = player.GetItemIndex(itemSlotIndex)

				if True == item.CanAddToQuickSlotItem(itemIndex):
					player.RequestAddToEmptyLocalQuickSlot(player.SLOT_TYPE_INVENTORY, itemSlotIndex)
				else:
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.QUICKSLOT_REGISTER_DISABLE_ITEM)

			else:
				selectedItemVNum = player.GetItemIndex(itemSlotIndex)
				itemCount = player.GetItemCount(itemSlotIndex)
				mouseModule.mouseController.AttachObject(self, player.SLOT_TYPE_INVENTORY, itemSlotIndex, selectedItemVNum, itemCount)

				if self.__IsUsableItemToItem(selectedItemVNum, itemSlotIndex):
					self.wndItem.SetUseMode(True)
				else:
					self.wndItem.SetUseMode(False)

				snd.PlaySound("sound/ui/pick.wav")

	def UseTransportBox(self):
		self.__SendUseItemToItemPacket(self.questionDialog.src, self.questionDialog.dst)
		self.OnCloseQuestionDialog()
	
	def UseProtein(self):
		self.__SendUseItemToItemPacket(self.questionDialog.src, self.questionDialog.dst)
		self.OnCloseQuestionDialog()				
					
	def __DropSrcItemToDestItemInInventory(self, srcItemVID, srcItemSlotPos, dstItemSlotPos):
		if app.ENABLE_SPECIAL_STORAGE:
			if srcItemSlotPos == dstItemSlotPos and not item.IsMetin(srcItemVID):
				return
		else:
			if srcItemSlotPos == dstItemSlotPos:
				return

		if srcItemVID >= 55701 and srcItemVID <= 55708 and player.GetItemIndex(dstItemSlotPos) == 55002:
			self.questionDialog = uiCommon.QuestionDialog()
			self.questionDialog.SetText("Vrei sa adaugi insotitorul in cutia de transport?")
			self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.UseTransportBox))
			self.questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
			self.questionDialog.Open()
			self.questionDialog.src = srcItemSlotPos
			self.questionDialog.dst = dstItemSlotPos
			
		if srcItemVID == 55001 and player.GetItemIndex(dstItemSlotPos) >= 55701 and player.GetItemIndex(dstItemSlotPos) <= 55708:
			self.questionDialog = uiCommon.QuestionDialog()
			self.questionDialog.SetText("Vrei sa hranesti insotitorul?")
			self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.UseProtein))
			self.questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
			self.questionDialog.Open()
			self.questionDialog.src = srcItemSlotPos
			self.questionDialog.dst = dstItemSlotPos			
			
		if srcItemVID == 71051 and player.GetItemIndex(dstItemSlotPos) >= 70500 and player.GetItemIndex(dstItemSlotPos) <= 70509:
			self.questionDialog = uiCommon.QuestionDialog()
			self.questionDialog.SetText("Vrei sa adaugi sufletele pe acest item?")
			self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.UseProtein))
			self.questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
			self.questionDialog.Open()
			self.questionDialog.src = srcItemSlotPos
			self.questionDialog.dst = dstItemSlotPos			
			
		if srcItemVID == 71051 and player.GetItemIndex(dstItemSlotPos) >= 9600 and player.GetItemIndex(dstItemSlotPos) <= 10770:
			self.questionDialog = uiCommon.QuestionDialog()
			self.questionDialog.SetText("Vrei sa adaugi sufletele pe acest item?")
			self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.UseProtein))
			self.questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
			self.questionDialog.Open()
			self.questionDialog.src = srcItemSlotPos
			self.questionDialog.dst = dstItemSlotPos			
			
		if srcItemVID == 71052 and player.GetItemIndex(dstItemSlotPos) >= 70500 and player.GetItemIndex(dstItemSlotPos) <= 70509:
			self.questionDialog = uiCommon.QuestionDialog()
			self.questionDialog.SetText("Vrei sa adaugi sufletele pe acest item?")
			self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.UseProtein))
			self.questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
			self.questionDialog.Open()
			self.questionDialog.src = srcItemSlotPos
			self.questionDialog.dst = dstItemSlotPos			
			
		if srcItemVID == 71052 and player.GetItemIndex(dstItemSlotPos) >= 9600 and player.GetItemIndex(dstItemSlotPos) <= 10770:
			self.questionDialog = uiCommon.QuestionDialog()
			self.questionDialog.SetText("Vrei sa adaugi sufletele pe acest item?")
			self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.UseProtein))
			self.questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
			self.questionDialog.Open()
			self.questionDialog.src = srcItemSlotPos
			self.questionDialog.dst = dstItemSlotPos			
			
		if srcItemVID >= 91021 and srcItemVID <= 91029 and player.GetItemIndex(dstItemSlotPos) >= 91010 and player.GetItemIndex(dstItemSlotPos) <= 91020:
			self.questionDialog = uiCommon.QuestionDialog()
			self.questionDialog.SetText("Sigur vrei sa folosesti acest item?")
			self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.UseProtein))
			self.questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
			self.questionDialog.Open()
			self.questionDialog.src = srcItemSlotPos
			self.questionDialog.dst = dstItemSlotPos	
			
		# cyh itemseal 2013 11 08
		if app.ENABLE_SEALBIND_SYSTEM and item.IsSealScroll(srcItemVID):
			self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)

		elif item.IsRefineScroll(srcItemVID):
			self.RefineItem(srcItemSlotPos, dstItemSlotPos)
			self.wndItem.SetUseMode(False)

		elif item.IsMetin(srcItemVID):
			self.AttachMetinToItem(srcItemSlotPos, dstItemSlotPos)

		elif item.IsDetachScroll(srcItemVID):
			self.DetachMetinFromItem(srcItemSlotPos, dstItemSlotPos)

		elif item.IsKey(srcItemVID):
			self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)

		elif (player.GetItemFlags(srcItemSlotPos) & ITEM_FLAG_APPLICABLE) == ITEM_FLAG_APPLICABLE:
			self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)

		elif item.GetUseType(srcItemVID) in self.USE_TYPE_TUPLE:
			self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)

		else:
			#snd.PlaySound("sound/ui/drop.wav")

			## 이동시킨 곳이 장착 슬롯일 경우 아이템을 사용해서 장착 시킨다 - [levites]
			if player.IsEquipmentSlot(dstItemSlotPos):

				## 들고 있는 아이템이 장비일때만
				if item.IsEquipmentVID(srcItemVID):
					self.__UseItem(srcItemSlotPos)

			else:
				self.__SendMoveItemPacket(srcItemSlotPos, dstItemSlotPos, 0)
				#net.SendItemMovePacket(srcItemSlotPos, dstItemSlotPos, 0)

	def __SellItem(self, itemSlotPos):
		if not player.IsEquipmentSlot(itemSlotPos):
			self.sellingSlotNumber = itemSlotPos
			itemIndex = player.GetItemIndex(itemSlotPos)
			itemCount = player.GetItemCount(itemSlotPos)


			self.sellingSlotitemIndex = itemIndex
			self.sellingSlotitemCount = itemCount

			item.SelectItem(itemIndex)
			## 안티 플레그 검사 빠져서 추가
			## 20140220
			if item.IsAntiFlag(item.ANTIFLAG_SELL):
				popup = uiCommon.PopupDialog()
				popup.SetText(localeInfo.SHOP_CANNOT_SELL_ITEM)
				popup.SetAcceptEvent(self.__OnClosePopupDialog)
				popup.Open()
				self.popup = popup
				return

			itemPrice = item.GetISellItemPrice()

			if item.Is1GoldItem():
				itemPrice = itemCount / itemPrice / 5
			else:
				itemPrice = itemPrice * itemCount / 5

			item.GetItemName(itemIndex)
			itemName = item.GetItemName()

			self.questionDialog = uiCommon.QuestionDialog()
			self.questionDialog.SetText(localeInfo.DO_YOU_SELL_ITEM(itemName, itemCount, itemPrice))
			self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.SellItem))
			self.questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
			self.questionDialog.Open()
			self.questionDialog.count = itemCount

			constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)

	def __OnClosePopupDialog(self):
		self.pop = None

	def RefineItem(self, scrollSlotPos, targetSlotPos):

		scrollIndex = player.GetItemIndex(scrollSlotPos)
		targetIndex = player.GetItemIndex(targetSlotPos)

		if player.REFINE_OK != player.CanRefine(scrollIndex, targetSlotPos):
			return

		###########################################################
		self.__SendUseItemToItemPacket(scrollSlotPos, targetSlotPos)
		#net.SendItemUseToItemPacket(scrollSlotPos, targetSlotPos)
		return
		###########################################################

		###########################################################
		#net.SendRequestRefineInfoPacket(targetSlotPos)
		#return
		###########################################################

		result = player.CanRefine(scrollIndex, targetSlotPos)

		if player.REFINE_ALREADY_MAX_SOCKET_COUNT == result:
			#snd.PlaySound("sound/ui/jaeryun_fail.wav")
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_NO_MORE_SOCKET)

		elif player.REFINE_NEED_MORE_GOOD_SCROLL == result:
			#snd.PlaySound("sound/ui/jaeryun_fail.wav")
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_NEED_BETTER_SCROLL)

		elif player.REFINE_CANT_MAKE_SOCKET_ITEM == result:
			#snd.PlaySound("sound/ui/jaeryun_fail.wav")
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_SOCKET_DISABLE_ITEM)

		elif player.REFINE_NOT_NEXT_GRADE_ITEM == result:
			#snd.PlaySound("sound/ui/jaeryun_fail.wav")
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_UPGRADE_DISABLE_ITEM)

		elif player.REFINE_CANT_REFINE_METIN_TO_EQUIPMENT == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_EQUIP_ITEM)

		if player.REFINE_OK != result:
			return

		self.refineDialog.Open(scrollSlotPos, targetSlotPos)

	def DetachMetinFromItem(self, scrollSlotPos, targetSlotPos):
		scrollIndex = player.GetItemIndex(scrollSlotPos)
		targetIndex = player.GetItemIndex(targetSlotPos)
		if app.ENABLE_SASH_SYSTEM and app.ENABLE_CHANGELOOK_SYSTEM:
			if not player.CanDetach(scrollIndex, targetSlotPos):
				item.SelectItem(scrollIndex)
				if item.GetValue(0) == sash.CLEAN_ATTR_VALUE0:
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SASH_FAILURE_CLEAN)
				elif item.GetValue(0) == changelook.CLEAN_ATTR_VALUE0:
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CHANGE_LOOK_FAILURE_CLEAN)
				else:
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_METIN_INSEPARABLE_ITEM)
				
				return
		elif app.ENABLE_SASH_SYSTEM:
			if not player.CanDetach(scrollIndex, targetSlotPos):
				item.SelectItem(scrollIndex)
				if item.GetValue(0) == sash.CLEAN_ATTR_VALUE0:
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SASH_FAILURE_CLEAN)
				else:
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_METIN_INSEPARABLE_ITEM)

				return
		elif app.ENABLE_CHANGELOOK_SYSTEM:
			if not player.CanDetach(scrollIndex, targetSlotPos):
				item.SelectItem(scrollIndex)
				if item.GetValue(0) == changelook.CLEAN_ATTR_VALUE0:
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CHANGE_LOOK_FAILURE_CLEAN)
				else:
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_METIN_INSEPARABLE_ITEM)

				return
		else:
			if not player.CanDetach(scrollIndex, targetSlotPos):
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_METIN_INSEPARABLE_ITEM)
				return
		
		self.questionDialog = uiCommon.QuestionDialog()
		self.questionDialog.SetText(localeInfo.REFINE_DO_YOU_SEPARATE_METIN)
		if app.ENABLE_SASH_SYSTEM:
			item.SelectItem(targetIndex)
			if item.GetItemType() == item.ITEM_TYPE_COSTUME and item.GetItemSubType() == item.COSTUME_TYPE_SASH:
				item.SelectItem(scrollIndex)
				if item.GetValue(0) == sash.CLEAN_ATTR_VALUE0:
					self.questionDialog.SetText(localeInfo.SASH_DO_YOU_CLEAN)

		if app.ENABLE_CHANGELOOK_SYSTEM:
			item.SelectItem(targetIndex)
			if item.GetItemType() == item.ITEM_TYPE_WEAPON or item.GetItemType() == item.ITEM_TYPE_ARMOR or item.GetItemType() == item.ITEM_TYPE_COSTUME:
				item.SelectItem(scrollIndex)
				if item.GetValue(0) == changelook.CLEAN_ATTR_VALUE0:
					self.questionDialog.SetText(localeInfo.CHANGE_LOOK_DO_YOU_CLEAN)

		self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.OnDetachMetinFromItem))
		self.questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
		self.questionDialog.Open()
		self.questionDialog.sourcePos = scrollSlotPos
		self.questionDialog.targetPos = targetSlotPos
		
	def AttachMetinToItem(self, metinSlotPos, targetSlotPos):
		if app.ENABLE_SPECIAL_STORAGE:
			metinIndex = player.GetItemIndex(player.STONE_INVENTORY, metinSlotPos)
		else:
			metinIndex = player.GetItemIndex(metinSlotPos)
		targetIndex = player.GetItemIndex(targetSlotPos)

		item.SelectItem(metinIndex)
		itemName = item.GetItemName()

		result = player.CanAttachMetin(metinIndex, targetSlotPos)

		if player.ATTACH_METIN_NOT_MATCHABLE_ITEM == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_CAN_NOT_ATTACH(itemName))

		if player.ATTACH_METIN_NO_MATCHABLE_SOCKET == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_NO_SOCKET(itemName))

		elif player.ATTACH_METIN_NOT_EXIST_GOLD_SOCKET == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_NO_GOLD_SOCKET(itemName))

		elif player.ATTACH_METIN_CANT_ATTACH_TO_EQUIPMENT == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_EQUIP_ITEM)

		if player.ATTACH_METIN_OK != result:
			return

		self.attachMetinDialog.Open(metinSlotPos, targetSlotPos)



	def OverOutItem(self):
		self.wndItem.SetUsableItem(False)
		if None != self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def OverInItem(self, overSlotPos):
		overSlotPos = self.__InventoryLocalSlotPosToGlobalSlotPos(overSlotPos)
		self.wndItem.SetUsableItem(False)

		if mouseModule.mouseController.isAttached():
			attachedItemType = mouseModule.mouseController.GetAttachedType()
			if app.ENABLE_SPECIAL_STORAGE:
				if player.SLOT_TYPE_INVENTORY == attachedItemType or player.SLOT_TYPE_STONE_INVENTORY == attachedItemType:
					attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
					attachedItemVNum = mouseModule.mouseController.GetAttachedItemIndex()
	
					if self.__CanUseSrcItemToDstItem(attachedItemVNum, attachedSlotPos, overSlotPos):
						self.wndItem.SetUsableItem(True)
						self.wndItem.SetUseMode(True)
						self.ShowToolTip(overSlotPos)
						return
			else:
				if player.SLOT_TYPE_INVENTORY == attachedItemType:
					attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
					attachedItemVNum = mouseModule.mouseController.GetAttachedItemIndex()
	
					if self.__CanUseSrcItemToDstItem(attachedItemVNum, attachedSlotPos, overSlotPos):
						self.wndItem.SetUsableItem(True)
						self.ShowToolTip(overSlotPos)
						return
	
				if self.__CanUseSrcItemToDstItem(attachedItemVNum, attachedSlotPos, overSlotPos):
					self.wndItem.SetUsableItem(True)
					self.ShowToolTip(overSlotPos)
					return

		self.ShowToolTip(overSlotPos)


	def __IsUsableItemToItem(self, srcItemVNum, srcSlotPos):
		"다른 아이템에 사용할 수 있는 아이템인가?"

		if srcItemVNum >= 55701 and srcItemVNum <= 55708:
			return True
		
		if srcItemVNum == 55001:
			return True		
		
		if srcItemVNum == 71051:
			return True		
		
		if srcItemVNum == 71052:
			return True		
		
		if srcItemVNum >= 91021 and srcItemVNum <= 91029:
			return True		
				
		if item.IsRefineScroll(srcItemVNum):
			return True
		elif item.IsMetin(srcItemVNum):
			return True
		elif item.IsDetachScroll(srcItemVNum):
			return True
		elif item.IsKey(srcItemVNum):
			return True
		elif (player.GetItemFlags(srcSlotPos) & ITEM_FLAG_APPLICABLE) == ITEM_FLAG_APPLICABLE:
			return True
		else:
			if item.GetUseType(srcItemVNum) in self.USE_TYPE_TUPLE:
				return True

		return False

	def __CanUseSrcItemToDstItem(self, srcItemVNum, srcSlotPos, dstSlotPos):
		"대상 아이템에 사용할 수 있는가?"

		if srcItemVNum >= 55701 and  srcItemVNum <= 55708 and player.GetItemIndex(dstSlotPos) == 55002:			
			return True		
		
		if srcItemVNum == 55001 and player.GetItemIndex(dstSlotPos) >= 55701 and player.GetItemIndex(dstSlotPos) <= 55708:			
			return True		
		
		if srcItemVNum == 71051 and player.GetItemIndex(dstSlotPos) >= 70500 and player.GetItemIndex(dstSlotPos) <= 70509:	
			return True
			
		if srcItemVNum == 71051 and player.GetItemIndex(dstSlotPos) >= 9600 and player.GetItemIndex(dstSlotPos) <= 10770:	
			return True
		
		if srcItemVNum == 71052 and player.GetItemIndex(dstSlotPos) >= 70500 and player.GetItemIndex(dstSlotPos) <= 70509:	
			return True
		
		if srcItemVNum == 71052 and player.GetItemIndex(dstSlotPos) >= 9600 and player.GetItemIndex(dstSlotPos) <= 10770:	
			return True
		
		if srcItemVNum >= 91021 and  srcItemVNum <= 91029 and player.GetItemIndex(dstSlotPos) >= 91010 and player.GetItemIndex(dstSlotPos) <= 91020:	
			return True
		
		if app.ENABLE_SPECIAL_STORAGE:
			if srcSlotPos == dstSlotPos and not item.IsMetin(srcItemVNum):
				return False
		else:
			if srcSlotPos == dstSlotPos:
				return False

		if item.IsRefineScroll(srcItemVNum):
			if player.REFINE_OK == player.CanRefine(srcItemVNum, dstSlotPos):
				return True
		elif item.IsMetin(srcItemVNum):
			if player.ATTACH_METIN_OK == player.CanAttachMetin(srcItemVNum, dstSlotPos):
				return True
		elif item.IsDetachScroll(srcItemVNum):
			if player.DETACH_METIN_OK == player.CanDetach(srcItemVNum, dstSlotPos):
				return True
		elif item.IsKey(srcItemVNum):
			if player.CanUnlock(srcItemVNum, dstSlotPos):
				return True

		elif (player.GetItemFlags(srcSlotPos) & ITEM_FLAG_APPLICABLE) == ITEM_FLAG_APPLICABLE:
			return True

		else:
			useType=item.GetUseType(srcItemVNum)

			if "USE_CLEAN_SOCKET" == useType:
				if self.__CanCleanBrokenMetinStone(dstSlotPos):
					return True
			elif "USE_CHANGE_ATTRIBUTE" == useType:
				if self.__CanChangeItemAttrList(dstSlotPos):
					return True
			elif "USE_ADD_ATTRIBUTE" == useType:
				if self.__CanAddItemAttr(dstSlotPos):
					return True
			elif "USE_ADD_ATTRIBUTE2" == useType:
				if self.__CanAddItemAttr(dstSlotPos):
					return True
			elif "USE_ADD_ACCESSORY_SOCKET" == useType:
				if self.__CanAddAccessorySocket(dstSlotPos):
					return True
			elif "USE_PUT_INTO_ACCESSORY_SOCKET" == useType:
				if self.__CanPutAccessorySocket(dstSlotPos, srcItemVNum):
					return True
			elif "USE_PUT_INTO_BELT_SOCKET" == useType:
				dstItemVNum = player.GetItemIndex(dstSlotPos)
				print "USE_PUT_INTO_BELT_SOCKET", srcItemVNum, dstItemVNum
			elif useType == "USE_COSTUME_ENCHANT" or useType == "USE_COSTUME_TRANSFORM":
				if not app.ENABLE_COSTUME_ATTR_SYSTEM:
					return FALSE
				
				dstItemVNum = player.GetItemIndex(dstSlotPos)
				item.SelectItem(dstItemVNum)
				if item.GetItemType() == item.ITEM_TYPE_COSTUME:
					return TRUE

				item.SelectItem(dstItemVNum)

				if item.ITEM_TYPE_BELT == item.GetItemType():
					return True

		return False

	def __CanCleanBrokenMetinStone(self, dstSlotPos):
		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)

		if item.ITEM_TYPE_WEAPON != item.GetItemType():
			return False

		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			if player.GetItemMetinSocket(dstSlotPos, i) == constInfo.ERROR_METIN_STONE:
				return True

		return False

	def __CanChangeItemAttrList(self, dstSlotPos):
		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)

		if not item.GetItemType() in (item.ITEM_TYPE_WEAPON, item.ITEM_TYPE_ARMOR, item.ITEM_TYPE_RING):
			return False

		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			if player.GetItemAttribute(dstSlotPos, i) != 0:
				return True

		return False

	def __CanAddSoulToItem(self, dstSlotPos):
		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)

		if item.GetItemType() == item.ITEM_TYPE_ARMOR:
			return True

		return False

	def __CanPutAccessorySocket(self, dstSlotPos, mtrlVnum):
		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)

		if item.GetItemType() != item.ITEM_TYPE_ARMOR:
			return False

		if not item.GetItemSubType() in (item.ARMOR_WRIST, item.ARMOR_NECK, item.ARMOR_EAR):
			return False

		curCount = player.GetItemMetinSocket(dstSlotPos, 0)
		maxCount = player.GetItemMetinSocket(dstSlotPos, 1)

		if mtrlVnum != constInfo.GET_ACCESSORY_MATERIAL_VNUM(dstItemVNum, item.GetItemSubType()):
			return False

		if curCount>=maxCount:
			return False

		return True

	def __CanAddAccessorySocket(self, dstSlotPos):
		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)

		if item.GetItemType() != item.ITEM_TYPE_ARMOR:
			return False

		if not item.GetItemSubType() in (item.ARMOR_WRIST, item.ARMOR_NECK, item.ARMOR_EAR):
			return False

		curCount = player.GetItemMetinSocket(dstSlotPos, 0)
		maxCount = player.GetItemMetinSocket(dstSlotPos, 1)

		ACCESSORY_SOCKET_MAX_SIZE = 3
		if maxCount >= ACCESSORY_SOCKET_MAX_SIZE:
			return False

		return True

	def __CanAddItemAttr(self, dstSlotPos):
		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)

		if not item.GetItemType() in (item.ITEM_TYPE_WEAPON, item.ITEM_TYPE_ARMOR, item.ITEM_TYPE_RING):
			return False

		attrCount = 0
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			if player.GetItemAttribute(dstSlotPos, i) != 0:
				attrCount += 1

		if attrCount<4:
			return True

		return False

	def ShowToolTip(self, slotIndex):
		if None != self.tooltipItem:
			self.tooltipItem.SetInventoryItem(slotIndex)

	def OnTop(self):
		if None != self.tooltipItem:
			self.tooltipItem.SetTop()
		if app.WJ_ENABLE_TRADABLE_ICON:
			map(lambda wnd:wnd.RefreshLockedSlot(), self.bindWnds)
			self.RefreshMarkSlots()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def UseItemSlot(self, slotIndex):
		curCursorNum = app.GetCursor()
		if app.SELL == curCursorNum:
			return
			

		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS():
			return

		slotIndex = self.__InventoryLocalSlotPosToGlobalSlotPos(slotIndex)
							
		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			if self.wndDragonSoulRefine.IsShow():
				self.wndDragonSoulRefine.AutoSetItem((player.INVENTORY, slotIndex), 1)
				return
		
		if app.ENABLE_SASH_SYSTEM:
			if self.isShowSashWindow():
				sash.Add(player.INVENTORY, slotIndex, 255)
				return

		if app.ENABLE_CHANGELOOK_SYSTEM:
			if self.isShowChangeLookWindow():
				changelook.Add(player.INVENTORY, slotIndex, 255)
				return

		self.__UseItem(slotIndex)
		mouseModule.mouseController.DeattachObject()
		self.OverOutItem()

	def __UseItem(self, slotIndex):
		ItemVNum = player.GetItemIndex(slotIndex)
		item.SelectItem(ItemVNum)
		
		if ItemVNum == 39116:
			self.searchbtn2()

		if ItemVNum == 39117:
			self.searchbtn2()
			
		if item.IsFlag(item.ITEM_FLAG_CONFIRM_WHEN_USE):
			net.SendItemUsePacket(slotIndex)
		elif player.GetItemTypeBySlot(slotIndex) == item.ITEM_TYPE_GIFTBOX:
			if app.ENABLE_SHOW_CHEST_DROP:
				if self.interface:
					if self.interface.dlgChestDrop:
						if not self.interface.dlgChestDrop.IsShow():
							self.interface.dlgChestDrop.Open(slotIndex)
							net.SendChestDropInfo(slotIndex)
		elif player.GetItemTypeBySlot(slotIndex) == item.ITEM_TYPE_GACHA:
			if app.ENABLE_SHOW_CHEST_DROP:
				if self.interface:
					if self.interface.dlgChestDrop:
						if not self.interface.dlgChestDrop.IsShow():
							self.interface.dlgChestDrop.Open(slotIndex)
							net.SendChestDropInfo(slotIndex)
		else:
			# self.__SendUseItemPacket(slotIndex)
			net.SendItemUsePacket(slotIndex)

	def searchbtn2(self):	
		self.testasd = uiSearchShop.ShopSearch()
		self.testasd.Show() 
			
	def __UseItemQuestionDialog_OnCancel(self):
		self.OnCloseQuestionDialog()

	def __UseItemQuestionDialog_OnAccept(self):
		self.__SendUseItemPacket(self.questionDialog.slotIndex)
		self.OnCloseQuestionDialog()

	def __SendUseItemToItemPacket(self, srcSlotPos, dstSlotPos):
		# 개인상점 열고 있는 동안 아이템 사용 방지
		if uiPrivateShopBuilder.IsBuildingPrivateShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.USE_ITEM_FAILURE_PRIVATE_SHOP)
			return

		net.SendItemUseToItemPacket(srcSlotPos, dstSlotPos)

	def __SendUseItemPacket(self, slotPos):
		# 개인상점 열고 있는 동안 아이템 사용 방지
		if uiPrivateShopBuilder.IsBuildingPrivateShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.USE_ITEM_FAILURE_PRIVATE_SHOP)
			return

		net.SendItemUsePacket(slotPos)

	def __SendMoveItemPacket(self, srcSlotPos, dstSlotPos, srcItemCount):
		# 개인상점 열고 있는 동안 아이템 사용 방지
		if uiPrivateShopBuilder.IsBuildingPrivateShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MOVE_ITEM_FAILURE_PRIVATE_SHOP)
			return

		net.SendItemMovePacket(srcSlotPos, dstSlotPos, srcItemCount)

	def SetDragonSoulRefineWindow(self, wndDragonSoulRefine):
		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			self.wndDragonSoulRefine = wndDragonSoulRefine
			
	if app.ENABLE_SASH_SYSTEM:
		def SetSashWindow(self, wndSashCombine, wndSashAbsorption):
			self.wndSashCombine = wndSashCombine
			self.wndSashAbsorption = wndSashAbsorption

		def isShowSashWindow(self):
			if self.wndSashCombine:
				if self.wndSashCombine.IsShow():
					return 1

			if self.wndSashAbsorption:
				if self.wndSashAbsorption.IsShow():
					return 1
			
			return 0
			
	if app.ENABLE_CHANGELOOK_SYSTEM:
		def SetChangeLookWindow(self, wndChangeLook):
			self.wndChangeLook = wndChangeLook

		def isShowChangeLookWindow(self):
			if self.wndChangeLook:
				if self.wndChangeLook.IsShow():
					return 1

			return 0

	def OnMoveWindow(self, x, y):
#		print "Inventory Global Pos : ", self.GetGlobalPosition()
		if self.wndBelt:
#			print "Belt Global Pos : ", self.wndBelt.GetGlobalPosition()
			self.wndBelt.AdjustPositionAndSize()
		if app.ENABLE_BIOLOG_SYSTEM:
			if self.wndCollect:
				self.wndCollect.AdjustPositionAndSize()

