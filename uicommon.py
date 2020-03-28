import ui
import localeInfo
import app
import ime
import uiScriptLocale
import chat
import uiToolTip
import constInfo
import item
import skill
import nonplayer
import player

class PopupDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__LoadDialog()
		self.acceptEvent = lambda *arg: None

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadDialog(self):
		try:
			PythonScriptLoader = ui.PythonScriptLoader()
			PythonScriptLoader.LoadScriptFile(self, "UIScript/PopupDialog.py")

			self.board = self.GetChild("board")
			self.message = self.GetChild("message")
			self.accceptButton = self.GetChild("accept")
			self.accceptButton.SetEvent(ui.__mem_func__(self.Close))

		except:
			import exception
			exception.Abort("PopupDialog.LoadDialog.BindObject")

	def Open(self):
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def Close(self):
		self.Hide()
		self.acceptEvent()

	def Destroy(self):
		self.Close()
		self.ClearDictionary()

	def SetWidth(self, width):
		height = self.GetHeight()
		self.SetSize(width, height)
		self.board.SetSize(width, height)
		self.SetCenterPosition()
		self.UpdateRect()

	def SetText(self, text):
		self.message.SetText(text)

	def SetAcceptEvent(self, event):
		self.acceptEvent = event

	def SetButtonName(self, name):
		self.accceptButton.SetText(name)

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def OnIMEReturn(self):
		self.Close()
		return True

class InputDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.__CreateDialog()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __CreateDialog(self):

		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/inputdialog.py")

		getObject = self.GetChild
		self.board = getObject("Board")
		self.acceptButton = getObject("AcceptButton")
		self.cancelButton = getObject("CancelButton")
		self.inputSlot = getObject("InputSlot")
		self.inputValue = getObject("InputValue")

	def Open(self):
		self.inputValue.SetFocus()
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def Close(self):
		self.ClearDictionary()
		self.board = None
		self.acceptButton = None
		self.cancelButton = None
		self.inputSlot = None
		self.inputValue = None
		self.Hide()

	def SetTitle(self, name):
		self.board.SetTitleName(name)

	def SetNumberMode(self):
		self.inputValue.SetNumberMode()

	def SetSecretMode(self):
		self.inputValue.SetSecret()

	def SetFocus(self):
		self.inputValue.SetFocus()

	def SetMaxLength(self, length):
		width = length * 6 + 10
		self.SetBoardWidth(max(width + 50, 160))
		self.SetSlotWidth(width)
		self.inputValue.SetMax(length)

	def SetSlotWidth(self, width):
		self.inputSlot.SetSize(width, self.inputSlot.GetHeight())
		self.inputValue.SetSize(width, self.inputValue.GetHeight())
		if self.IsRTL():
			self.inputValue.SetPosition(self.inputValue.GetWidth(), 0)

	def SetBoardWidth(self, width):
		self.SetSize(max(width + 50, 160), self.GetHeight())
		self.board.SetSize(max(width + 50, 160), self.GetHeight())
		if self.IsRTL():
			self.board.SetPosition(self.board.GetWidth(), 0)
		self.UpdateRect()

	def SetAcceptEvent(self, event):
		self.acceptButton.SetEvent(event)
		self.inputValue.OnIMEReturn = event

	def SetCancelEvent(self, event):
		self.board.SetCloseEvent(event)
		self.cancelButton.SetEvent(event)
		self.inputValue.OnPressEscapeKey = event

	def GetText(self):
		return self.inputValue.GetText()

class InputDialogWithDescription(InputDialog):

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.__CreateDialog()

	def __del__(self):
		InputDialog.__del__(self)

	def __CreateDialog(self):

		pyScrLoader = ui.PythonScriptLoader()
		if localeInfo.IsARABIC() :
			pyScrLoader.LoadScriptFile(self, uiScriptLocale.LOCALE_UISCRIPT_PATH + "inputdialogwithdescription.py")
		else:
			pyScrLoader.LoadScriptFile(self, "uiscript/inputdialogwithdescription.py")

		try:
			getObject = self.GetChild
			self.board = getObject("Board")
			self.acceptButton = getObject("AcceptButton")
			self.cancelButton = getObject("CancelButton")
			self.inputSlot = getObject("InputSlot")
			self.inputValue = getObject("InputValue")
			self.description = getObject("Description")

		except:
			import exception
			exception.Abort("InputDialogWithDescription.LoadBoardDialog.BindObject")

	def SetDescription(self, text):
		self.description.SetText(text)

