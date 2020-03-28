import app
import os
import net
import mouseModule
import snd
import localeInfo
import ui
import uiScriptLocale
import uiGuild, dbg, chat, uiToolTip, wndMgr
from _weakref import proxy

BAN_DESCRIPTION_TYPE = [
	localeInfo.ADMIN_MANAGER_BAN_TYPE_DESCRIPTION_1,
	localeInfo.ADMIN_MANAGER_BAN_TYPE_DESCRIPTION_2,
	localeInfo.ADMIN_MANAGER_BAN_TYPE_DESCRIPTION_3
]

DESCRIPTION_TYPE_BAN = [
	localeInfo.ADMIN_MANAGER_BAN_TYPE_1, 
	localeInfo.ADMIN_MANAGER_BAN_TYPE_2, 
	localeInfo.ADMIN_MANAGER_BAN_TYPE_3,
]

class CheckBox(ui.ImageBox):
	def __init__(self, parent, key, x, y, event, filename = "d:/ymir work/ui/public/Parameter_Slot_03.sub"):
		ui.ImageBox.__init__(self)
		self.SetParent(parent)
		self.SetPosition(x, y)
		
		self.txt = ui.TextLine()
		self.txt.SetParent(parent)
		self.txt.SetPosition(x + 5, y + 2)
		self.txt.SetText(DESCRIPTION_TYPE_BAN[key])
		self.txt.Show()

		self.LoadImage(filename)
		self.mouse = uiGuild.MouseReflector(self)
		self.mouse.SetSize(self.GetWidth(), self.GetHeight())

		image = ui.MakeImageBox(self, "d:/ymir work/ui/public/check_image.sub", 30, - 1)
		image.AddFlag("not_pick")
		image.SetWindowHorizontalAlignCenter()
		image.SetWindowVerticalAlignCenter()
		image.Hide()
		self.Enable = True
		self.image = image
		self.event = event
		self.Show()
		self.mouse.UpdateRect()

	def __del__(self):
		ui.ImageBox.__del__(self)

	def SetCheck(self, flag):
		if flag:
			self.image.Show()
		else:
			self.image.Hide()

	def Disable(self):
		self.Enable = False
		
	def IsSelected(self):
		if self.image.IsShow():
			return True
		return False

	def OnMouseOverIn(self):
		if not self.Enable:
			return
		self.mouse.Show()

	def OnMouseOverOut(self):
		if not self.Enable:
			return
		self.mouse.Hide()

	def OnMouseLeftButtonDown(self):
		if not self.Enable:
			return
		self.mouse.Down()

	def OnMouseLeftButtonUp(self):
		if not self.Enable:
			return
		self.mouse.Up()
		self.event()

class AdminTool(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		
		self.ACTION_BAN_PERMANENTLY = 0
		self.ACTION_BAN_IP = 1		
		self.ACTION_BAN_TIME = 2
		self.TYPE_MAX_NUM = 3

		self.Initialize()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Initialize(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/AdminTool.py")
		except:
			import exception
			exception.Abort("AdminTool.Initialize.LoadObject")
		try:
			self.GetChild("titlebar").SetCloseEvent(self.Close)
		except:
			import exception
			exception.Abort("AdminTool.Initialize.BindObject")

		self.main = {
			"board" : self.GetChild("board"),				
			"selected" : {},
			"btn_block" : self.GetChild("block_button"),
			"box_day" : self.GetChild("ban_result_day"),
			"box_hour" : self.GetChild("ban_result_hour"),
			"box_min" : self.GetChild("ban_result_minute"),
			"box_category_time" : [self.GetChild("ban_result_day_slot"), self.GetChild("ban_result_hour_slot"), self.GetChild("ban_result_minute_slot")],
			"user_name" : self.GetChild("ban_result_user_name"),
			"reason" : self.GetChild("ban_result_reason"),			
		}
	
		for key in xrange(self.TYPE_MAX_NUM):
			self.main["selected"].update({key : CheckBox(self, key, 10 + (key * 90), 120, lambda arg = key: self.OnSelectType(arg))})

		self.main["btn_block"].SAFE_SetEvent(self.OnRecvBanUser)	
		self.OnSelectType(self.ACTION_BAN_TIME)	
		self.SetCenterPosition()

	def GetTypeSelected(self):
		for i in xrange(self.TYPE_MAX_NUM):
			if self.main["selected"][i].IsSelected():
				return i

	def OnSelectType(self, key):
		for i in xrange(self.TYPE_MAX_NUM):
			if key == i:
				self.main["selected"][i].SetCheck(True)
			else:
				self.main["selected"][i].SetCheck(False)

		self.MakeInterface(self.GetTypeSelected())
		
	def MakeInterface(self, type):
			
		def appendBoxTime(key):
			for wnd in self.main["box_category_time"]:
				if key: 
					wnd.Show()
				else:
					wnd.Hide()

		if type in [self.ACTION_BAN_PERMANENTLY, self.ACTION_BAN_IP]:
			appendBoxTime(False)
			return

		appendBoxTime(True)

	def OnRecvBanUser(self):

		def div(type, key):
			return [key * 24 * 60 * 60, key * 60 * 60, key * 60][type - 1]

		def get(type, key):
			if type is "s":
				return str(self.main[key].GetText())

			return int(self.main[key].GetText())

		def callable(x, y, z):
			return x + y + z
			
		def tokens():
			return get("s", "user_name"), get("s", "reason"), get("i", "box_day"), get("i", "box_hour"), get("i", "box_min")

		user_name, reason, day, hour, minute = tokens()
		net.SendAdminBanManagerPacket(self.GetTypeSelected(), user_name, reason, callable(div(1, day), div(2, hour), div(3, minute)))

	def Destroy(self):
		self.ClearDictionary()

	def Close(self):
		self.Hide()

	def OnUpdate(self):
		(x, y) = wndMgr.GetMousePosition()

		def IsCursorSelected(key):
			return self.main["selected"][key].IsIn()

		for key in xrange(self.TYPE_MAX_NUM):
			if IsCursorSelected(key):
				self.toolTip = uiToolTip.ToolTip()
				self.toolTip.SetPosition(x + 25, y)
				self.toolTip.AppendDescription(BAN_DESCRIPTION_TYPE[key], None, 0xffffa879)	

	def Open(self):
		pass