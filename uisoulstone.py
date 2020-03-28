import ui
import net
import chat
import playerSettingModule
import chr
import skill
import player
import app

MAX_SKILL_COUNT = 6

ITEM_SOULSTONE_VNUM = 50513
ITEM_EXORZISMUS_VNUM = 71001
ITEM_PROBABILITY_VNUM = 71094

class SoulStoneBoard(ui.ScriptWindow):

	class BlockTextLineShower(ui.Window):

		def __init__(self):
			ui.Window.__init__(self)

			self.scrollBar = ui.ScrollBar()
			self.scrollBar.SetParent(self)
			self.scrollBar.SetScrollEvent(self.OnScroll)

			self.lastLineColor = {"r":0.0,"g":0.0,"b":0.0}

			self.Clear()

		def SetSize(self, width, height):
			ui.Window.SetSize(self, width, height)
			self.scrollBar.SetScrollBarSize(self.GetHeight())
			self.scrollBar.SetPosition(width - self.scrollBar.GetWidth(), 0)

		def SetLastLineColor(self, r, g, b):
			self.lastLineColor = {"r":float(r),"g":float(g),"b":float(b)}

		def Clear(self):
			self.textLineList = []
			self.textBlocks = []
			self.currentBlock = 0
			self.lastShowTime = 0
			self.y = 0
			self.basePos = 0
			self.canWrite = FALSE
			self.scrollBar.Hide()

		def GetBaseY(self):
			return self.basePos * 17

		def IsWriting(self):
			return self.canWrite == TRUE

		def OnScroll(self):
			pos = self.scrollBar.GetPos()
			self.__SetBasePos(pos * (len(self.textLineList) - 1 - (self.GetHeight() / 17)))

		def __SetBasePos(self, basePos):
			if int(basePos) == self.basePos:
				return
			self.basePos = int(basePos)
			self.RefreshLines()

		def AddBlock(self, text, resetShowTime = FALSE):
			self.textBlocks.append(text + "[ENTER]")
			self.canWrite = TRUE
			if resetShowTime == TRUE:
				self.lastShowTime = app.GetTime()

		def __AddTextLine(self):
			textLine = ui.TextLine()
			textLine.SetParent(self)
			textLine.SetPosition(0, self.y)
			textLine.SetWindowHorizontalAlignCenter()
			textLine.SetHorizontalAlignCenter()
			textLine.REAL_Y = self.y
			textLine.Show()
			self.textLineList.append(textLine)

			self.y += 17

			return self.textLineList[len(self.textLineList) - 1]

		def __WriteBlock(self):
			if self.canWrite == FALSE:
				return

			text = self.textBlocks[self.currentBlock]
			pos = text.find("[ENTER]")

			line = None

			while pos > -1:
				currentText = text[:pos]
				text = text[pos+len("[ENTER]"):]
				pos = text.find("[ENTER]")

				writtenText = ""
				line = self.__AddTextLine()
				while currentText != "":
					subpos = currentText.find(" ")
					if subpos == -1:
						addText = currentText
						currentText = ""
					else:
						addText = currentText[:subpos]
						currentText = currentText[subpos+len(" "):]

					line.SetText(writtenText + " " + addText)
					if len(writtenText) > 0 and line.GetTextWidth() > self.GetWidth() - self.scrollBar.GetWidth() - 20:
						line.SetText(writtenText)
						line = self.__AddTextLine()
						line.SetText(addText)
						writtenText = addText
					else:
						writtenText += " " + addText

			if pos == -1 and line != None and len(self.textBlocks) == self.currentBlock+1:
				line.SetFontColor(self.lastLineColor["r"], self.lastLineColor["g"], self.lastLineColor["b"])

			if len(self.textLineList) > 0:
				if (len(self.textLineList) - 1) * 17 + self.textLineList[len(self.textLineList) - 1].GetTextHeight() > self.GetHeight():
					self.scrollBar.Show()
					self.scrollBar.SetPos(1.0)
				else:
					self.scrollBar.Hide()

			self.currentBlock += 1

			self.RefreshLines()

			if self.currentBlock == len(self.textBlocks):
				self.canWrite = FALSE

		def RefreshLines(self):
			for i in xrange(len(self.textLineList)):
				line = self.textLineList[i]
				if line.REAL_Y < self.GetBaseY() or line.REAL_Y + line.GetTextHeight() > self.GetBaseY() + self.GetHeight():
					line.Hide()
				else:
					line.SetPosition(0, line.REAL_Y - self.GetBaseY())
					line.Show()

		def OnUpdate(self):
			if self.canWrite == TRUE:
				if app.GetTime() - 1.2 > self.lastShowTime:
					self.__WriteBlock()
					self.lastShowTime = app.GetTime()

	ITEM_EXORZISMUS_SLOT = 0
	ITEM_PROBABILITY_SLOT = 1

	ITEM_VNUM_BY_SLOT_INDEX = {
		ITEM_EXORZISMUS_SLOT : ITEM_EXORZISMUS_VNUM,
		ITEM_PROBABILITY_SLOT : ITEM_PROBABILITY_VNUM,
	}

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.selectedInventoryIndex = -1

		self.skillIndexList = []
		self.activeSkillIndex = {"slot":-1,"real":0,}
		self.itemSlotActive = {self.ITEM_EXORZISMUS_SLOT : FALSE, self.ITEM_PROBABILITY_SLOT : FALSE, }
		self.hasAffect = {self.ITEM_EXORZISMUS_SLOT : FALSE, self.ITEM_PROBABILITY_SLOT : FALSE, }
		self.waitForResult = FALSE

		self.__Load()

	def __del__(self):
		ui.ScriptWindow.__del__(self)
		print " -------------------------------------- DELETE SOUL STONE BOARD"

	def Destroy(self):
		self.ClearDictionary()
		print " -------------------------------------- DESTROY SOUL STONE BOARD"

	def __Load_LoadScript(self, fileName):
		try:
			pyScriptLoader = ui.PythonScriptLoader()
			pyScriptLoader.LoadScriptFile(self, fileName)
		except:
			import exception
			exception.Abort("SoulStoneBoard.__Load_LoadScript")

	def __Load_BindObject(self):
		try:
			GetObject = self.GetChild
			self.board = GetObject("board")
			self.main = {
				"skill_slot" : GetObject("skill_slot"),
				"item_slot" : GetObject("item_slot"),
				"button" : GetObject("button"),
			}
		except:
			import exception
			exception.Abort("SoulStoneBoard.__Load_BindObject")

		self.board.SetCloseEvent(self.Close)

		self.main["skill_slot"].SAFE_SetButtonEvent("LEFT", "EXIST", self.OnClickSkillSlot)
		self.main["skill_slot"].SAFE_SetButtonEvent("RIGHT", "EXIST", self.OnClickSkillSlot)

		self.main["item_slot"].SetItemSlot(self.ITEM_EXORZISMUS_SLOT, ITEM_EXORZISMUS_VNUM)
		self.main["item_slot"].SetItemSlot(self.ITEM_PROBABILITY_SLOT, ITEM_PROBABILITY_VNUM)
		self.main["item_slot"].SAFE_SetButtonEvent("LEFT", "EXIST", self.OnClickItemSlot)
		self.main["item_slot"].SAFE_SetButtonEvent("RIGHT", "EXIST", self.OnClickItemSlot)

		self.main["button"].SAFE_SetEvent(self.OnClickButton)

		self.rapidTextLine = self.BlockTextLineShower()
		self.rapidTextLine.SetParent(self)
		self.rapidTextLine.SetPosition(0, 38 + 32 + 10 + 32 + 10 + 10)
		self.rapidTextLine.SetSize(self.GetWidth() - 20 * 2, 80)
		self.rapidTextLine.SetWindowHorizontalAlignCenter()
		self.rapidTextLine.Show()

	def __Load(self):
		self.__Load_LoadScript("uiscript/soulstoneboard.py")
		self.__Load_BindObject()

	def Open(self, soulStoneIndex = -1):
		if net.GetMainActorSkillGroup() == 0:
			chat.AppendChat(chat.CHAT_TYPE_INFO, "Du musst erst eine Klasse wählen.")
			return
		self.RefreshSkill()
		if len(self.skillIndexList) == 0:
			chat.AppendChat(chat.CHAT_TYPE_INFO, "Du benötigst eine Fertigkeit auf Großmeister um einen Seelenstein zu benutzen.")
			return
		self.selectedInventoryIndex = soulStoneIndex
		self.rapidTextLine.Clear()
		self.SetSize(self.GetWidth(), 150)
		self.main["button"].SetPosition(self.main["button"].GetLeft(), self.GetHeight() - 21 - 15)
		self.Show()

	def Close(self):
		self.Hide()

	def SetSize(self, width, height):
		ui.Window.SetSize(self, width, height)
		try:
			self.board.SetSize(width, height)
		except AttributeError:
			pass

	def OnPressEscapeKey(self):
		self.Close()
		return TRUE

	def SetAffectExoFlag(self, flag):
		self.hasAffect[self.ITEM_EXORZISMUS_SLOT] = flag
		self.CheckItem()

	def SetAffectProbFlag(self, flag):
		self.hasAffect[self.ITEM_PROBABILITY_SLOT] = flag
		self.CheckItem()

	def CheckSkillChange(self):
		skillIndexList = []

		for i in xrange(MAX_SKILL_COUNT):

			skillIndex = player.GetSkillIndex(i + 1)
			skillGrade = player.GetSkillGrade(i + 1)

			if 0 != skillIndex and skillGrade == 2:
				skillIndexList.append(skillIndex)

		if len(skillIndexList) != len(self.skillIndexList):
			return TRUE

		for i in xrange(len(skillIndexList)):
			if skillIndexList[i] != self.skillIndexList[i]:
				return TRUE

		return FALSE

	def RefreshSkill(self):
		if not self.CheckSkillChange():
			return

		hiddenSlots = 0
		skillCount = 0
		self.skillIndexList = []

		findActiveSlot = FALSE

		for i in xrange(MAX_SKILL_COUNT):

			self.main["skill_slot"].DeactivateSlot(i)

			skillIndex = player.GetSkillIndex(i + 1)
			skillGrade = player.GetSkillGrade(i + 1)
			skillLevel = player.GetSkillLevel(i + 1)

			if 0 == skillIndex or skillGrade != 2: # skillGrade != SKILL_GRADE_GRANDMASTER
				self.main["skill_slot"].ClearSlot(MAX_SKILL_COUNT - hiddenSlots - 1)
				self.main["skill_slot"].HideSlotBaseImage(MAX_SKILL_COUNT - hiddenSlots - 1)
				hiddenSlots += 1
				continue

			self.main["skill_slot"].SetSkillSlotNew(skillCount, skillIndex, skillGrade, skillLevel)
			self.main["skill_slot"].SetSlotCountNew(skillCount, skillGrade, skillLevel)
			self.main["skill_slot"].SetCoverButton(skillCount)

			self.main["skill_slot"].ShowSlotBaseImage(skillCount)

			if self.activeSkillIndex["real"] == skillIndex:
				findActiveSlot = TRUE
				self.activeSkillIndex["slot"] = skillCount

				self.main["skill_slot"].ActivateSlot(skillCount)

			skillCount += 1
			self.skillIndexList.append(skillIndex)

		if findActiveSlot == FALSE:
			self.activeSkillIndex = {"slot":-1,"real":0,}

		if skillCount == 0:
			return

		self.main["skill_slot"].SetSize(32 * skillCount + (5 * skillCount - 1), self.main["skill_slot"].GetHeight())
		self.main["skill_slot"].UpdateRect()

	def OnClickSkillSlot(self, index):
		if self.activeSkillIndex["slot"] != -1:
			self.main["skill_slot"].DeactivateSlot(self.activeSkillIndex["slot"])
			if self.activeSkillIndex["slot"] == index:
				self.activeSkillIndex = {"slot":-1,"real":0,}
				return

		self.activeSkillIndex = {"slot":index,"real":self.skillIndexList[index],}
		self.main["skill_slot"].ActivateSlot(index)

	def OnClickItemSlot(self, index):
		if self.itemSlotActive[index] == TRUE:
			self.main["item_slot"].DeactivateSlot(index)
			self.itemSlotActive[index] = FALSE
		else:
			if self.FindInInventory(self.ITEM_VNUM_BY_SLOT_INDEX[index]) == -1:
				chat.AppendChat(chat.CHAT_TYPE_INFO, "Du besitzt diesen Gegenstand nicht.")
				return
			self.main["item_slot"].ActivateSlot(index)
			self.itemSlotActive[index] = TRUE

	def FindInInventory(self, vnum):
		for i in xrange(player.INVENTORY_PAGE_SIZE * player.INVENTORY_PAGE_COUNT):
			if player.GetItemIndex(i) == vnum:
				return i
		return -1

	def CheckItem(self):
		for key in self.itemSlotActive:
			if self.itemSlotActive[key] == TRUE and self.hasAffect[key] == FALSE:
				if self.FindInInventory(self.ITEM_VNUM_BY_SLOT_INDEX[key]) == -1:
					self.main["item_slot"].DeactivateSlot(key)
					self.itemSlotActive[key] = FALSE
			elif self.itemSlotActive[key] == FALSE and self.itemSlotActive[key] == TRUE:
				self.main["item_slot"].ActivateSlot(key)
				self.itemSlotActive[key] = TRUE

	def OnUpdate(self):
		self.RefreshSkill()
		self.CheckItem()

	def OnClickButton(self):
		if self.waitForResult == TRUE:
			return

		if self.rapidTextLine.IsWriting():
			chat.AppendChat(chat.CHAT_TYPE_INFO, "Warte noch etwas, bevor du den nächsten Seelenstein einsetzt.")
			return

		if self.activeSkillIndex["real"] == 0:
			chat.AppendChat(chat.CHAT_TYPE_INFO, "Du musst erst eine Fertigkeit wählen.")
			return

		if self.selectedInventoryIndex == -1:
			soulStonePos = self.FindInInventory(ITEM_SOULSTONE_VNUM)
		else:
			soulStonePos = self.selectedInventoryIndex
			if player.GetItemIndex(soulStonePos) != ITEM_SOULSTONE_VNUM:
				soulStonePos = self.FindInInventory(ITEM_SOULSTONE_VNUM)
		if soulStonePos == -1:
			chat.AppendChat(chat.CHAT_TYPE_INFO, "Du benötigst einen Seelenstein.")
			return
		if self.itemSlotActive[self.ITEM_EXORZISMUS_SLOT] == TRUE and self.hasAffect[self.ITEM_EXORZISMUS_SLOT] == FALSE:
			pos = self.FindInInventory(ITEM_EXORZISMUS_VNUM)
			if pos == -1:
				chat.AppendChat(chat.CHAT_TYPE_INFO, "Du hast keine Exorzismus-Schriftrolle.")
				return
			net.SendItemUsePacket(pos)
		if self.itemSlotActive[self.ITEM_PROBABILITY_SLOT] == TRUE and self.hasAffect[self.ITEM_PROBABILITY_SLOT] == FALSE:
			pos = self.FindInInventory(ITEM_PROBABILITY_VNUM)
			if pos == -1:
				chat.AppendChat(chat.CHAT_TYPE_INFO, "Du hast kein konzentriertes Lesen.")
				return
			net.SendItemUsePacket(pos)
		net.SendItemUsePacket(soulStonePos)
		net.SendQuestInputStringPacket(str(self.activeSkillIndex["real"]))
		self.main["button"].Disable()
		self.waitForResult = TRUE

	def OnRecvResult(self, result):
		if self.waitForResult == FALSE:
			return

		self.main["button"].Enable()
		self.waitForResult = FALSE

		if int(result) == -1:
			return

		self.SetSize(self.GetWidth(), 255)
		self.main["button"].SetPosition(self.main["button"].GetLeft(), self.GetHeight() - 21 - 15)

		self.rapidTextLine.Clear()
		if int(result) != 0:
			self.rapidTextLine.SetLastLineColor(0.1, 0.8, 0.1)
		else:
			self.rapidTextLine.SetLastLineColor(0.8, 0.1, 0.1)

		if int(result) != 0:
			data = open("locale/ro/soulstone_win.txt", "r").readlines()
		else:
			data = open("locale/ro/soulstone_loss.txt", "r").readlines()

		for line in data:
			if line.replace("\n", "") != "":
				self.rapidTextLine.AddBlock(line.replace("\n", ""))
