import player
import exchange
import net
import localeInfo
import chat
import item

import ui
import mouseModule
import uiPickMoney
import wndMgr
import app

###################################################################################################
## Exchange
class ExchangeDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.TitleName = 0
		self.tooltipItem = 0
		self.xStart = 0
		self.yStart = 0
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.interface = 0
			self.wndInventory = 0
			self.lockedItems = {i:(-1,-1) for i in range(exchange.EXCHANGE_ITEM_MAX_NUM)}

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def LoadDialog(self):
		PythonScriptLoader = ui.PythonScriptLoader()
		PythonScriptLoader.LoadScriptFile(self, "UIScript/exchangedialog.py")

		## Owner
		self.OwnerSlot = self.GetChild("Owner_Slot")
		self.OwnerSlot.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectOwnerEmptySlot))
		self.OwnerSlot.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectOwnerItemSlot))
		self.OwnerSlot.SetOverInItemEvent(ui.__mem_func__(self.OverInOwnerItem))
		self.OwnerSlot.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
		self.OwnerMoney = self.GetChild("Owner_Money_Value")
		self.OwnerAcceptLight = self.GetChild("Owner_Accept_Light")
		self.OwnerAcceptLight.Disable()
		self.OwnerMoneyButton = self.GetChild("Owner_Money")
		self.OwnerMoneyButton.SetEvent(ui.__mem_func__(self.OpenPickMoneyDialog))

		## Target
		self.TargetSlot = self.GetChild("Target_Slot")
		self.TargetSlot.SetOverInItemEvent(ui.__mem_func__(self.OverInTargetItem))
		self.TargetSlot.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
		self.TargetMoney = self.GetChild("Target_Money_Value")
		self.TargetAcceptLight = self.GetChild("Target_Accept_Light")
		self.TargetAcceptLight.Disable()

		## PickMoneyDialog
		dlgPickMoney = uiPickMoney.PickMoneyDialog()
		dlgPickMoney.LoadDialog()
		dlgPickMoney.SetAcceptEvent(ui.__mem_func__(self.OnPickMoney))
		dlgPickMoney.SetTitleName(localeInfo.EXCHANGE_MONEY)
		dlgPickMoney.SetMax(10)
		dlgPickMoney.Hide()
		self.dlgPickMoney = dlgPickMoney

		## Button
		self.AcceptButton = self.GetChild("Owner_Accept_Button")
		self.AcceptButton.SetToggleDownEvent(ui.__mem_func__(self.AcceptExchange))

		self.TitleName = self.GetChild("TitleName")
		self.GetChild("TitleBar").SetCloseEvent(net.SendExchangeExitPacket)

	def Destroy(self):
		print "---------------------------------------------------------------------------- DESTROY EXCHANGE"
		self.ClearDictionary()
		self.dlgPickMoney.Destroy()
		self.dlgPickMoney = 0
		self.OwnerSlot = 0
		self.OwnerMoney = 0
		self.OwnerAcceptLight = 0
		self.OwnerMoneyButton = 0
		self.TargetSlot = 0
		self.TargetMoney = 0
		self.TargetAcceptLight = 0
		self.TitleName = 0
		self.AcceptButton = 0
		self.tooltipItem = 0
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.interface = 0
			self.wndInventory = 0
			self.lockedItems = {i:(-1,-1) for i in range(exchange.EXCHANGE_ITEM_MAX_NUM)}


	def OpenDialog(self):
		self.TitleName.SetText(localeInfo.EXCHANGE_TITLE % (exchange.GetNameFromTarget(), exchange.GetLevelFromTarget()))
		self.AcceptButton.Enable()
		self.AcceptButton.SetUp()
		self.Show()
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.interface.SetOnTopWindow(player.ON_TOP_WND_EXCHANGE)
			self.interface.RefreshMarkInventoryBag()

		(self.xStart, self.yStart, z) = player.GetMainCharacterPosition()

	def CloseDialog(self):
		wndMgr.OnceIgnoreMouseLeftButtonUpEvent()

		if 0 != self.tooltipItem:
			self.tooltipItem.HideToolTip()

		self.dlgPickMoney.Close()
		self.Hide()
		if app.WJ_ENABLE_TRADABLE_ICON:
			for exchangePos, (itemInvenPage, itemSlotPos) in self.lockedItems.items():
				if itemInvenPage == self.wndInventory.GetInventoryPageIndex():
					self.wndInventory.wndItem.SetCanMouseEventSlot(itemSlotPos)

			self.lockedItems = {i:(-1,-1) for i in range(exchange.EXCHANGE_ITEM_MAX_NUM)}
			self.interface.SetOnTopWindow(player.ON_TOP_WND_NONE)
			self.interface.RefreshMarkInventoryBag()

	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = tooltipItem

	def OpenPickMoneyDialog(self):

		if exchange.GetElkFromSelf() > 0:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.EXCHANGE_CANT_EDIT_MONEY)
			return

		self.dlgPickMoney.Open(player.GetElk())

	def OnPickMoney(self, money):
		net.SendExchangeElkAddPacket(money)

	def AcceptExchange(self):
		net.SendExchangeAcceptPacket()
		self.AcceptButton.Disable()

	def SelectOwnerEmptySlot(self, SlotIndex):

		if False == mouseModule.mouseController.isAttached():
			return

		if mouseModule.mouseController.IsAttachedMoney():
			net.SendExchangeElkAddPacket(mouseModule.mouseController.GetAttachedMoneyAmount())
		else:
			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			if (player.SLOT_TYPE_INVENTORY == attachedSlotType
				or player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == attachedSlotType):

				attachedInvenType = player.SlotTypeToInvenType(attachedSlotType)
				SrcSlotNumber = mouseModule.mouseController.GetAttachedSlotNumber()
				DstSlotNumber = SlotIndex

				itemID = player.GetItemIndex(attachedInvenType, SrcSlotNumber)
				item.SelectItem(itemID)

				if item.IsAntiFlag(item.ANTIFLAG_GIVE):
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.EXCHANGE_CANNOT_GIVE)
					mouseModule.mouseController.DeattachObject()
					return

				net.SendExchangeItemAddPacket(attachedInvenType, SrcSlotNumber, DstSlotNumber)
			if app.ENABLE_SPECIAL_STORAGE:
				if player.SLOT_TYPE_UPGRADE_INVENTORY == attachedSlotType or\
					player.SLOT_TYPE_BOOK_INVENTORY == attachedSlotType or\
					player.SLOT_TYPE_STONE_INVENTORY == attachedSlotType:
					attachedInvenType = player.SlotTypeToInvenType(attachedSlotType)
					SrcSlotNumber = mouseModule.mouseController.GetAttachedSlotNumber()
					DstSlotNumber = SlotIndex
	
					itemID = player.GetItemIndex(attachedSlotType, SrcSlotNumber)
					item.SelectItem(itemID)
					
					if item.IsAntiFlag(item.ANTIFLAG_GIVE):
						chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.EXCHANGE_CANNOT_GIVE)
						mouseModule.mouseController.DeattachObject()
						return
						
					net.SendExchangeItemAddPacket(attachedInvenType, SrcSlotNumber, DstSlotNumber)

		mouseModule.mouseController.DeattachObject()

	def SelectOwnerItemSlot(self, SlotIndex):

		if player.ITEM_MONEY == mouseModule.mouseController.GetAttachedItemIndex():

			money = mouseModule.mouseController.GetAttachedItemCount()
			net.SendExchangeElkAddPacket(money)

	def RefreshOwnerSlot(self):
		for i in xrange(exchange.EXCHANGE_ITEM_MAX_NUM):
			itemIndex = exchange.GetItemVnumFromSelf(i)
			itemCount = exchange.GetItemCountFromSelf(i)
			if 1 == itemCount:
				itemCount = 0
			self.OwnerSlot.SetItemSlot(i, itemIndex, itemCount)
			if app.ENABLE_CHANGELOOK_SYSTEM:
				itemTransmutedVnum = exchange.GetItemTransmutation(i, True)
				if itemTransmutedVnum:
					self.OwnerSlot.DisableCoverButton(i)
				else:
					self.OwnerSlot.EnableCoverButton(i)
		self.OwnerSlot.RefreshSlot()

	def RefreshTargetSlot(self):
		for i in xrange(exchange.EXCHANGE_ITEM_MAX_NUM):
			itemIndex = exchange.GetItemVnumFromTarget(i)
			itemCount = exchange.GetItemCountFromTarget(i)
			if 1 == itemCount:
				itemCount = 0
			self.TargetSlot.SetItemSlot(i, itemIndex, itemCount)
			if app.ENABLE_CHANGELOOK_SYSTEM:
				itemTransmutedVnum = exchange.GetItemTransmutation(i, False)
				if itemTransmutedVnum:
					self.TargetSlot.DisableCoverButton(i)
				else:
					self.TargetSlot.EnableCoverButton(i)
		self.TargetSlot.RefreshSlot()

	def Refresh(self):

		self.RefreshOwnerSlot()
		self.RefreshTargetSlot()
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.RefreshLockedSlot()

		self.OwnerMoney.SetText(str(exchange.GetElkFromSelf()))
		self.TargetMoney.SetText(str(exchange.GetElkFromTarget()))

		if True == exchange.GetAcceptFromSelf():
			self.OwnerAcceptLight.Down()
		else:
			self.AcceptButton.Enable()
			self.AcceptButton.SetUp()
			self.OwnerAcceptLight.SetUp()

		if True == exchange.GetAcceptFromTarget():
			self.TargetAcceptLight.Down()
		else:
			self.TargetAcceptLight.SetUp()

	def OverInOwnerItem(self, slotIndex):

		if 0 != self.tooltipItem:
			self.tooltipItem.SetExchangeOwnerItem(slotIndex)

	def OverInTargetItem(self, slotIndex):

		if 0 != self.tooltipItem:
			self.tooltipItem.SetExchangeTargetItem(slotIndex)

	def OverOutItem(self):

		if 0 != self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def OnTop(self):
		self.tooltipItem.SetTop()
		if app.WJ_ENABLE_TRADABLE_ICON:
			if self.interface:
				self.interface.SetOnTopWindow(player.ON_TOP_WND_EXCHANGE)
				self.interface.RefreshMarkInventoryBag()

	def OnUpdate(self):

		USE_EXCHANGE_LIMIT_RANGE = 1000

		(x, y, z) = player.GetMainCharacterPosition()
		if abs(x - self.xStart) > USE_EXCHANGE_LIMIT_RANGE or abs(y - self.yStart) > USE_EXCHANGE_LIMIT_RANGE:
			(self.xStart, self.yStart, z) = player.GetMainCharacterPosition()
			net.SendExchangeExitPacket()

	if app.WJ_ENABLE_TRADABLE_ICON:
		def CantTradableItem(self, destSlotIndex, srcSlotIndex):
			if True == exchange.GetAcceptFromTarget():
				return

			itemInvenPage = srcSlotIndex / player.INVENTORY_PAGE_SIZE
			localSlotPos = srcSlotIndex - (itemInvenPage * player.INVENTORY_PAGE_SIZE)
			self.lockedItems[destSlotIndex] = (itemInvenPage, localSlotPos)

			if self.wndInventory.GetInventoryPageIndex() == itemInvenPage and self.IsShow():
				self.wndInventory.wndItem.SetCantMouseEventSlot(localSlotPos)

		def RefreshLockedSlot(self):
			if self.wndInventory:
				for exchangePos, (itemInvenPage, itemSlotPos) in self.lockedItems.items():
					if self.wndInventory.GetInventoryPageIndex() == itemInvenPage:
						self.wndInventory.wndItem.SetCantMouseEventSlot(itemSlotPos)

				self.wndInventory.wndItem.RefreshSlot()

		def BindInterface(self, interface):
			self.interface = interface

		def SetInven(self, wndInventory):
			from _weakref import proxy
			self.wndInventory = proxy(wndInventory)			