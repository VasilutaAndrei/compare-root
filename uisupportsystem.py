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
import uiToolTip


AFFECT_DICT = {
		item.APPLY_INT : localeInfo.TOOLTIP_INT,
	}
	
	
def checkdiv(n):
	x = str(n/10.0)
	if len(x) > 3:
		return str(x)[0:3]
	return str(x)

def pointop(n):
	t = int(n)
	if t / 10 < 1:
		return "0."+n
	else:		
		return n[0:len(n)-1]+"."+n[len(n)-1:]
		
class SupportMainGui(ui.ScriptWindow):
	class TextToolTip(ui.Window):
		def __init__(self, y):
			ui.Window.__init__(self, "TOP_MOST")

			textLine = ui.TextLine()
			textLine.SetParent(self)
			textLine.SetHorizontalAlignLeft()
			textLine.SetOutline()
			textLine.Show()
			self.y = y
			self.textLine = textLine

		def __del__(self):
			ui.Window.__del__(self)

		def SetText(self, text):
			self.textLine.SetText(text)

		def OnRender(self):
			(mouseX, mouseY) = wndMgr.GetMousePosition()
			self.textLine.SetPosition(mouseX, mouseY - 60 + self.y)

	def __init__(self, vnum = 0):
		ui.ScriptWindow.__init__(self)
		self.vnum = vnum
		self.__LoadWindow()
		

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Show(self):
		ui.ScriptWindow.Show(self)

	def Close(self):
		self.Hide()
		constInfo.SUPPORTGUI = 0
		
	def OnPressEscapeKey(self):
		self.Close()
		return TRUE	

	def __LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/supportinformationwindow.py")
		except:
			import exception
			exception.Abort("supportinformationwindow.LoadWindow.LoadObject")
			
		try:
			self.combSlot = self.GetChild("CombSlot")
			self.boardclose = self.GetChild("CloseButton")
			self.boardclose.SetEvent(ui.__mem_func__(self.Close,))
			self.combSlot.SetSelectEmptySlotEvent(ui.__mem_func__(self.__OnSelectEmptySlot))

		except:
			import exception
			exception.Abort("supportinformationwindow.LoadWindow.BindObject")
						
	def __OnSelectEmptySlot(self, selectedSlotPos):
		isAttached = mouseModule.mouseController.isAttached()
		if isAttached:
			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			targetIndex = player.GetItemIndex(attachedSlotPos)
			if attachedSlotType != player.SLOT_TYPE_INVENTORY:
				return
				
			mouseModule.mouseController.DeattachObject()
				
			item.SelectItem(targetIndex)
			itemType = item.GetItemType()
			itemSubType = item.GetItemSubType()
			itemVnum = player.GetItemIndex(attachedSlotPos)
			if itemType != item.ITEM_TYPE_COSTUME:
				chat.AppendChat(chat.CHAT_TYPE_INFO, "<Buffi> Nu poti face asa ceva!")
				return				
			self.combSlot.SetItemSlot(selectedSlotPos, player.GetItemIndex(attachedSlotPos), player.GetItemCount(attachedSlotPos))
	
			if selectedSlotPos == 1:
				net.SendChatPacket("/support_system %s" % (str(itemVnum)))
			else:
				net.SendChatPacket("/support_system_d %s" % (str(itemVnum)))
					
			for i in xrange(4):
				self.combSlot.ClearSlot(i)
	