import event, uiCommon, app, wndMgr, net, player, ui, uiToolTip, background, uiScriptLocale, localeInfo, chat
#ranking
class BattleFieldWindow(ui.ScriptWindow):
	DEFAULT_DESC_Y = 7
	DESCRIPTION_FILE_NAME = "locale/ro/desc_battle_field.txt"
	SHOW_LINE_COUNT_MAX = 18
	
	M2EMPIREICON = {
		0: 'd:/ymir work/ui/public/battle/empire_empty.sub', 
		1: 'd:/ymir work/ui/public/battle/empire_shinsu.sub', 
		2: 'd:/ymir work/ui/public/battle/empire_chunjo.sub', 
		3: 'd:/ymir work/ui/public/battle/empire_jinno.sub'
	}
	
	class DescriptionBox(ui.Window):
		def __init__(self):
			ui.Window.__init__(self)
			self.descIndex = 0
		def __del__(self):
			ui.Window.__del__(self)
		def SetIndex(self, index):
			self.descIndex = index
		def OnRender(self):
			event.RenderEventSet(self.descIndex)
			
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.isLoaded = 0
		self.descIndex = 0
		
		self.rankDict = { }
		self.rankingDict = { }
		
		self.openTimeStamp = 0
		self.closeTimeStamp = 0
		self.isOpen = False
		self.isEvent = False
		
		self.currentRanking = 0
		self.__LoadWindow()		
		
	def __del__(self):
		ui.ScriptWindow.__del__(self)
		
	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1
		
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/BattleFieldWindow.py")
			
			self.__BindObject()
			self.__BindEvent()
			self.__DescBattleField()
		except:
			import exception
			exception.Abort("BattleFieldWindow.__LoadWindow")
			
	def __BindObject(self):
		self.titleBar = self.GetChild("titlebar")
		self.textBoard = self.GetChild("text_board")
		self.btnPrev = self.GetChild("prev_button")
		self.btnNext = self.GetChild("next_button")		
		self.btnEnter = self.GetChild("enter_button")
		self.notice = self.GetChild("notice")
		self.list = self.GetChild("list")
		
		self.tab01 = self.GetChild("tab_01")
		self.tab02 = self.GetChild("tab_02")
		self.tabBtn01 = self.GetChild("tab_button_01")
		self.tabBtn02 = self.GetChild("tab_button_02")
		
		self.myPoint = self.GetChild("my_point")
		
	def __BindEvent(self):
		self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))
		self.btnPrev.SetEvent(ui.__mem_func__(self.PrevDescriptionPage))
		self.btnNext.SetEvent(ui.__mem_func__(self.NextDescriptionPage))
		
		self.tabBtn01.SetEvent(lambda stateKey = 0: self.__OnClickTabButton(stateKey))
		self.tabBtn02.SetEvent(lambda stateKey = 1: self.__OnClickTabButton(stateKey))
		
		self.btnEnter.SetEvent(ui.__mem_func__(self.EnterBattleField))
		
		self.descriptionBox = self.DescriptionBox()
		self.descriptionBox.SetParent(self.textBoard)
		self.descriptionBox.Show()

	def Destroy(self):
		self.isLoaded = 0
		self.ClearDictionary()
		
		self.descIndex = None
		self.titleBar = None
		self.textBoard = None
		self.btnPrev = None
		self.btnNext = None
		self.btnEnter = None
		self.notice = None
		self.list = None
		self.tab01 = None
		self.tab02 = None
		self.tabBtn01 = None
		self.tabBtn02 = None
		
		self.descriptionBox = None
		
		self.__del__()
	
	def Close(self):
		self.currentRanking = 0
		self.rankDict = { }
		
		self.Hide()
		
	def Open(self):
		self.__OnClickTabButton(0)
		self.SetPoint(player.GetBattlePoints())
		self.RefreshRankingList(self.GetState())
		
		self.Show()

	def OnPressEscapeKey(self):
		self.Close()
		return True
		
	def __DescBattleField(self):
		event.ClearEventSet(self.descIndex)
		self.descIndex = event.RegisterEventSet(self.DESCRIPTION_FILE_NAME)
		event.SetFontColor( self.descIndex, 0.7843, 0.7843, 0.7843 )
		event.SetVisibleLineCount(self.descIndex, self.SHOW_LINE_COUNT_MAX)			
		event.SetRestrictedCount(self.descIndex, 47)

	def PrevDescriptionPage(self):
		if True == event.IsWait(self.descIndex):
			if event.GetVisibleStartLine(self.descIndex) - self.SHOW_LINE_COUNT_MAX >= 0:
				event.SetVisibleStartLine(self.descIndex, event.GetVisibleStartLine(self.descIndex) - self.SHOW_LINE_COUNT_MAX)
				event.Skip(self.descIndex)
		else:
			event.Skip(self.descIndex)
	
	def NextDescriptionPage(self):
		if True == event.IsWait(self.descIndex):
			event.SetVisibleStartLine(self.descIndex, event.GetVisibleStartLine(self.descIndex) + self.SHOW_LINE_COUNT_MAX)
			event.Skip(self.descIndex)
		else:
			event.Skip(self.descIndex)
			
	def OnUpdate(self):		
		(xposEventSet, yposEventSet) = self.textBoard.GetGlobalPosition()
		event.UpdateEventSet(self.descIndex, xposEventSet + self.DEFAULT_DESC_Y, -(yposEventSet + self.DEFAULT_DESC_Y))
		self.descriptionBox.SetIndex(self.descIndex)
		
		self.UpdateNotice()
		self.RefreshButtons()
		
	def SetState(self, stateKey):
		self.currentRanking = stateKey
		self.RefreshRankingList(stateKey)
		
	def GetState(self):
		return self.currentRanking
		
	def __OnClickTabButton(self, stateKey):
		if stateKey == 0:
			self.tab01.Show()
			self.tab02.Hide()
			self.tabBtn02.SetUp()
			self.SetState(stateKey)
		elif stateKey == 1:
			self.tab01.Hide()
			self.tab02.Show()
			self.tabBtn01.SetUp()
			self.SetState(stateKey)
			
	def SetPoint(self, point):
		self.myPoint.SetText(str(point))
		
	def EnterBattleField(self):
		net.SendRequestEnterBattle()
		
	def AddRankingMember(self, position, type, name, empire, score):
		if not self.rankingDict.has_key(type):
			self.rankingDict[type] = {}
			
		if not self.rankingDict[type].has_key(position):
			self.rankingDict[type][position] = {}
	
		self.rankingDict[type][position] = [name, empire, score]
		
	def BindMiniMap(self, minimap):
		self.miniMap = minimap
		
	def TransformTime(self, seconds, returnType = 0):
		m, s = divmod(seconds, 60)
		h, m = divmod(m, 60)
		
		if returnType == 0:
			return "%02d:%02d" % (h, m)
		elif returnType == 1:
			return "%d" % h
		
	def SetOpenInfo(self, openTime, closeTime, isOpen, isEvent):
		self.openTimeStamp = app.GetGlobalTimeStamp() + openTime
		self.closeTimeStamp = app.GetGlobalTimeStamp() + closeTime
		self.isOpen = isOpen
		self.isEvent = isEvent
		
	def UpdateNotice(self):
		openTime = max(0, self.openTimeStamp - app.GetGlobalTimeStamp())
		closeTime = max(0, self.closeTimeStamp - app.GetGlobalTimeStamp())
		
		if openTime > 60 and closeTime > 60:
			if self.isOpen == 0:
				self.notice.SetText(uiScriptLocale.BATTLE_FIELD_OPERATION_TIME_OPEN % (self.TransformTime(openTime), self.TransformTime(closeTime - openTime, 1)))
			else:
				self.isOpen = 0
		elif openTime <= 60 and closeTime > 60:
			if self.isOpen == 1:
				self.notice.SetText(uiScriptLocale.BATTLE_FIELD_OPERATION_TIME_END % (self.TransformTime(closeTime)))
			else:
				self.isOpen = 1
		elif openTime <= 60 and closeTime <= 60:
			if self.isOpen == 0:
				self.notice.SetText(uiScriptLocale.BATTLE_FIELD_OPERATION_TIME_NA)
			else:
				self.isOpen = 0

	def RefreshButtons(self):
		if self.miniMap:
			self.miniMap.RefreshBattleButton(self.isOpen, self.isEvent)
					
	def ButtonToolTipProgress(self):
		pass
		
	def OverInToolTipButton(self, btnText, text_len = 0):
		pass
	
	def OverOutToolTipButton(self):
		pass

	def RefreshRankingList(self, type):
		for k in xrange(len(self.rankDict)):
			self.rankDict[k][0].Hide()
	
		if not self.rankingDict.has_key(type):
			return
		
		for i in xrange(len(self.rankingDict[type])):
			self.rankDict[i] = []
			
			#if player.GetName() == self.rankingDict[type][i][0]:
			#	self.rankDict[i].append(ui.MakeImageBox(self.list, "d:/ymir work/ui/public/battle/my_rank.sub", 1, 23 + i*23))
			#else:
			self.rankDict[i].append(ui.MakeImageBox(self.list, "d:/ymir work/ui/public/battle/rank_list.sub", 1, 23 + i*23))
		
			textLinePos = ui.MakeTextLine(self.rankDict[i][0], False, False)
			textLineName = ui.MakeTextLine(self.rankDict[i][0], False, False)
			textLineKingdom = ui.MakeImageBox(self.rankDict[i][0], self.M2EMPIREICON[self.rankingDict[type][i][1]], 194, 3)
			textLinePoints = ui.MakeTextLine(self.rankDict[i][0], False, False)
			
			textLinePos.SetPosition(31, 9)
			textLinePos.SetText(str(i+1))
			
			textLineName.SetPosition(120, 9)
			textLineName.SetText(self.rankingDict[type][i][0])
			
			textLinePoints.SetPosition(260, 9)
			textLinePoints.SetText(str(self.rankingDict[type][i][2]))
			
			self.rankDict[i].append(textLinePos)
			self.rankDict[i].append(textLineName)
			self.rankDict[i].append(textLineKingdom)
			self.rankDict[i].append(textLinePoints)
			
			self.rankDict[i][0].Show()
			self.rankDict[i][3].Show()
		

