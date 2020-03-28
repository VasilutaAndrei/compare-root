import app
import ui
import player
import net
import chr

class GameButtonWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		import whisper 
		self.adminWhisperManager = whisper.WhisperManager()
		import uiadmintool 
		self.wndAdminTool = uiadmintool.AdminTool()
		self.__LoadWindow("UIScript/gamewindow.py")

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadWindow(self, filename):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, filename)
		except Exception, msg:
			import dbg
			dbg.TraceError("GameButtonWindow.LoadScript - %s" % (msg))
			app.Abort()
			return False

		try:
			self.gameButtonDict={
				"STATUS" : self.GetChild("StatusPlusButton"),
				"SKILL" : self.GetChild("SkillPlusButton"),
				# "PANEL" : self.GetChild("PANEL"),
				"QUEST" : self.GetChild("QuestButton"),
				"HELP" : self.GetChild("HelpButton"),
				"BUILD" : self.GetChild("BuildGuildBuilding"),
				"EXIT_OBSERVER" : self.GetChild("ExitObserver"),
				"GIFT" : self.GetChild("GiftIcon"),
				"AP_0" : self.GetChild("AP_0"),
				"AP_1" : self.GetChild("AP_1"),
				"AP_2" : self.GetChild("AP_2"),
			}

			self.gameButtonDict["EXIT_OBSERVER"].SetEvent(ui.__mem_func__(self.__OnClickExitObserver))
			self.gameButtonDict["AP_0"].SetEvent(ui.__mem_func__(self.OpenWhisperSystem))
			self.gameButtonDict["AP_1"].SetEvent(ui.__mem_func__(self.BlockChatWindow))
			self.gameButtonDict["AP_2"].SetEvent(ui.__mem_func__(self.OpenAdminTool))
				
		except Exception, msg:
			import dbg
			dbg.TraceError("GameButtonWindow.LoadScript - %s" % (msg))
			app.Abort()
			return False

		self.__HideAllGameButton()
		self.SetObserverMode(player.IsObserverMode())
		return True

	def Destroy(self):
		for key in self.gameButtonDict:
			self.gameButtonDict[key].SetEvent(0)

		self.gameButtonDict={}

	def SetButtonEvent(self, name, event):
		try:
			self.gameButtonDict[name].SetEvent(event)
		except Exception, msg:
			print "GameButtonWindow.LoadScript - %s" % (msg)
			app.Abort()
			return

	def ShowBuildButton(self):
		self.gameButtonDict["BUILD"].Show()

	def HideBuildButton(self):
		self.gameButtonDict["BUILD"].Hide()

	def CheckGameButton(self):

		if not self.IsShow():
			return

		statusPlusButton=self.gameButtonDict["STATUS"]
		skillPlusButton=self.gameButtonDict["SKILL"]
		AP_0=self.gameButtonDict["AP_0"]
		AP_1=self.gameButtonDict["AP_1"]
		AP_2=self.gameButtonDict["AP_2"]
		helpButton=self.gameButtonDict["HELP"]

		if player.GetStatus(player.STAT) > 0:
			statusPlusButton.Show()
		else:
			statusPlusButton.Hide()

		if self.__IsSkillStat():
			skillPlusButton.Show()
		else:
			skillPlusButton.Hide()
			
		if chr.IsGameMaster(player.GetMainCharacterIndex()):
			AP_0.Show()
			AP_1.Show()
			AP_2.Show()
		else:
			AP_0.Hide()
			AP_1.Hide()
			AP_2.Hide()

		if 0 == player.GetPlayTime():
			helpButton.Show()
		else:
			helpButton.Hide()

	def __IsSkillStat(self):
		if player.GetStatus(player.SKILL_ACTIVE) > 0:
			return True

		return False

	def __OnClickExitObserver(self):
		net.SendChatPacket("/observer_exit")

	def BlockChatWindow(self):
		import uiblockchat 
		self.BlockChatWindow = uiblockchat.BlockChatWindow()
		self.BlockChatWindow.OpenWindow()

	def KickChatWindow(self):
		import uikick 
		self.KickChatWindow = uikick.KickChatWindow()
		self.KickChatWindow.OpenWindow()
		
	def OpenWhisperSystem(self):
		if self.adminWhisperManager.IsShow():
			self.adminWhisperManager.Hide()
		else:
			self.adminWhisperManager.Show()	
		
	def	OpenAdminTool(self):
		if self.wndAdminTool.IsShow():
			self.wndAdminTool.Hide()
		else:
			self.wndAdminTool.Show()			
		
	def __OxEventShow(self):
		if self.wndAdminTool.IsShow():
			self.wndAdminTool.Hide()
		else:
			self.wndAdminTool.Show()			

		
	def __HideAllGameButton(self):
		for btn in self.gameButtonDict.values():
			btn.Hide()
			
	def SetObserverMode(self, isEnable):
		if isEnable:
			self.gameButtonDict["EXIT_OBSERVER"].Show()
		else:
			self.gameButtonDict["EXIT_OBSERVER"].Hide()

	def ShowGiftButton(self):
		self.gameButtonDict["GIFT"].Show()

	def HideGiftButton(self):
		self.gameButtonDict["GIFT"].Hide()