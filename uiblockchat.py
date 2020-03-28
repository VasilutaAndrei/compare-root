import ui
import dbg
import app
import net
import player

class BlockChatWindow(ui.Window):
	def __init__(self):
		ui.Window.__init__(self)
		self.BuildWindow()

	def __del__(self):
		ui.Window.__del__(self)

	def BuildWindow(self):
		self.Board = ui.BoardWithTitleBar()
		self.Board.SetSize(288, 150)
		self.Board.SetCenterPosition()
		self.Board.AddFlag('movable')
		self.Board.AddFlag('float')
		self.Board.SetTitleName('BLOCK CHAT PANNEL')
		self.Board.SetCloseEvent(self.Close)
		self.comp = Component()

		self.block = self.comp.Button(self.Board, 'Blocheaza', '', 100, 131, self.BlockChat, 'd:/ymir work/ui/public/middle_button_01.sub', 'd:/ymir work/ui/public/middle_button_02.sub', 'd:/ymir work/ui/public/middle_button_03.sub')
		self.slotbar_name, self.name = self.comp.EditLine(self.Board, '', 55, 41, 160, 15, 30)
		self.slotbar_reason, self.reason = self.comp.EditLine(self.Board, '', 55, 102, 160, 15, 30)
		self.slotbar_time, self.time = self.comp.EditLine(self.Board, '', 55, 89, 160, 15, 30)
		self.TName = self.comp.TextLine(self.Board, 'Nume:', 19, 43, self.comp.RGB(255, 255, 255))
		self.TReason = self.comp.TextLine(self.Board, 'Motiv:', 20, 103, self.comp.RGB(255, 255, 255))
		self.TTime = self.comp.TextLine(self.Board, 'Durata(Ora/e):', 21, 72, self.comp.RGB(255, 255, 255))
		

	def BlockChat(self):
		net.SendChatPacket("/block_chat " + str(self.name.GetText()) + " " + str(self.time.GetText())+"h" )
		net.SendChatPacket("/notice Chatul jucatorului " + str(self.name.GetText()) + " a fost blocat pentru " + str(self.time.GetText()) +" ore" + " de catre " +  player.GetName() +" motivul fiind: " + str(self.reason.GetText()))
	
	def OpenWindow(self):
		if self.Board.IsShow():
			self.Board.Hide()
		else:
			self.Board.Show()
	
	def Close(self):
		self.Board.Hide()

class Component:
	def Button(self, parent, buttonName, tooltipText, x, y, func, UpVisual, OverVisual, DownVisual):
		button = ui.Button()
		if parent != None:
			button.SetParent(parent)
		button.SetPosition(x, y)
		button.SetUpVisual(UpVisual)
		button.SetOverVisual(OverVisual)
		button.SetDownVisual(DownVisual)
		button.SetText(buttonName)
		button.SetToolTipText(tooltipText)
		button.Show()
		button.SetEvent(func)
		return button

	def EditLine(self, parent, editlineText, x, y, width, heigh, max):
		SlotBar = ui.SlotBar()
		if parent != None:
			SlotBar.SetParent(parent)
		SlotBar.SetSize(width, heigh)
		SlotBar.SetPosition(x, y)
		SlotBar.Show()
		Value = ui.EditLine()
		Value.SetParent(SlotBar)
		Value.SetSize(width, heigh)
		Value.SetPosition(1, 1)
		Value.SetMax(max)
		Value.SetLimitWidth(width)
		Value.SetMultiLine()
		Value.SetText(editlineText)
		Value.Show()
		return SlotBar, Value

	def TextLine(self, parent, textlineText, x, y, color):
		textline = ui.TextLine()
		if parent != None:
			textline.SetParent(parent)
		textline.SetPosition(x, y)
		if color != None:
			textline.SetFontColor(color[0], color[1], color[2])
		textline.SetText(textlineText)
		textline.Show()
		return textline

	def RGB(self, r, g, b):
		return (r*255, g*255, b*255)
