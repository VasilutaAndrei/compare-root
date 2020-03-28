#########################################################
#	Pagina de bonusuri pentru Story2 & devgames.pro		#
#		     http://metin2.mmo-arena.ro/				#
#			   http://www.devgames.pro/					#
#########################################################
import ui
import chat
import app
import player
import snd
import item
import net
import game

class BonusBoardDialog(ui.ScriptWindow):
	MaxBoni = { "1": 16000, "2": 320, "3": 32, "4": 32, "5": 32, "6": 32, "7": 16, "9": 40, "10": 60, "11": 60, "12": 16, "13": 24, "14": 16, "15": 30, "16": 30, "17": 50, "18": 100, "19": 100, "20": 100, "21": 100, "22": 100, "23": 20, "24": 40, "27": 15, "28": 30, "29": 72, "30": 72, "31": 72, "32": 72, "33": 72, "34": 72, "35": 60, "36": 60, "37": 40, "38": 60, "39": 20, "41": 10, "43": 60, "44": 60, "45": 40, "48": 1, "53": 50 }
	BonusDict = ["Bonusuri PvP", "Bonusuri PvM", "Bonusuri extra"]
	BonusIDListe = [["", 0, 0],["PV acumulat:", 1, 0],["PM acumulat:", 2, 0],["Viteza farmecului:", 9, 0],["Regenerare PV:", 10, 32],["Regenerare PM:", 11, 33],["ªansa de otrãvire:", 12, 37],["ªansa de blocare:", 13, 38],["ªansa unei lov. critice:", 15, 40],["ªansa unei lov. pãtr:", 16, 41],["Tare împotriva semi-om:", 17, 43],["Tare împotriva animalelor:", 18, 44],["Tare împotriva orcilor:", 19, 45],["Tare împotriva esoteriecilor:", 20, 46],["Tare împotriva vampirilor:", 21, 47],["Tare împotriva diavolului:", 22, 48],["Absorbire PV:", 23, 63],["Absorbire PM:", 24, 64],["Blocare atac corporal:", 27, 67],["Evitare atac cu sãgeþi:", 28, 68],["Apãrare cu sabia:", 29, 69],["Apãrare cu douã mâini:", 30, 70],["Apãrare pumnal:", 31, 71],["Apãrare clopot:", 32, 72],["Apãrare evantai:", 33, 73],["Rezistenþã la sãgeþi:", 34, 74],["Rezistenþã la foc:", 35, 75],["Rezistenþã la magie:", 37, 77],["Rezistenþã la vânt:", 38, 78],["Rezistenþã la otravã:", 41, 81],["Bonus exp acumulat:", 43, 83],["Bonus yang acumulat:", 44, 84],["Bonus drop acumulat:", 45, 85],["APPLY_SKILL", 51, 0],["Valoarea atacului:", 53, 0],["Tare împotriva monstrilor:", 63, 53]]
	SpecialBoni = { 1: "Norm.State", 2: "Norm.State", 3: "Norm.State", 4: "Norm.State", 5: "Norm.State", 6: "Norm.State", 55: "Norm.State", 56: "Norm.State", 58: "Norm.State" }
	PvPOffenseBoni = ["Tare împotriva semi-om:", "ªansa unei lov. critice:", "ªansa unei lov. pãtr:", "Viteza farmecului:", "Valoarea atacului:", "ªansa de otrãvire:", "ªansa de blocare:", "Rezistenþã la otravã:", "Rezistenþã la foc:", "Regenerare PM:"]
	PvPDefenseBoni = ["Apãrare cu sabia:", "Apãrare cu douã mâini:", "Apãrare pumnal:", "Apãrare clopot:", "Apãrare evantai:", "Rezistenþã la sãgeþi:", "Evitare atac cu sãgeþi:", "Rezistenþã la magie:", "Blocare atac corporal:", "Regenerare PV:"]
	PvMOffenseBoni = ["PV acumulat:", "Tare împotriva animalelor:", "Tare împotriva vampirilor:", "Tare împotriva orcilor:", "Absorbire PM:", "Rezistenþã la vânt:"]
	PvMDefenseBoni = ["PM acumulat:", "Tare împotriva monstrilor:", "Tare împotriva diavolului:", "Tare împotriva esoteriecilor:", "Absorbire PV:"]
	LeftoversOffenseBoni = ["Bonus exp acumulat:", "Bonus yang acumulat:"]
	LeftoversDefenseBoni = ["Bonus drop acumulat:"]

	BonusList = []
	UI = []
	
	TestSystem = 0
	ProcessTimeStamp = 0
	
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.LoadUI()
		game.BPisLoaded = 1
		
	def __del__(self):
		ui.ScriptWindow.__del__(self)
		self.Board.Hide()
		game.BPisLoaded = 0

	def LoadUI(self):
		self.Board = ui.BoardWithTitleBar()
		self.Board.SetSize(323, 418)
		self.Board.SetCenterPosition()
		self.Board.AddFlag("movable")
		self.Board.AddFlag("float")
		self.Board.SetTitleName("Statistici bonusuri active")
		self.Board.SetCloseEvent(self.__del__)
		self.Board.Show()
		
		Vertical = ui.Line()
		Vertical.SetParent(self.Board)
		Vertical.SetPosition(10, 50)
		Vertical.SetSize(300, 0)
		Vertical.SetColor(0xff777777)
		Vertical.Show()
		self.UI.append(Vertical)
		
		x = 25
		for i in xrange(3):
			ChangeBonusDict = ui.Button()
			ChangeBonusDict.SetParent(self.Board)
			ChangeBonusDict.SetUpVisual("d:/ymir work/ui/public/large_button_01.sub")
			ChangeBonusDict.SetOverVisual("d:/ymir work/ui/public/large_button_02.sub")
			ChangeBonusDict.SetDownVisual("d:/ymir work/ui/public/large_button_03.sub")
			ChangeBonusDict.SetText(self.BonusDict[i])
			ChangeBonusDict.SetPosition(x, 380)
			ChangeBonusDict.SetEvent(lambda arg = ChangeBonusDict.GetText(): self.ChangeBonusDict(arg))
			ChangeBonusDict.Show()
			x += 97
			self.UI.append(ChangeBonusDict)
			
		x = 37
		Type = ["Bonusurile ofensive & defensive sunt afisate in timp real!"]
		for i in xrange(1):
			BonusDescription = ui.TextLine()
			BonusDescription.SetParent(self.Board)
			BonusDescription.SetPosition(x, 33)
			BonusDescription.SetText(str(Type[i]))
			BonusDescription.SetFontColor(4.0, 0.83, 0)
			BonusDescription.Show()			
			x += 128
			self.UI.append(BonusDescription)

		self.SetBoni(self.BonusDict[0])
		self.dict = self.BonusDict[0]
		
	def SetBoni(self, type):
		Offense = [[25, 70], [25, 100], [25, 130], [25, 160], [25, 190], [25, 220], [25, 250], [25, 280], [25, 310], [25, 340]]
		Defense = [[170, 70], [170, 100], [170, 130], [170, 160], [170, 190], [170, 220], [170, 250], [170, 280], [170, 310], [170, 340]]
		for bonus in self.BonusIDListe:
			if type == self.BonusDict[0]:
				self.CheckBonus(bonus, self.PvPOffenseBoni, Offense)
				self.CheckBonus(bonus, self.PvPDefenseBoni, Defense)
			elif type == self.BonusDict[1]:
				self.CheckBonus(bonus, self.PvMOffenseBoni, Offense)
				self.CheckBonus(bonus, self.PvMDefenseBoni, Defense)
			elif type == self.BonusDict[2]:
				self.CheckBonus(bonus, self.LeftoversOffenseBoni, Offense)
				self.CheckBonus(bonus, self.LeftoversDefenseBoni, Defense)
			else:
				return
				
	def CheckBonus(self, bonus, bonuslist, offset):
		for boni in bonuslist:
			if bonus[0] == boni:
				try:
					Index = bonuslist.index(boni)
					BonusDescription = ui.TextLine()
					BonusDescription.SetParent(self.Board)
					BonusDescription.SetPosition(offset[Index][0], offset[Index][1])
					BonusDescription.SetText(str(bonus[0]))
					BonusDescription.Show()
					
					BonusSlotBar = ui.SlotBar()
					BonusSlotBar.SetParent(self.Board)
					BonusSlotBar.SetSize(125, 15)
					BonusSlotBar.SetPosition(offset[Index][0], offset[Index][1] + 15)
					BonusSlotBar.Show()
					
					BonusAttrLine = ui.TextLine()
					BonusAttrLine.SetParent(self.Board)
					BonusAttrLine.SetPosition(offset[Index][0] + 5, offset[Index][1] + 15)
					
					try:
						Type = self.SpecialBoni[bonus[1]]
						Attribute = self.EquipAttribute(bonus)
					except:
						Attribute = player.GetStatus(int(bonus[2]))
					if self.TestSystem != 1:
						BonusAttrLine.SetText(str(Attribute))
						try:
							if int(Attribute) >= int(self.MaxBoni[str(bonus[1])]):
								BonusAttrLine.SetFontColor(1.0, 0.63, 0)
							else:
								BonusAttrLine.SetFontColor(1, 1, 1)
						except:
							BonusAttrLine.SetFontColor(1, 1, 1)
					else:
						BonusAttrLine.SetText("Test system is active")
						BonusAttrLine.SetFontColor(0.1, 0.7, 1.0)
					
					BonusAttrLine.Show()
					self.BonusList.append([BonusDescription, BonusAttrLine, BonusSlotBar])
				except:
					pass		
				
	def EquipAttribute(self, bonus):
		value = 0
		for slot in xrange(90, 101):
			for attr in xrange(0, 7):
				attr, val = player.GetItemAttribute(slot, attr)
				if int(attr) == bonus[1]:
					value += int(val)
		return int(value)

	def ChangeBonusDict(self, dict):
		self.dict = dict
		for bonus in self.BonusList:
			try:
				for array in bonus:
					array.Hide()
			except:
				pass			
		self.SetBoni(dict)
		
	def OnUpdate(self):
		import item
		if int(app.GetTime()) > int(self.ProcessTimeStamp) + 6:
			self.SetBoni(self.dict)
			self.ProcessTimeStamp = app.GetTime()

#BonusBoardDialog().Show()
