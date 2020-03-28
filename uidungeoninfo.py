#(C) 2019 Owsap Productions
#V.1.0.8

import app
import ui
import dbg
import uiToolTip
import grp
import item
import player
import constInfo2
import localeInfo
import uiScriptLocale
import uiCommon

class DungeonInfo(ui.ScriptWindow):
	TOOLTIP_NORMAL_COLOR = grp.GenerateColor(0.9490, 0.9058, 0.7568, 1.0)
	TOOLTIP_SPECIAL_COLOR = grp.GenerateColor(1.0, 0.7843, 0.0, 1.0)
	MIN_SCROLLBAR_LIST = 10

	DUNGEON_TYPE = {
		0 : localeInfo.DUNGEON_INFO_TYPE0,
		1 : localeInfo.DUNGEON_INFO_TYPE1,
		2 : localeInfo.DUNGEON_INFO_TYPE2
	}

	DUNGEON_ORGANIZATION = {
		0 : localeInfo.DUNGEON_INFO_ORGANIZATION0,
		1 : localeInfo.DUNGEON_INFO_ORGANIZATION1,
		2 : localeInfo.DUNGEON_INFO_ORGANIZATION2
	}

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.dungeonIndex = 0
		self.dungeonButton = {}
		self.dungeonImage = {}
		self.dungeonImageIcon = {}
		self.dungeonName = {}
		self.questionDialog = None
		self.dungeonRankingIndex = None

		self.isLoaded = False

	def __del__(self):
		ui.ScriptWindow.__del__(self)

		self.dungeonIndex = 0
		self.dungeonButton = {}
		self.dungeonImage = {}
		self.dungeonImageIcon = {}
		self.dungeonName = {}
		self.questionDialog = None
		self.dungeonRankingIndex = None

		self.isLoaded = False

	def LoadDialog(self):
		try:
			dbg.TraceError("uidungeoninfo.py LoadDialog")
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/dungeoninfowindow.py")
		except:
			import exception
			exception.Abort("DungeonInfo.LoadDialog.LoadScript")

		try:
			self.dungeonBoard = self.GetChild("DungeonBoard")
			self.dungeonBoardTitleBar = self.GetChild("DungeonBoardTitleBar")

			self.dungeonButtonBoard = self.GetChild("DungeonButtonBoard")
			self.dungeonButtonThinBoard = self.GetChild("DungeonButtonThinBoard")

			self.dungeonInfoItem = self.GetChild("DungeonInfoItem")
			self.dungeonInfoItemSlot = self.GetChild("DungeonInfoItemSlot")

			self.dungeonScrollBar = self.GetChild("ScrollBar")
			self.dungeonInfoBoard = self.GetChild("DungeonInfoBoard")

			self.dungeonInfoName = self.GetChild("DungeonInfoName")
			self.dungeonInfoType = self.GetChild("DungeonInfoType")
			self.dungeonInfoOrganization = self.GetChild("DungeonInfoOrganization")
			self.dungeonInfoLevelLimit = self.GetChild("DungeonInfoLevelLimit")
			self.dungeonInfoPartyMembers = self.GetChild("DungeonInfoPartyMembers")
			self.dungeonInfoCooldown = self.GetChild("DungeonInfoCooldown")
			self.dungeonInfoDuration = self.GetChild("DungeonInfoDuration")
			self.dungeonInfoEntrance = self.GetChild("DungeonInfoEntrance")
			self.dungeonInfoStrengthBonus = self.GetChild("DungeonInfoStrengthBonus")
			self.dungeonInfoResistanceBonus = self.GetChild("DungeonInfoResistanceBonus")
			self.dungeonInfoTotalFinished = self.GetChild("DungeonInfoTotalFinished")
			self.dungeonInfoFastestTime = self.GetChild("DungeonInfoFastestTime")
			self.dungeonInfoHighestDamage = self.GetChild("DungeonInfoHighestDamage")

			self.dungeonInfoTeleportButton = self.GetChild("DungeonInfoTeleportButton")
			self.closeDungeonBoard = self.GetChild("CloseDungeonBoard")

			self.dungeonRank1Button = self.GetChild("DungeonRank1Button")
			self.dungeonRank2Button = self.GetChild("DungeonRank2Button")
			self.dungeonRank3Button = self.GetChild("DungeonRank3Button")

		except:
			import exception
			exception.Abort("DungeonInfo.LoadDialog.GetChild")

		self.dungeonBoardTitleBar.SetCloseEvent(ui.__mem_func__(self.Close))
		self.closeDungeonBoard.SetEvent(ui.__mem_func__(self.Close))
		self.dungeonInfoTeleportButton.SetEvent(self.TeleportDungeon)

		self.dungeonRank1Button.SetEvent(lambda arg = 1: self.OpenRankingBoard(arg))
		self.dungeonRank2Button.SetEvent(lambda arg = 2: self.OpenRankingBoard(arg))
		self.dungeonRank3Button.SetEvent(lambda arg = 3: self.OpenRankingBoard(arg))

		self.toolTip = uiToolTip.ToolTip()

		self.LoadDungeonButtons()
		self.LoadDungeonInfoBoard(self.dungeonIndex)

		self.isLoaded = True

	def Close(self):
		if self.toolTip:
			self.toolTip = None

		self.isLoaded = False
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def Open(self):
		dbg.TraceError("uidungeoninfo.py open")
		if not self.isLoaded:
			self.LoadDialog()

		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def LoadDungeonButtons(self):
		dbg.TraceError("uidungeoninfo.py LoadDungeonButtons")
		if not constInfo2.dungeonInfo:
			return

		for index in xrange(min(self.MIN_SCROLLBAR_LIST, len(constInfo2.dungeonInfo))):
			self.AppendDungeonButton(
				index,\
				self.dungeonButtonBoard,\
				3, 3 + (38 * index)
			)

		if len(constInfo2.dungeonInfo) <= self.MIN_SCROLLBAR_LIST:
			self.dungeonScrollBar.SetMiddleBarSize(float(len(constInfo2.dungeonInfo)) / float(len(constInfo2.dungeonInfo)))
			self.dungeonScrollBar.Show()
		else:
			self.dungeonScrollBar.SetMiddleBarSize(float(self.MIN_SCROLLBAR_LIST) / float(len(constInfo2.dungeonInfo)))
			self.dungeonScrollBar.Show()

		self.dungeonScrollBar.SetScrollEvent(self.OnScroll)

	def OnScroll(self):
		button_count = len(self.dungeonButton)
		pos = int(self.dungeonScrollBar.GetPos() * (len(constInfo2.dungeonInfo) - button_count))

		self.dungeonButton = {}
		self.dungeonImage = {}
		self.dungeonImageIcon = {}
		self.dungeonName = {}

		for idx in xrange(min(self.MIN_SCROLLBAR_LIST, button_count)):
			realPos = idx + pos

			self.AppendDungeonButton(
				realPos,\
				self.dungeonButtonBoard,\
				3, 3 + (38 * idx)
			)

			if realPos != self.dungeonIndex:
				self.dungeonButton[realPos].SetUpVisual("d:/ymir work/ui/game/mailbox/post_default.sub")
				self.dungeonButton[realPos].SetOverVisual("d:/ymir work/ui/game/mailbox/post_over.sub")
				self.dungeonButton[realPos].SetDownVisual("d:/ymir work/ui/game/mailbox/post_select.sub")

	def AppendDungeonButton(self, index, parent, x, y):
		self.dungeonButton[index] = ui.Button()
		self.dungeonButton[index].SetParent(parent)
		self.dungeonButton[index].SetUpVisual("d:/ymir work/ui/game/mailbox/post_select.sub")
		self.dungeonButton[index].SetOverVisual("d:/ymir work/ui/game/mailbox/post_select.sub")
		self.dungeonButton[index].SetDownVisual("d:/ymir work/ui/game/mailbox/post_select.sub")
		self.dungeonButton[index].SetPosition(x, y)
		self.dungeonButton[index].SetEvent(lambda: self.LoadDungeonInfoBoard(index))
		#self.dungeonButton[index].SetText("%d" % index)
		self.dungeonButton[index].Show()

		self.dungeonImage[index] = ui.ImageBox()
		self.dungeonImage[index].SetParent(self.dungeonButton[index])
		self.dungeonImage[index].LoadImage("d:/ymir work/ui/game/mailbox/mailbox_icon_empty.sub")
		self.dungeonImage[index].SetPosition(1, 2)
		self.dungeonImage[index].Show()

		self.dungeonImageIcon[index] = ui.Button()
		self.dungeonImageIcon[index].SetParent(self.dungeonImage[index])

		#imageIcon = constInfo2.dungeonInfo[index]['item_vnum']
		mapIndex = constInfo2.dungeonInfo[index]['map_index']
		#if imageIcon > 0:
		self.dungeonImageIcon[index].SetUpVisual("d:/ymir work/ui/game/dungeon_info/icons/%d.tga" % mapIndex)
		self.dungeonImageIcon[index].SetOverVisual("d:/ymir work/ui/game/dungeon_info/icons/%d.tga" % mapIndex)
		self.dungeonImageIcon[index].SetDownVisual("d:/ymir work/ui/game/dungeon_info/icons/%d.tga" % mapIndex)
		self.dungeonImageIcon[index].SetEvent(lambda: self.LoadDungeonInfoBoard(index))
		#else:
		#	self.dungeonImageIcon[index].SetUpVisual("d:/ymir work/ui/pet/skill_button/skill_enable_button.sub")
		#	self.dungeonImageIcon[index].SetOverVisual("d:/ymir work/ui/pet/skill_button/skill_enable_button.sub")
		#	self.dungeonImageIcon[index].SetDownVisual("d:/ymir work/ui/pet/skill_button/skill_enable_button.sub")

		self.dungeonImageIcon[index].SetPosition(0, 0)
		self.dungeonImageIcon[index].Show()

		self.dungeonName[index] = ui.TextLine()
		self.dungeonName[index].SetParent(self.dungeonButton[index])
		self.dungeonName[index].SetPosition(40, 10)
		self.dungeonName[index].SetText("%s" % constInfo2.dungeonInfo[index]['map'])
		self.dungeonName[index].Show()

	def LoadDungeonInfoBoard(self, index):
		dbg.TraceError("uidungeoninfo.py LoadDungeonInfoBoard")
		self.dungeonIndex = index

		self.dungeonButton[self.dungeonIndex].SetUpVisual("d:/ymir work/ui/game/mailbox/post_select.sub")
		self.dungeonButton[self.dungeonIndex].SetOverVisual("d:/ymir work/ui/game/mailbox/post_select.sub")
		self.dungeonButton[self.dungeonIndex].SetDownVisual("d:/ymir work/ui/game/mailbox/post_select.sub")

		pos = int(self.dungeonScrollBar.GetPos() * (len(constInfo2.dungeonInfo) - len(self.dungeonButton)))
		for idx in xrange(len(self.dungeonButton)):
			realPos = idx + pos
			if realPos != self.dungeonIndex:
				self.dungeonButton[realPos].SetUpVisual("d:/ymir work/ui/game/mailbox/post_default.sub")
				self.dungeonButton[realPos].SetOverVisual("d:/ymir work/ui/game/mailbox/post_over.sub")
				self.dungeonButton[realPos].SetDownVisual("d:/ymir work/ui/game/mailbox/post_select.sub")

		dungeonMap = str(constInfo2.dungeonInfo[self.dungeonIndex]['map'])
		dungeonType = constInfo2.dungeonInfo[self.dungeonIndex]['type']
		dungeonOrganization = constInfo2.dungeonInfo[self.dungeonIndex]['organization']
		dungeonLevelLimit = constInfo2.dungeonInfo[self.dungeonIndex]['level_limit']
		dungeonPartyMembers = constInfo2.dungeonInfo[self.dungeonIndex]['party_members']
		dungeonCooldown = constInfo2.dungeonInfo[self.dungeonIndex]['cooldown']
		dungeonDuration = constInfo2.dungeonInfo[self.dungeonIndex]['duration']
		dungeonEntranceMap = str(constInfo2.dungeonInfo[self.dungeonIndex]['entrance_map'])
		dungeonStrengthBonus = str(constInfo2.dungeonInfo[self.dungeonIndex]['strength_bonus'])
		dungeonResistanceBonus = str(constInfo2.dungeonInfo[self.dungeonIndex]['resistance_bonus'])
		dungeonItemVnum = int(constInfo2.dungeonInfo[self.dungeonIndex]['item_vnum'])
		dungeonFinished = int(constInfo2.dungeonInfo[self.dungeonIndex]['finished'])
		dungeonFastestTime = constInfo2.dungeonInfo[self.dungeonIndex]['fastest_time']
		dungeonHighestDamage = int(constInfo2.dungeonInfo[self.dungeonIndex]['highest_damage'])

		self.dungeonInfoName.SetText("%s" % dungeonMap)
		self.dungeonInfoType.SetText("%s : %s" % (uiScriptLocale.DUNGEON_INFO_TYPE, self.DUNGEON_TYPE[dungeonType]))
		self.dungeonInfoOrganization.SetText("%s : %s" % (uiScriptLocale.DUNGEON_INFO_ORGANIZATION, self.DUNGEON_ORGANIZATION[dungeonOrganization]))
		self.dungeonInfoLevelLimit.SetText("%s : %d - 120" % (uiScriptLocale.DUNGEON_INFO_LEVEL_LIMIT, dungeonLevelLimit))
		self.dungeonInfoPartyMembers.SetText("%s : %d" % (uiScriptLocale.DUNGEON_INFO_PARTY_MEMBERS, dungeonPartyMembers))
		self.dungeonInfoCooldown.SetText("%s : %s" % (uiScriptLocale.DUNGEON_INFO_COOLDOWN, self.FormatTime(dungeonCooldown)))
		self.dungeonInfoDuration.SetText("%s : %s" % (uiScriptLocale.DUNGEON_INFO_DURATION, self.FormatTime(dungeonDuration)))
		self.dungeonInfoEntrance.SetText("%s : %s" % (uiScriptLocale.DUNGEON_INFO_ENTRANCE, dungeonEntranceMap))
		self.dungeonInfoStrengthBonus.SetText("%s : %s" % (uiScriptLocale.DUNGEON_INFO_STRENGTH, dungeonStrengthBonus))
		self.dungeonInfoResistanceBonus.SetText("%s : %s" % (uiScriptLocale.DUNGEON_INFO_RESISTANCE, dungeonResistanceBonus))
		self.dungeonInfoTotalFinished.SetText("%s : %d" % (uiScriptLocale.DUNGEON_INFO_TOTAL_FINISHED, dungeonFinished))
		self.dungeonInfoFastestTime.SetText("%s : %s" % (uiScriptLocale.DUNGEON_INFO_FASTEST_TIME, self.FormatTime(dungeonFastestTime)))
		self.dungeonInfoHighestDamage.SetText("%s : %d" % (uiScriptLocale.DUNGEON_INFO_HIGHEST_DAMAGE, dungeonHighestDamage))

		if dungeonItemVnum > 0:
			self.dungeonInfoItemSlot.LoadImage("icon/item/%d.tga" % dungeonItemVnum)
		else:
			self.dungeonInfoItemSlot.LoadImage("d:/ymir work/ui/pet/skill_button/skill_enable_button.sub")

	def FormatTime(self, seconds):
		if seconds == 0:
			return localeInfo.DUNGEON_INFO_NONE

		m, s = divmod(seconds, 60)
		h, m = divmod(m, 60)

		return "%d:%02d:%02d" % (h, m, s)

	def TeleportDungeon(self):
		self.questionDialog = uiCommon.QuestionDialogWithTimeLimit()
		self.questionDialog.Open("Queres teleportar para %s?" % str(constInfo2.dungeonInfo[self.dungeonIndex]['map']), 5)
		self.questionDialog.SetAcceptText(localeInfo.UI_ACCEPT)
		self.questionDialog.SetCancelText(localeInfo.UI_DENY)
		self.questionDialog.SetAcceptEvent(lambda arg = True: self.AnswerTeleport(arg))
		self.questionDialog.SetCancelEvent(lambda arg = False: self.AnswerTeleport(arg))
		self.questionDialog.SetCancelOnTimeOver()
		self.questionDialog.SetTop()

	def AnswerTeleport(self, answer):
		if not self.questionDialog:
			return

		if answer == True:
			import event

			dungeonMapCoordX = int(constInfo2.dungeonInfo[self.dungeonIndex]['map_coord_x'])
			dungeonMapCoordY = int(constInfo2.dungeonInfo[self.dungeonIndex]['map_coord_y'])

			constInfo2.dungeonData["quest_cmd"] = "WARP#%d#%d" % (dungeonMapCoordX, dungeonMapCoordY)
			event.QuestButtonClick(int(constInfo2.dungeonData["quest_index"]))

		self.questionDialog.Close()
		self.questionDialog = None

	def OpenRankingBoard(self, rankType):
		dbg.TraceError("uidungeoninfo.py OpenRankingBoard")
		if rankType > 0:
			import event
			constInfo2.dungeonData["quest_cmd"] = "RANKING#%d#%d" % (self.dungeonIndex, rankType)
			constInfo2.dungeonRanking["ranking_type"] = rankType
			event.QuestButtonClick(int(constInfo2.dungeonData["quest_index"]))

	def OnUpdate(self):
		dbg.TraceError("uidungeoninfo.py OnUpdate")
		if self.toolTip:
			if self.dungeonInfoItemSlot.IsIn():
				self.toolTip.ClearToolTip()

				dungeonItemVnum = constInfo2.dungeonInfo[self.dungeonIndex]['item_vnum']
				if dungeonItemVnum > 0:
					item.SelectItem(dungeonItemVnum)

					self.toolTip.AppendTextLine(item.GetItemName(), self.TOOLTIP_SPECIAL_COLOR)
					self.toolTip.AppendDescription(item.GetItemDescription(), 26)

					self.toolTip.AlignHorizonalCenter()
					self.toolTip.ShowToolTip()

			else:
				self.toolTip.HideToolTip()

