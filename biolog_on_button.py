import ui
import player
import mouseModule
import net
import os
import app
import snd
import item
if app.ENABLE_BIOLOG_SYSTEM:
	import uiprofessionalbiolog, uiToolTip
import player
import chat
import grp
import uiScriptLocale
import uiRefine
import uiAttachMetin
import uiPickMoney
import uiCommon
import uiPrivateShopBuilder

import localeInfo
import constInfo
import ime
import wndMgr
import background
import event
import playerSettingModule
import event
import apollo_interface
import exchange
import background
import shop
import uiSearchShop
import safebox
import chr
import upgradeStorage

class CollectInventoryWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.isLoaded = 0
		self.updated = 0
		self.tooltipItem = uiToolTip.ItemToolTip()
		self.tooltipItem.Hide()
		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Show(self):
		self.__LoadWindow()
		ui.ScriptWindow.Show(self)
		
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
			self.GetChild("titlebar").SetEvent(self.Close)
			self.ORIGINAL_WIDTH = self.GetWidth()
			self.wndBeltInventoryLayer = self.GetChild("BeltInventoryLayer")
			self.wndItem = self.GetChild("BeltInventorySlot")
			self.wndItem.SetItemSlot(0, 21128, 0)
			self.time_value = self.GetChild("time_value")
			self.biolog_count = self.GetChild("count_value")
			self.sendBtn = self.GetChild("send_biolog")
		#	self.BtnClose = self.GetChild("inchide_fereastra")
			self.wndItem.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
			self.wndItem.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
		except:
			import exception
			exception.Abort("CollectInventoryWindow.LoadWindow.BindObject")

		if self.sendBtn:
			self.sendBtn.SetEvent(ui.__mem_func__(self.AcceptBiolog))
			
	def BtnClose(self):
		ui.ScriptWindow.__del__(self)
		
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
		if str(uiprofessionalbiolog.BIOLOG_BINARY_LOADED['countActual'][0]) == "0000":
			self.biolog_count.SetText(localeInfo.BIOLOG_APPEND_1) 
			self.time_value.SetText(localeInfo.BIOLOG_APPEND_2)
		else:
			if int(uiprofessionalbiolog.BIOLOG_BINARY_LOADED["vnum"][0]) > 0 and uiprofessionalbiolog.BIOLOG_BINARY_LOADED["vnum"][0] != 21128:
				self.SetTime(int(uiprofessionalbiolog.BIOLOG_BINARY_LOADED["time"][0]))
				self.SetItem(0, int(uiprofessionalbiolog.BIOLOG_BINARY_LOADED["vnum"][0]), 0)
				self.biolog_count.SetText(str(uiprofessionalbiolog.BIOLOG_BINARY_LOADED['countActual'][0]) + "/" + str(uiprofessionalbiolog.BIOLOG_BINARY_LOADED['countNeed'][0]))

	def OverInItem(self):
		if uiprofessionalbiolog.BIOLOG_BINARY_LOADED["vnum"][0] and uiprofessionalbiolog.BIOLOG_BINARY_LOADED["vnum"][0] != 21128:
			self.tooltipItem.SetItemToolTip(uiprofessionalbiolog.BIOLOG_BINARY_LOADED["vnum"][0])

	def OverOutItem(self):
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()	
			
	def Close(self):
		self.Hide()
		