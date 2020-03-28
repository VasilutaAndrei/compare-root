import ui
import os
import net
import snd
import dbg
import app
import uiTip
import player
import constInfo
import uiToolTip
import localeInfo
import uiScriptLocale

STAT = 0

COLOR1 = 0xff5F0303
COLOR2 = 0xff035F31

class Board(ui.BoardWithTitleBar):
	def __init__(self):
		ui.BoardWithTitleBar.__init__(self)
		self.LoadBoard()

	def __del__(self):
		ui.BoardWithTitleBar.__del__(self)

	def Destroy(self):
		self.Hide()
		return TRUE

	def LoadBoard(self):
		self.SetSize(200, 5 * 94)
		self.Show()
		self.AddFlag("movable")
		self.AddFlag("float")
		self.SetTitleName(uiScriptLocale.TITLE_SYSTEM)
		self.SetCenterPosition()
		self.SetCloseEvent(self.Close)
		
		self.TitleText = ui.TextLine()
		self.TitleText.SetParent(self)
		self.TitleText.SetPosition(0, 55)
		self.TitleText.SetText(uiScriptLocale.TITLE_SYSTEM_CHOOSE)
		self.TitleText.SetWindowHorizontalAlignCenter()
		self.TitleText.SetHorizontalAlignCenter()
		self.TitleText.Show()
		
		self.TitleListBase = ui.SlotBar()
		self.TitleListBase.SetParent(self)
		self.TitleListBase.SetSize(200 - 40, 385)
		self.TitleListBase.SetPosition(19, 44)
		self.TitleListBase.Show()
		
		self.TitleList = ui.ListBox()
		self.TitleList.SetParent(self.TitleListBase)
		self.TitleList.SetSize(200 - 57, 381)
		self.TitleList.SetPosition(0, 0)
		self.TitleList.Show()
		
		self.TitleListScrollBar = ui.ScrollBar()
		self.TitleListScrollBar.SetParent(self.TitleListBase)
		self.TitleListScrollBar.SetPosition(19, 7)
		self.TitleListScrollBar.SetScrollBarSize(130)
		self.TitleListScrollBar.SetWindowHorizontalAlignRight()
		self.TitleListScrollBar.SetScrollEvent(ui.__mem_func__(self.OnScrollList))
		self.TitleListScrollBar.Hide()
		
		self.TitleList.ClearItem()
		DICT = {0 : localeInfo.TITILE_NAME_0, 1 : localeInfo.TITILE_NAME_1, 2 : localeInfo.TITILE_NAME_2, 3 : localeInfo.TITILE_NAME_3, 4 : localeInfo.TITILE_NAME_4, 5 : localeInfo.TITILE_NAME_5, 6 : localeInfo.TITILE_NAME_6, 7 : localeInfo.TITILE_NAME_7, 8 : localeInfo.TITILE_NAME_8, 9 : localeInfo.TITILE_NAME_9, 10 : localeInfo.TITILE_NAME_10, 11 : localeInfo.TITILE_NAME_11, 12 : localeInfo.TITILE_NAME_12, 13 : localeInfo.TITILE_NAME_13, 14 : localeInfo.TITILE_NAME_14, 15 : localeInfo.TITILE_NAME_15, 16 : localeInfo.TITILE_NAME_16, 17 : localeInfo.TITILE_NAME_17, 18 : localeInfo.TITILE_NAME_18, 19 : localeInfo.TITILE_NAME_19, 20 : localeInfo.TITILE_NAME_20}
		for i in xrange(21):			
			self.TitleList.InsertItem(i, "%s" % (DICT[i]))
		self.TitleList.SAFE_SetStringEvent("MOUSE_OVER_IN", self.ShowToolTip)
		self.TitleList.SAFE_SetStringEvent("MOUSE_OVER_OUT", self.HideToolTip)
		
		self.ChooseButton = ui.Button()
		self.ChooseButton.SetParent(self)
		self.ChooseButton.SetPosition(100 - 40, 437)
		self.ChooseButton.SetUpVisual("d:/ymir work/ui/public/Large_button_01.sub")
		self.ChooseButton.SetOverVisual("d:/ymir work/ui/public/Large_button_02.sub")
		self.ChooseButton.SetDownVisual("d:/ymir work/ui/public/Large_button_03.sub")
		# self.ChooseButton.SetEvent(lambda : self.__ClickTitleButton(a, b))
		self.ChooseButton.SetEvent(lambda : self.__ClickTitleButton())
		self.ChooseButton.SetText(localeInfo.TITILE_CHOOSE)
		self.ChooseButton.ButtonText.SetFontColor(1, 1, 1)
		self.ChooseButton.Show()
		
		self.toolTip = uiToolTip.ToolTip(130)
		self.toolTip.ClearToolTip()

	def ShowToolTip(self, line = 0):
		if self.toolTip:
			line = self.TitleList.GetOverLine()
			if line > 0:
				self.toolTip.ClearToolTip()
				DICT = {0 : localeInfo.TITILE_DESC_0, 1 : localeInfo.TITILE_DESC_1, 2 : localeInfo.TITILE_DESC_2, 3 : localeInfo.TITILE_DESC_3, 4 : localeInfo.TITILE_DESC_4, 5 : localeInfo.TITILE_DESC_5, 6 : localeInfo.TITILE_DESC_6, 7 : localeInfo.TITILE_DESC_7, 8 : localeInfo.TITILE_DESC_8, 9 : localeInfo.TITILE_DESC_9, 10 : localeInfo.TITILE_DESC_10, 11 : localeInfo.TITILE_DESC_11, 12 : localeInfo.TITILE_DESC_12, 13 : localeInfo.TITILE_DESC_13, 14 : localeInfo.TITILE_DESC_14, 15 : localeInfo.TITILE_DESC_15, 16 : localeInfo.TITILE_DESC_16, 17 : localeInfo.TITILE_DESC_17, 18 : localeInfo.TITILE_DESC_18, 19 : localeInfo.TITILE_DESC_19, 20 : localeInfo.TITILE_DESC_20}
				DICT2 = {1 : localeInfo.TITILE_BNS_1, 2 : localeInfo.TITILE_BNS_2, 3 : localeInfo.TITILE_BNS_3, 4 : localeInfo.TITILE_BNS_4, 5 : localeInfo.TITILE_BNS_5, 6 : localeInfo.TITILE_BNS_6, 7 : localeInfo.TITILE_BNS_7, 8 : localeInfo.TITILE_BNS_8, 9 : localeInfo.TITILE_BNS_9, 10 : localeInfo.TITILE_BNS_10, 11 : localeInfo.TITILE_BNS_11, 12 : localeInfo.TITILE_BNS_12, 13 : localeInfo.TITILE_BNS_13, 14 : localeInfo.TITILE_BNS_14, 15 : localeInfo.TITILE_BNS_15, 16 : localeInfo.TITILE_BNS_16, 17 : localeInfo.TITILE_BNS_17, 18 : localeInfo.TITILE_BNS_18, 19 : localeInfo.TITILE_BNS_19, 20 : localeInfo.TITILE_BNS_20}
				self.toolTip.AutoAppendTextLine(DICT[line])
				self.toolTip.AutoAppendTextLine(DICT2[line], COLOR2)
				self.toolTip.AlignHorizonalCenter()
				self.toolTip.ShowToolTip()
			else:
				self.toolTip.ClearToolTip()
				self.toolTip.HideToolTip()

	def HideToolTip(self):
		if self.toolTip:
			self.toolTip.ClearToolTip()
			self.toolTip.HideToolTip()

	def OnScrollList(self):
		viewItemCount = self.TitleList.GetViewItemCount()
		itemCount = self.TitleList.GetItemCount()
		pos = self.TitleListScrollBar.GetPos() * (itemCount - viewItemCount)
		self.TitleList.SetBasePos(int(pos))

	def Open(self):
		global STAT
		if not STAT:
			STAT = 1
			self.Show()
		else:
			return

	def __ClickTitleButton(self):
		titleID = self.TitleList.GetSelectedItem()
		
		player.ChooseTitle(titleID)

	def Close(self):
		global STAT
		if STAT:
			STAT = 0
		
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return TRUE