class InputDialogWithDescription2(InputDialog):

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.__CreateDialog()

	def __del__(self):
		InputDialog.__del__(self)

	def __CreateDialog(self):

		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/inputdialogwithdescription2.py")

		try:
			getObject = self.GetChild
			self.board = getObject("Board")
			self.acceptButton = getObject("AcceptButton")
			self.cancelButton = getObject("CancelButton")
			self.inputSlot = getObject("InputSlot")
			self.inputValue = getObject("InputValue")
			self.description1 = getObject("Description1")
			self.description2 = getObject("Description2")

		except:
			import exception
			exception.Abort("InputDialogWithDescription.LoadBoardDialog.BindObject")

	def SetDescription1(self, text):
		self.description1.SetText(text)

	def SetDescription2(self, text):
		self.description2.SetText(text)

class QuestionDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__CreateDialog()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __CreateDialog(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/questiondialog.py")

		self.board = self.GetChild("board")
		self.textLine = self.GetChild("message")
		self.acceptButton = self.GetChild("accept")
		self.cancelButton = self.GetChild("cancel")

	def Open(self):
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def Close(self):
		self.Hide()

	def SetWidth(self, width):
		height = self.GetHeight()
		self.SetSize(width, height)
		self.board.SetSize(width, height)
		self.SetCenterPosition()
		self.UpdateRect()

	def SAFE_SetAcceptEvent(self, event):
		self.acceptButton.SAFE_SetEvent(event)

	def SAFE_SetCancelEvent(self, event):
		self.cancelButton.SAFE_SetEvent(event)

	def SetAcceptEvent(self, event):
		self.acceptButton.SetEvent(event)

	def SetCancelEvent(self, event):
		self.cancelButton.SetEvent(event)

	def SetText(self, text):
		self.textLine.SetText(text)

	def SetAcceptText(self, text):
		self.acceptButton.SetText(text)

	def SetCancelText(self, text):
		self.cancelButton.SetText(text)

	def OnPressEscapeKey(self):
		self.Close()
		return True
		
class QuestionDialog2(QuestionDialog):

	def __init__(self):
		QuestionDialog.__init__(self)
		self.__CreateDialog()

	def __del__(self):
		QuestionDialog.__del__(self)

	def __CreateDialog(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/questiondialog2.py")

		self.board = self.GetChild("board")
		self.textLine1 = self.GetChild("message1")
		self.textLine2 = self.GetChild("message2")
		self.acceptButton = self.GetChild("accept")
		self.cancelButton = self.GetChild("cancel")

	def SetText1(self, text, alignLeft = False):
		self.textLine1.SetText(text)
		if alignLeft == True:
			self.textLine1.SetPosition(15, 30)
			self.textLine1.SetWindowHorizontalAlignLeft()
			self.textLine1.SetHorizontalAlignLeft()
		else:
			self.textLine1.SetPosition(0, 25)
			self.textLine1.SetWindowHorizontalAlignCenter()
			self.textLine1.SetHorizontalAlignCenter()

	def SetText2(self, text, alignLeft = False):
		self.textLine2.SetText(text)
		if alignLeft == True:
			self.textLine2.SetPosition(15, 50)
			self.textLine2.SetWindowHorizontalAlignLeft()
			self.textLine2.SetHorizontalAlignLeft()
		else:
			self.textLine2.SetPosition(0, 50)
			self.textLine2.SetWindowHorizontalAlignCenter()
			self.textLine2.SetHorizontalAlignCenter()
		
	def AutoResize(self):
		if self.textLine1.GetTextSize()[0] > self.textLine2.GetTextSize()[0]:
			self.SetWidth(self.textLine1.GetTextSize()[0] + 30)
		else:
			self.SetWidth(self.textLine2.GetTextSize()[0] + 30)
		
class QuestionDropDialog(ui.ScriptWindow):					
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__CreateDialog()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __CreateDialog(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/questiondropdialog.py")

		self.board = self.GetChild("board")
		self.textLine = self.GetChild("message")
		self.acceptButton = self.GetChild("accept")
		self.cancelButton = self.GetChild("cancel")
		self.destroyButton = self.GetChild("destroy")		
		self.itemSlot = self.GetChild("ItemSlot")
		
		self.itemSlot.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		self.itemSlot.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
	
	def SetItemSlot(self, slotIndex):
		itemIndex = player.GetItemIndex(slotIndex)
		itemCount = player.GetItemCount(slotIndex)
		self.itemSlot.SetItemSlot(0, itemIndex, itemCount)

		item.SelectItem(player.GetItemIndex(slotIndex))

		metinSlot = [player.GetItemMetinSocket(slotIndex, i) for i in xrange(player.METIN_SOCKET_MAX_NUM)]
		attrSlot = [player.GetItemAttribute(slotIndex, i) for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM)]
		
		if item.IsAntiFlag(item.ITEM_ANTIFLAG_DROP):
			self.acceptButton.Down()
			self.acceptButton.Disable()
		
		self.itemToolTip = uiToolTip.ItemToolTip()
		self.itemToolTip.AddItemData(player.GetItemIndex(slotIndex), metinSlot, attrSlot)
		
		if itemCount <= 1:
			self.SetText(item.GetItemName())
		else:
			self.SetText("%s x %s" % (item.GetItemName(),str(itemCount)))
		
	def Open(self):
		if 0 != self.itemToolTip:
			self.itemToolTip.HideToolTip()
			
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def Close(self):
		if 0 != self.itemToolTip:
			self.itemToolTip.HideToolTip()
		self.Hide()

	def SetDlgSize(self, width, height):
		self.SetSize(width, height)
		self.board.SetSize(width, height)
		self.SetCenterPosition()
		self.UpdateRect()
		
	def OverInItem(self, slotNumber):
		if 0 != self.itemToolTip:
			self.itemToolTip.ShowToolTip()
			
	def OverOutItem(self):
		if 0 != self.itemToolTip:
			self.itemToolTip.HideToolTip()

	def SAFE_SetAcceptEvent(self, event):
		self.acceptButton.SAFE_SetEvent(event)

	def SAFE_SetCancelEvent(self, event):
		self.cancelButton.SAFE_SetEvent(event)

	def SetAcceptEvent(self, event):
		self.acceptButton.SetEvent(event)

	def SetCancelEvent(self, event):
		self.cancelButton.SetEvent(event)
		
	def SetDestroyEvent(self, event):
		self.destroyButton.SetEvent(event)
		
	def SetText(self, text):
		self.textLine.SetText(text)
		self.textLine.SetFontColor(0.72, 1.0, 0.0)

	def SetAcceptText(self, text):
		self.acceptButton.SetText(text)

	def SetCancelText(self, text):
		self.cancelButton.SetText(text)

	def OnPressEscapeKey(self):
		self.Close()
		return True
class QuestionDialogWithTimeLimit(QuestionDialog2):

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.__CreateDialog()
		self.endTime = 0

	def __del__(self):
		QuestionDialog2.__del__(self)

	def __CreateDialog(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/questiondialog2.py")

		self.board = self.GetChild("board")
		self.textLine1 = self.GetChild("message1")
		self.textLine2 = self.GetChild("message2")
		self.acceptButton = self.GetChild("accept")
		self.cancelButton = self.GetChild("cancel")

	def Open(self, msg, timeout):
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

		self.SetText1(msg)
		self.endTime = app.GetTime() + timeout

	def OnUpdate(self):
		leftTime = max(0, self.endTime - app.GetTime())
		self.SetText2(localeInfo.UI_LEFT_TIME % (leftTime))

class MoneyInputDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.moneyHeaderText = localeInfo.MONEY_INPUT_DIALOG_SELLPRICE
		self.__CreateDialog()
		self.SetMaxLength(13)

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __CreateDialog(self):

		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/moneyinputdialog.py")

		getObject = self.GetChild
		self.board = self.GetChild("board")
		self.acceptButton = getObject("AcceptButton")
		self.cancelButton = getObject("CancelButton")
		self.inputValue = getObject("InputValue")
		#self.inputValue.SetNumberMode()
		self.inputValue.OnIMEUpdate = ui.__mem_func__(self.__OnValueUpdate)
		self.moneyText = getObject("MoneyValue")

	def Open(self):
		self.inputValue.SetText("")
		self.inputValue.SetFocus()
		self.__OnValueUpdate()
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def Close(self):
		self.ClearDictionary()
		self.board = None
		self.acceptButton = None
		self.cancelButton = None
		self.inputValue = None
		self.Hide()

	def SetTitle(self, name):
		self.board.SetTitleName(name)

	def SetFocus(self):
		self.inputValue.SetFocus()

	def SetMaxLength(self, length):
		self.inputValue.SetMax(length)
		self.inputValue.SetUserMax(length)

	def SetMoneyHeaderText(self, text):
		self.moneyHeaderText = text

	def SetAcceptEvent(self, event):
		self.acceptButton.SetEvent(event)
		self.inputValue.OnIMEReturn = event

	def SetCancelEvent(self, event):
		self.board.SetCloseEvent(event)
		self.cancelButton.SetEvent(event)
		self.inputValue.OnPressEscapeKey = event

	def SetValue(self, value):
		value=str(value)
		self.inputValue.SetText(value)
		self.__OnValueUpdate()
		ime.SetCursorPosition(len(value))		


	def GetText(self):
		return self.inputValue.GetText()

	def __OnValueUpdate(self):
		ui.EditLine.OnIMEUpdate(self.inputValue)

		text = self.inputValue.GetText()
		for i in xrange(len(text)):
			if not text[i].isdigit():
				text=text[0:i]+text[i+1:]
				self.inputValue.SetText(text)
		self.moneyText.SetText(self.moneyHeaderText + localeInfo.NumberToMoneyString(text))

class ItemQuestionDialog(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__CreateDialog()
		
		self.tooltipItem = uiToolTip.ItemToolTip()
		self.window_type = 0 # "inv" or "shop"
		self.count = 0
		self.height = 0 # 30 for buy & sell
		
	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __CreateDialog(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/questiondialogitem.py")

		self.board = self.GetChild("board")
		self.textLine = self.GetChild("message")
		self.acceptButton = self.GetChild("accept")
		self.cancelButton = self.GetChild("cancel")
		self.destroyButton = self.GetChild("destroy")


		self.titleBar = ui.TitleBar()
		self.titleBar.SetParent(self.board)
		self.titleBar.MakeTitleBar(244, "yellow")
		self.titleBar.SetPosition(8, 7)
		self.titleBar.Show()

		self.titleName = ui.TextLine()
		self.titleName.SetParent(self.titleBar)
		self.titleName.SetPosition(0, 4)
		self.titleName.SetWindowHorizontalAlignCenter()
		self.titleName.SetHorizontalAlignCenter()
		self.titleName.Show()

		self.slotList = []
		for i in xrange(3):
			slot = ui.ImageBox()
			slot.LoadImage("d:/ymir work/ui/public/slot_base.sub")
			slot.SetParent(self)
			slot.SetWindowHorizontalAlignCenter()
			self.slotList.append(slot)

	def Open(self, vnum, slot, type_w, text="", mode =0):
		#self.Lock()
		item.SelectItem(vnum)
		xSlotCount, ySlotCount = item.GetItemSize(1,2,3,4,5,6)	

		self.window_type = type_w

		

		try:
			if self.window_type == 0:
				metinSlot = [player.GetItemMetinSocket(player.INVENTORY, slot, i) for i in xrange(player.METIN_SOCKET_MAX_NUM)]
				self.count = player.GetItemCount(slot)
			elif self.window_type == 1:
				metinSlot = [shop.GetItemMetinSocket(slot, i) for i in xrange(player.METIN_SOCKET_MAX_NUM)]

				itemCount = shop.GetItemCount(slot)
				self.count = itemCount
				chat.AppendChat(1,"%d"%itemCount)
				
		except:
			pass

		if type_w == 1 or mode == 1:
			self.destroyButton.Hide()
			
		if vnum in (50300, 70037):
			self.titleName.SetText("%s %s" % (skill.GetSkillName(metinSlot[0]), item.GetItemName()))
		elif vnum == 70104:
			self.titleName.SetText("%s %s" % (nonplayer.GetMonsterName(metinSlot[0]), item.GetItemName()))
		else:
			self.titleName.SetText(item.GetItemName())

		if text:
			textLine2 = ui.TextLine()
			textLine2.SetPosition(0, 80 + 32*ySlotCount)
			textLine2.SetWindowHorizontalAlignCenter()
			textLine2.SetHorizontalAlignCenter()
			textLine2.SetVerticalAlignCenter()
			textLine2.SetParent(self.board)
			textLine2.SetText(text)
			textLine2.Hide()
			self.textLine2 = textLine2
			self.textLine.SetText(text)

		slotGrid = ui.SlotWindow()
		slotGrid.SetParent(self)
		slotGrid.SetPosition(-16, 60)
		slotGrid.SetWindowHorizontalAlignCenter()
		slotGrid.AppendSlot(0, 0, 0, 32*xSlotCount, 32*ySlotCount)
		slotGrid.AddFlag("not_pick")
		slotGrid.Show()
		self.slotGrid = slotGrid
		
		
		if self.count > 1:
			self.slotGrid.SetItemSlot(0, vnum, self.count)
		else:
			self.slotGrid.SetItemSlot(0, vnum)

		#if self.window_type == 0:
			#if constInfo.ValidarObjeto(vnum) == True:
			#	self.slotGrid.SetValueItem(0, str(constInfo.ObtenerVnum(vnum)))
		#elif self.window_type == 1:
			#if constInfo.ValidarObjeto(vnum) == True:
				#self.slotGrid.SetValueItem(0, str(constInfo.ObtenerVnum(vnum)))


		if text:
			self.height -= 10

				
		self.SetSize(260, 110 + 8 + 32*ySlotCount + self.height)
		self.board.SetSize(260, 110 + 8 + 32*ySlotCount + self.height)
		self.board.AddFlag("not_pick")
		self.textLine.SetPosition(0, 42)

		for i in xrange(min(3, ySlotCount)):
			self.slotList[i].SetPosition(0, 28 + ySlotCount*32 - i*32)
			self.slotList[i].OnMouseOverIn = lambda arg = slot: self.OverInItem(arg)
			self.slotList[i].OnMouseOverOut = lambda arg = self.tooltipItem: self.OverOutItem(arg)
			self.slotList[i].Show()
		
		if type_w == 0:
			self.GetChild("accept").SetPosition(-65, 74 + 8 + 32*ySlotCount + self.height)
			self.GetChild("cancel").SetPosition(64, 74 + 8+ 32*ySlotCount + self.height)
			self.GetChild("destroy").SetPosition(0, 74 + 8+ 32*ySlotCount + self.height)
			self.GetChild("accept").SetText("Arunca")
		else:
			self.GetChild("accept").SetPosition(-35, 74 + 8 + 32*ySlotCount + self.height)
			self.GetChild("accept").SetText("Cumpara")
			self.GetChild("cancel").SetPosition(35, 74 + 8+ 32*ySlotCount + self.height)


		if mode == 1:
			self.GetChild("accept").SetText("Vinde")
			self.GetChild("accept").SetPosition(-35, 74 + 8 + 32*ySlotCount + self.height)
			self.GetChild("cancel").SetPosition(35, 74 + 8+ 32*ySlotCount + self.height)


		self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))
		
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def SetCloseEvent(self, event):
		self.titleBar.SetCloseEvent(event)
		
	def SetMessage(self, text):
		self.textLine.SetText(text)

	def OverInItem(self, slot):
		if self.window_type == 1:
			self.tooltipItem.SetShopItem(slot)
		elif self.window_type == 0:
			self.tooltipItem.SetInventoryItem(slot)
		
	def OverOutItem(self, tooltipItem):
		if 0 != tooltipItem:
			self.tooltipItem.HideToolTip()
			self.tooltipItem.ClearToolTip()
	
	def Close(self):
		self.ClearDictionary()
		self.slotList = []
		self.titleBar = None
		self.titleName = None
		self.textLine2 = None
		self.slotGrid = None
		
		self.tooltipItem = 0
		self.Hide()
		#self.Unlock()
		
		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)
		
	def SetWidth(self, width):
		height = self.GetHeight()
		self.SetSize(width, height)
		self.board.SetSize(width, height)
		self.SetCenterPosition()
		self.UpdateRect()

	def SAFE_SetAcceptEvent(self, event):
		self.acceptButton.SAFE_SetEvent(event)

	def SAFE_SetCancelEvent(self, event):
		self.cancelButton.SAFE_SetEvent(event)

	def SetAcceptEvent(self, event):
		self.acceptButton.SetEvent(event)

	def SetDestroyEvent(self, event):
		self.destroyButton.SetEvent(event)

	def SetCancelEvent(self, event):
		self.cancelButton.SetEvent(event)

	def SetText(self, text):
		self.textLine.SetText(text)

	def SetAcceptText(self, text):
		self.acceptButton.SetText(text)

	def SetCancelText(self, text):
		self.cancelButton.SetText(text)

	def OnPressEscapeKey(self):
		self.Close()
		
		return True
		
