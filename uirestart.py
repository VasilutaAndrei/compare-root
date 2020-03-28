import dbg
import app
import net
if app.ENABLE_BATTLE_FIELD:
	import background
import ui

###################################################################################################
## Restart
class RestartDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def LoadDialog(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/restartdialog.py")
		except Exception, msg:
			import sys
			(type, msg, tb)=sys.exc_info()
			dbg.TraceError("RestartDialog.LoadDialog - %s:%s" % (type, msg))
			app.Abort()
			return 0

		try:
			self.restartHereButton=self.GetChild("restart_here_button")
			self.restartTownButton=self.GetChild("restart_town_button")
			if app.ENABLE_BATTLE_FIELD:
				self.board=self.GetChild("board")
				self.restartInstantButton=self.GetChild("restart_immediately_button")
		except:
			import sys
			(type, msg, tb)=sys.exc_info()
			dbg.TraceError("RestartDialog.LoadDialog - %s:%s" % (type, msg))
			app.Abort()
			return 0

		self.restartHereButton.SetEvent(ui.__mem_func__(self.RestartHere))
		self.restartTownButton.SetEvent(ui.__mem_func__(self.RestartTown))
		if app.ENABLE_BATTLE_FIELD:
			self.restartInstantButton.SetEvent(ui.__mem_func__(self.RestartInstant))

		return 1

	def Destroy(self):
		self.restartHereButton=0
		self.restartTownButton=0
		if app.ENABLE_BATTLE_FIELD:
			self.board=0
			self.restartInstantButton=0
		self.ClearDictionary()

	def OpenDialog(self):
		if app.ENABLE_BATTLE_FIELD:
			if background.IsBattleFieldMap():
				self.board.SetSize(200,88+25)
				self.restartInstantButton.Show()
			else:
				self.board.SetSize(200,88)
				self.restartInstantButton.Hide()
				
		self.Show()

	def Close(self):
		self.Hide()
		return True

	def RestartHere(self):
		net.SendChatPacket("/restart_here")

	def RestartTown(self):
		net.SendChatPacket("/restart_town")

	if app.ENABLE_BATTLE_FIELD:
		def RestartInstant(self):
			net.SendChatPacket("/restart_battle")		
		
	def OnPressExitKey(self):
		return True

	def OnPressEscapeKey(self):
		return True