class DungeonRank(ui.ScriptWindow):
	SLOT_RANKING = 0
	SLOT_PLAYER_NAME = 1
	SLOT_PLAYER_LEVEL = 2
	SLOT_POINT_TYPE = 3

	MAX_LINE_COUNT = 5

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.NowStartLineNumber = 0
		self.dungeonRankingScrollBar = None
		self.ResultButtonList = []
		self.ResultSlotList = {}
		self.MyResultSlotList = []

		self.isLoaded = False

	def __del__(self):
		ui.ScriptWindow.__del__(self)

		self.NowStartLineNumber = 0
		self.dungeonRankingScrollBar = None
		self.ResultButtonList = []
		self.ResultSlotList = {}
		self.MyResultSlotList = []

		self.isLoaded = False

	def LoadDialog(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/dungeonrankingwindow.py")
		except:
			import exception
			exception.Abort("DungeonRank.LoadDialog.LoadScript")

		try:
			self.dungeonRankingTitleBar = self.GetChild("DungeonRankingTitleBar")
			self.dungeonRankingTitleName = self.GetChild("DungeonRankingTitleName")
			self.dungeonRankingScrollBar = self.GetChild("DungeonRankingScrollBar")

			self.dungeonRankingResultPosition = self.GetChild("ResultRanking")
			self.dungeonRankingResultName = self.GetChild("ResultName")
			self.dungeonRankingResultLevel = self.GetChild("ResultLevel")
			self.dungeonRankingResultPoints = self.GetChild("ResultPoints")

		except:
			import exception
			exception.Abort("DungeonRank.__LoadWindow.SetObject")

		self.dungeonRankingTitleBar.SetCloseEvent(ui.__mem_func__(self.Close))
		self.dungeonRankingScrollBar.SetScrollEvent(ui.__mem_func__(self.OnScrollControl))

		self.MakeUiBoard()
		self.RefreshDungeonRanking()

		self.isLoaded = True

	def MakeUiBoard(self):
		try:
			yPos = 0
			for i in range(0, self.MAX_LINE_COUNT+1):
				yPos = 65 + i * 24
				if i == 5:
					yPos += 10

				## ¼øÀ§
				RankingSlotImage = ui.MakeImageBox(self, "d:/ymir work/ui/public/parameter_slot_00.sub", 23, yPos)
				RankingSlotImage.SetAlpha(0)
				RankingSlot = ui.MakeTextLine(RankingSlotImage)
				self.Children.append(RankingSlotImage)
				self.Children.append(RankingSlot)

				## ±æµå¸í
				GuildNameImage = ui.MakeImageBox(self, "d:/ymir work/ui/public/parameter_slot_04.sub", 77, yPos)
				GuildNameImage.SetAlpha(0)
				GuildNameSlot = ui.MakeTextLine(GuildNameImage)
				self.Children.append(GuildNameImage)
				self.Children.append(GuildNameSlot)

				## Âü¿©ÀÎ¿ø
				MemberCountSlotImage = ui.MakeImageBox(self, "d:/ymir work/ui/public/parameter_slot_00.sub", 205, yPos)
				MemberCountSlotImage.SetAlpha(0)
				MemberCountSlot = ui.MakeTextLine(MemberCountSlotImage)
				self.Children.append(MemberCountSlotImage)
				self.Children.append(MemberCountSlot)

				## Å¬¸®¾î ½Ã°£
				ClearTimeSlotImage = ui.MakeImageBox(self, "d:/ymir work/ui/public/parameter_slot_00.sub", 270, yPos)
				ClearTimeSlotImage.SetAlpha(0)
				ClearTimeSlot = ui.MakeTextLine(ClearTimeSlotImage)
				self.Children.append(ClearTimeSlotImage)
				self.Children.append(ClearTimeSlot)

				if i < self.MAX_LINE_COUNT:
					tempguildlankingslotlist = []
					tempguildlankingslotlist.append(RankingSlot)

					tempguildlankingslotlist.append(GuildNameSlot)
					tempguildlankingslotlist.append(MemberCountSlot)
					tempguildlankingslotlist.append(ClearTimeSlot)
					self.ResultSlotList[i] = tempguildlankingslotlist
				else:
					self.MyResultSlotList.append(RankingSlot)
					self.MyResultSlotList.append(GuildNameSlot)
					self.MyResultSlotList.append(MemberCountSlot)
					self.MyResultSlotList.append(ClearTimeSlot)

				## °á°ú ¸ñ·Ï ¹öÆ°
				itemSlotButtonImage = ui.MakeButton(self, 21, yPos, "", "d:/ymir work/ui/game/guild/dragonlairranking/", "ranking_list_button01.sub", "ranking_list_button02.sub", "ranking_list_button02.sub")
				itemSlotButtonImage.Show()
				itemSlotButtonImage.Disable()
				self.Children.append(itemSlotButtonImage)

				if i < self.MAX_LINE_COUNT:
					self.ResultButtonList.append(itemSlotButtonImage)

		except:
			import exception
			exception.Abort("GuildWindow_GuildDragonLairWindow.MakeUiBoard")

	def RefreshDungeonRanking(self):
		self.AllClear()

		dungeonRankingType = constInfo2.dungeonRanking["ranking_type"]
		dungeonRankingList = constInfo2.dungeonRanking["ranking_list"]

		if not dungeonRankingList:
			return

		if dungeonRankingType == 1:
			self.dungeonRankingTitleName.SetText(uiScriptLocale.DUNGEON_RANKING_TYPE1)
			self.dungeonRankingResultPoints.SetText(uiScriptLocale.DUNGEON_RANKING_POINT_TYPE1)
		elif dungeonRankingType == 2:
			self.dungeonRankingTitleName.SetText(uiScriptLocale.DUNGEON_RANKING_TYPE2)
			self.dungeonRankingResultPoints.SetText(uiScriptLocale.DUNGEON_RANKING_POINT_TYPE2)
		elif dungeonRankingType == 3:
			self.dungeonRankingTitleName.SetText(uiScriptLocale.DUNGEON_RANKING_TYPE3)
			self.dungeonRankingResultPoints.SetText(uiScriptLocale.DUNGEON_RANKING_POINT_TYPE3)

		for line, ResultSlotList in self.ResultSlotList.items():
			nowindex = line + self.NowStartLineNumber

			if nowindex >= len(dungeonRankingList):
				break

			rankingData = dungeonRankingList[nowindex]

			ResultSlotList[self.SLOT_RANKING].SetText(str(nowindex+1))
			ResultSlotList[self.SLOT_PLAYER_NAME].SetText(str(rankingData[0]))
			ResultSlotList[self.SLOT_PLAYER_LEVEL].SetText(str(rankingData[1]))
			if dungeonRankingType == 2:
				ResultSlotList[self.SLOT_POINT_TYPE].SetText(self.FormatTime(rankingData[2]))
			else:
				ResultSlotList[self.SLOT_POINT_TYPE].SetText(str(rankingData[2]))
			self.ResultButtonList[line].Show()

		self.MyResultSlotList[self.SLOT_RANKING].SetText("-")
		self.MyResultSlotList[self.SLOT_PLAYER_NAME].SetText("-")
		self.MyResultSlotList[self.SLOT_PLAYER_LEVEL].SetText("-")
		self.MyResultSlotList[self.SLOT_POINT_TYPE].SetText("-")

		self.dungeonRankingScrollBar.SetMiddleBarSize(float(self.MAX_LINE_COUNT) / float(self.CheckNowItemCount()))

	def FormatTime(self, seconds):
		if seconds == 0:
			return 0

		m, s = divmod(seconds, 60)
		h, m = divmod(m, 60)

		return "%d:%02d:%02d" % (h, m, s)

	def AllClear(self):
		for line, ResultSlotList in self.ResultSlotList.items():
			ResultSlotList[self.SLOT_RANKING].SetText("")
			ResultSlotList[self.SLOT_PLAYER_NAME].SetText("")
			ResultSlotList[self.SLOT_PLAYER_LEVEL].SetText("")
			ResultSlotList[self.SLOT_POINT_TYPE].SetText("")
			self.ResultButtonList[line].SetUp()
			self.ResultButtonList[line].Hide()

		self.MyResultSlotList[self.SLOT_RANKING].SetText("-")
		self.MyResultSlotList[self.SLOT_PLAYER_NAME].SetText("-")
		self.MyResultSlotList[self.SLOT_PLAYER_LEVEL].SetText("-")
		self.MyResultSlotList[self.SLOT_POINT_TYPE].SetText("-")

	def Close(self):
		self.isLoaded = False
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def CheckNowItemCount(self):
		if len(constInfo2.dungeonRanking["ranking_list"]) <= self.MAX_LINE_COUNT:
			return self.MAX_LINE_COUNT
		else:
			return len(constInfo2.dungeonRanking["ranking_list"])

	def OnScrollControl(self):
		nowitemcount = 0
		if len(constInfo2.dungeonRanking["ranking_list"]) <= self.MAX_LINE_COUNT :
			nowitemcount = 0
		else:
			nowitemcount = (len(constInfo2.dungeonRanking["ranking_list"]) - self.MAX_LINE_COUNT)

		pos = self.dungeonRankingScrollBar.GetPos() * nowitemcount

		if not int(pos) == self.NowStartLineNumber:
			self.NowStartLineNumber = int(pos)
			self.RefreshDungeonRanking()

	def Open(self):
		if not self.isLoaded:
			self.LoadDialog()

		self.NowStartLineNumber = 0
		self.dungeonRankingScrollBar.SetPos(0)

		self.SetCenterPosition()
		self.SetTop()
		self.Show()