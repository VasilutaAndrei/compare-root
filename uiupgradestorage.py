import ui
import mouseModule
import player
import net
import snd
import upgradeStorage
import chat
import app
import localeInfo
import uiScriptLocale
import ime
import uiPickMoney

class UpgradeItemsStorageWindow(ui.ScriptWindow):

	BOX_WIDTH = 176

	dlgPickMoney = None

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.tooltipItem = None
		self.sellingSlotNumber = -1
		self.pageButtonList = []
		self.curPageIndex = 0
		self.isLoaded = 0
		self.AttachedItemCount = 0
		# self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)
		upgradeStorage.ClearVector()

	def Open(self):
		self.__LoadWindow()
		self.ShowWindow()
		ui.ScriptWindow.Show(self)		

	def Destroy(self):
		upgradeStorage.ClearVector()
		self.ClearDictionary()

		self.tooltipItem = None
		self.wndBoard = None
		self.wndItem = None

		self.dlgPickMoney.Destroy()
		self.dlgPickMoney = None

		self.pageButtonList = []

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1

		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "UIScript/UpgradeItemsStorageWindow.py")

		from _weakref import proxy

		## Item
		wndItem = ui.GridSlotWindow()
		wndItem.SetParent(self)
		wndItem.SetPosition(8, 35)
		wndItem.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySlot))
		wndItem.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectItemSlot))
		wndItem.SetUnselectItemSlotEvent(ui.__mem_func__(self.UseItemSlot))
		wndItem.SetUseSlotEvent(ui.__mem_func__(self.UseItemSlot))
		wndItem.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		wndItem.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
		wndItem.Show()

		## Close Button
		self.GetChild("TitleBar").SetCloseEvent(ui.__mem_func__(self.Close))
		self.GetChild("ExitButton").SetEvent(ui.__mem_func__(self.Close))

		self.wndItem = wndItem
		self.wndBoard = self.GetChild("board")

		dlgPickMoney = uiPickMoney.PickMoneyDialog()
		dlgPickMoney.LoadDialog()
		dlgPickMoney.Hide()
		self.dlgPickMoney = dlgPickMoney

		## Initialize
		self.SetTableSize(2)

	def ShowWindow(self):
		self.SetTableSize(2)
		self.Show()

	def __MakePageButton(self, pageCount):

		self.curPageIndex = 0
		self.pageButtonList = []

		text = "I"
		pos = -int(float(pageCount-1)/2 * 52)
		for i in xrange(pageCount):
			button = ui.RadioButton()
			button.SetParent(self)
			button.SetUpVisual("d:/ymir work/ui/game/windows/tab_button_middle_01.sub")
			button.SetOverVisual("d:/ymir work/ui/game/windows/tab_button_middle_02.sub")
			button.SetDownVisual("d:/ymir work/ui/game/windows/tab_button_middle_03.sub")
			button.SetWindowHorizontalAlignCenter()
			button.SetWindowVerticalAlignBottom()
			button.SetPosition(pos, 75)
			button.SetText(text)
			button.SetEvent(lambda arg=i: self.SelectPage(arg))
			button.Show()
			self.pageButtonList.append(button)

			pos += 52
			text += "I"

		self.pageButtonList[0].Down()

	def SelectPage(self, index):

		self.curPageIndex = index

		for btn in self.pageButtonList:
			btn.SetUp()

		self.pageButtonList[index].Down()
		self.RefreshUpgradeItemsStorage()

	def __LocalPosToGlobalPos(self, local):
		return self.curPageIndex*upgradeStorage.UPGRADE_ITEMS_STORAGE_PAGE_SIZE + local

	def SetTableSize(self, size):
		size = upgradeStorage.UPGRADE_ITEMS_STORAGE_SLOT_Y_COUNT

		self.__MakePageButton(2)

		self.wndItem.ArrangeSlot(0, upgradeStorage.UPGRADE_ITEMS_STORAGE_SLOT_X_COUNT, size, 32, 32, 0, 0)
		self.wndItem.RefreshSlot()
		self.wndItem.SetSlotBaseImage("d:/ymir work/ui/public/Slot_Base.sub", 1.0, 1.0, 1.0, 1.0)

		wnd_height = 130 + 32 * size
		self.wndBoard.SetSize(self.BOX_WIDTH, wnd_height)
		self.SetSize(self.BOX_WIDTH, wnd_height)
		self.UpdateRect()

	def RefreshUpgradeItemsStorage(self):
		getItemID=upgradeStorage.GetItemID
		getItemCount=upgradeStorage.GetItemCount
		setItemID=self.wndItem.SetItemSlot

		for i in xrange(upgradeStorage.UPGRADE_ITEMS_STORAGE_PAGE_SIZE):
			slotIndex = self.__LocalPosToGlobalPos(i)
			itemCount = getItemCount(slotIndex)
			if itemCount <= 1:
				itemCount = 0
			setItemID(i, getItemID(slotIndex), itemCount)

		self.wndItem.RefreshSlot()

	def SetItemToolTip(self, tooltip):
		self.tooltipItem = tooltip

	def Close(self):
		self.Hide()
		self.OverOutItem()
		if self.dlgPickMoney:
			self.dlgPickMoney.Close()
		else:
			self.dlgPickMoney = None
		upgradeStorage.ClearVector()

	## Slot Event
	def SelectEmptySlot(self, selectedSlotPos):

		selectedSlotPos = self.__LocalPosToGlobalPos(selectedSlotPos)

		if mouseModule.mouseController.isAttached():

			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()

			if player.SLOT_TYPE_UPGRADE_ITEMS_STORAGE == attachedSlotType:
				net.SendUpgradeItemsStorageItemMovePacket(attachedSlotPos, selectedSlotPos, self.AttachedItemCount)
				self.AttachedItemCount = 0
			else:
				attachedInvenType = player.SlotTypeToInvenType(attachedSlotType)
				if player.RESERVED_WINDOW == attachedInvenType:
					return

				net.SendUpgradeItemsStorageCheckinPacket(attachedInvenType, attachedSlotPos, selectedSlotPos)

			mouseModule.mouseController.DeattachObject()

	def SelectItemSlot(self, selectedSlotPos):

		selectedSlotPos = self.__LocalPosToGlobalPos(selectedSlotPos)

		if mouseModule.mouseController.isAttached():

			attachedSlotType = mouseModule.mouseController.GetAttachedType()

			if player.SLOT_TYPE_INVENTORY == attachedSlotType:
				attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			elif player.SLOT_TYPE_UPGRADE_ITEMS_STORAGE == attachedSlotType:
				attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
				net.SendUpgradeItemsStorageItemMovePacket(attachedSlotPos, selectedSlotPos, 0)

			mouseModule.mouseController.DeattachObject()

		else:

			curCursorNum = app.GetCursor()
			if app.SELL == curCursorNum:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.UPGRADE_ITEMS_STORAGE_SELL_DISABLE_SAFEITEM)

			elif app.BUY == curCursorNum:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SHOP_BUY_INFO)

			elif app.IsPressed(app.DIK_LALT):
				link = upgradeStorage.GetItemLink(selectedSlotPos)
				ime.PasteString(link)

			elif app.IsPressed(app.DIK_LSHIFT):
				itemCount = upgradeStorage.GetItemCount(selectedSlotPos)

				if itemCount > 1:
					self.dlgPickMoney.SetTitleName(localeInfo.PICK_ITEM_TITLE)
					self.dlgPickMoney.SetAcceptEvent(ui.__mem_func__(self.OnPickItem))
					self.dlgPickMoney.Open(itemCount)
					self.dlgPickMoney.itemGlobalSlotIndex = selectedSlotPos

			else:
				selectedItemID = upgradeStorage.GetItemID(selectedSlotPos)
				itemCount = player.GetItemCount(selectedSlotPos)
				mouseModule.mouseController.AttachObject(self, player.SLOT_TYPE_UPGRADE_ITEMS_STORAGE, selectedSlotPos, selectedItemID, itemCount)

				snd.PlaySound("sound/ui/pick.wav")

	def OnPickItem(self, count):
		itemSlotIndex = self.dlgPickMoney.itemGlobalSlotIndex
		selectedItemVNum = upgradeStorage.GetItemID(itemSlotIndex)
		mouseModule.mouseController.AttachObject(self, player.SLOT_TYPE_UPGRADE_ITEMS_STORAGE, itemSlotIndex, selectedItemVNum, count)
		self.AttachedItemCount = count

	def UseItemSlot(self, attachedSlotPos):
		attachedSlotPos = self.__LocalPosToGlobalPos(attachedSlotPos)
		for i in xrange(player.INVENTORY_PAGE_SIZE):
			net.SendUpgradeItemsStorageCheckoutPacket(attachedSlotPos, i)

	def __ShowToolTip(self, slotIndex):
		if self.tooltipItem:
			self.tooltipItem.SetUpgradeItemsStorageItem(slotIndex)

	def OverInItem(self, slotIndex):
		slotIndex = self.__LocalPosToGlobalPos(slotIndex)
		self.__ShowToolTip(slotIndex)

	def OverOutItem(self):
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def OnPressEscapeKey(self):
		self.Close()
		return True
