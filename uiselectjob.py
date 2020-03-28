import ui, event, constInfo, app, uiCommon, chat, net, playerSettingModule, player, localeInfo, wndMgr

JOB_NAME_DICT = {
	0	:	['Razboinic Corp','Razboinic Mental'],
	1	:	['Ninja Lame','Ninja Arc'],
	2	:	['Sura Arme','Sura Magie Neagra'],
	3	:	['Saman Zmeu','Saman Leac'],
	# 4	:	['Lycan Instinct','N.A.']
}

JOB_LIST = { 	
	0	:	localeInfo.JOB_WARRIOR,
	1	:	localeInfo.JOB_ASSASSIN,
	2	:	localeInfo.JOB_SURA,
	3	:	localeInfo.JOB_SHAMAN,
	# 4	:	localeInfo.JOB_WOLFMAN,
}

FACE_IMAGE_DICT = {
	playerSettingModule.RACE_WARRIOR_M	: "icon/face/warrior_m.tga",
	playerSettingModule.RACE_WARRIOR_W	: "icon/face/warrior_w.tga",
	playerSettingModule.RACE_ASSASSIN_M	: "icon/face/assassin_m.tga",
	playerSettingModule.RACE_ASSASSIN_W	: "icon/face/assassin_w.tga",
	playerSettingModule.RACE_SURA_M		: "icon/face/sura_m.tga",
	playerSettingModule.RACE_SURA_W		: "icon/face/sura_w.tga",
	playerSettingModule.RACE_SHAMAN_M	: "icon/face/shaman_m.tga",
	playerSettingModule.RACE_SHAMAN_W	: "icon/face/shaman_w.tga",
}
# if app.ENABLE_WOLFMAN_CHARACTER:
	# FACE_IMAGE_DICT.update({playerSettingModule.RACE_WOLFMAN_M  : "icon/face/wolfman_m.tga",})
	
class JobSelectWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.isLoaded = 0
		self.__LoadWindow()
	
	def __LoadWindow(self):
		if (self.isLoaded == 1):
			return
			
		self.isLoaded = 1
		try:
			PythonScriptLoader = ui.PythonScriptLoader()
			PythonScriptLoader.LoadScriptFile(self, "UIScript/selectjobwindow.py")
		except:
			import exception
			exception.Abort("SelectJob.LoadWindow.LoadObject")
			
		try:
			self.__BindObjects()
		except:
			import exception
			exception.Abort("SelectJob.LoadWindow.BindObject")
		
		self.__BindEvents()
	
	def __BindObjects(self):
		self.titlebar = self.GetChild("TitleBar")
		
		self.selectButtonFirst = self.GetChild("SelectButtonFirst")
		self.selectButtonSecond = self.GetChild("SelectButtonSecond")
		
		self.firstSkillSlotBack = self.GetChild("FirstSkillSlotBack")
		self.secondSkillSlotBack = self.GetChild("SecondSkillSlotBack")
		
		self.firstSkillSlot = self.GetChild("FirstSkillSlot")
		self.secondSkillSlot = self.GetChild("SecondSkillSlot")
		
		self.raceImage = self.GetChild("RaceImage")
		self.infoText = self.GetChild("InfoText")

	def __BindEvents(self):
		self.isLoaded = 1
		self.titlebar.SetCloseEvent(ui.__mem_func__(self.Close))

		self.selectButtonFirst.SetEvent(ui.__mem_func__(self.SelectJobFirstQuestion))
		self.selectButtonSecond.SetEvent(ui.__mem_func__(self.SelectJobSecondQuestion))
		
		self.selectButtonFirst.SetText(JOB_NAME_DICT[self.GetRealRace()][0])
		self.selectButtonSecond.SetText(JOB_NAME_DICT[self.GetRealRace()][1])
		
		self.infoText.SetText("%s - %s" % (player.GetName(), JOB_LIST[self.GetRealRace()]))

		self.raceImage.LoadImage(FACE_IMAGE_DICT[net.GetMainActorRace()])
		
		if self.GetRealRace() == 4:
			self.selectButtonSecond.SetEvent(ui.__mem_func__(self.EmptyFunc))
			
			for k in xrange(6):
				self.secondSkillSlotBack.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
				
				self.secondSkillSlot.ClearSlot(k)
				self.secondSkillSlot.SetCoverButton(k, "d:/ymir work/ui/pet/skill_button/skill_enable_button.sub", "d:/ymir work/ui/pet/skill_button/skill_enable_button.sub", "d:/ymir work/ui/pet/skill_button/skill_enable_button.sub", "d:/ymir work/ui/pet/skill_button/skill_enable_button.sub", False, False)
				self.secondSkillSlot.SetAlwaysRenderCoverButton(k)
				
				self.secondSkillSlot.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)

		for i in xrange(6):
			self.firstSkillSlotBack.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
			
			self.firstSkillSlot.SetSkillSlotNew(i, self.GetSkillIndex()+i, 3, 1)
			self.firstSkillSlot.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)

		if self.GetRealRace() != 4:
			for j in xrange(6):
				self.secondSkillSlotBack.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
				
				self.secondSkillSlot.SetSkillSlotNew(j, self.GetSkillIndex()+j+15, 3, 1)
				self.secondSkillSlot.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
		
	def GetSkillIndex(self):
		if self.GetRealRace() == 4:
			return 170
		else:
			return self.GetRealRace() * 30 + 1
				
	def GetRealRace(self):
		race = net.GetMainActorRace()
		if race >= 4:
			return race-4
		else:
			return race
			
	def __OnCloseQuestionDialog(self):
		if self.questionDialog:
			self.questionDialog.Close()
		self.questionDialog = None
		
	def EmptyFunc(self):
		chat.AppendChat(chat.CHAT_TYPE_INFO, "Lycan are doar un set de abilitati disponibil momentan.")
			
	def SelectJobFirstQuestion(self):
		self.questionDialog = uiCommon.QuestionDialog()
		self.questionDialog.SetText("Esti sigur ca vrei sa alegi abilitatea: %s" % JOB_NAME_DICT[self.GetRealRace()][0])
		self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.SelectJobFirst))
		self.questionDialog.SetCancelEvent(ui.__mem_func__(self.__OnCloseQuestionDialog))
		self.questionDialog.Open()
			
	def SelectJobFirst(self):
		constInfo.SelectJob['QCMD'] = str(1)
		event.QuestButtonClick(constInfo.SelectJob['QID'])
		self.RealClose()
		self.__OnCloseQuestionDialog()
		
	def SelectJobSecondQuestion(self):
		self.questionDialog = uiCommon.QuestionDialog()
		self.questionDialog.SetText("Esti sigur ca vrei sa alegi abilitatea: %s" % JOB_NAME_DICT[self.GetRealRace()][1])
		self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.SelectJobSecond))
		self.questionDialog.SetCancelEvent(ui.__mem_func__(self.__OnCloseQuestionDialog))
		self.questionDialog.Open()

	def SelectJobSecond(self):
		constInfo.SelectJob['QCMD'] = str(2)
		event.QuestButtonClick(constInfo.SelectJob['QID'])
		self.RealClose()
		self.__OnCloseQuestionDialog()

	def __del__(self):
		ui.ScriptWindow.__del__(self)
	
	def Open(self):
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def Close(self):
		self.wndpopupdialog = uiCommon.PopupDialog()
		self.wndpopupdialog.SetText("Nu poti inchide aceasta fereastra.")
		self.wndpopupdialog.Open()
		
	def RealClose(self):
		self.Hide()
		
	def Destroy(self):
		self.RealClose()
		self.ClearDictionary()