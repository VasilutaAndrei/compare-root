import ui
import uiScriptLocale
import wndMgr
import player
import localeInfo
import net
import app
import constInfo
import systemSetting

if app.ENABLE_FISH_EVENT:
	import uiMiniGameFishEvent
	
if app.ENABLE_ATTENDANCE_EVENT:
	import uiMiniGameAttendance

class MiniGameDialog(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.isLoaded = 0
		
		self.board = None
		self.closeButton = None
		self.buttonDict	= {}
		
		self.__LoadWindow()
		
	def __del__(self):
		ui.ScriptWindow.__del__(self)
		self.Destroy()
		
	def Destroy(self):
		self.isLoaded = 0
		
		self.board			= None
		self.closeButton	= None
		
		self.buttonDict	= {}
		
	def Show(self):
		self.__LoadWindow()
		ui.ScriptWindow.Show(self)
		        
	def Close(self):
		self.Hide()
		
	def OnPressEscapeKey(self):
		self.Close()
		return True
		
	def __LoadWindow(self):
		if self.isLoaded == 1:
			return
		
		self.isLoaded = 1
		
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/MiniGameDialog.py")
		except:
			import exception
			exception.Abort("MiniGameDialog.LoadWindow.LoadObject")
			
		try:
			self.board = self.GetChild("board")
			self.closeButton = self.GetChild("close_button")
			self.closeButton.SetEvent(ui.__mem_func__(self.Close))
		except:
			import exception
			exception.Abort("MiniGameDialog.LoadWindow.BindObject")
		
		self.Hide()
		
	def AppendButton(self, name, func):
		if self.buttonDict.has_key(name):
			return
	
		button = ui.Button()
		button.SetParent(self.board)
		button.SetPosition(10, (10 * (len(self.buttonDict) + 1)) + len(self.buttonDict) * 25)
		button.SetUpVisual("d:/ymir work/ui/public/XLarge_Button_01.sub")
		button.SetOverVisual("d:/ymir work/ui/public/XLarge_Button_02.sub")
		button.SetDownVisual("d:/ymir work/ui/public/XLarge_Button_03.sub")
		
		if name:
			button.SetText(name)
		
		if func: 
			button.SetEvent(ui.__mem_func__(func))
			
		button.Show()
		self.buttonDict[name] = button
		
	def DeleteButton(self, name):
		if not self.buttonDict.has_key(name):
			return
			
		self.buttonDict[name].Hide()
		del self.buttonDict[name]
		
	def DeleteAllButton(self):
		for button in self.buttonDict.values():
			button.Hide()
			del button
			
		self.buttonDict.clear()
				
	def RefreshDialog(self):
		self.board.SetSize(200, (25 * (len(self.buttonDict) + 1)) + (10 * ((len(self.buttonDict) + 1) + 1)))
		self.SetSize(200, (25 * (len(self.buttonDict) + 1)) + (10 * ((len(self.buttonDict) + 1) + 1)))
		self.closeButton.SetPosition( 10, (10 * (len(self.buttonDict) + 1)) + len(self.buttonDict) * 25 )

class MiniGameWindow(ui.ScriptWindow):
	def __init__(self):
		self.isLoaded = 0

		self.miniGameDialog = None
		
		if app.ENABLE_FISH_EVENT:
			self.fishGame = None
			
		if app.ENABLE_ATTENDANCE_EVENT:
			self.tooltipItem = None
			self.attendanceGame = None
		
		ui.ScriptWindow.__init__(self)
		
		self.__LoadWindow()
		
	def __del__(self):
		ui.ScriptWindow.__del__(self)
		
	def Show(self):
		self.__LoadWindow()
		ui.ScriptWindow.Show(self)

		#if self.miniGameDialog:
		#	self.miniGameDialog.Show()
		        
	def Close(self):
		self.Hide()
		
	def Hide(self):
		if self.miniGameDialog:
			self.miniGameDialog.Hide()
		
		wndMgr.Hide(self.hWnd)
		
	def Destroy(self):
		self.isLoaded = 0

		if self.miniGameDialog:
			self.miniGameDialog.Destroy()
			self.miniGameDialog = None		
			
		self.tooltipItem = None
		self.wndInterface = None
		self.wndInventory = None

		if app.ENABLE_FISH_EVENT:
			if self.fishGame:
				self.fishGame.Destroy()
				self.fishGame = None
		if app.ENABLE_ATTENDANCE_EVENT:
			self.tooltipItem = None
			
			if self.attendanceGame:
				self.attendanceGame.Destroy()
				self.attendanceGame = None

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return
			
		self.isLoaded = 1
		
		try:
			self.__LoadScript("UIScript/MiniGameWindow.py")
			
		except:
			import exception
			exception.Abort("MiniGameWindow.LoadWindow.LoadObject")
			
		try:
			self.eventBannerButton = ui.Button()
			self.eventBannerButton.SetParent(self.GetChild("mini_game_window"))
			self.eventBannerButton.SetPosition(-25, 0)
			self.eventBannerButton.SetUpVisual("d:/ymir work/ui/minigame/banner.sub")
			self.eventBannerButton.SetOverVisual("d:/ymir work/ui/minigame/banner.sub")
			self.eventBannerButton.SetDownVisual("d:/ymir work/ui/minigame/banner.sub")
			self.eventBannerButton.SetEvent(ui.__mem_func__(self.__ClickIntegrationEventBannerButton))
			self.eventBannerButton.Hide()
		except:
			import exception
			exception.Abort("MiniGameWindow.LoadWindow.EventBannerButton.BindObject")
		
		try:
			self.miniGameDialog = MiniGameDialog()
			self.miniGameDialog.Hide()
		except:
			import exception
			exception.Abort("MiniGameWindow.LoadWindow.MiniGameDialog")
				
		self.Show()
		
	def __LoadScript(self, fileName):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, fileName)
		
	def __ClickIntegrationEventBannerButton(self):
		if not self.miniGameDialog:
			return
			
		if self.miniGameDialog.IsShow():
			self.miniGameDialog.Close()
		else:			
			self.miniGameDialog.Show()
			
	def IntegrationMiniGame(self, enable):
		if enable:
			self.eventBannerButton.Show()	
		else:
			self.eventBannerButton.Hide()

		if app.ENABLE_ATTENDANCE_EVENT:
			if self.attendanceGame:
				self.attendanceGame.Destroy()
				self.attendanceGame = None

		if self.miniGameDialog:
			self.miniGameDialog.DeleteAllButton()
			
			if False == enable:
				self.miniGameDialog.Hide()
			else:
				if app.ENABLE_FISH_EVENT:
					if not self.fishGame:
						self.fishGame = uiMiniGameFishEvent.MiniGameFish()
						
						if self.tooltipItem:
							self.fishGame.SetItemToolTip(self.tooltipItem)
							
						if self.wndInterface:
							self.fishGame.BindInterface(self.wndInterface)
							
						if self.wndInventory:
							self.fishGame.BindInventory(self.wndInventory)
						
					if constInfo.IS_ENABLE_FISH_EVENT:
						self.miniGameDialog.AppendButton(uiScriptLocale.BANNER_FISH_BUTTON, self.__ClickFishEventButton)
					else:
						self.miniGameDialog.DeleteButton(uiScriptLocale.BANNER_FISH_BUTTON)
						
				if app.ENABLE_ATTENDANCE_EVENT:
					if not self.attendanceGame:
						self.attendanceGame = uiMiniGameAttendance.MiniGameAttendance()
						
						if self.tooltipItem:
							self.attendanceGame.SetItemToolTip(self.tooltipItem)
						
					if constInfo.IS_ENABLE_ATTENDANCE_EVENT:
						self.miniGameDialog.AppendButton(uiScriptLocale.BANNER_ATTENDANCE_BUTTON, self.__ClickAttendanceButton)

			self.miniGameDialog.RefreshDialog()
			
	def SetItemToolTip(self, tooltip):
		self.tooltipItem = tooltip
		
	def BindInterface(self, interface):
		self.wndInterface = interface
		
	def BindInventory(self, inventory):
		self.wndInventory = inventory
			
	if app.ENABLE_FISH_EVENT:
		def __ClickFishEventButton(self):
			if self.miniGameDialog:
				self.miniGameDialog.Close()
			
			if self.fishGame:
				self.fishGame.Open()
				
		def MiniGameFishUse(self, shape, useCount):			
			if self.fishGame:
				self.fishGame.MiniGameFishUse(shape, useCount)
				
		def MiniGameFishAdd(self, pos, shape):			
			if self.fishGame:
				self.fishGame.MiniGameFishAdd(pos, shape)
				
		def MiniGameFishReward(self, vnum):			
			if self.fishGame:
				self.fishGame.MiniGameFishReward(vnum)
				
		def MiniGameFishCount(self, count):			
			if self.fishGame:
				self.fishGame.MiniGameFishCount(count)
			
	if app.ENABLE_ATTENDANCE_EVENT:
		def __ClickAttendanceButton(self):
			if self.miniGameDialog:
				self.miniGameDialog.Close()
			
			if self.attendanceGame:
				self.attendanceGame.Open()
				
		def MiniGameAttendanceSetData(self, type, value):
			if not self.attendanceGame:
				return
				
			if type == 1:
				self.attendanceGame.MiniGameAttendanceSetDay(value)
			elif type == 2:
				self.attendanceGame.MiniGameAttendanceSetMissionClear(value)
			elif type == 3:
				self.attendanceGame.MiniGameAttendanceSetReward(value)
				
			self.attendanceGame.RefreshAttendanceBoard()
					
	def HideMiniGameDialog(self):
		if self.eventBannerButton:
			if self.eventBannerButton.IsShow():
				self.eventBannerButton.Hide()
		
		if self.miniGameDialog:
			if self.miniGameDialog.IsShow():
				self.miniGameDialog.Hide()
			
	def ShowMiniGameDialog(self):
		if self.eventBannerButton:
			self.eventBannerButton.Show()		
			