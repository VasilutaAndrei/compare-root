import dbg
import player
import item
import grp
import wndMgr
import skill
import shop
import exchange
import grpText
import safebox
import localeInfo
import app
import background
import nonplayer
import chr
import ui
import mouseModule
import constInfo
if app.ENABLE_SASH_SYSTEM:
	import sash

WARP_SCROLLS = [22011, 22000, 22010]

DESC_DEFAULT_MAX_COLS = 26
DESC_WESTERN_MAX_COLS = 35
DESC_WESTERN_MAX_WIDTH = 220

def chop(n):
	return round(n - 0.5, 1)

def pointop(n):
	t = int(n)
	if t / 10 < 1:
		return "0."+n
	else:		
		return n[0:len(n)-1]+"."+n[len(n)-1:]	
	
def SplitDescription(desc, limit):
	total_tokens = desc.split()
	line_tokens = []
	line_len = 0
	lines = []
	for token in total_tokens:
		if "|" in token:
			sep_pos = token.find("|")
			line_tokens.append(token[:sep_pos])

			lines.append(" ".join(line_tokens))
			line_len = len(token) - (sep_pos + 1)
			line_tokens = [token[sep_pos+1:]]
		else:
			line_len += len(token)
			if len(line_tokens) + line_len > limit:
				lines.append(" ".join(line_tokens))
				line_len = len(token)
				line_tokens = [token]
			else:
				line_tokens.append(token)

	if line_tokens:
		lines.append(" ".join(line_tokens))

	return lines

###################################################################################################
## ToolTip
##
##   NOTE : 현재는 Item과 Skill을 상속으로 특화 시켜두었음
##          하지만 그다지 의미가 없어 보임
##
class ToolTip(ui.ThinBoard):

	TOOL_TIP_WIDTH = 190
	TOOL_TIP_HEIGHT = 10

	TEXT_LINE_HEIGHT = 17

	TITLE_COLOR = grp.GenerateColor(0.9490, 0.9058, 0.7568, 1.0)
	SPECIAL_TITLE_COLOR = grp.GenerateColor(1.0, 0.7843, 0.0, 1.0)
	NORMAL_COLOR = grp.GenerateColor(0.7607, 0.7607, 0.7607, 1.0)
	FONT_COLOR = grp.GenerateColor(0.7607, 0.7607, 0.7607, 1.0)
	PRICE_COLOR = 0xffFFB96D

	HIGH_PRICE_COLOR = SPECIAL_TITLE_COLOR
	MIDDLE_PRICE_COLOR = grp.GenerateColor(0.85, 0.85, 0.85, 1.0)
	LOW_PRICE_COLOR = grp.GenerateColor(0.7, 0.7, 0.7, 1.0)

	ENABLE_COLOR = grp.GenerateColor(0.7607, 0.7607, 0.7607, 1.0)
	DISABLE_COLOR = grp.GenerateColor(0.9, 0.4745, 0.4627, 1.0)

	NEGATIVE_COLOR = grp.GenerateColor(0.9, 0.4745, 0.4627, 1.0)
	POSITIVE_COLOR = grp.GenerateColor(0.5411, 0.7254, 0.5568, 1.0)
	SPECIAL_POSITIVE_COLOR = grp.GenerateColor(0.6911, 0.8754, 0.7068, 1.0)
	SPECIAL_POSITIVE_COLOR2 = grp.GenerateColor(0.8824, 0.9804, 0.8824, 1.0)

	CONDITION_COLOR = 0xffBEB47D
	ITEM_CHEST_USED = 0xff32CD32	
	CAN_LEVEL_UP_COLOR = 0xff8EC292
	CANNOT_LEVEL_UP_COLOR = DISABLE_COLOR
	NEED_SKILL_POINT_COLOR = 0xff9A9CDB
	ITEM_ID_COLOR = 0xffFFFF00
	PET_BNS_COLOR = 0xffB8B10D

	def __init__(self, width = TOOL_TIP_WIDTH, isPickable=False):
		ui.ThinBoard.__init__(self, "TOP_MOST")

		if isPickable:
			pass
		else:
			self.AddFlag("not_pick")

		self.AddFlag("float")

		self.followFlag = True
		self.toolTipWidth = width

		self.xPos = -1
		self.yPos = -1

		self.defFontName = localeInfo.UI_DEF_FONT
		self.ClearToolTip()

	def __del__(self):
		ui.ThinBoard.__del__(self)

	def ClearToolTip(self):
		self.toolTipHeight = 12
		self.childrenList = []
		if app.ENABLE_ATTENDANCE_EVENT:
			self.isAttendanceRewardItem = False
			
	def SetFollow(self, flag):
		self.followFlag = flag

	def SetDefaultFontName(self, fontName):
		self.defFontName = fontName

	def AppendSpace(self, size):
		self.toolTipHeight += size
		self.ResizeToolTip()

	def AppendHorizontalLine(self):

		for i in xrange(2):
			horizontalLine = ui.Line()
			horizontalLine.SetParent(self)
			horizontalLine.SetPosition(0, self.toolTipHeight + 3 + i)
			horizontalLine.SetWindowHorizontalAlignCenter()
			horizontalLine.SetSize(150, 0)
			horizontalLine.Show()

			if 0 == i:
				horizontalLine.SetColor(0xff555555)
			else:
				horizontalLine.SetColor(0xff000000)

			self.childrenList.append(horizontalLine)

		self.toolTipHeight += 11
		self.ResizeToolTip()

	def AlignHorizonalCenter(self):
		for child in self.childrenList:
			(x, y)=child.GetLocalPosition()
			child.SetPosition(self.toolTipWidth/2, y)

		self.ResizeToolTip()

	def AutoAppendTextLine(self, text, color = FONT_COLOR, centerAlign = True):
		textLine = ui.TextLine()
		textLine.SetParent(self)
		textLine.SetFontName(self.defFontName)
		textLine.SetPackedFontColor(color)
		textLine.SetText(text)
		textLine.SetOutline()
		textLine.SetFeather(False)
		textLine.Show()

		if centerAlign:
			textLine.SetPosition(self.toolTipWidth/2, self.toolTipHeight)
			textLine.SetHorizontalAlignCenter()

		else:
			textLine.SetPosition(10, self.toolTipHeight)

		self.childrenList.append(textLine)

		(textWidth, textHeight)=textLine.GetTextSize()

		textWidth += 40
		textHeight += 5

		if self.toolTipWidth < textWidth:
			self.toolTipWidth = textWidth

		self.toolTipHeight += textHeight

		return textLine

	def AutoAppendNewTextLine(self, text, color = FONT_COLOR, centerAlign = True):
		textLine = ui.TextLine()
		textLine.SetParent(self)
		textLine.SetFontName(self.defFontName)
		textLine.SetPackedFontColor(color)
		textLine.SetText(text)
		textLine.SetOutline()
		textLine.SetFeather(FALSE)
		textLine.Show()
		if localeInfo.IsARABIC():
			textLine.SetHorizontalAlignRight()
		
		textLine.SetPosition(15, self.toolTipHeight)
		
		self.childrenList.append(textLine)
		(textWidth, textHeight) = textLine.GetTextSize()
		textWidth += 30
		textHeight += 10
		if self.toolTipWidth < textWidth:
			self.toolTipWidth = textWidth
		
		self.toolTipHeight += textHeight
		self.ResizeToolTipText(textWidth, self.toolTipHeight)
		return textLine
		
	def AppendTextLine(self, text, color = FONT_COLOR, centerAlign = True):
		textLine = ui.TextLine()
		textLine.SetParent(self)
		textLine.SetFontName(self.defFontName)
		textLine.SetPackedFontColor(color)
		textLine.SetText(text)
		textLine.SetOutline()
		textLine.SetFeather(False)
		textLine.Show()

		if centerAlign:
			textLine.SetPosition(self.toolTipWidth/2, self.toolTipHeight)
			textLine.SetHorizontalAlignCenter()

		else:
			textLine.SetPosition(10, self.toolTipHeight)

		self.childrenList.append(textLine)

		self.toolTipHeight += self.TEXT_LINE_HEIGHT
		self.ResizeToolTip()

		return textLine

	def AppendDescription(self, desc, limit, color = FONT_COLOR):
		if localeInfo.IsEUROPE():
			self.__AppendDescription_WesternLanguage(desc, color)
		else:
			self.__AppendDescription_EasternLanguage(desc, limit, color)

	def __AppendDescription_EasternLanguage(self, description, characterLimitation, color=FONT_COLOR):
		length = len(description)
		if 0 == length:
			return

		lineCount = grpText.GetSplitingTextLineCount(description, characterLimitation)
		for i in xrange(lineCount):
			if 0 == i:
				self.AppendSpace(5)
			self.AppendTextLine(grpText.GetSplitingTextLine(description, characterLimitation, i), color)

	def __AppendDescription_WesternLanguage(self, desc, color=FONT_COLOR):
		lines = SplitDescription(desc, DESC_WESTERN_MAX_COLS)
		if not lines:
			return

		self.AppendSpace(5)
		for line in lines:
			self.AppendTextLine(line, color)


	def ResizeToolTip(self):
		self.SetSize(self.toolTipWidth, self.TOOL_TIP_HEIGHT + self.toolTipHeight)
		
	def SetTitle(self, name):
		self.AppendTextLine(name, self.TITLE_COLOR)

	def GetLimitTextLineColor(self, curValue, limitValue):
		if curValue < limitValue:
			return self.DISABLE_COLOR

		return self.ENABLE_COLOR

	def GetChangeTextLineColor(self, value, isSpecial=False):
		if value > 0:
			if isSpecial:
				return self.SPECIAL_POSITIVE_COLOR
			else:
				return self.POSITIVE_COLOR

		if 0 == value:
			return self.NORMAL_COLOR

		return self.NEGATIVE_COLOR

	def SetToolTipPosition(self, x = -1, y = -1):
		self.xPos = x
		self.yPos = y

	def ShowToolTip(self):
		self.SetTop()
		self.Show()

		self.OnUpdate()

	def HideToolTip(self):
		self.Hide()

	def OnUpdate(self):

		if not self.followFlag:
			return

		x = 0
		y = 0
		width = self.GetWidth()
		height = self.toolTipHeight

		if -1 == self.xPos and -1 == self.yPos:

			(mouseX, mouseY) = wndMgr.GetMousePosition()

			if mouseY < wndMgr.GetScreenHeight() - 300:
				y = mouseY + 40
			else:
				y = mouseY - height - 30

			x = mouseX - width/2

		else:

			x = self.xPos - width/2
			y = self.yPos - height

		x = max(x, 0)
		y = max(y, 0)
		x = min(x + width/2, wndMgr.GetScreenWidth() - width/2) - width/2
		y = min(y + self.GetHeight(), wndMgr.GetScreenHeight()) - self.GetHeight()

		parentWindow = self.GetParentProxy()
		if parentWindow:
			(gx, gy) = parentWindow.GetGlobalPosition()
			x -= gx
			y -= gy

		self.SetPosition(x, y)

class ItemToolTip(ToolTip):

	CHARACTER_NAMES = (
		localeInfo.TOOLTIP_WARRIOR,
		localeInfo.TOOLTIP_ASSASSIN,
		localeInfo.TOOLTIP_SURA,
		localeInfo.TOOLTIP_SHAMAN
	)
	# if app.ENABLE_WOLFMAN_CHARACTER:
		# CHARACTER_NAMES += (
			# localeInfo.TOOLTIP_WOLFMAN,
		# )
	if app.ENABLE_SEND_TARGET_INFO:
		isStone = False
		isBook = False
		isBook2 = False

	CHARACTER_COUNT = len(CHARACTER_NAMES)
	WEAR_NAMES = (
		localeInfo.TOOLTIP_ARMOR,
		localeInfo.TOOLTIP_HELMET,
		localeInfo.TOOLTIP_SHOES,
		localeInfo.TOOLTIP_WRISTLET,
		localeInfo.TOOLTIP_WEAPON,
		localeInfo.TOOLTIP_NECK,
		localeInfo.TOOLTIP_EAR,
		localeInfo.TOOLTIP_UNIQUE,
		localeInfo.TOOLTIP_SHIELD,
		localeInfo.TOOLTIP_ARROW,
	)
	WEAR_COUNT = len(WEAR_NAMES)

	AFFECT_DICT = {
		item.APPLY_MAX_HP : localeInfo.TOOLTIP_MAX_HP,
		item.APPLY_MAX_SP : localeInfo.TOOLTIP_MAX_SP,
		item.APPLY_CON : localeInfo.TOOLTIP_CON,
		item.APPLY_INT : localeInfo.TOOLTIP_INT,
		item.APPLY_STR : localeInfo.TOOLTIP_STR,
		item.APPLY_DEX : localeInfo.TOOLTIP_DEX,
		item.APPLY_ATT_SPEED : localeInfo.TOOLTIP_ATT_SPEED,
		item.APPLY_MOV_SPEED : localeInfo.TOOLTIP_MOV_SPEED,
		item.APPLY_CAST_SPEED : localeInfo.TOOLTIP_CAST_SPEED,
		item.APPLY_HP_REGEN : localeInfo.TOOLTIP_HP_REGEN,
		item.APPLY_SP_REGEN : localeInfo.TOOLTIP_SP_REGEN,
		item.APPLY_POISON_PCT : localeInfo.TOOLTIP_APPLY_POISON_PCT,
		item.APPLY_STUN_PCT : localeInfo.TOOLTIP_APPLY_STUN_PCT,
		item.APPLY_SLOW_PCT : localeInfo.TOOLTIP_APPLY_SLOW_PCT,
		item.APPLY_CRITICAL_PCT : localeInfo.TOOLTIP_APPLY_CRITICAL_PCT,
		item.APPLY_PENETRATE_PCT : localeInfo.TOOLTIP_APPLY_PENETRATE_PCT,

		item.APPLY_ATTBONUS_WARRIOR : localeInfo.TOOLTIP_APPLY_ATTBONUS_WARRIOR,
		item.APPLY_ATTBONUS_ASSASSIN : localeInfo.TOOLTIP_APPLY_ATTBONUS_ASSASSIN,
		item.APPLY_ATTBONUS_SURA : localeInfo.TOOLTIP_APPLY_ATTBONUS_SURA,
		item.APPLY_ATTBONUS_SHAMAN : localeInfo.TOOLTIP_APPLY_ATTBONUS_SHAMAN,
		item.APPLY_ATTBONUS_MONSTER : localeInfo.TOOLTIP_APPLY_ATTBONUS_MONSTER,

		item.APPLY_ATTBONUS_HUMAN : localeInfo.TOOLTIP_APPLY_ATTBONUS_HUMAN,
		item.APPLY_ATTBONUS_ANIMAL : localeInfo.TOOLTIP_APPLY_ATTBONUS_ANIMAL,
		item.APPLY_ATTBONUS_ORC : localeInfo.TOOLTIP_APPLY_ATTBONUS_ORC,
		item.APPLY_ATTBONUS_MILGYO : localeInfo.TOOLTIP_APPLY_ATTBONUS_MILGYO,
		item.APPLY_ATTBONUS_UNDEAD : localeInfo.TOOLTIP_APPLY_ATTBONUS_UNDEAD,
		item.APPLY_ATTBONUS_DEVIL : localeInfo.TOOLTIP_APPLY_ATTBONUS_DEVIL,
		item.APPLY_STEAL_HP : localeInfo.TOOLTIP_APPLY_STEAL_HP,
		item.APPLY_STEAL_SP : localeInfo.TOOLTIP_APPLY_STEAL_SP,
		item.APPLY_MANA_BURN_PCT : localeInfo.TOOLTIP_APPLY_MANA_BURN_PCT,
		item.APPLY_DAMAGE_SP_RECOVER : localeInfo.TOOLTIP_APPLY_DAMAGE_SP_RECOVER,
		item.APPLY_BLOCK : localeInfo.TOOLTIP_APPLY_BLOCK,
		item.APPLY_DODGE : localeInfo.TOOLTIP_APPLY_DODGE,
		item.APPLY_RESIST_SWORD : localeInfo.TOOLTIP_APPLY_RESIST_SWORD,
		item.APPLY_RESIST_TWOHAND : localeInfo.TOOLTIP_APPLY_RESIST_TWOHAND,
		item.APPLY_RESIST_DAGGER : localeInfo.TOOLTIP_APPLY_RESIST_DAGGER,
		item.APPLY_RESIST_BELL : localeInfo.TOOLTIP_APPLY_RESIST_BELL,
		item.APPLY_RESIST_FAN : localeInfo.TOOLTIP_APPLY_RESIST_FAN,
		item.APPLY_RESIST_BOW : localeInfo.TOOLTIP_RESIST_BOW,
		item.APPLY_RESIST_FIRE : localeInfo.TOOLTIP_RESIST_FIRE,
		item.APPLY_RESIST_ELEC : localeInfo.TOOLTIP_RESIST_ELEC,
		item.APPLY_RESIST_MAGIC : localeInfo.TOOLTIP_RESIST_MAGIC,
		item.APPLY_RESIST_WIND : localeInfo.TOOLTIP_APPLY_RESIST_WIND,
		item.APPLY_REFLECT_MELEE : localeInfo.TOOLTIP_APPLY_REFLECT_MELEE,
		item.APPLY_REFLECT_CURSE : localeInfo.TOOLTIP_APPLY_REFLECT_CURSE,
		item.APPLY_POISON_REDUCE : localeInfo.TOOLTIP_APPLY_POISON_REDUCE,
		item.APPLY_KILL_SP_RECOVER : localeInfo.TOOLTIP_APPLY_KILL_SP_RECOVER,
		item.APPLY_EXP_DOUBLE_BONUS : localeInfo.TOOLTIP_APPLY_EXP_DOUBLE_BONUS,
		item.APPLY_GOLD_DOUBLE_BONUS : localeInfo.TOOLTIP_APPLY_GOLD_DOUBLE_BONUS,
		item.APPLY_ITEM_DROP_BONUS : localeInfo.TOOLTIP_APPLY_ITEM_DROP_BONUS,
		item.APPLY_POTION_BONUS : localeInfo.TOOLTIP_APPLY_POTION_BONUS,
		item.APPLY_KILL_HP_RECOVER : localeInfo.TOOLTIP_APPLY_KILL_HP_RECOVER,
		item.APPLY_IMMUNE_STUN : localeInfo.TOOLTIP_APPLY_IMMUNE_STUN,
		item.APPLY_IMMUNE_SLOW : localeInfo.TOOLTIP_APPLY_IMMUNE_SLOW,
		item.APPLY_IMMUNE_FALL : localeInfo.TOOLTIP_APPLY_IMMUNE_FALL,
		item.APPLY_BOW_DISTANCE : localeInfo.TOOLTIP_BOW_DISTANCE,
		item.APPLY_DEF_GRADE_BONUS : localeInfo.TOOLTIP_DEF_GRADE,
		item.APPLY_ATT_GRADE_BONUS : localeInfo.TOOLTIP_ATT_GRADE,
		item.APPLY_MAGIC_ATT_GRADE : localeInfo.TOOLTIP_MAGIC_ATT_GRADE,
		item.APPLY_MAGIC_DEF_GRADE : localeInfo.TOOLTIP_MAGIC_DEF_GRADE,
		item.APPLY_MAX_STAMINA : localeInfo.TOOLTIP_MAX_STAMINA,
		item.APPLY_MALL_ATTBONUS : localeInfo.TOOLTIP_MALL_ATTBONUS,
		item.APPLY_MALL_DEFBONUS : localeInfo.TOOLTIP_MALL_DEFBONUS,
		item.APPLY_MALL_EXPBONUS : localeInfo.TOOLTIP_MALL_EXPBONUS,
		item.APPLY_MALL_ITEMBONUS : localeInfo.TOOLTIP_MALL_ITEMBONUS,
		item.APPLY_MALL_GOLDBONUS : localeInfo.TOOLTIP_MALL_GOLDBONUS,
		item.APPLY_SKILL_DAMAGE_BONUS : localeInfo.TOOLTIP_SKILL_DAMAGE_BONUS,
		item.APPLY_NORMAL_HIT_DAMAGE_BONUS : localeInfo.TOOLTIP_NORMAL_HIT_DAMAGE_BONUS,
		item.APPLY_SKILL_DEFEND_BONUS : localeInfo.TOOLTIP_SKILL_DEFEND_BONUS,
		item.APPLY_NORMAL_HIT_DEFEND_BONUS : localeInfo.TOOLTIP_NORMAL_HIT_DEFEND_BONUS,
		item.APPLY_PC_BANG_EXP_BONUS : localeInfo.TOOLTIP_MALL_EXPBONUS_P_STATIC,
		item.APPLY_PC_BANG_DROP_BONUS : localeInfo.TOOLTIP_MALL_ITEMBONUS_P_STATIC,
		item.APPLY_RESIST_WARRIOR : localeInfo.TOOLTIP_APPLY_RESIST_WARRIOR,
		item.APPLY_RESIST_ASSASSIN : localeInfo.TOOLTIP_APPLY_RESIST_ASSASSIN,
		item.APPLY_RESIST_SURA : localeInfo.TOOLTIP_APPLY_RESIST_SURA,
		item.APPLY_RESIST_SHAMAN : localeInfo.TOOLTIP_APPLY_RESIST_SHAMAN,
		item.APPLY_MAX_HP_PCT : localeInfo.TOOLTIP_APPLY_MAX_HP_PCT,
		item.APPLY_MAX_SP_PCT : localeInfo.TOOLTIP_APPLY_MAX_SP_PCT,
		item.APPLY_ENERGY : localeInfo.TOOLTIP_ENERGY,
		item.APPLY_COSTUME_ATTR_BONUS : localeInfo.TOOLTIP_COSTUME_ATTR_BONUS,

		item.APPLY_MAGIC_ATTBONUS_PER : localeInfo.TOOLTIP_MAGIC_ATTBONUS_PER,
		item.APPLY_MELEE_MAGIC_ATTBONUS_PER : localeInfo.TOOLTIP_MELEE_MAGIC_ATTBONUS_PER,
		item.APPLY_RESIST_ICE : localeInfo.TOOLTIP_RESIST_ICE,
		item.APPLY_RESIST_EARTH : localeInfo.TOOLTIP_RESIST_EARTH,
		item.APPLY_RESIST_DARK : localeInfo.TOOLTIP_RESIST_DARK,
		item.APPLY_ANTI_CRITICAL_PCT : localeInfo.TOOLTIP_ANTI_CRITICAL_PCT,
		item.APPLY_ANTI_PENETRATE_PCT : localeInfo.TOOLTIP_ANTI_PENETRATE_PCT,
		item.APPLY_ATTBONUS_WOLFMAN : localeInfo.TOOLTIP_APPLY_ATTBONUS_WOLFMAN,
	}
	
	AFFECT_DICT_POINT = {
		item.APPLY_MAX_HP : 6,
		item.APPLY_MAX_SP : 8,
		item.APPLY_CON : 13,
		item.APPLY_INT : 15,
		item.APPLY_STR : 12,
		item.APPLY_DEX : 14,
		item.APPLY_ATT_SPEED : 17,
		item.APPLY_MOV_SPEED : 19,
		item.APPLY_CAST_SPEED : 21,
		item.APPLY_HP_REGEN : 32,
		item.APPLY_SP_REGEN : 33,
		item.APPLY_POISON_PCT : 37,
		item.APPLY_STUN_PCT : 38,
		item.APPLY_SLOW_PCT : 39,
		item.APPLY_CRITICAL_PCT : 40,
		item.APPLY_PENETRATE_PCT : 41,
		item.APPLY_ATTBONUS_WARRIOR : 54,
		item.APPLY_ATTBONUS_ASSASSIN : 55,
		item.APPLY_ATTBONUS_SURA : 56,
		item.APPLY_ATTBONUS_SHAMAN : 57,
		item.APPLY_ATTBONUS_MONSTER : 53,
		item.APPLY_ATTBONUS_HUMAN : 43,
		item.APPLY_ATTBONUS_ANIMAL : 44,
		item.APPLY_ATTBONUS_ORC : 45,
		item.APPLY_ATTBONUS_MILGYO : 46,
		item.APPLY_ATTBONUS_UNDEAD : 47,
		item.APPLY_ATTBONUS_DEVIL : 48,
		item.APPLY_STEAL_HP : 63,
		item.APPLY_STEAL_SP : 64,
		item.APPLY_MANA_BURN_PCT : 65,
		item.APPLY_DAMAGE_SP_RECOVER : 66,
		item.APPLY_BLOCK : 67,
		item.APPLY_DODGE : 68,
		item.APPLY_RESIST_SWORD : 69,
		item.APPLY_RESIST_TWOHAND : 70,
		item.APPLY_RESIST_DAGGER : 71,
		item.APPLY_RESIST_BELL : 72,
		item.APPLY_RESIST_FAN : 73,
		item.APPLY_RESIST_BOW : 74,
		item.APPLY_RESIST_FIRE : 75,
		item.APPLY_RESIST_ELEC : 76,
		item.APPLY_RESIST_MAGIC : 77,
		item.APPLY_RESIST_WIND : 78,
		item.APPLY_REFLECT_MELEE : 79,
		item.APPLY_REFLECT_CURSE : 80,
		item.APPLY_POISON_REDUCE : 81,
		item.APPLY_KILL_SP_RECOVER : 82,
		item.APPLY_EXP_DOUBLE_BONUS : 83,
		item.APPLY_GOLD_DOUBLE_BONUS : 84,
		item.APPLY_ITEM_DROP_BONUS : 85,
		item.APPLY_POTION_BONUS : 86,
		item.APPLY_KILL_HP_RECOVER : 87,
		item.APPLY_IMMUNE_STUN : 88,
		item.APPLY_IMMUNE_SLOW : 89,
		item.APPLY_IMMUNE_FALL : 90,
		item.APPLY_BOW_DISTANCE : 34,
		item.APPLY_DEF_GRADE_BONUS : 96,
		item.APPLY_ATT_GRADE_BONUS : 95,
		item.APPLY_MAGIC_ATT_GRADE : 97,
		item.APPLY_MAGIC_DEF_GRADE : 98,
		item.APPLY_MAX_STAMINA : 10,
		item.APPLY_MALL_ATTBONUS : 114,
		item.APPLY_MALL_DEFBONUS : 115,
		item.APPLY_MALL_EXPBONUS : 116,
		item.APPLY_MALL_ITEMBONUS : 117,
		item.APPLY_MALL_GOLDBONUS : 118,
		item.APPLY_SKILL_DAMAGE_BONUS : 121,
		item.APPLY_NORMAL_HIT_DAMAGE_BONUS : 122,
		item.APPLY_SKILL_DEFEND_BONUS : 123,
		item.APPLY_NORMAL_HIT_DEFEND_BONUS : 124,
		item.APPLY_PC_BANG_EXP_BONUS : 125,
		item.APPLY_PC_BANG_DROP_BONUS : 126,
		item.APPLY_RESIST_WARRIOR : 59,
		item.APPLY_RESIST_ASSASSIN : 60,
		item.APPLY_RESIST_SURA : 61,
		item.APPLY_RESIST_SHAMAN : 62,
		item.APPLY_MAX_HP_PCT : 119,
		item.APPLY_MAX_SP_PCT : 120,
		# item.APPLY_ENERGY : 128,
		item.APPLY_COSTUME_ATTR_BONUS : 130,
		item.APPLY_MAGIC_ATTBONUS_PER : 131,
		item.APPLY_MELEE_MAGIC_ATTBONUS_PER : 132,
		item.APPLY_RESIST_ICE : 133,
		item.APPLY_RESIST_EARTH : 134,
		item.APPLY_RESIST_DARK : 135,
		item.APPLY_ANTI_CRITICAL_PCT : 136,
		item.APPLY_ANTI_PENETRATE_PCT : 137,
		item.APPLY_ATTBONUS_WOLFMAN : 94,
	}
	
	if app.ENABLE_WOLFMAN_CHARACTER:
		AFFECT_DICT.update({
			item.APPLY_BLEEDING_PCT : localeInfo.TOOLTIP_APPLY_BLEEDING_PCT,
			item.APPLY_BLEEDING_REDUCE : localeInfo.TOOLTIP_APPLY_BLEEDING_REDUCE,
			item.APPLY_ATTBONUS_WOLFMAN : localeInfo.TOOLTIP_APPLY_ATTBONUS_WOLFMAN,
			item.APPLY_RESIST_CLAW : localeInfo.TOOLTIP_APPLY_RESIST_CLAW,
			item.APPLY_RESIST_WOLFMAN : localeInfo.TOOLTIP_APPLY_RESIST_WOLFMAN,
		})

	ATTRIBUTE_NEED_WIDTH = {
		23 : 230,
		24 : 230,
		25 : 230,
		26 : 220,
		27 : 210,

		35 : 210,
		36 : 210,
		37 : 210,
		38 : 210,
		39 : 210,
		40 : 210,
		41 : 210,

		42 : 220,
		43 : 230,
		45 : 230,
	}

	ANTI_FLAG_DICT = {
		0 : item.ITEM_ANTIFLAG_WARRIOR,
		1 : item.ITEM_ANTIFLAG_ASSASSIN,
		2 : item.ITEM_ANTIFLAG_SURA,
		3 : item.ITEM_ANTIFLAG_SHAMAN,
	}
	# if app.ENABLE_WOLFMAN_CHARACTER:
		# ANTI_FLAG_DICT.update({
			# 4 : item.ITEM_ANTIFLAG_WOLFMAN,
		# })

	FONT_COLOR = grp.GenerateColor(0.7607, 0.7607, 0.7607, 1.0)

	def __init__(self, *args, **kwargs):
		ToolTip.__init__(self, *args, **kwargs)
		self.itemVnum = 0
		self.isShopItem = False

		# 아이템 툴팁을 표시할 때 현재 캐릭터가 착용할 수 없는 아이템이라면 강제로 Disable Color로 설정 (이미 그렇게 작동하고 있으나 꺼야 할 필요가 있어서)
		self.bCannotUseItemForceSetDisableColor = True

	def __del__(self):
		ToolTip.__del__(self)

	def SetCannotUseItemForceSetDisableColor(self, enable):
		self.bCannotUseItemForceSetDisableColor = enable

	def CanEquip(self):
		if not item.IsEquipmentVID(self.itemVnum):
			return True

		race = player.GetRace()
		job = chr.RaceToJob(race)
		if not self.ANTI_FLAG_DICT.has_key(job):
			return False

		if item.IsAntiFlag(self.ANTI_FLAG_DICT[job]):
			return False

		sex = chr.RaceToSex(race)

		MALE = 1
		FEMALE = 0

		if item.IsAntiFlag(item.ITEM_ANTIFLAG_MALE) and sex == MALE:
			return False

		if item.IsAntiFlag(item.ITEM_ANTIFLAG_FEMALE) and sex == FEMALE:
			return False

		for i in xrange(item.LIMIT_MAX_NUM):
			(limitType, limitValue) = item.GetLimit(i)

			if item.LIMIT_LEVEL == limitType:
				if player.GetStatus(player.LEVEL) < limitValue:
					return False
			"""
			elif item.LIMIT_STR == limitType:
				if player.GetStatus(player.ST) < limitValue:
					return False
			elif item.LIMIT_DEX == limitType:
				if player.GetStatus(player.DX) < limitValue:
					return False
			elif item.LIMIT_INT == limitType:
				if player.GetStatus(player.IQ) < limitValue:
					return False
			elif item.LIMIT_CON == limitType:
				if player.GetStatus(player.HT) < limitValue:
					return False
			"""

		return True

	def AppendTextLine(self, text, color = FONT_COLOR, centerAlign = True):
		if not self.CanEquip() and self.bCannotUseItemForceSetDisableColor:
			color = self.DISABLE_COLOR

		return ToolTip.AppendTextLine(self, text, color, centerAlign)

	def ClearToolTip(self):
		self.isShopItem = False
		self.toolTipWidth = self.TOOL_TIP_WIDTH
		ToolTip.ClearToolTip(self)

	def SetInventoryItem(self, slotIndex, window_type = player.INVENTORY):
		itemVnum = player.GetItemIndex(window_type, slotIndex)
		if 0 == itemVnum:
			return

		self.ClearToolTip()
		if shop.IsOpen():
			if not shop.IsPrivateShop():
				item.SelectItem(itemVnum)
				self.AppendSellingPrice(player.GetISellItemPrice(window_type, slotIndex))

		metinSlot = [player.GetItemMetinSocket(window_type, slotIndex, i) for i in xrange(player.METIN_SOCKET_MAX_NUM)]
		attrSlot = [player.GetItemAttribute(window_type, slotIndex, i) for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM)]

		if app.ENABLE_CHANGELOOK_SYSTEM:
			self.AddItemData(itemVnum, metinSlot, attrSlot, 0, player.INVENTORY, slotIndex)
		else:
			self.AddItemData(itemVnum, metinSlot, attrSlot)
	if app.ENABLE_SEND_TARGET_INFO:
		def SetItemToolTipStone(self, itemVnum):
			self.itemVnum = itemVnum
			item.SelectItem(itemVnum)
			itemType = item.GetItemType()

			itemDesc = item.GetItemDescription()
			itemSummary = item.GetItemSummary()
			attrSlot = 0
			self.__AdjustMaxWidth(attrSlot, itemDesc)
			itemName = item.GetItemName()
			realName = itemName[:itemName.find("+")]
			self.SetTitle(realName + " +0 - +4")

			## Description ###
			self.AppendDescription(itemDesc, 26)
			self.AppendDescription(itemSummary, 26, self.CONDITION_COLOR)

			if item.ITEM_TYPE_METIN == itemType:
				self.AppendMetinInformation()
				self.AppendMetinWearInformation()

			for i in xrange(item.LIMIT_MAX_NUM):
				(limitType, limitValue) = item.GetLimit(i)

				if item.LIMIT_REAL_TIME_START_FIRST_USE == limitType:
					self.AppendRealTimeStartFirstUseLastTime(item, metinSlot, i)

				elif item.LIMIT_TIMER_BASED_ON_WEAR == limitType:
					self.AppendTimerBasedOnWearLastTime(metinSlot)

			self.ShowToolTip()

	def SetShopItem(self, slotIndex):
		itemVnum = shop.GetItemID(slotIndex)
		if 0 == itemVnum:
			return

		price = shop.GetItemPrice(slotIndex)
		self.ClearToolTip()
		self.isShopItem = True

		metinSlot = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(shop.GetItemMetinSocket(slotIndex, i))
		attrSlot = []
		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(shop.GetItemAttribute(slotIndex, i))

		if app.ENABLE_CHANGELOOK_SYSTEM:
			transmutation = shop.GetItemTransmutation(slotIndex)
			if not transmutation:
				self.AddItemData(itemVnum, metinSlot, attrSlot)
			else:
				self.AddItemData(itemVnum, metinSlot, attrSlot, 0, player.INVENTORY, -1, transmutation)
		else:
			self.AddItemData(itemVnum, metinSlot, attrSlot)
		if app.__MULTI_SHOP__:
			if shop.GetBuyWithItem(slotIndex) != 0:
				self.AppendPriceTextLine(shop.GetBuyWithItemCount(slotIndex), shop.GetBuyWithItem(slotIndex))
			else:
				self.AppendPrice(price)
		else:
			self.AppendPrice(price)

	if app.ENABLE_BATTLE_FIELD:
		def SetShopItemBySecondaryCoin(self, slotIndex, coinType):
			itemVnum = shop.GetItemID(slotIndex)
			if 0 == itemVnum:
				return
	
			price = shop.GetItemPrice(slotIndex)
			self.ClearToolTip()
			self.isShopItem = True
	
			metinSlot = []
			for i in xrange(player.METIN_SOCKET_MAX_NUM):
				metinSlot.append(shop.GetItemMetinSocket(slotIndex, i))
			attrSlot = []
			for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
				attrSlot.append(shop.GetItemAttribute(slotIndex, i))
	
			self.AddItemData(itemVnum, metinSlot, attrSlot)
			self.AppendPriceBySecondaryCoin(price, coinType)
	else:
		def SetShopItemBySecondaryCoin(self, slotIndex):
			itemVnum = shop.GetItemID(slotIndex)
			if 0 == itemVnum:
				return
	
			price = shop.GetItemPrice(slotIndex)
			self.ClearToolTip()
			self.isShopItem = True
	
			metinSlot = []
			for i in xrange(player.METIN_SOCKET_MAX_NUM):
				metinSlot.append(shop.GetItemMetinSocket(slotIndex, i))
			attrSlot = []
			for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
				attrSlot.append(shop.GetItemAttribute(slotIndex, i))
	
			self.AddItemData(itemVnum, metinSlot, attrSlot)
			self.AppendPriceBySecondaryCoin(price)
			
	def SetExchangeOwnerItem(self, slotIndex):
		itemVnum = exchange.GetItemVnumFromSelf(slotIndex)
		if 0 == itemVnum:
			return

		self.ClearToolTip()

		metinSlot = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(exchange.GetItemMetinSocketFromSelf(slotIndex, i))
		attrSlot = []
		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(exchange.GetItemAttributeFromSelf(slotIndex, i))
		if app.ENABLE_CHANGELOOK_SYSTEM:
			transmutation = exchange.GetItemTransmutation(slotIndex, True)
			if not transmutation:
				self.AddItemData(itemVnum, metinSlot, attrSlot)
			else:
				self.AddItemData(itemVnum, metinSlot, attrSlot, 0, player.INVENTORY, -1, transmutation)
		else:
			self.AddItemData(itemVnum, metinSlot, attrSlot)

	def SetExchangeTargetItem(self, slotIndex):
		itemVnum = exchange.GetItemVnumFromTarget(slotIndex)
		if 0 == itemVnum:
			return

		self.ClearToolTip()

		metinSlot = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(exchange.GetItemMetinSocketFromTarget(slotIndex, i))
		attrSlot = []
		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(exchange.GetItemAttributeFromTarget(slotIndex, i))
		if app.ENABLE_CHANGELOOK_SYSTEM:
			transmutation = exchange.GetItemTransmutation(slotIndex, False)
			if not transmutation:
				self.AddItemData(itemVnum, metinSlot, attrSlot)
			else:
				self.AddItemData(itemVnum, metinSlot, attrSlot, 0, player.INVENTORY, -1, transmutation)
		else:
			self.AddItemData(itemVnum, metinSlot, attrSlot)

	def SetPrivateShopBuilderItem(self, invenType, invenPos, price):
		itemVnum = player.GetItemIndex(invenType, invenPos)
		if 0 == itemVnum:
			return

		item.SelectItem(itemVnum)
		self.ClearToolTip()

		metinSlot = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(player.GetItemMetinSocket(invenPos, i))
		attrSlot = []
		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(player.GetItemAttribute(invenPos, i))

		if app.ENABLE_CHANGELOOK_SYSTEM:
			self.AddItemData(itemVnum, metinSlot, attrSlot, 0, invenType, invenPos)
		else:
			self.AddItemData(itemVnum, metinSlot, attrSlot, 0)
		self.AppendSellingPrice(shop.GetPrivateShopItemPrice(invenType, invenPos))
		
	def SetSafeBoxItem(self, slotIndex):
		itemVnum = safebox.GetItemID(slotIndex)
		if 0 == itemVnum:
			return

		self.ClearToolTip()
		metinSlot = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(safebox.GetItemMetinSocket(slotIndex, i))
		attrSlot = []
		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(safebox.GetItemAttribute(slotIndex, i))

		if app.ENABLE_CHANGELOOK_SYSTEM:
			self.AddItemData(itemVnum, metinSlot, attrSlot, safebox.GetItemFlags(slotIndex), player.SAFEBOX, slotIndex)
		else:
			self.AddItemData(itemVnum, metinSlot, attrSlot, safebox.GetItemFlags(slotIndex))
			
	def SetMallItem(self, slotIndex):
		itemVnum = safebox.GetMallItemID(slotIndex)
		if 0 == itemVnum:
			return

		self.ClearToolTip()
		metinSlot = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(safebox.GetMallItemMetinSocket(slotIndex, i))
		attrSlot = []
		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(safebox.GetMallItemAttribute(slotIndex, i))

		if app.ENABLE_CHANGELOOK_SYSTEM:
			self.AddItemData(itemVnum, metinSlot, attrSlot, 0, player.MALL, slotIndex)
		else:
			self.AddItemData(itemVnum, metinSlot, attrSlot)


	def SetItemToolTip(self, itemVnum):
		self.ClearToolTip()
		metinSlot = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(0)
		attrSlot = []
		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append((0, 0))

		self.AddItemData(itemVnum, metinSlot, attrSlot)

	if app.ENABLE_ATTENDANCE_EVENT:
		def SetAttendanceRewardItem(self, itemVnum, itemCount):
			if 0 == itemVnum:
				return

			self.ClearToolTip()
			self.isAttendanceRewardItem = True
			
			metinSlot = []
			for i in xrange(player.METIN_SOCKET_MAX_NUM):
				metinSlot.append(0)
			attrSlot = []
			for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
				attrSlot.append((0, 0))
				
			metinSlot[0] = itemCount

			self.AddItemData(itemVnum, metinSlot, attrSlot)		
		
	def __AppendAttackSpeedInfo(self, item):
		atkSpd = item.GetValue(0)

		if atkSpd < 80:
			stSpd = localeInfo.TOOLTIP_ITEM_VERY_FAST
		elif atkSpd <= 95:
			stSpd = localeInfo.TOOLTIP_ITEM_FAST
		elif atkSpd <= 105:
			stSpd = localeInfo.TOOLTIP_ITEM_NORMAL
		elif atkSpd <= 120:
			stSpd = localeInfo.TOOLTIP_ITEM_SLOW
		else:
			stSpd = localeInfo.TOOLTIP_ITEM_VERY_SLOW

		self.AppendTextLine(localeInfo.TOOLTIP_ITEM_ATT_SPEED % stSpd, self.NORMAL_COLOR)

	def __AppendAttackGradeInfo(self):
		atkGrade = item.GetValue(1)
		self.AppendTextLine(localeInfo.TOOLTIP_ITEM_ATT_GRADE % atkGrade, self.GetChangeTextLineColor(atkGrade))

	if app.ENABLE_SASH_SYSTEM:
		def CalcSashValue(self, value, abs):
			if not value:
				return 0
			
			valueCalc = int((round(value * abs) / 100) - .5) + int(int((round(value * abs) / 100) - .5) > 0)
			if valueCalc <= 0 and value > 0:
				value = 1
			else:
				value = valueCalc
			
			return value

	def __AppendAttackPowerInfo(self, itemAbsChance = 0):
		minPower = item.GetValue(3)
		maxPower = item.GetValue(4)
		addPower = item.GetValue(5)
		
		if app.ENABLE_SASH_SYSTEM:
			if itemAbsChance:
				minPower = self.CalcSashValue(minPower, itemAbsChance)
				maxPower = self.CalcSashValue(maxPower, itemAbsChance)
				addPower = self.CalcSashValue(addPower, itemAbsChance)
		
		if maxPower > minPower:
			self.AppendTextLine(localeInfo.TOOLTIP_ITEM_ATT_POWER % (minPower + addPower, maxPower + addPower), self.POSITIVE_COLOR)
		else:
			self.AppendTextLine(localeInfo.TOOLTIP_ITEM_ATT_POWER_ONE_ARG % (minPower + addPower), self.POSITIVE_COLOR)

	def __AppendMagicAttackInfo(self, itemAbsChance = 0):
		minMagicAttackPower = item.GetValue(1)
		maxMagicAttackPower = item.GetValue(2)
		addPower = item.GetValue(5)
		
		if app.ENABLE_SASH_SYSTEM:
			if itemAbsChance:
				minMagicAttackPower = self.CalcSashValue(minMagicAttackPower, itemAbsChance)
				maxMagicAttackPower = self.CalcSashValue(maxMagicAttackPower, itemAbsChance)
				addPower = self.CalcSashValue(addPower, itemAbsChance)
		
		if minMagicAttackPower > 0 or maxMagicAttackPower > 0:
			if maxMagicAttackPower > minMagicAttackPower:
				self.AppendTextLine(localeInfo.TOOLTIP_ITEM_MAGIC_ATT_POWER % (minMagicAttackPower + addPower, maxMagicAttackPower + addPower), self.POSITIVE_COLOR)
			else:
				self.AppendTextLine(localeInfo.TOOLTIP_ITEM_MAGIC_ATT_POWER_ONE_ARG % (minMagicAttackPower + addPower), self.POSITIVE_COLOR)

	def __AppendMagicDefenceInfo(self, itemAbsChance = 0):
		magicDefencePower = item.GetValue(0)
		
		if app.ENABLE_SASH_SYSTEM:
			if itemAbsChance:
				magicDefencePower = self.CalcSashValue(magicDefencePower, itemAbsChance)
		
		if magicDefencePower > 0:
			self.AppendTextLine(localeInfo.TOOLTIP_ITEM_MAGIC_DEF_POWER % magicDefencePower, self.GetChangeTextLineColor(magicDefencePower))

	def __AppendAttributeInformation(self, attrSlot, itemAbsChance = 0):
		if 0 != attrSlot:
			for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
				type = attrSlot[i][0]
				value = attrSlot[i][1]
				if 0 == value:
					continue
				
				affectString = self.__GetAffectString(type, value)
				if app.ENABLE_SASH_SYSTEM:
					if item.GetItemType() == item.ITEM_TYPE_COSTUME and item.GetItemSubType() == item.COSTUME_TYPE_SASH and itemAbsChance:
						value = self.CalcSashValue(value, itemAbsChance)
						affectString = self.__GetAffectString(type, value)
				
				if affectString:
					affectColor = self.__GetAttributeColor(i, value)
					self.AppendTextLine(affectString, affectColor)

	def __GetAttributeColor(self, index, value):
		if value > 0:
			if index >= player.ATTRIBUTE_SLOT_RARE_START and index < player.ATTRIBUTE_SLOT_RARE_END:
				return self.SPECIAL_POSITIVE_COLOR2
			else:
				return self.SPECIAL_POSITIVE_COLOR
		elif value == 0:
			return self.NORMAL_COLOR
		else:
			return self.NEGATIVE_COLOR

	def __IsPolymorphItem(self, itemVnum):
		if itemVnum >= 70103 and itemVnum <= 70106:
			return 1
		return 0

	def __SetPolymorphItemTitle(self, monsterVnum):
		if localeInfo.IsVIETNAM():
			itemName =item.GetItemName()
			itemName+=" "
			itemName+=nonplayer.GetMonsterName(monsterVnum)
		else:
			itemName =nonplayer.GetMonsterName(monsterVnum)
			itemName+=" "
			itemName+=item.GetItemName()
		self.SetTitle(itemName)

	def __SetNormalItemTitle(self):
		if app.ENABLE_SEND_TARGET_INFO:
			if self.isStone:
				itemName = item.GetItemName()
				realName = itemName[:itemName.find("+")]
				self.SetTitle(realName + " +0 - +4")
			else:
				self.SetTitle(item.GetItemName())
		else:
			self.SetTitle(item.GetItemName())

	def __SetSpecialItemTitle(self):
		self.AppendTextLine(item.GetItemName(), self.SPECIAL_TITLE_COLOR)

	def __SetItemTitle(self, itemVnum, metinSlot, attrSlot):
		if app.ENABLE_ATTENDANCE_EVENT:
			if self.isAttendanceRewardItem:
				self.SetTitle(item.GetItemName()+" - |cffffc800|H|h"+str(metinSlot[0])+"buc|h|r")
				return
				
		if localeInfo.IsCANADA():
			if 72726 == itemVnum or 72730 == itemVnum:
				self.AppendTextLine(item.GetItemName(), grp.GenerateColor(1.0, 0.7843, 0.0, 1.0))
				return

		if self.__IsPolymorphItem(itemVnum):
			self.__SetPolymorphItemTitle(metinSlot[0])
		else:
			if self.__IsAttr(attrSlot):
				self.__SetSpecialItemTitle()
				return

			self.__SetNormalItemTitle()

	def __IsAttr(self, attrSlot):
		if not attrSlot:
			return False

		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			type = attrSlot[i][0]
			if 0 != type:
				return True

		return False

	def AddRefineItemData(self, itemVnum, metinSlot, attrSlot = 0):
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlotData=metinSlot[i]
			if self.GetMetinItemIndex(metinSlotData) == constInfo.ERROR_METIN_STONE:
				metinSlot[i]=player.METIN_SOCKET_TYPE_SILVER

		self.AddItemData(itemVnum, metinSlot, attrSlot)

	def AddItemData_Offline(self, itemVnum, itemDesc, itemSummary, metinSlot, attrSlot):
		self.__AdjustMaxWidth(attrSlot, itemDesc)
		self.__SetItemTitle(itemVnum, metinSlot, attrSlot)

		if self.__IsHair(itemVnum):
			self.__AppendHairIcon(itemVnum)
			
		### Description ###
		self.AppendDescription(itemDesc, 26)
		self.AppendDescription(itemSummary, 26, self.CONDITION_COLOR)
	
	def check_sigillo(self, item_vnum):
		for x in range(55701,55709):
			if x == item_vnum:
				return TRUE	
		if item_vnum == 55708:
			return TRUE
		return FALSE	
	
	def pet_system(self, item_vnum):
		for x in range(53001,53999):
			if x == item_vnum:
				return TRUE	
		if item_vnum == 53999:
			return TRUE
		return FALSE	
	
	def title_system(self, item_vnum):
		for x in range(39120,39140):
			if x == item_vnum:
				return TRUE	
		if item_vnum == 39140:
			return TRUE
		return FALSE	
	
	def sigilii_buffi(self, item_vnum):
		for x in range(91010,91020):
			if x == item_vnum:
				return TRUE	
		if item_vnum == 91020:
			return TRUE
		return FALSE	
	
	def sigilii_costume(self, item_vnum):
		for x in range(91025,91026):
			if x == item_vnum:
				return TRUE	
		if item_vnum == 91020:
			return TRUE
		return FALSE	
	
	def AddItemData(self, itemVnum, metinSlot, attrSlot = 0, flags = 0, window_type = player.INVENTORY, slotIndex = -1, transmutation = -1):

		self.itemVnum = itemVnum
		item.SelectItem(itemVnum)
		itemType = item.GetItemType()
		itemSubType = item.GetItemSubType()
		cofres = 0
		
		if 50026 == itemVnum:
			if 0 != metinSlot:
				name = item.GetItemName()
				if metinSlot[0] > 0:
					name += " "
					name += localeInfo.NumberToMoneyString(metinSlot[0])
				self.SetTitle(name)
				self.__AppendSealInformation(window_type, slotIndex) ## cyh itemseal 2013 11 11
				self.ShowToolTip()
			return

		### Skill Book ###
		if app.ENABLE_SEND_TARGET_INFO:
			if 50300 == itemVnum and not self.isBook:
				if 0 != metinSlot and not self.isBook:
					self.__SetSkillBookToolTip(metinSlot[0], localeInfo.TOOLTIP_SKILLBOOK_NAME, 1)
					self.ShowToolTip()
				elif self.isBook:
					self.SetTitle(item.GetItemName())
					self.AppendDescription(item.GetItemDescription(), 26)
					self.AppendDescription(item.GetItemSummary(), 26, self.CONDITION_COLOR)
					self.ShowToolTip()					
				return
			if cofres ==1:
				list_item =[[50300,localeInfo.TOOLTIP_SKILLBOOK_NAME],[70037,localeInfo.TOOLTIP_SKILL_FORGET_BOOK_NAME],[70055,localeInfo.TOOLTIP_SKILL_FORGET_BOOK_NAME]]
				for i in list_item:
					if itemVnum == i[0]:
						self.ShowToolTip()

			elif 70037 == itemVnum :
				if 0 != metinSlot and not self.isBook2:
					self.__SetSkillBookToolTip(metinSlot[0], localeInfo.TOOLTIP_SKILL_FORGET_BOOK_NAME, 0)
					self.AppendDescription(item.GetItemDescription(), 26)
					self.AppendDescription(item.GetItemSummary(), 26, self.CONDITION_COLOR)
					self.ShowToolTip()
				elif self.isBook2:
					self.SetTitle(item.GetItemName())
					self.AppendDescription(item.GetItemDescription(), 26)
					self.AppendDescription(item.GetItemSummary(), 26, self.CONDITION_COLOR)
					self.ShowToolTip()					
				return
			elif 70055 == itemVnum:
				if 0 != metinSlot:
					self.__SetSkillBookToolTip(metinSlot[0], localeInfo.TOOLTIP_SKILL_FORGET_BOOK_NAME, 0)
					self.AppendDescription(item.GetItemDescription(), 26)
					self.AppendDescription(item.GetItemSummary(), 26, self.CONDITION_COLOR)
					self.ShowToolTip()
				return
		else:
			if 50300 == itemVnum:
				if 0 != metinSlot:
					self.__SetSkillBookToolTip(metinSlot[0], localeInfo.TOOLTIP_SKILLBOOK_NAME, 1)
					self.ShowToolTip()
				return
			elif 70037 == itemVnum:
				if 0 != metinSlot:
					self.__SetSkillBookToolTip(metinSlot[0], localeInfo.TOOLTIP_SKILL_FORGET_BOOK_NAME, 0)
					self.AppendDescription(item.GetItemDescription(), 26)
					self.AppendDescription(item.GetItemSummary(), 26, self.CONDITION_COLOR)
					self.ShowToolTip()
				return
			elif 70055 == itemVnum:
				if 0 != metinSlot:
					self.__SetSkillBookToolTip(metinSlot[0], localeInfo.TOOLTIP_SKILL_FORGET_BOOK_NAME, 0)
					self.AppendDescription(item.GetItemDescription(), 26)
					self.AppendDescription(item.GetItemSummary(), 26, self.CONDITION_COLOR)
					self.ShowToolTip()
				return
		###########################################################################################


		itemDesc = item.GetItemDescription()
		itemSummary = item.GetItemSummary()

		isCostumeItem = 0
		isCostumeHair = 0
		isCostumeBody = 0
		if app.ENABLE_SASH_SYSTEM:
			isCostumeSash = 0
		if app.ENABLE_COSTUME_WEAPON_SYSTEM:
			isCostumeWeapon = 0

		if app.ENABLE_COSTUME_SYSTEM:
			if item.ITEM_TYPE_COSTUME == itemType:
				isCostumeItem = 1
				isCostumeHair = item.COSTUME_TYPE_HAIR == itemSubType
				isCostumeBody = item.COSTUME_TYPE_BODY == itemSubType
				if app.ENABLE_SASH_SYSTEM:
					isCostumeSash = itemSubType == item.COSTUME_TYPE_SASH
				if app.ENABLE_COSTUME_WEAPON_SYSTEM:
					isCostumeWeapon = item.COSTUME_TYPE_WEAPON == itemSubType
				#dbg.TraceError("IS_COSTUME_ITEM! body(%d) hair(%d)" % (isCostumeBody, isCostumeHair))

		self.__AdjustMaxWidth(attrSlot, itemDesc)
		self.__SetItemTitle(itemVnum, metinSlot, attrSlot)

		### Hair Preview Image ###
		if self.__IsHair(itemVnum):
			self.__AppendHairIcon(itemVnum)

		if app.ENABLE_ATTENDANCE_EVENT:
			if self.isAttendanceRewardItem:
				if not self.__IsHair(itemVnum):
					self.__AppendAttendanceRewardItemIcon(itemVnum)			
			
		### Description ###
		self.AppendDescription(itemDesc, 26)
		self.AppendDescription(itemSummary, 26, self.CONDITION_COLOR)
		
		if self.check_sigillo(itemVnum) or itemVnum == 55002:
			if attrSlot[0][1] != 0:
				self.AppendSpace(5)
				self.AppendTextLine("Level: "+str(metinSlot[1])+"("+str(metinSlot[2])+")", self.SPECIAL_TITLE_COLOR)
				self.AppendTextLine("HP: +"+pointop(str(attrSlot[0][1]))+"%", self.SPECIAL_POSITIVE_COLOR)
				self.AppendTextLine("DEF: +"+pointop(str(attrSlot[1][1]))+"%", self.SPECIAL_POSITIVE_COLOR)
				self.AppendTextLine("ATAC: +"+pointop(str(attrSlot[2][1]))+"%", self.SPECIAL_POSITIVE_COLOR)
				self.AppendSpace(5)
				if metinSlot[1] >= 50:
					self.AppendTextLine("Bonusuri Extra:", self.SPECIAL_TITLE_COLOR)
					self.AppendTextLine("+10% Tarie impotriva monstrilor", self.SPECIAL_POSITIVE_COLOR)
				if metinSlot[1] >= 81:
					self.AppendTextLine("+10% Paguba Abilitatii", self.SPECIAL_POSITIVE_COLOR)
				if metinSlot[1] >= 101:
					self.AppendTextLine("+10% Tarie impotriva semi-oamenilor", self.SPECIAL_POSITIVE_COLOR)
				if metinSlot[1] >= 119:
					self.AppendTextLine("+10% Rezistenta la Abilitati", self.SPECIAL_POSITIVE_COLOR)
				if metinSlot[1] < 50:
					self.AppendTextLine("|cFF0df2f2Insotitorul nu are bonusuri extra", self.SPECIAL_POSITIVE_COLOR)
				if itemVnum != 55002:
					days = (int(attrSlot[3][1])/60)/24
					hours = (int(attrSlot[3][1]) - (days*60*24)) / 60
					mins = int(attrSlot[3][1]) - (days*60*24) - (hours*60)
					self.AppendTextLine("Durata: %d Zile %d Ore %d Minute" % (days, hours, mins), self.NORMAL_COLOR)		
		
		if self.sigilii_buffi(itemVnum):
			if attrSlot[0][1] != 0:
				self.AppendSpace(5)
				self.__AppendPetIcon(itemVnum)
				self.AppendSpace(5)
				self.AppendTextLine("LV: "+str(str(attrSlot[0][1])), self.SPECIAL_TITLE_COLOR)
				self.AppendTextLine("INT: "+str(attrSlot[1][1])+"  BONUS "+str(attrSlot[2][1])+" ", self.NORMAL_COLOR)
				self.AppendTextLine("EXP: "+str(str(metinSlot[0])), self.NORMAL_COLOR)
				self.AppendSpace(5)
				if attrSlot[3][1] != 0:
					days = (int(attrSlot[3][1])/60)/24
					hours = (int(attrSlot[3][1]) - (days*60*24)) / 60
					mins = int(attrSlot[3][1]) - (days*60*24) - (hours*60)
					self.AppendTextLine("Timp ramas: %d Zile %d Ore %d Minute" % (days, hours, mins), self.NORMAL_COLOR)
				else:
					self.AppendTextLine("Expirat.", self.DISABLE_COLOR)
					
				if metinSlot[1] != 0:
					item.SelectItem(metinSlot[1])
					itemName = item.GetItemName()
					self.AppendTextLine("Costum echipat:", self.SPECIAL_POSITIVE_COLOR)
					self.AppendTextLine(itemName, self.SPECIAL_POSITIVE_COLOR)
				elif metinSlot[1] == 0:
					self.AppendTextLine("Fara costum.", self.DISABLE_COLOR)
		
		if self.pet_system(itemVnum):
			self.AppendSpace(5)
			# self.__AppendPetIcon(itemVnum)
			for g in xrange(item.ITEM_APPLY_MAX_NUM):
				(affectType, affectValue) = item.GetAffect(g)
				affectString = self.__GetAffectString(affectType, affectValue)
				if affectString:
					# affectColor = 0xffADFF2F
					affectColor = self.GetChangeTextLineColor(affectValue)
					self.AppendTextLine(affectString, affectColor)
			self.__AppendAttributeInformation(attrSlot)
			bHasRealtimeFlag = 0
			for i in xrange(item.LIMIT_MAX_NUM):
				(limitType, limitValue) = item.GetLimit(i)
				if item.LIMIT_REAL_TIME == limitType:
					bHasRealtimeFlag = 1
			if bHasRealtimeFlag == 1:
				self.AppendMallItemLastTime(metinSlot[0])				
		
		if self.title_system(itemVnum):
			self.AppendSpace(5)
			for g in xrange(item.ITEM_APPLY_MAX_NUM):
				(affectType, affectValue) = item.GetAffect(g)
				affectString = self.__GetAffectString(affectType, affectValue)
				if affectString:
					affectColor = 0xffE6E6FA #VLAD EDIT
					self.AppendTextLine(affectString, affectColor)
			self.__AppendAttributeInformation(attrSlot)
			bHasRealtimeFlag = 0
			for i in xrange(item.LIMIT_MAX_NUM):
				(limitType, limitValue) = item.GetLimit(i)
				if item.LIMIT_REAL_TIME == limitType:
					bHasRealtimeFlag = 1
			if bHasRealtimeFlag == 1:
				self.AppendMallItemLastTime(metinSlot[0])				
				
#Descriere_iteme
		if itemVnum in (71051, 71052, 91021, 91022, 91023, 91024, 91025, 91026, 91027, 91028, 91029):
			Suflete = int(metinSlot[0])
			item.SelectItem(metinSlot[1])
			itemName = item.GetItemName()
			serenity_list = {
				71051 : ["Obiect necesar pentru rafinarea Sufletelor", self.SPECIAL_POSITIVE_COLOR],
				71052 : ["Obiect necesar pentru rafinarea Sufletelor", self.SPECIAL_POSITIVE_COLOR],
				91021 : ["Aceasta carte ofera samanului tau un bonus de inteligenta", "+ 35 puncte int", self.SPECIAL_POSITIVE_COLOR],
				91022 : ["Aceasta carte ofera samanului tau un bonus de inteligenta", "+ 70 puncte int", self.SPECIAL_POSITIVE_COLOR],
				91023 : ["Aceasta carte ofera samanului tau un bonus de inteligenta", "+ 100 puncte int", self.SPECIAL_POSITIVE_COLOR],
				91024 : ["Acest pergament sterge bonusul int pe care il detine samanul tau", "Bonusul INT dispare", self.SPECIAL_POSITIVE_COLOR],
				91025 : ["Acest sigiliu confera samanului tau o durabilitate extra", "Durabilitate: + 1 zi", "Itemul dispare dupa utilizare!", self.SPECIAL_POSITIVE_COLOR],
				91026 : ["Acest sigiliu confera samanului tau o durabilitate extra", "Durabilitate: + 2 zile", "Itemul dispare dupa utilizare!", self.SPECIAL_POSITIVE_COLOR],
				91027 : ["Acest sigiliu confera samanului tau o durabilitate extra", "Durabilitate: + 7 zile", "Itemul dispare dupa utilizare!", self.SPECIAL_POSITIVE_COLOR],
				91028 : ["Acest sigiliu confera samanului tau o durabilitate extra", "Durabilitate: + 14 zile", "Itemul dispare dupa utilizare!", self.SPECIAL_POSITIVE_COLOR],
				91029 : ["Acest sigiliu sterge costum si frizura echipate de shamanul tau", "Costumul si freza dispar", "Itemul dispare dupa utilizare!", self.SPECIAL_POSITIVE_COLOR],
				}				
				
			self.AppendSpace(5)	
			for i in xrange(len(serenity_list[itemVnum])):
				self.AppendTextLine(serenity_list[itemVnum][i], self.SPECIAL_POSITIVE_COLOR)					
#end
		if app.ENABLE_FEATURES_REFINE_SYSTEM:
			if itemVnum in (player.REFINE_VNUM_POTION_LOW, player.REFINE_VNUM_POTION_MEDIUM, player.REFINE_VNUM_POTION_EXTRA):

				self.DESCRIPTION_VNUMS = [
					localeInfo.REFINE_TOOLTIP_ITEM_DESCRIPTION_1,
					localeInfo.REFINE_TOOLTIP_ITEM_DESCRIPTION_2,
					localeInfo.REFINE_TOOLTIP_ITEM_DESCRIPTION_3,
					localeInfo.REFINE_TOOLTIP_ITEM_DESCRIPTION_4
				]
				
				self.PERCENTAGE_VNUMS = {
					player.REFINE_VNUM_POTION_LOW : player.REFINE_PERCENTAGE_LOW,
					player.REFINE_VNUM_POTION_MEDIUM : player.REFINE_PERCENTAGE_MEDIUM,
					player.REFINE_VNUM_POTION_EXTRA : player.REFINE_PERCENTAGE_EXTRA
				}
				
				self.COLORS = [
					self.NORMAL_COLOR, self.SPECIAL_POSITIVE_COLOR, self.DISABLE_COLOR, self.HIGH_PRICE_COLOR
				]
					
				self.AppendSpace(5)

				for it in xrange(len(self.DESCRIPTION_VNUMS) - 1):
					self.AppendDescription(self.DESCRIPTION_VNUMS[it], None, self.COLORS[it])
				self.AppendDescription(self.DESCRIPTION_VNUMS[3] % (self.PERCENTAGE_VNUMS[itemVnum]), None, self.COLORS[3])				
				
		### Weapon ###
		if item.ITEM_TYPE_WEAPON == itemType:

			self.__AppendLimitInformation()

			self.AppendSpace(5)

			## 부채일 경우 마공을 먼저 표시한다.
			if item.WEAPON_FAN == itemSubType:
				self.__AppendMagicAttackInfo()
				self.__AppendAttackPowerInfo()

			else:
				self.__AppendAttackPowerInfo()
				self.__AppendMagicAttackInfo()

			self.__AppendAffectInformation()
			self.__AppendAttributeInformation(attrSlot)
			
			if app.ENABLE_CHANGELOOK_SYSTEM:
				self.AppendTransmutation(window_type, slotIndex, transmutation)

			
			self.AppendWearableInformation()
			self.__AppendMetinSlotInfo(metinSlot)

		### Armor ###
		elif item.ITEM_TYPE_ARMOR == itemType:
			self.__AppendLimitInformation()

			## 방어력
			defGrade = item.GetValue(1)
			defBonus = item.GetValue(5)*2 ## 방어력 표시 잘못 되는 문제를 수정
			if defGrade > 0:
				self.AppendSpace(5)
				self.AppendTextLine(localeInfo.TOOLTIP_ITEM_DEF_GRADE % (defGrade+defBonus), self.GetChangeTextLineColor(defGrade))

			self.__AppendMagicDefenceInfo()
			self.__AppendAffectInformation()
			self.__AppendAttributeInformation(attrSlot)

			if app.ENABLE_CHANGELOOK_SYSTEM:
				self.AppendTransmutation(window_type, slotIndex, transmutation)

			
			self.AppendWearableInformation()

			if itemSubType in (item.ARMOR_WRIST, item.ARMOR_NECK, item.ARMOR_EAR):
				self.__AppendAccessoryMetinSlotInfo(metinSlot, constInfo.GET_ACCESSORY_MATERIAL_VNUM(itemVnum, itemSubType))
			else:
				self.__AppendMetinSlotInfo(metinSlot)

		### Soul and Pendant slot ###
		elif item.ITEM_TYPE_RING == itemType:
			self.AppendSpace(5)
			self.__AppendLimitInformation()
			self.__AppendAffectInformation()
			self.__AppendAttributeInformation(attrSlot)
			self.AppendSpace(5)
			self.AppendWearableInformation()
			
		### Belt Item ###
		elif item.ITEM_TYPE_BELT == itemType:
			self.__AppendLimitInformation()
			self.__AppendAffectInformation()
			self.__AppendAttributeInformation(attrSlot)

			self.__AppendAccessoryMetinSlotInfo(metinSlot, constInfo.GET_BELT_MATERIAL_VNUM(itemVnum))

		## 코스츔 아이템 ##
		elif 0 != isCostumeItem:
			self.__AppendLimitInformation()
			
			if app.ENABLE_SASH_SYSTEM:
				if isCostumeSash:
					## ABSORPTION RATE
					absChance = int(metinSlot[sash.ABSORPTION_SOCKET])
					self.AppendTextLine(localeInfo.SASH_ABSORB_CHANCE % (absChance), self.CONDITION_COLOR)
					## END ABSOPRTION RATE
					
					itemAbsorbedVnum = int(metinSlot[sash.ABSORBED_SOCKET])
					if itemAbsorbedVnum:
						## ATTACK / DEFENCE
						item.SelectItem(itemAbsorbedVnum)
						if item.GetItemType() == item.ITEM_TYPE_WEAPON:
							if item.GetItemSubType() == item.WEAPON_FAN:
								self.__AppendMagicAttackInfo(metinSlot[sash.ABSORPTION_SOCKET])
								item.SelectItem(itemAbsorbedVnum)
								self.__AppendAttackPowerInfo(metinSlot[sash.ABSORPTION_SOCKET])
							else:
								self.__AppendAttackPowerInfo(metinSlot[sash.ABSORPTION_SOCKET])
								item.SelectItem(itemAbsorbedVnum)
								self.__AppendMagicAttackInfo(metinSlot[sash.ABSORPTION_SOCKET])
						elif item.GetItemType() == item.ITEM_TYPE_ARMOR:
							defGrade = item.GetValue(1)
							defBonus = item.GetValue(5) * 2
							defGrade = self.CalcSashValue(defGrade, metinSlot[sash.ABSORPTION_SOCKET])
							defBonus = self.CalcSashValue(defBonus, metinSlot[sash.ABSORPTION_SOCKET])
							
							if defGrade > 0:
								self.AppendSpace(5)
								self.AppendTextLine(localeInfo.TOOLTIP_ITEM_DEF_GRADE % (defGrade + defBonus), self.GetChangeTextLineColor(defGrade))
							
							item.SelectItem(itemAbsorbedVnum)
							self.__AppendMagicDefenceInfo(metinSlot[sash.ABSORPTION_SOCKET])
						## END ATTACK / DEFENCE
						
						## EFFECT
						item.SelectItem(itemAbsorbedVnum)
						for i in xrange(item.ITEM_APPLY_MAX_NUM):
							(affectType, affectValue) = item.GetAffect(i)
							affectValue = self.CalcSashValue(affectValue, metinSlot[sash.ABSORPTION_SOCKET])
							affectString = self.__GetAffectString(affectType, affectValue)
							if affectString and affectValue > 0:
								self.AppendTextLine(affectString, self.GetChangeTextLineColor(affectValue))
							
							item.SelectItem(itemAbsorbedVnum)
						# END EFFECT
						
						item.SelectItem(itemVnum)
						## ATTR
						self.__AppendAttributeInformation(attrSlot, metinSlot[sash.ABSORPTION_SOCKET])
						# END ATTR
					else:
						# ATTR
						self.__AppendAttributeInformation(attrSlot)
						# END ATTR
				else:
					self.__AppendAffectInformation()
					self.__AppendAttributeInformation(attrSlot)
			else:
				self.__AppendAffectInformation()
				self.__AppendAttributeInformation(attrSlot)
			
			if app.ENABLE_CHANGELOOK_SYSTEM:
				self.AppendTransmutation(window_type, slotIndex, transmutation)

			self.AppendWearableInformation()

			bHasRealtimeFlag = 0
			for i in xrange(item.LIMIT_MAX_NUM):
				(limitType, limitValue) = item.GetLimit(i)
				if item.LIMIT_REAL_TIME == limitType:
					bHasRealtimeFlag = 1
			
			if cofres == 0:
				if 1 == bHasRealtimeFlag:
					self.AppendMallItemLastTime(metinSlot[0])
				#dbg.TraceError("1) REAL_TIME flag On ")

		## Rod ##
		elif item.ITEM_TYPE_ROD == itemType:

			if 0 != metinSlot:
				curLevel = item.GetValue(0) / 10
				curEXP = metinSlot[0]
				maxEXP = item.GetValue(2)
				self.__AppendLimitInformation()
				self.__AppendRodInformation(curLevel, curEXP, maxEXP)

		## Pick ##
		elif item.ITEM_TYPE_PICK == itemType:

			if 0 != metinSlot:
				curLevel = item.GetValue(0) / 10
				curEXP = metinSlot[0]
				maxEXP = item.GetValue(2)
				self.__AppendLimitInformation()
				self.__AppendPickInformation(curLevel, curEXP, maxEXP)

		## Lottery ##
		elif item.ITEM_TYPE_LOTTERY == itemType:
			if 0 != metinSlot:

				ticketNumber = int(metinSlot[0])
				stepNumber = int(metinSlot[1])

				self.AppendSpace(5)
				self.AppendTextLine(localeInfo.TOOLTIP_LOTTERY_STEP_NUMBER % (stepNumber), self.NORMAL_COLOR)
				self.AppendTextLine(localeInfo.TOOLTIP_LOTTO_NUMBER % (ticketNumber), self.NORMAL_COLOR);

		### Metin ###
		elif item.ITEM_TYPE_METIN == itemType:
			self.AppendMetinInformation()
			self.AppendMetinWearInformation()

		### Fish ###
		elif item.ITEM_TYPE_FISH == itemType:
			if 0 != metinSlot:
				self.__AppendFishInfo(metinSlot[0])
				
		elif app.ENABLE_BATTLE_FIELD and item.ITEM_TYPE_GACHA == itemType:
			if 0 != metinSlot:
				if self.isShopItem:
					restUsableCount = int(item.GetLimit(1)[1])
				else:
					restUsableCount = int(metinSlot[0])

				self.AppendSpace(5)
				self.AppendTextLine(localeInfo.TOOLTIP_REST_USABLE_COUNT % (restUsableCount), grp.GenerateColor(0.5, 1.0, 0.3, 1.0))
				
		## item.ITEM_TYPE_BLEND
		elif item.ITEM_TYPE_BLEND == itemType:
			self.__AppendLimitInformation()

			if metinSlot:
				affectType = metinSlot[0]
				affectValue = metinSlot[1]
				time = metinSlot[2]
				self.AppendSpace(5)
				affectText = self.__GetAffectString(affectType, affectValue)

				self.AppendTextLine(affectText, self.NORMAL_COLOR)

				if time > 0:
					minute = (time / 60)
					second = (time % 60)
					timeString = localeInfo.TOOLTIP_POTION_TIME

					if minute > 0:
						timeString += str(minute) + localeInfo.TOOLTIP_POTION_MIN
					if second > 0:
						timeString += " " + str(second) + localeInfo.TOOLTIP_POTION_SEC

					self.AppendTextLine(timeString)
				else:
					self.AppendTextLine(localeInfo.BLEND_POTION_NO_TIME)
			else:
				self.AppendTextLine("BLEND_POTION_NO_INFO")

		elif item.ITEM_TYPE_UNIQUE == itemType:
			if 0 != metinSlot:
				bHasRealtimeFlag = 0

				for i in xrange(item.LIMIT_MAX_NUM):
					(limitType, limitValue) = item.GetLimit(i)

					if item.LIMIT_REAL_TIME == limitType:
						bHasRealtimeFlag = 1

				if 1 == bHasRealtimeFlag:
					self.AppendMallItemLastTime(metinSlot[0])
				else:
					time = metinSlot[player.METIN_SOCKET_MAX_NUM-1]

					if 1 == item.GetValue(2): ## 실시간 이용 Flag / 장착 안해도 준다
						self.AppendMallItemLastTime(time)
					else:
						self.AppendUniqueItemLastTime(time)

		### Use ###
		elif item.ITEM_TYPE_USE == itemType:
			self.__AppendLimitInformation()

			if item.USE_POTION == itemSubType or item.USE_POTION_NODELAY == itemSubType:
				self.__AppendPotionInformation()

			elif item.USE_ABILITY_UP == itemSubType:
				self.__AppendAbilityPotionInformation()


			## 영석 감지기
			if 27989 == itemVnum or 76006 == itemVnum:
				if 0 != metinSlot:
					useCount = int(metinSlot[0])

					self.AppendSpace(5)
					self.AppendTextLine(localeInfo.TOOLTIP_REST_USABLE_COUNT % (6 - useCount), self.NORMAL_COLOR)

			## 이벤트 감지기
			elif 50004 == itemVnum:
				if 0 != metinSlot:
					useCount = int(metinSlot[0])

					self.AppendSpace(5)
					self.AppendTextLine(localeInfo.TOOLTIP_REST_USABLE_COUNT % (10 - useCount), self.NORMAL_COLOR)
					
			## suflet1
			elif 71051 == itemVnum:
				if 0 != metinSlot:
					useCount = int(metinSlot[0])

					self.AppendSpace(5)
					self.AppendTextLine("Suflete: "+str(metinSlot[0]), self.NORMAL_COLOR)
			## suflet2
			elif 71052 == itemVnum:
				if 0 != metinSlot:
					useCount = int(metinSlot[0])

					self.AppendSpace(5)
					self.AppendTextLine("Suflete: "+str(metinSlot[0]), self.NORMAL_COLOR)

			## 자동물약
			elif constInfo.IS_AUTO_POTION(itemVnum):
				if 0 != metinSlot:
					## 0: 활성화, 1: 사용량, 2: 총량
					isActivated = int(metinSlot[0])
					usedAmount = float(metinSlot[1])
					totalAmount = float(metinSlot[2])

					if 0 == totalAmount:
						totalAmount = 1

					self.AppendSpace(5)

					if 0 != isActivated:
						self.AppendTextLine("(%s)" % (localeInfo.TOOLTIP_AUTO_POTION_USING), self.SPECIAL_POSITIVE_COLOR)
						self.AppendSpace(5)

					self.AppendTextLine(localeInfo.TOOLTIP_AUTO_POTION_REST % (100.0 - ((usedAmount / totalAmount) * 100.0)), self.POSITIVE_COLOR)

			## 귀환 기억부
			elif itemVnum in WARP_SCROLLS:
				if 0 != metinSlot:
					xPos = int(metinSlot[0])
					yPos = int(metinSlot[1])

					if xPos != 0 and yPos != 0:
						(mapName, xBase, yBase) = background.GlobalPositionToMapInfo(xPos, yPos)

						localeMapName=localeInfo.MINIMAP_ZONE_NAME_DICT.get(mapName, "")

						self.AppendSpace(5)

						if localeMapName!="":
							self.AppendTextLine(localeInfo.TOOLTIP_MEMORIZED_POSITION % (localeMapName, int(xPos-xBase)/100, int(yPos-yBase)/100), self.NORMAL_COLOR)
						else:
							self.AppendTextLine(localeInfo.TOOLTIP_MEMORIZED_POSITION_ERROR % (int(xPos)/100, int(yPos)/100), self.NORMAL_COLOR)
							dbg.TraceError("NOT_EXIST_IN_MINIMAP_ZONE_NAME_DICT: %s" % mapName)

			#####
			if item.USE_SPECIAL == itemSubType:
				bHasRealtimeFlag = 0
				for i in xrange(item.LIMIT_MAX_NUM):
					(limitType, limitValue) = item.GetLimit(i)

					if item.LIMIT_REAL_TIME == limitType:
						bHasRealtimeFlag = 1

				## 있다면 관련 정보를 표시함. ex) 남은 시간 : 6일 6시간 58분
				if 1 == bHasRealtimeFlag:
					self.AppendMallItemLastTime(metinSlot[0])
				else:
					# ... 이거... 서버에는 이런 시간 체크 안되어 있는데...
					# 왜 이런게 있는지 알지는 못하나 그냥 두자...
					if 0 != metinSlot:
						time = metinSlot[player.METIN_SOCKET_MAX_NUM-1]

						## 실시간 이용 Flag
						if 1 == item.GetValue(2):
							self.AppendMallItemLastTime(time)

			elif item.USE_TIME_CHARGE_PER == itemSubType:
				bHasRealtimeFlag = 0
				for i in xrange(item.LIMIT_MAX_NUM):
					(limitType, limitValue) = item.GetLimit(i)

					if item.LIMIT_REAL_TIME == limitType:
						bHasRealtimeFlag = 1
				if metinSlot[2]:
					self.AppendTextLine(localeInfo.TOOLTIP_TIME_CHARGER_PER(metinSlot[2]))
				else:
					self.AppendTextLine(localeInfo.TOOLTIP_TIME_CHARGER_PER(item.GetValue(0)))

				## 있다면 관련 정보를 표시함. ex) 남은 시간 : 6일 6시간 58분
				if 1 == bHasRealtimeFlag:
					self.AppendMallItemLastTime(metinSlot[0])

			elif item.USE_TIME_CHARGE_FIX == itemSubType:
				bHasRealtimeFlag = 0
				for i in xrange(item.LIMIT_MAX_NUM):
					(limitType, limitValue) = item.GetLimit(i)

					if item.LIMIT_REAL_TIME == limitType:
						bHasRealtimeFlag = 1
				if metinSlot[2]:
					self.AppendTextLine(localeInfo.TOOLTIP_TIME_CHARGER_FIX(metinSlot[2]))
				else:
					self.AppendTextLine(localeInfo.TOOLTIP_TIME_CHARGER_FIX(item.GetValue(0)))

				## 있다면 관련 정보를 표시함. ex) 남은 시간 : 6일 6시간 58분
				if 1 == bHasRealtimeFlag:
					self.AppendMallItemLastTime(metinSlot[0])

		elif item.ITEM_TYPE_QUEST == itemType:
			if app.ENABLE_ATTENDANCE_EVENT:
				if itemVnum == 71150:
					self.AppendMagicEggInformation(metinSlot)
					
			if itemVnum >= 53001 and itemVnum <= 53099:
				self.AppendSpace(5)
				self.__AppendPetIcon(itemVnum)
				for g in xrange(item.ITEM_APPLY_MAX_NUM):
					(affectType, affectValue) = item.GetAffect(g)
					affectString = self.__GetAffectString(affectType, affectValue)
					if affectString:
						affectColor = 0xffB8B10D
						self.AppendTextLine(affectString, affectColor)
				self.__AppendAttributeInformation(attrSlot)
				bHasRealtimeFlag = 0
				for i in xrange(item.LIMIT_MAX_NUM):
					(limitType, limitValue) = item.GetLimit(i)
					if item.LIMIT_REAL_TIME == limitType:
						bHasRealtimeFlag = 1
				if bHasRealtimeFlag == 1:
					self.AppendMallItemLastTime(metinSlot[0])

		elif item.ITEM_TYPE_DS == itemType:
			self.AppendTextLine(self.__DragonSoulInfoString(itemVnum))
			self.__AppendAttributeInformation(attrSlot)
			
		elif 71051 == itemVnum:
			if 0 != metinSlot:
				useCount = int(metinSlot[0])

				self.AppendSpace(5)
				self.AppendTextLine("Acest cufar contine suflete: "+str(metinSlot[0]), self.NORMAL_COLOR)

		elif 71052 == itemVnum:
			if 0 != metinSlot:
				useCount = int(metinSlot[0])

				self.AppendSpace(5)
				self.AppendTextLine("Acest cufar contine suflete: "+str(metinSlot[0]), self.NORMAL_COLOR)

		else:
			self.__AppendLimitInformation()

		for i in xrange(item.LIMIT_MAX_NUM):
			(limitType, limitValue) = item.GetLimit(i)
			#dbg.TraceError("LimitType : %d, limitValue : %d" % (limitType, limitValue))

			if cofres == 0:
				if item.LIMIT_REAL_TIME_START_FIRST_USE == limitType:
					self.AppendRealTimeStartFirstUseLastTime(item, metinSlot, i)
				elif item.LIMIT_TIMER_BASED_ON_WEAR == limitType:
					self.AppendTimerBasedOnWearLastTime(metinSlot)
				#dbg.TraceError("2) REAL_TIME_START_FIRST_USE flag On ")

			elif item.LIMIT_TIMER_BASED_ON_WEAR == limitType:
				self.AppendTimerBasedOnWearLastTime(metinSlot)
				#dbg.TraceError("1) REAL_TIME flag On ")

		self.__AppendSealInformation(window_type, slotIndex) ## cyh itemseal 2013 11 11

		if chr.IsGameMaster(player.GetMainCharacterIndex()):
			self.AppendTextLine(localeInfo.ITEM_VNUM_TOOLTIP % (int(itemVnum)), self.ITEM_ID_COLOR)

		self.ShowToolTip()

	def __DragonSoulInfoString (self, dwVnum):
		step = (dwVnum / 100) % 10
		refine = (dwVnum / 10) % 10
		if 0 == step:
			return localeInfo.DRAGON_SOUL_STEP_LEVEL1 + " " + localeInfo.DRAGON_SOUL_STRENGTH(refine)
		elif 1 == step:
			return localeInfo.DRAGON_SOUL_STEP_LEVEL2 + " " + localeInfo.DRAGON_SOUL_STRENGTH(refine)
		elif 2 == step:
			return localeInfo.DRAGON_SOUL_STEP_LEVEL3 + " " + localeInfo.DRAGON_SOUL_STRENGTH(refine)
		elif 3 == step:
			return localeInfo.DRAGON_SOUL_STEP_LEVEL4 + " " + localeInfo.DRAGON_SOUL_STRENGTH(refine)
		elif 4 == step:
			return localeInfo.DRAGON_SOUL_STEP_LEVEL5 + " " + localeInfo.DRAGON_SOUL_STRENGTH(refine)
		else:
			return ""

	if app.__MULTI_SHOP__:
		def AppendPriceTextLine(self, price, priceVnum):
			item.SelectItem(priceVnum)
			windowBack = ui.Window()
			windowBack.SetParent(self)

			textLine = ui.TextLine()
			textLine.SetParent(windowBack)
			textLine.SetFontName(self.defFontName)
			textLine.SetPackedFontColor(self.FONT_COLOR)
			textLine.SetText("%sx" % (localeInfo.TOOLTIP_BUYPRICE % int(price)))
			textLine.SetOutline()
			textLine.SetFeather(False)
			textLine.SetPosition(0, 10)
			textLine.Show()

			itemImage = ui.ImageBox()
			itemImage.SetParent(windowBack)
			itemImage.LoadImage(item.GetIconImageFileName())
			itemImage.SetPosition(textLine.GetTextSize()[0] + 2, 0)
			itemImage.Show()

			textLineName = ui.TextLine()
			textLineName.SetParent(windowBack)
			textLineName.SetFontName(self.defFontName)
			textLineName.SetPackedFontColor(self.FONT_COLOR)
			textLineName.SetText("%s" % item.GetItemName())
			textLineName.SetOutline()
			textLineName.SetFeather(False)
			textLineName.SetPosition(textLine.GetTextSize()[0] + itemImage.GetWidth() + 4, 10)
			textLineName.Show()

			windowBack.SetPosition(0, self.toolTipHeight)
			windowBack.SetSize(textLine.GetTextSize()[0] + itemImage.GetWidth() + textLineName.GetTextSize()[0] + 6, 32)
			windowBack.SetWindowHorizontalAlignCenter()
			windowBack.Show()

			self.toolTipHeight += itemImage.GetHeight()

			self.childrenList.append(textLine)
			self.childrenList.append(textLineName)
			self.childrenList.append(itemImage)
			self.childrenList.append(windowBack)
			self.ResizeToolTip()

	if app.ENABLE_ATTENDANCE_EVENT:
		def AppendMagicEggInformation(self, metinSlot):				
			self.AppendSpace(5)
			if metinSlot[1] == 0:
				self.AppendTextLine("[ 3 Deschideri ramase ]", self.NORMAL_COLOR)
			else:
				self.AppendTextLine("[ %d Deschideri ramase ]" % metinSlot[0], self.NORMAL_COLOR)
				
				if app.GetGlobalTimeStamp() > metinSlot[1]:
					self.AppendSpace(5)
					self.AppendTextLine("O noua deschidere posibila", self.NORMAL_COLOR)
				else:
					leftSec = max(0, metinSlot[1] - app.GetGlobalTimeStamp())
					self.AppendSpace(5)
					self.AppendTextLine(localeInfo.LEFT_TIME + " : " + localeInfo.SecondToDHM(leftSec), self.NORMAL_COLOR)				

	## 헤어인가?
	def __IsHair(self, itemVnum):
		return (self.__IsOldHair(itemVnum) or
			self.__IsNewHair(itemVnum) or
			self.__IsNewHair2(itemVnum) or
			self.__IsNewHair3(itemVnum) or
			self.__IsCostumeHair(itemVnum)
			)

	def __IsOldHair(self, itemVnum):
		return itemVnum > 73000 and itemVnum < 74000

	def __IsNewHair(self, itemVnum):
		return itemVnum > 74000 and itemVnum < 75000

	def __IsNewHair2(self, itemVnum):
		return itemVnum > 75000 and itemVnum < 76000

	def __IsNewHair3(self, itemVnum):
		return ((74012 < itemVnum and itemVnum < 74022) or
			(74262 < itemVnum and itemVnum < 74272) or
			(74512 < itemVnum and itemVnum < 74522) or
			(74762 < itemVnum and itemVnum < 74772) or
			(45000 < itemVnum and itemVnum < 47000))

	def __IsCostumeHair(self, itemVnum):
		return app.ENABLE_COSTUME_SYSTEM and self.__IsNewHair3(itemVnum - 100000)

	if app.ENABLE_ATTENDANCE_EVENT:
		def __AppendAttendanceRewardItemIcon(self, itemVnum):
			itemImage = ui.ImageBox()
			itemImage.SetParent(self)
			itemImage.Show()
			item.SelectItem(itemVnum)
			itemImage.LoadImage(item.GetIconImageFileName())
			itemImage.SetPosition((self.toolTipWidth/2)-16, self.toolTipHeight)
			self.toolTipHeight += itemImage.GetHeight()
			self.childrenList.append(itemImage)
			self.ResizeToolTip()		
		
	def __AppendPetIcon(self, itemVnum):
		itemImage = ui.ImageBox()
		itemImage.SetParent(self)
		itemImage.Show()
		
		# itemImage.LoadImage(item.GetIconImageFileName())
		itemImage.LoadImage("icon/pet/%d.sub" % (itemVnum))
		itemImage.SetPosition((self.toolTipWidth/2) - itemImage.GetWidth()/2, self.toolTipHeight)
		self.toolTipHeight += itemImage.GetHeight()
		self.childrenList.append(itemImage)
		self.ResizeToolTip()		
		
	def __AppendHairIcon(self, itemVnum):
		itemImage = ui.ImageBox()
		itemImage.SetParent(self)
		itemImage.Show()

		if self.__IsOldHair(itemVnum):
			itemImage.LoadImage("d:/ymir work/item/quest/"+str(itemVnum)+".tga")
		elif self.__IsNewHair3(itemVnum):
			itemImage.LoadImage("icon/hair/%d.sub" % (itemVnum))
		elif self.__IsNewHair(itemVnum): # 기존 헤어 번호를 연결시켜서 사용한다. 새로운 아이템은 1000만큼 번호가 늘었다.
			itemImage.LoadImage("d:/ymir work/item/quest/"+str(itemVnum-1000)+".tga")
		elif self.__IsNewHair2(itemVnum):
			itemImage.LoadImage("icon/hair/%d.sub" % (itemVnum))
		elif self.__IsCostumeHair(itemVnum):
			itemImage.LoadImage("icon/hair/%d.sub" % (itemVnum - 100000))

		itemImage.SetPosition(itemImage.GetWidth()/2, self.toolTipHeight)
		self.toolTipHeight += itemImage.GetHeight()
		#self.toolTipWidth += itemImage.GetWidth()/2
		self.childrenList.append(itemImage)
		self.ResizeToolTip()

	## 사이즈가 큰 Description 일 경우 툴팁 사이즈를 조정한다
	def __AdjustMaxWidth(self, attrSlot, desc):
		newToolTipWidth = self.toolTipWidth
		newToolTipWidth = max(self.__AdjustAttrMaxWidth(attrSlot), newToolTipWidth)
		newToolTipWidth = max(self.__AdjustDescMaxWidth(desc), newToolTipWidth)
		if newToolTipWidth > self.toolTipWidth:
			self.toolTipWidth = newToolTipWidth
			self.ResizeToolTip()

	def __AdjustAttrMaxWidth(self, attrSlot):
		if 0 == attrSlot:
			return self.toolTipWidth

		maxWidth = self.toolTipWidth
		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			type = attrSlot[i][0]
			value = attrSlot[i][1]
			if self.ATTRIBUTE_NEED_WIDTH.has_key(type):
				if value > 0:
					maxWidth = max(self.ATTRIBUTE_NEED_WIDTH[type], maxWidth)

					# ATTR_CHANGE_TOOLTIP_WIDTH
					#self.toolTipWidth = max(self.ATTRIBUTE_NEED_WIDTH[type], self.toolTipWidth)
					#self.ResizeToolTip()
					# END_OF_ATTR_CHANGE_TOOLTIP_WIDTH

		return maxWidth

	def __AdjustDescMaxWidth(self, desc):
		if len(desc) < DESC_DEFAULT_MAX_COLS:
			return self.toolTipWidth

		return DESC_WESTERN_MAX_WIDTH

	def __SetSkillBookToolTip(self, skillIndex, bookName, skillGrade):
		skillName = skill.GetSkillName(skillIndex)

		if not skillName:
			return

		if localeInfo.IsVIETNAM():
			itemName = bookName + " " + skillName
		else:
			itemName = skillName + " " + bookName
		self.SetTitle(itemName)

	def __AppendPickInformation(self, curLevel, curEXP, maxEXP):
		self.AppendSpace(5)
		self.AppendTextLine(localeInfo.TOOLTIP_PICK_LEVEL % (curLevel), self.NORMAL_COLOR)
		self.AppendTextLine(localeInfo.TOOLTIP_PICK_EXP % (curEXP, maxEXP), self.NORMAL_COLOR)

		if curEXP == maxEXP:
			self.AppendSpace(5)
			self.AppendTextLine(localeInfo.TOOLTIP_PICK_UPGRADE1, self.NORMAL_COLOR)
			self.AppendTextLine(localeInfo.TOOLTIP_PICK_UPGRADE2, self.NORMAL_COLOR)
			self.AppendTextLine(localeInfo.TOOLTIP_PICK_UPGRADE3, self.NORMAL_COLOR)


	def __AppendRodInformation(self, curLevel, curEXP, maxEXP):
		self.AppendSpace(5)
		self.AppendTextLine(localeInfo.TOOLTIP_FISHINGROD_LEVEL % (curLevel), self.NORMAL_COLOR)
		self.AppendTextLine(localeInfo.TOOLTIP_FISHINGROD_EXP % (curEXP, maxEXP), self.NORMAL_COLOR)

		if curEXP == maxEXP:
			self.AppendSpace(5)
			self.AppendTextLine(localeInfo.TOOLTIP_FISHINGROD_UPGRADE1, self.NORMAL_COLOR)
			self.AppendTextLine(localeInfo.TOOLTIP_FISHINGROD_UPGRADE2, self.NORMAL_COLOR)
			self.AppendTextLine(localeInfo.TOOLTIP_FISHINGROD_UPGRADE3, self.NORMAL_COLOR)

	def __AppendSoulInformation(self, curLevel, curEXP, maxEXP):
		self.AppendSpace(5)
		self.AppendTextLine(localeInfo.TOOLTIP_SOULITEM_LEVEL % (curLevel), self.NORMAL_COLOR)
		self.AppendTextLine(localeInfo.TOOLTIP_SOULITEM_EXP % (curEXP, maxEXP), self.NORMAL_COLOR)

		if curEXP == maxEXP:
			self.AppendSpace(5)
			self.AppendTextLine(localeInfo.TOOLTIP_SOULITEM_UPGRADE1, self.NORMAL_COLOR)
			self.AppendTextLine(localeInfo.TOOLTIP_SOULITEM_UPGRADE2, self.NORMAL_COLOR)
			self.AppendTextLine(localeInfo.TOOLTIP_SOULITEM_UPGRADE3, self.NORMAL_COLOR)

	def __AppendLimitInformation(self):
		if app.ENABLE_ATTENDANCE_EVENT:
			if self.isAttendanceRewardItem:
				return
				
		appendSpace = False

		for i in xrange(item.LIMIT_MAX_NUM):

			(limitType, limitValue) = item.GetLimit(i)

			if limitValue > 0:
				if False == appendSpace:
					self.AppendSpace(5)
					appendSpace = True

			else:
				continue

			if item.LIMIT_LEVEL == limitType:
				color = self.GetLimitTextLineColor(player.GetStatus(player.LEVEL), limitValue)
				self.AppendTextLine(localeInfo.TOOLTIP_ITEM_LIMIT_LEVEL % (limitValue), color)
			"""
			elif item.LIMIT_STR == limitType:
				color = self.GetLimitTextLineColor(player.GetStatus(player.ST), limitValue)
				self.AppendTextLine(localeInfo.TOOLTIP_ITEM_LIMIT_STR % (limitValue), color)
			elif item.LIMIT_DEX == limitType:
				color = self.GetLimitTextLineColor(player.GetStatus(player.DX), limitValue)
				self.AppendTextLine(localeInfo.TOOLTIP_ITEM_LIMIT_DEX % (limitValue), color)
			elif item.LIMIT_INT == limitType:
				color = self.GetLimitTextLineColor(player.GetStatus(player.IQ), limitValue)
				self.AppendTextLine(localeInfo.TOOLTIP_ITEM_LIMIT_INT % (limitValue), color)
			elif item.LIMIT_CON == limitType:
				color = self.GetLimitTextLineColor(player.GetStatus(player.HT), limitValue)
				self.AppendTextLine(localeInfo.TOOLTIP_ITEM_LIMIT_CON % (limitValue), color)
			"""

	## cyh itemseal 2013 11 11
	def __AppendSealInformation(self, window_type, slotIndex):
		if not app.ENABLE_SEALBIND_SYSTEM:
			return

		itemSealDate = player.GetItemSealDate(window_type, slotIndex)
		if itemSealDate == item.GetDefaultSealDate():
			return

		if itemSealDate == item.GetUnlimitedSealDate():
			self.AppendSpace(5)
			self.AppendTextLine(localeInfo.TOOLTIP_SEALED, self.NEGATIVE_COLOR)

		elif itemSealDate > 0:
			self.AppendSpace(5)
			hours, minutes = player.GetItemUnSealLeftTime(window_type, slotIndex)
			self.AppendTextLine(localeInfo.TOOLTIP_UNSEAL_LEFT_TIME % (hours, minutes), self.NEGATIVE_COLOR)

	def __GetAffectString(self, affectType, affectValue):
		if 0 == affectType:
			return None

		if 0 == affectValue:
			return None

		try:
			return self.AFFECT_DICT[affectType](affectValue)
		except TypeError:
			return "UNKNOWN_VALUE[%s] %s" % (affectType, affectValue)
		except KeyError:
			return "UNKNOWN_TYPE[%s] %s" % (affectType, affectValue)

	def __AppendAffectInformation(self):
		for i in xrange(item.ITEM_APPLY_MAX_NUM):

			(affectType, affectValue) = item.GetAffect(i)

			affectString = self.__GetAffectString(affectType, affectValue)
			if affectString:
				self.AppendTextLine(affectString, self.GetChangeTextLineColor(affectValue))

	def AppendWearableInformation(self):

		self.AppendSpace(5)
		self.AppendTextLine(localeInfo.TOOLTIP_ITEM_WEARABLE_JOB, self.NORMAL_COLOR)

		flagList = (
			not item.IsAntiFlag(item.ITEM_ANTIFLAG_WARRIOR),
			not item.IsAntiFlag(item.ITEM_ANTIFLAG_ASSASSIN),
			not item.IsAntiFlag(item.ITEM_ANTIFLAG_SURA),
			not item.IsAntiFlag(item.ITEM_ANTIFLAG_SHAMAN))
		# if app.ENABLE_WOLFMAN_CHARACTER:
			# flagList += (not item.IsAntiFlag(item.ITEM_ANTIFLAG_WOLFMAN),)
		characterNames = ""
		for i in xrange(self.CHARACTER_COUNT):

			name = self.CHARACTER_NAMES[i]
			flag = flagList[i]

			if flag:
				characterNames += " "
				characterNames += name

		textLine = self.AppendTextLine(characterNames, self.NORMAL_COLOR, True)
		textLine.SetFeather()

		if item.IsAntiFlag(item.ITEM_ANTIFLAG_MALE):
			textLine = self.AppendTextLine(localeInfo.FOR_FEMALE, self.NORMAL_COLOR, True)
			textLine.SetFeather()

		if item.IsAntiFlag(item.ITEM_ANTIFLAG_FEMALE):
			textLine = self.AppendTextLine(localeInfo.FOR_MALE, self.NORMAL_COLOR, True)
			textLine.SetFeather()

	def AppendAntiFlagInformation(self):
		flagList = [
			[item.ITEM_ANTIFLAG_GIVE, "Negociaza"],
			[item.ITEM_ANTIFLAG_DROP, "Arunca"],
			[item.ITEM_ANTIFLAG_SELL, "Vinde"],
			[item.ITEM_ANTIFLAG_MYSHOP, "Magazin"],
			[item.ITEM_ANTIFLAG_SAFEBOX, "Depozit"],
		]

		antiflagNames = ""
		for i in xrange(len(flagList)):
			if item.IsAntiFlag(flagList[i][0]):
				antiflagNames += flagList[i][1]
				antiflagNames += ","

		if antiflagNames != "":
			self.AppendSpace(5)
			self.AppendTextLine("[ Imposibil ]", self.DISABLE_COLOR)
			textLine = self.AppendTextLine(antiflagNames[:-1], self.DISABLE_COLOR, True)
			textLine.SetFeather()
			
	def __AppendPotionInformation(self):
		self.AppendSpace(5)

		healHP = item.GetValue(0)
		healSP = item.GetValue(1)
		healStatus = item.GetValue(2)
		healPercentageHP = item.GetValue(3)
		healPercentageSP = item.GetValue(4)

		if healHP > 0:
			self.AppendTextLine(localeInfo.TOOLTIP_POTION_PLUS_HP_POINT % healHP, self.GetChangeTextLineColor(healHP))
		if healSP > 0:
			self.AppendTextLine(localeInfo.TOOLTIP_POTION_PLUS_SP_POINT % healSP, self.GetChangeTextLineColor(healSP))
		if healStatus != 0:
			self.AppendTextLine(localeInfo.TOOLTIP_POTION_CURE)
		if healPercentageHP > 0:
			self.AppendTextLine(localeInfo.TOOLTIP_POTION_PLUS_HP_PERCENT % healPercentageHP, self.GetChangeTextLineColor(healPercentageHP))
		if healPercentageSP > 0:
			self.AppendTextLine(localeInfo.TOOLTIP_POTION_PLUS_SP_PERCENT % healPercentageSP, self.GetChangeTextLineColor(healPercentageSP))

	def __AppendAbilityPotionInformation(self):

		self.AppendSpace(5)

		abilityType = item.GetValue(0)
		time = item.GetValue(1)
		point = item.GetValue(2)

		if abilityType == item.APPLY_ATT_SPEED:
			self.AppendTextLine(localeInfo.TOOLTIP_POTION_PLUS_ATTACK_SPEED % point, self.GetChangeTextLineColor(point))
		elif abilityType == item.APPLY_MOV_SPEED:
			self.AppendTextLine(localeInfo.TOOLTIP_POTION_PLUS_MOVING_SPEED % point, self.GetChangeTextLineColor(point))

		if time > 0:
			minute = (time / 60)
			second = (time % 60)
			timeString = localeInfo.TOOLTIP_POTION_TIME

			if minute > 0:
				timeString += str(minute) + localeInfo.TOOLTIP_POTION_MIN
			if second > 0:
				timeString += " " + str(second) + localeInfo.TOOLTIP_POTION_SEC

			self.AppendTextLine(timeString)

	def GetPriceColor(self, price):
		if price>=constInfo.HIGH_PRICE:
			return self.HIGH_PRICE_COLOR
		if price>=constInfo.MIDDLE_PRICE:
			return self.MIDDLE_PRICE_COLOR
		else:
			return self.LOW_PRICE_COLOR

	def AppendPrice(self, price):
		self.AppendSpace(5)
		self.AppendTextLine(localeInfo.TOOLTIP_BUYPRICE  % (localeInfo.NumberToMoneyString(price)), self.GetPriceColor(price))
		
	if app.ENABLE_BATTLE_FIELD:
		def AppendPriceBySecondaryCoin(self, price, coinType):
			self.AppendSpace(5)
			self.AppendTextLine(localeInfo.TOOLTIP_BUYPRICE  % (localeInfo.NumberToSecondaryCoinString(price, coinType)), self.GetPriceColor(price))
	else:
		def AppendPriceBySecondaryCoin(self, price):
			self.AppendSpace(5)
			self.AppendTextLine(localeInfo.TOOLTIP_BUYPRICE  % (localeInfo.NumberToSecondaryCoinString(price)), self.GetPriceColor(price))		
	def AppendSellingPrice(self, price):
		if item.IsAntiFlag(item.ITEM_ANTIFLAG_SELL):
			self.AppendTextLine(localeInfo.TOOLTIP_ANTI_SELL, self.DISABLE_COLOR)
			self.AppendSpace(5)
		else:
			self.AppendTextLine(localeInfo.TOOLTIP_SELLPRICE % (localeInfo.NumberToMoneyString(price)), self.GetPriceColor(price))
			self.AppendSpace(5)

	def AppendMetinInformation(self):
		if constInfo.ENABLE_FULLSTONE_DETAILS:
			for i in xrange(item.ITEM_APPLY_MAX_NUM):
				(affectType, affectValue) = item.GetAffect(i)
				affectString = self.__GetAffectString(affectType, affectValue)
				if affectString:
					self.AppendSpace(5)
					self.AppendTextLine(affectString, self.GetChangeTextLineColor(affectValue))

	def AppendMetinWearInformation(self):

		self.AppendSpace(5)
		self.AppendTextLine(localeInfo.TOOLTIP_SOCKET_REFINABLE_ITEM, self.NORMAL_COLOR)

		flagList = (item.IsWearableFlag(item.WEARABLE_BODY),
					item.IsWearableFlag(item.WEARABLE_HEAD),
					item.IsWearableFlag(item.WEARABLE_FOOTS),
					item.IsWearableFlag(item.WEARABLE_WRIST),
					item.IsWearableFlag(item.WEARABLE_WEAPON),
					item.IsWearableFlag(item.WEARABLE_NECK),
					item.IsWearableFlag(item.WEARABLE_EAR),
					item.IsWearableFlag(item.WEARABLE_UNIQUE),
					item.IsWearableFlag(item.WEARABLE_SHIELD),
					item.IsWearableFlag(item.WEARABLE_ARROW))

		wearNames = ""
		for i in xrange(self.WEAR_COUNT):

			name = self.WEAR_NAMES[i]
			flag = flagList[i]

			if flag:
				wearNames += "  "
				wearNames += name

		textLine = ui.TextLine()
		textLine.SetParent(self)
		textLine.SetFontName(self.defFontName)
		textLine.SetPosition(self.toolTipWidth/2, self.toolTipHeight)
		textLine.SetHorizontalAlignCenter()
		textLine.SetPackedFontColor(self.NORMAL_COLOR)
		textLine.SetText(wearNames)
		textLine.Show()
		self.childrenList.append(textLine)

		self.toolTipHeight += self.TEXT_LINE_HEIGHT
		self.ResizeToolTip()

	def GetMetinSocketType(self, number):
		if player.METIN_SOCKET_TYPE_NONE == number:
			return player.METIN_SOCKET_TYPE_NONE
		elif player.METIN_SOCKET_TYPE_SILVER == number:
			return player.METIN_SOCKET_TYPE_SILVER
		elif player.METIN_SOCKET_TYPE_GOLD == number:
			return player.METIN_SOCKET_TYPE_GOLD
		else:
			item.SelectItem(number)
			if item.METIN_NORMAL == item.GetItemSubType():
				return player.METIN_SOCKET_TYPE_SILVER
			elif item.METIN_GOLD == item.GetItemSubType():
				return player.METIN_SOCKET_TYPE_GOLD
			elif "USE_PUT_INTO_ACCESSORY_SOCKET" == item.GetUseType(number):
				return player.METIN_SOCKET_TYPE_SILVER
			elif "USE_PUT_INTO_RING_SOCKET" == item.GetUseType(number):
				return player.METIN_SOCKET_TYPE_SILVER
			elif "USE_PUT_INTO_BELT_SOCKET" == item.GetUseType(number):
				return player.METIN_SOCKET_TYPE_SILVER

		return player.METIN_SOCKET_TYPE_NONE

	def GetMetinItemIndex(self, number):
		if player.METIN_SOCKET_TYPE_SILVER == number:
			return 0
		if player.METIN_SOCKET_TYPE_GOLD == number:
			return 0

		return number

	def __AppendAccessoryMetinSlotInfo(self, metinSlot, mtrlVnum):
		ACCESSORY_SOCKET_MAX_SIZE = 3

		cur=min(metinSlot[0], ACCESSORY_SOCKET_MAX_SIZE)
		end=min(metinSlot[1], ACCESSORY_SOCKET_MAX_SIZE)

		affectType1, affectValue1 = item.GetAffect(0)
		affectList1=[0, max(1, affectValue1*10/100), max(2, affectValue1*20/100), max(3, affectValue1*40/100)]

		affectType2, affectValue2 = item.GetAffect(1)
		affectList2=[0, max(1, affectValue2*10/100), max(2, affectValue2*20/100), max(3, affectValue2*40/100)]

		affectType3, affectValue3 = item.GetAffect(2)
		affectList3=[0, max(1, affectValue3*10/100), max(2, affectValue3*20/100), max(3, affectValue3*40/100)]

		mtrlPos=0
		mtrlList=[mtrlVnum]*cur+[player.METIN_SOCKET_TYPE_SILVER]*(end-cur)
		for mtrl in mtrlList:
			affectString1 = self.__GetAffectString(affectType1, affectList1[mtrlPos+1]-affectList1[mtrlPos])
			affectString2 = self.__GetAffectString(affectType2, affectList2[mtrlPos+1]-affectList2[mtrlPos])
			affectString3 = self.__GetAffectString(affectType3, affectList3[mtrlPos+1]-affectList3[mtrlPos])

			leftTime = 0
			if cur == mtrlPos+1:
				leftTime=metinSlot[2]

			self.__AppendMetinSlotInfo_AppendMetinSocketData(mtrlPos, mtrl, affectString1, affectString2, affectString3, leftTime)
			mtrlPos+=1

	def __AppendMetinSlotInfo(self, metinSlot):
		if self.__AppendMetinSlotInfo_IsEmptySlotList(metinSlot):
			return

		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			self.__AppendMetinSlotInfo_AppendMetinSocketData(i, metinSlot[i])

	def __AppendMetinSlotInfo_IsEmptySlotList(self, metinSlot):
		if 0 == metinSlot:
			return 1

		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlotData=metinSlot[i]
			if 0 != self.GetMetinSocketType(metinSlotData):
				if 0 != self.GetMetinItemIndex(metinSlotData):
					return 0

		return 1

	def __AppendMetinSlotInfo_AppendMetinSocketData(self, index, metinSlotData, custumAffectString="", custumAffectString2="", custumAffectString3="", leftTime=0):

		slotType = self.GetMetinSocketType(metinSlotData)
		itemIndex = self.GetMetinItemIndex(metinSlotData)

		if 0 == slotType:
			return

		self.AppendSpace(5)

		slotImage = ui.ImageBox()
		slotImage.SetParent(self)
		slotImage.Show()

		## Name
		nameTextLine = ui.TextLine()
		nameTextLine.SetParent(self)
		nameTextLine.SetFontName(self.defFontName)
		nameTextLine.SetPackedFontColor(self.NORMAL_COLOR)
		nameTextLine.SetOutline()
		nameTextLine.SetFeather()
		nameTextLine.Show()

		self.childrenList.append(nameTextLine)

		if player.METIN_SOCKET_TYPE_SILVER == slotType:
			slotImage.LoadImage("d:/ymir work/ui/game/windows/metin_slot_silver.sub")
		elif player.METIN_SOCKET_TYPE_GOLD == slotType:
			slotImage.LoadImage("d:/ymir work/ui/game/windows/metin_slot_gold.sub")

		self.childrenList.append(slotImage)

		if localeInfo.IsARABIC():
			slotImage.SetPosition(self.toolTipWidth - slotImage.GetWidth() - 9, self.toolTipHeight-1)
			nameTextLine.SetPosition(self.toolTipWidth - 50, self.toolTipHeight + 2)
		else:
			slotImage.SetPosition(9, self.toolTipHeight-1)
			nameTextLine.SetPosition(50, self.toolTipHeight + 2)

		metinImage = ui.ImageBox()
		metinImage.SetParent(self)
		metinImage.Show()
		self.childrenList.append(metinImage)

		if itemIndex:

			item.SelectItem(itemIndex)

			## Image
			try:
				metinImage.LoadImage(item.GetIconImageFileName())
			except:
				dbg.TraceError("ItemToolTip.__AppendMetinSocketData() - Failed to find image file %d:%s" %
					(itemIndex, item.GetIconImageFileName())
				)

			nameTextLine.SetText(item.GetItemName())

			## Affect
			affectTextLine = ui.TextLine()
			affectTextLine.SetParent(self)
			affectTextLine.SetFontName(self.defFontName)
			affectTextLine.SetPackedFontColor(self.POSITIVE_COLOR)
			affectTextLine.SetOutline()
			affectTextLine.SetFeather()
			affectTextLine.Show()

			if localeInfo.IsARABIC():
				metinImage.SetPosition(self.toolTipWidth - metinImage.GetWidth() - 10, self.toolTipHeight)
				affectTextLine.SetPosition(self.toolTipWidth - 50, self.toolTipHeight + 16 + 2)
			else:
				metinImage.SetPosition(10, self.toolTipHeight)
				affectTextLine.SetPosition(50, self.toolTipHeight + 16 + 2)

			if custumAffectString:
				affectTextLine.SetText(custumAffectString)
			elif itemIndex!=constInfo.ERROR_METIN_STONE:
				affectType, affectValue = item.GetAffect(0)
				affectString = self.__GetAffectString(affectType, affectValue)
				if affectString:
					affectTextLine.SetText(affectString)
			else:
				affectTextLine.SetText(localeInfo.TOOLTIP_APPLY_NOAFFECT)

			self.childrenList.append(affectTextLine)

			if constInfo.ENABLE_FULLSTONE_DETAILS and (not custumAffectString2) and (itemIndex!=constInfo.ERROR_METIN_STONE):
				custumAffectString2 = self.__GetAffectString(*item.GetAffect(1))

			if custumAffectString2:
				affectTextLine = ui.TextLine()
				affectTextLine.SetParent(self)
				affectTextLine.SetFontName(self.defFontName)
				affectTextLine.SetPackedFontColor(self.POSITIVE_COLOR)
				affectTextLine.SetPosition(50, self.toolTipHeight + 16 + 2 + 16 + 2)
				affectTextLine.SetOutline()
				affectTextLine.SetFeather()
				affectTextLine.Show()
				affectTextLine.SetText(custumAffectString2)
				self.childrenList.append(affectTextLine)
				self.toolTipHeight += 16 + 2

			if constInfo.ENABLE_FULLSTONE_DETAILS and (not custumAffectString3) and (itemIndex!=constInfo.ERROR_METIN_STONE):
				custumAffectString3 = self.__GetAffectString(*item.GetAffect(2))

			if custumAffectString3:
				affectTextLine = ui.TextLine()
				affectTextLine.SetParent(self)
				affectTextLine.SetFontName(self.defFontName)
				affectTextLine.SetPackedFontColor(self.POSITIVE_COLOR)
				affectTextLine.SetPosition(50, self.toolTipHeight + 16 + 2 + 16 + 2)
				affectTextLine.SetOutline()
				affectTextLine.SetFeather()
				affectTextLine.Show()
				affectTextLine.SetText(custumAffectString3)
				self.childrenList.append(affectTextLine)
				self.toolTipHeight += 16 + 2

			if 0 != leftTime:
				timeText = (localeInfo.LEFT_TIME + " : " + localeInfo.SecondToDHM(leftTime))

				timeTextLine = ui.TextLine()
				timeTextLine.SetParent(self)
				timeTextLine.SetFontName(self.defFontName)
				timeTextLine.SetPackedFontColor(self.POSITIVE_COLOR)
				timeTextLine.SetPosition(50, self.toolTipHeight + 16 + 2 + 16 + 2)
				timeTextLine.SetOutline()
				timeTextLine.SetFeather()
				timeTextLine.Show()
				timeTextLine.SetText(timeText)
				self.childrenList.append(timeTextLine)
				self.toolTipHeight += 16 + 2

		else:
			nameTextLine.SetText(localeInfo.TOOLTIP_SOCKET_EMPTY)

		self.toolTipHeight += 35
		self.ResizeToolTip()

	def __AppendFishInfo(self, size):
		if size > 0:
			self.AppendSpace(5)
			self.AppendTextLine(localeInfo.TOOLTIP_FISH_LEN % (float(size) / 100.0), self.NORMAL_COLOR)

	def AppendUniqueItemLastTime(self, restMin):
		if app.ENABLE_ATTENDANCE_EVENT:
			if self.isAttendanceRewardItem:
				return	
		restSecond = restMin*60
		self.AppendSpace(5)
		self.AppendTextLine(localeInfo.LEFT_TIME + " : " + localeInfo.SecondToDHM(restSecond), self.NORMAL_COLOR)

	def AppendMallItemLastTime(self, endTime):
		if app.ENABLE_ATTENDANCE_EVENT:
			if self.isAttendanceRewardItem:
				return
		leftSec = max(0, endTime - app.GetGlobalTimeStamp())
		self.AppendSpace(5)
		self.AppendTextLine(localeInfo.LEFT_TIME + " : " + localeInfo.SecondToDHM(leftSec), self.NORMAL_COLOR)

	def AppendTimerBasedOnWearLastTime(self, metinSlot):
		if app.ENABLE_ATTENDANCE_EVENT:
			if self.isAttendanceRewardItem:
				return
		if 0 == metinSlot[0]:
			self.AppendSpace(5)
			self.AppendTextLine(localeInfo.CANNOT_USE, self.DISABLE_COLOR)
		else:
			endTime = app.GetGlobalTimeStamp() + metinSlot[0]
			self.AppendMallItemLastTime(endTime)

	def AppendRealTimeStartFirstUseLastTime(self, item, metinSlot, limitIndex):
		if app.ENABLE_ATTENDANCE_EVENT:
			if self.isAttendanceRewardItem:
				return
		useCount = metinSlot[1]
		endTime = metinSlot[0]

		# 한 번이라도 사용했다면 Socket0에 종료 시간(2012년 3월 1일 13시 01분 같은..) 이 박혀있음.
		# 사용하지 않았다면 Socket0에 이용가능시간(이를테면 600 같은 값. 초단위)이 들어있을 수 있고, 0이라면 Limit Value에 있는 이용가능시간을 사용한다.
		if 0 == useCount:
			if 0 == endTime:
				(limitType, limitValue) = item.GetLimit(limitIndex)
				endTime = limitValue

			endTime += app.GetGlobalTimeStamp()

		self.AppendMallItemLastTime(endTime)
		
	if app.ENABLE_SASH_SYSTEM:
		def SetSashResultItem(self, slotIndex, window_type = player.INVENTORY):
			(itemVnum, MinAbs, MaxAbs) = sash.GetResultItem()
			if not itemVnum:
				return
			
			self.ClearToolTip()
			
			metinSlot = [player.GetItemMetinSocket(window_type, slotIndex, i) for i in xrange(player.METIN_SOCKET_MAX_NUM)]
			attrSlot = [player.GetItemAttribute(window_type, slotIndex, i) for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM)]
			
			item.SelectItem(itemVnum)
			itemType = item.GetItemType()
			itemSubType = item.GetItemSubType()
			if itemType != item.ITEM_TYPE_COSTUME and itemSubType != item.COSTUME_TYPE_SASH:
				return
			
			absChance = MaxAbs
			itemDesc = item.GetItemDescription()
			self.__AdjustMaxWidth(attrSlot, itemDesc)
			self.__SetItemTitle(itemVnum, metinSlot, attrSlot)
			self.AppendDescription(itemDesc, 26)
			self.AppendDescription(item.GetItemSummary(), 26, self.CONDITION_COLOR)
			self.__AppendLimitInformation()
			
			## ABSORPTION RATE
			if MinAbs == MaxAbs:
				self.AppendTextLine(localeInfo.SASH_ABSORB_CHANCE % (MinAbs), self.CONDITION_COLOR)
			else:
				self.AppendTextLine(localeInfo.SASH_ABSORB_CHANCE2 % (MinAbs, MaxAbs), self.CONDITION_COLOR)
			## END ABSOPRTION RATE
			
			itemAbsorbedVnum = int(metinSlot[sash.ABSORBED_SOCKET])
			if itemAbsorbedVnum:
				## ATTACK / DEFENCE
				item.SelectItem(itemAbsorbedVnum)
				if item.GetItemType() == item.ITEM_TYPE_WEAPON:
					if item.GetItemSubType() == item.WEAPON_FAN:
						self.__AppendMagicAttackInfo(absChance)
						item.SelectItem(itemAbsorbedVnum)
						self.__AppendAttackPowerInfo(absChance)
					else:
						self.__AppendAttackPowerInfo(absChance)
						item.SelectItem(itemAbsorbedVnum)
						self.__AppendMagicAttackInfo(absChance)
				elif item.GetItemType() == item.ITEM_TYPE_ARMOR:
					defGrade = item.GetValue(1)
					defBonus = item.GetValue(5) * 2
					defGrade = self.CalcSashValue(defGrade, absChance)
					defBonus = self.CalcSashValue(defBonus, absChance)
					
					if defGrade > 0:
						self.AppendSpace(5)
						self.AppendTextLine(localeInfo.TOOLTIP_ITEM_DEF_GRADE % (defGrade + defBonus), self.GetChangeTextLineColor(defGrade))
					
					item.SelectItem(itemAbsorbedVnum)
					self.__AppendMagicDefenceInfo(absChance)
				## END ATTACK / DEFENCE
				
				## EFFECT
				item.SelectItem(itemAbsorbedVnum)
				for i in xrange(item.ITEM_APPLY_MAX_NUM):
					(affectType, affectValue) = item.GetAffect(i)
					affectValue = self.CalcSashValue(affectValue, absChance)
					affectString = self.__GetAffectString(affectType, affectValue)
					if affectString and affectValue > 0:
						self.AppendTextLine(affectString, self.GetChangeTextLineColor(affectValue))
					
					item.SelectItem(itemAbsorbedVnum)
				# END EFFECT
				
			item.SelectItem(itemVnum)
			## ATTR
			self.__AppendAttributeInformation(attrSlot, MaxAbs)
			# END ATTR
			
			self.AppendWearableInformation()
			self.ShowToolTip()

		def SetSashResultAbsItem(self, slotIndex1, slotIndex2, window_type = player.INVENTORY):
			itemVnumSash = player.GetItemIndex(window_type, slotIndex1)
			itemVnumTarget = player.GetItemIndex(window_type, slotIndex2)
			if not itemVnumSash or not itemVnumTarget:
				return
			
			self.ClearToolTip()
			
			item.SelectItem(itemVnumSash)
			itemType = item.GetItemType()
			itemSubType = item.GetItemSubType()
			if itemType != item.ITEM_TYPE_COSTUME and itemSubType != item.COSTUME_TYPE_SASH:
				return
			
			metinSlot = [player.GetItemMetinSocket(window_type, slotIndex1, i) for i in xrange(player.METIN_SOCKET_MAX_NUM)]
			attrSlot = [player.GetItemAttribute(window_type, slotIndex2, i) for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM)]
			
			itemDesc = item.GetItemDescription()
			self.__AdjustMaxWidth(attrSlot, itemDesc)
			self.__SetItemTitle(itemVnumSash, metinSlot, attrSlot)
			self.AppendDescription(itemDesc, 26)
			self.AppendDescription(item.GetItemSummary(), 26, self.CONDITION_COLOR)
			item.SelectItem(itemVnumSash)
			self.__AppendLimitInformation()
			
			## ABSORPTION RATE
			self.AppendTextLine(localeInfo.SASH_ABSORB_CHANCE % (metinSlot[sash.ABSORPTION_SOCKET]), self.CONDITION_COLOR)
			## END ABSOPRTION RATE
			
			## ATTACK / DEFENCE
			itemAbsorbedVnum = itemVnumTarget
			item.SelectItem(itemAbsorbedVnum)
			if item.GetItemType() == item.ITEM_TYPE_WEAPON:
				if item.GetItemSubType() == item.WEAPON_FAN:
					self.__AppendMagicAttackInfo(metinSlot[sash.ABSORPTION_SOCKET])
					item.SelectItem(itemAbsorbedVnum)
					self.__AppendAttackPowerInfo(metinSlot[sash.ABSORPTION_SOCKET])
				else:
					self.__AppendAttackPowerInfo(metinSlot[sash.ABSORPTION_SOCKET])
					item.SelectItem(itemAbsorbedVnum)
					self.__AppendMagicAttackInfo(metinSlot[sash.ABSORPTION_SOCKET])
			elif item.GetItemType() == item.ITEM_TYPE_ARMOR:
				defGrade = item.GetValue(1)
				defBonus = item.GetValue(5) * 2
				defGrade = self.CalcSashValue(defGrade, metinSlot[sash.ABSORPTION_SOCKET])
				defBonus = self.CalcSashValue(defBonus, metinSlot[sash.ABSORPTION_SOCKET])
				
				if defGrade > 0:
					self.AppendSpace(5)
					self.AppendTextLine(localeInfo.TOOLTIP_ITEM_DEF_GRADE % (defGrade + defBonus), self.GetChangeTextLineColor(defGrade))
				
				item.SelectItem(itemAbsorbedVnum)
				self.__AppendMagicDefenceInfo(metinSlot[sash.ABSORPTION_SOCKET])
			## END ATTACK / DEFENCE
			
			## EFFECT
			item.SelectItem(itemAbsorbedVnum)
			for i in xrange(item.ITEM_APPLY_MAX_NUM):
				(affectType, affectValue) = item.GetAffect(i)
				affectValue = self.CalcSashValue(affectValue, metinSlot[sash.ABSORPTION_SOCKET])
				affectString = self.__GetAffectString(affectType, affectValue)
				if affectString and affectValue > 0:
					self.AppendTextLine(affectString, self.GetChangeTextLineColor(affectValue))
				
				item.SelectItem(itemAbsorbedVnum)
			## END EFFECT
			
			## ATTR
			item.SelectItem(itemAbsorbedVnum)
			for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
				type = attrSlot[i][0]
				value = attrSlot[i][1]
				if not value:
					continue
				
				value = self.CalcSashValue(value, metinSlot[sash.ABSORPTION_SOCKET])
				affectString = self.__GetAffectString(type, value)
				if affectString and value > 0:
					affectColor = self.__GetAttributeColor(i, value)
					self.AppendTextLine(affectString, affectColor)
				
				item.SelectItem(itemAbsorbedVnum)
			## END ATTR
			
			## WEARABLE
			item.SelectItem(itemVnumSash)
			self.AppendSpace(5)
			self.AppendTextLine(localeInfo.TOOLTIP_ITEM_WEARABLE_JOB, self.NORMAL_COLOR)
			
			item.SelectItem(itemVnumSash)
			flagList = (
						not item.IsAntiFlag(item.ITEM_ANTIFLAG_WARRIOR),
						not item.IsAntiFlag(item.ITEM_ANTIFLAG_ASSASSIN),
						not item.IsAntiFlag(item.ITEM_ANTIFLAG_SURA),
						not item.IsAntiFlag(item.ITEM_ANTIFLAG_SHAMAN)
			)
			
			# if app.ENABLE_WOLFMAN_CHARACTER:
				# flagList += (not item.IsAntiFlag(item.ITEM_ANTIFLAG_WOLFMAN),)
			
			characterNames = ""
			for i in xrange(self.CHARACTER_COUNT):
				name = self.CHARACTER_NAMES[i]
				flag = flagList[i]
				if flag:
					characterNames += " "
					characterNames += name
			
			textLine = self.AppendTextLine(characterNames, self.NORMAL_COLOR, True)
			textLine.SetFeather()
			
			item.SelectItem(itemVnumSash)
			if item.IsAntiFlag(item.ITEM_ANTIFLAG_MALE):
				textLine = self.AppendTextLine(localeInfo.FOR_FEMALE, self.NORMAL_COLOR, True)
				textLine.SetFeather()
			
			if item.IsAntiFlag(item.ITEM_ANTIFLAG_FEMALE):
				textLine = self.AppendTextLine(localeInfo.FOR_MALE, self.NORMAL_COLOR, True)
				textLine.SetFeather()
			## END WEARABLE
			
			self.ShowToolTip()

	if app.ENABLE_CHANGELOOK_SYSTEM:
		def AppendTransmutation(self, window_type, slotIndex, transmutation):
			itemVnum = 0
			if transmutation == -1:
				if window_type == player.INVENTORY:
					itemVnum = player.GetItemTransmutation(window_type, slotIndex)
				elif window_type == player.SAFEBOX:
					itemVnum = safebox.GetItemTransmutation(slotIndex)
				elif window_type == player.MALL:
					itemVnum = safebox.GetItemMallTransmutation(slotIndex)
			else:
				itemVnum = transmutation
			
			if not itemVnum:
				return
			
			item.SelectItem(itemVnum)
			itemName = item.GetItemName()
			
			if item.GetItemType() == item.ITEM_TYPE_COSTUME:
				if item.GetItemSubType() == item.COSTUME_TYPE_BODY:
					malefemale = ""
					if item.IsAntiFlag(item.ITEM_ANTIFLAG_MALE):
						malefemale = localeInfo.FOR_FEMALE

					if item.IsAntiFlag(item.ITEM_ANTIFLAG_FEMALE):
						malefemale = localeInfo.FOR_MALE
					itemName += " ( " + malefemale +  " )"
			
			if not itemName or itemName == "":
				return
			
			self.AppendSpace(5)
			title = "[ " + localeInfo.CHANGE_LOOK_TITLE + " ]"
			self.AppendTextLine(title, self.NORMAL_COLOR)
			textLine = self.AppendTextLine(itemName, self.CONDITION_COLOR, True)
			textLine.SetFeather()	
	
class HyperlinkItemToolTip(ItemToolTip):
	def __init__(self):
		ItemToolTip.__init__(self, isPickable=True)

	def SetHyperlinkItem(self, tokens):
		minTokenCount = 3 + player.METIN_SOCKET_MAX_NUM
		if app.ENABLE_CHANGELOOK_SYSTEM:
			minTokenCount += 1
		maxTokenCount = minTokenCount + 2 * player.ATTRIBUTE_SLOT_MAX_NUM
		if tokens and len(tokens) >= minTokenCount and len(tokens) <= maxTokenCount:
			head, vnum, flag = tokens[:3]
			itemVnum = int(vnum, 16)
			metinSlot = [int(metin, 16) for metin in tokens[3:6]]

			rests = tokens[6:]
			transmutation = 0
			if app.ENABLE_CHANGELOOK_SYSTEM:
				rests = tokens[7:]
				cnv = [int(cnv, 16) for cnv in tokens[6:7]]
				transmutation = int(cnv[0])
			if rests:
				attrSlot = []

				rests.reverse()
				while rests:
					key = int(rests.pop(), 16)
					if rests:
						val = int(rests.pop())
						attrSlot.append((key, val))

				attrSlot += [(0, 0)] * (player.ATTRIBUTE_SLOT_MAX_NUM - len(attrSlot))
			else:
				attrSlot = [(0, 0)] * player.ATTRIBUTE_SLOT_MAX_NUM

			self.ClearToolTip()
			#if app.ENABLE_CHANGELOOK_SYSTEM:
			#	import chat
			#	chat.AppendChat(chat.CHAT_TYPE_INFO, str(transmutation))
			#	if not transmutation:
			#		self.AddItemData(itemVnum, metinSlot, attrSlot)
			#	else:
			#		self.AddItemData(itemVnum, metinSlot, attrSlot, 0, player.INVENTORY, -1, transmutation)
			#else:
			self.AddItemData(itemVnum, metinSlot, attrSlot)

			ItemToolTip.OnUpdate(self)

	def OnUpdate(self):
		pass

	def OnMouseLeftButtonDown(self):
		self.Hide()

class SkillToolTip(ToolTip):

	POINT_NAME_DICT = {
		player.LEVEL : localeInfo.SKILL_TOOLTIP_LEVEL,
		player.IQ : localeInfo.SKILL_TOOLTIP_INT,
	}

	SKILL_TOOL_TIP_WIDTH = 200
	PARTY_SKILL_TOOL_TIP_WIDTH = 340

	PARTY_SKILL_EXPERIENCE_AFFECT_LIST = (	( 2, 2,  10,),
											( 8, 3,  20,),
											(14, 4,  30,),
											(22, 5,  45,),
											(28, 6,  60,),
											(34, 7,  80,),
											(38, 8, 100,), )

	PARTY_SKILL_PLUS_GRADE_AFFECT_LIST = (	( 4, 2, 1, 0,),
											(10, 3, 2, 0,),
											(16, 4, 2, 1,),
											(24, 5, 2, 2,), )

	PARTY_SKILL_ATTACKER_AFFECT_LIST = (	( 36, 3, ),
											( 26, 1, ),
											( 32, 2, ), )

	SKILL_GRADE_NAME = {	player.SKILL_GRADE_MASTER : localeInfo.SKILL_GRADE_NAME_MASTER,
							player.SKILL_GRADE_GRAND_MASTER : localeInfo.SKILL_GRADE_NAME_GRAND_MASTER,
							player.SKILL_GRADE_PERFECT_MASTER : localeInfo.SKILL_GRADE_NAME_PERFECT_MASTER, }

	if app.ENABLE_SKILLS_LEVEL_OVER_P:
		SKILL_GRADE_NAME.update({player.SKILL_GRADE_SAGE_MASTER : localeInfo.SKILL_GRADE_NAME_SAGE_MASTER,})

	AFFECT_NAME_DICT =	{
							"HP" : localeInfo.TOOLTIP_SKILL_AFFECT_ATT_POWER,
							"ATT_GRADE" : localeInfo.TOOLTIP_SKILL_AFFECT_ATT_GRADE,
							"DEF_GRADE" : localeInfo.TOOLTIP_SKILL_AFFECT_DEF_GRADE,
							"ATT_SPEED" : localeInfo.TOOLTIP_SKILL_AFFECT_ATT_SPEED,
							"MOV_SPEED" : localeInfo.TOOLTIP_SKILL_AFFECT_MOV_SPEED,
							"DODGE" : localeInfo.TOOLTIP_SKILL_AFFECT_DODGE,
							"RESIST_NORMAL" : localeInfo.TOOLTIP_SKILL_AFFECT_RESIST_NORMAL,
							"REFLECT_MELEE" : localeInfo.TOOLTIP_SKILL_AFFECT_REFLECT_MELEE,
						}
	AFFECT_APPEND_TEXT_DICT =	{
									"DODGE" : "%",
									"RESIST_NORMAL" : "%",
									"REFLECT_MELEE" : "%",
								}

	def __init__(self):
		ToolTip.__init__(self, self.SKILL_TOOL_TIP_WIDTH)
	def __del__(self):
		ToolTip.__del__(self)

	def SetSkill(self, skillIndex, skillLevel = -1):

		if 0 == skillIndex:
			return

		if skill.SKILL_TYPE_GUILD == skill.GetSkillType(skillIndex):

			if self.SKILL_TOOL_TIP_WIDTH != self.toolTipWidth:
				self.toolTipWidth = self.SKILL_TOOL_TIP_WIDTH
				self.ResizeToolTip()

			self.AppendDefaultData(skillIndex)
			self.AppendSkillConditionData(skillIndex)
			self.AppendGuildSkillData(skillIndex, skillLevel)

		else:

			if self.SKILL_TOOL_TIP_WIDTH != self.toolTipWidth:
				self.toolTipWidth = self.SKILL_TOOL_TIP_WIDTH
				self.ResizeToolTip()

			slotIndex = player.GetSkillSlotIndex(skillIndex)
			skillGrade = player.GetSkillGrade(slotIndex)
			skillLevel = player.GetSkillLevel(slotIndex)
			skillCurrentPercentage = player.GetSkillCurrentEfficientPercentage(slotIndex)
			skillNextPercentage = player.GetSkillNextEfficientPercentage(slotIndex)

			self.AppendDefaultData(skillIndex)
			self.AppendSkillConditionData(skillIndex)
			self.AppendSkillDataNew(slotIndex, skillIndex, skillGrade, skillLevel, skillCurrentPercentage, skillNextPercentage)
			self.AppendSkillRequirement(skillIndex, skillLevel)

		self.ShowToolTip()

	def SetSkillNew(self, slotIndex, skillIndex, skillGrade, skillLevel):

		if 0 == skillIndex:
			return

		if player.SKILL_INDEX_TONGSOL == skillIndex:

			slotIndex = player.GetSkillSlotIndex(skillIndex)
			skillLevel = player.GetSkillLevel(slotIndex)

			self.AppendDefaultData(skillIndex)
			self.AppendPartySkillData(skillGrade, skillLevel)

		elif player.SKILL_INDEX_RIDING == skillIndex:

			slotIndex = player.GetSkillSlotIndex(skillIndex)
			self.AppendSupportSkillDefaultData(skillIndex, skillGrade, skillLevel, 30)

		elif player.SKILL_INDEX_SUMMON == skillIndex:

			maxLevel = 10

			self.ClearToolTip()
			self.__SetSkillTitle(skillIndex, skillGrade)

			## Description
			description = skill.GetSkillDescription(skillIndex)
			self.AppendDescription(description, 25)

			if skillLevel == 10:
				self.AppendSpace(5)
				self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL_MASTER % (skillLevel), self.NORMAL_COLOR)
				self.AppendTextLine(localeInfo.SKILL_SUMMON_DESCRIPTION % (skillLevel*10), self.NORMAL_COLOR)

			else:
				self.AppendSpace(5)
				self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL % (skillLevel), self.NORMAL_COLOR)
				self.__AppendSummonDescription(skillLevel, self.NORMAL_COLOR)

				self.AppendSpace(5)
				self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL % (skillLevel+1), self.NEGATIVE_COLOR)
				self.__AppendSummonDescription(skillLevel+1, self.NEGATIVE_COLOR)

		elif skill.SKILL_TYPE_GUILD == skill.GetSkillType(skillIndex):

			if self.SKILL_TOOL_TIP_WIDTH != self.toolTipWidth:
				self.toolTipWidth = self.SKILL_TOOL_TIP_WIDTH
				self.ResizeToolTip()

			self.AppendDefaultData(skillIndex)
			self.AppendSkillConditionData(skillIndex)
			self.AppendGuildSkillData(skillIndex, skillLevel)

		else:

			if self.SKILL_TOOL_TIP_WIDTH != self.toolTipWidth:
				self.toolTipWidth = self.SKILL_TOOL_TIP_WIDTH
				self.ResizeToolTip()

			slotIndex = player.GetSkillSlotIndex(skillIndex)

			skillCurrentPercentage = player.GetSkillCurrentEfficientPercentage(slotIndex)
			skillNextPercentage = player.GetSkillNextEfficientPercentage(slotIndex)

			self.AppendDefaultData(skillIndex, skillGrade)
			self.AppendSkillConditionData(skillIndex)
			self.AppendSkillDataNew(slotIndex, skillIndex, skillGrade, skillLevel, skillCurrentPercentage, skillNextPercentage)
			self.AppendSkillRequirement(skillIndex, skillLevel)

		self.ShowToolTip()

	def __SetSkillTitle(self, skillIndex, skillGrade):
		self.SetTitle(skill.GetSkillName(skillIndex, skillGrade))
		self.__AppendSkillGradeName(skillIndex, skillGrade)

	def __AppendSkillGradeName(self, skillIndex, skillGrade):
		if self.SKILL_GRADE_NAME.has_key(skillGrade):
			self.AppendSpace(5)
			self.AppendTextLine(self.SKILL_GRADE_NAME[skillGrade] % (skill.GetSkillName(skillIndex, 0)), self.CAN_LEVEL_UP_COLOR)

	def SetSkillOnlyName(self, slotIndex, skillIndex, skillGrade):
		if 0 == skillIndex:
			return

		slotIndex = player.GetSkillSlotIndex(skillIndex)

		self.toolTipWidth = self.SKILL_TOOL_TIP_WIDTH
		self.ResizeToolTip()

		self.ClearToolTip()
		self.__SetSkillTitle(skillIndex, skillGrade)
		self.AppendDefaultData(skillIndex, skillGrade)
		self.AppendSkillConditionData(skillIndex)
		self.ShowToolTip()

	def AppendDefaultData(self, skillIndex, skillGrade = 0):
		self.ClearToolTip()
		self.__SetSkillTitle(skillIndex, skillGrade)

		## Level Limit
		levelLimit = skill.GetSkillLevelLimit(skillIndex)
		if levelLimit > 0:

			color = self.NORMAL_COLOR
			if player.GetStatus(player.LEVEL) < levelLimit:
				color = self.NEGATIVE_COLOR

			self.AppendSpace(5)
			self.AppendTextLine(localeInfo.TOOLTIP_ITEM_LIMIT_LEVEL % (levelLimit), color)

		## Description
		description = skill.GetSkillDescription(skillIndex)
		self.AppendDescription(description, 25)

	def AppendSupportSkillDefaultData(self, skillIndex, skillGrade, skillLevel, maxLevel):
		self.ClearToolTip()
		self.__SetSkillTitle(skillIndex, skillGrade)

		## Description
		description = skill.GetSkillDescription(skillIndex)
		self.AppendDescription(description, 25)

		if 1 == skillGrade:
			skillLevel += 19
		elif 2 == skillGrade:
			skillLevel += 29
		elif 3 == skillGrade:
			skillLevel = 40

		self.AppendSpace(5)
		self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL_WITH_MAX % (skillLevel, maxLevel), self.NORMAL_COLOR)

	def AppendSkillConditionData(self, skillIndex):
		conditionDataCount = skill.GetSkillConditionDescriptionCount(skillIndex)
		if conditionDataCount > 0:
			self.AppendSpace(5)
			for i in xrange(conditionDataCount):
				self.AppendTextLine(skill.GetSkillConditionDescription(skillIndex, i), self.CONDITION_COLOR)

	def AppendGuildSkillData(self, skillIndex, skillLevel):
		skillMaxLevel = 7
		skillCurrentPercentage = float(skillLevel) / float(skillMaxLevel)
		skillNextPercentage = float(skillLevel+1) / float(skillMaxLevel)
		## Current Level
		if skillLevel > 0:
			if self.HasSkillLevelDescription(skillIndex, skillLevel):
				self.AppendSpace(5)
				if skillLevel == skillMaxLevel:
					self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL_MASTER % (skillLevel), self.NORMAL_COLOR)
				else:
					self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL % (skillLevel), self.NORMAL_COLOR)

				#####

				for i in xrange(skill.GetSkillAffectDescriptionCount(skillIndex)):
					self.AppendTextLine(skill.GetSkillAffectDescription(skillIndex, i, skillCurrentPercentage), self.ENABLE_COLOR)

				## Cooltime
				coolTime = skill.GetSkillCoolTime(skillIndex, skillCurrentPercentage)
				if coolTime > 0:
					self.AppendTextLine(localeInfo.TOOLTIP_SKILL_COOL_TIME + str(coolTime), self.ENABLE_COLOR)

				## SP
				needGSP = skill.GetSkillNeedSP(skillIndex, skillCurrentPercentage)
				if needGSP > 0:
					self.AppendTextLine(localeInfo.TOOLTIP_NEED_GSP % (needGSP), self.ENABLE_COLOR)

		## Next Level
		if skillLevel < skillMaxLevel:
			if self.HasSkillLevelDescription(skillIndex, skillLevel+1):
				self.AppendSpace(5)
				self.AppendTextLine(localeInfo.TOOLTIP_NEXT_SKILL_LEVEL_1 % (skillLevel+1, skillMaxLevel), self.DISABLE_COLOR)

				#####

				for i in xrange(skill.GetSkillAffectDescriptionCount(skillIndex)):
					self.AppendTextLine(skill.GetSkillAffectDescription(skillIndex, i, skillNextPercentage), self.DISABLE_COLOR)

				## Cooltime
				coolTime = skill.GetSkillCoolTime(skillIndex, skillNextPercentage)
				if coolTime > 0:
					self.AppendTextLine(localeInfo.TOOLTIP_SKILL_COOL_TIME + str(coolTime), self.DISABLE_COLOR)

				## SP
				needGSP = skill.GetSkillNeedSP(skillIndex, skillNextPercentage)
				if needGSP > 0:
					self.AppendTextLine(localeInfo.TOOLTIP_NEED_GSP % (needGSP), self.DISABLE_COLOR)

	def AppendSkillDataNew(self, slotIndex, skillIndex, skillGrade, skillLevel, skillCurrentPercentage, skillNextPercentage):

		self.skillMaxLevelStartDict = { 0 : 17, 1 : 7, 2 : 10, }
		self.skillMaxLevelEndDict = { 0 : 20, 1 : 10, 2 : 10, }

		if app.ENABLE_SKILLS_LEVEL_OVER_P:
			self.skillMaxLevelStartDict.update({3 : 10,})
			self.skillMaxLevelEndDict.update({3 : 10,})

		skillLevelUpPoint = 1
		realSkillGrade = player.GetSkillGrade(slotIndex)
		skillMaxLevelStart = self.skillMaxLevelStartDict.get(realSkillGrade, 15)
		skillMaxLevelEnd = self.skillMaxLevelEndDict.get(realSkillGrade, 20)

		## Current Level
		if skillLevel > 0:
			if self.HasSkillLevelDescription(skillIndex, skillLevel):
				self.AppendSpace(5)
				if skillGrade == skill.SKILL_GRADE_COUNT:
					pass
				elif skillLevel == skillMaxLevelEnd:
					self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL_MASTER % (skillLevel), self.NORMAL_COLOR)
				else:
					self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL % (skillLevel), self.NORMAL_COLOR)
				self.AppendSkillLevelDescriptionNew(skillIndex, skillCurrentPercentage, self.ENABLE_COLOR)

		## Next Level
		if skillGrade != skill.SKILL_GRADE_COUNT:
			if skillLevel < skillMaxLevelEnd:
				if self.HasSkillLevelDescription(skillIndex, skillLevel+skillLevelUpPoint):
					self.AppendSpace(5)
					## HP보강, 관통회피 보조스킬의 경우
					if skillIndex == 141 or skillIndex == 142:
						self.AppendTextLine(localeInfo.TOOLTIP_NEXT_SKILL_LEVEL_3 % (skillLevel+1), self.DISABLE_COLOR)
					else:
						self.AppendTextLine(localeInfo.TOOLTIP_NEXT_SKILL_LEVEL_1 % (skillLevel+1, skillMaxLevelEnd), self.DISABLE_COLOR)
					self.AppendSkillLevelDescriptionNew(skillIndex, skillNextPercentage, self.DISABLE_COLOR)

	def AppendSkillLevelDescriptionNew(self, skillIndex, skillPercentage, color):

		affectDataCount = skill.GetNewAffectDataCount(skillIndex)
		if affectDataCount > 0:
			for i in xrange(affectDataCount):
				type, minValue, maxValue = skill.GetNewAffectData(skillIndex, i, skillPercentage)

				if not self.AFFECT_NAME_DICT.has_key(type):
					continue

				minValue = int(minValue)
				maxValue = int(maxValue)
				affectText = self.AFFECT_NAME_DICT[type]

				if "HP" == type:
					if minValue < 0 and maxValue < 0:
						minValue *= -1
						maxValue *= -1

					else:
						affectText = localeInfo.TOOLTIP_SKILL_AFFECT_HEAL

				affectText += str(minValue)
				if minValue != maxValue:
					affectText += " - " + str(maxValue)
				affectText += self.AFFECT_APPEND_TEXT_DICT.get(type, "")

				#import debugInfo
				#if debugInfo.IsDebugMode():
				#	affectText = "!!" + affectText

				self.AppendTextLine(affectText, color)

		else:
			for i in xrange(skill.GetSkillAffectDescriptionCount(skillIndex)):
				self.AppendTextLine(skill.GetSkillAffectDescription(skillIndex, i, skillPercentage), color)


		## Duration
		duration = skill.GetDuration(skillIndex, skillPercentage)
		if duration > 0:
			self.AppendTextLine(localeInfo.TOOLTIP_SKILL_DURATION % (duration), color)

		## Cooltime
		coolTime = skill.GetSkillCoolTime(skillIndex, skillPercentage)
		if coolTime > 0:
			self.AppendTextLine(localeInfo.TOOLTIP_SKILL_COOL_TIME + str(coolTime), color)

		## SP
		needSP = skill.GetSkillNeedSP(skillIndex, skillPercentage)
		if needSP != 0:
			continuationSP = skill.GetSkillContinuationSP(skillIndex, skillPercentage)

			if skill.IsUseHPSkill(skillIndex):
				self.AppendNeedHP(needSP, continuationSP, color)
			else:
				self.AppendNeedSP(needSP, continuationSP, color)

	def AppendSkillRequirement(self, skillIndex, skillLevel):

		skillMaxLevel = skill.GetSkillMaxLevel(skillIndex)

		if skillLevel >= skillMaxLevel:
			return

		isAppendHorizontalLine = False

		## Requirement
		if skill.IsSkillRequirement(skillIndex):

			if not isAppendHorizontalLine:
				isAppendHorizontalLine = True
				self.AppendHorizontalLine()

			requireSkillName, requireSkillLevel = skill.GetSkillRequirementData(skillIndex)

			color = self.CANNOT_LEVEL_UP_COLOR
			if skill.CheckRequirementSueccess(skillIndex):
				color = self.CAN_LEVEL_UP_COLOR
			self.AppendTextLine(localeInfo.TOOLTIP_REQUIREMENT_SKILL_LEVEL % (requireSkillName, requireSkillLevel), color)

		## Require Stat
		requireStatCount = skill.GetSkillRequireStatCount(skillIndex)
		if requireStatCount > 0:

			for i in xrange(requireStatCount):
				type, level = skill.GetSkillRequireStatData(skillIndex, i)
				if self.POINT_NAME_DICT.has_key(type):

					if not isAppendHorizontalLine:
						isAppendHorizontalLine = True
						self.AppendHorizontalLine()

					name = self.POINT_NAME_DICT[type]
					color = self.CANNOT_LEVEL_UP_COLOR
					if player.GetStatus(type) >= level:
						color = self.CAN_LEVEL_UP_COLOR
					self.AppendTextLine(localeInfo.TOOLTIP_REQUIREMENT_STAT_LEVEL % (name, level), color)

	def HasSkillLevelDescription(self, skillIndex, skillLevel):
		if skill.GetSkillAffectDescriptionCount(skillIndex) > 0:
			return True
		if skill.GetSkillCoolTime(skillIndex, skillLevel) > 0:
			return True
		if skill.GetSkillNeedSP(skillIndex, skillLevel) > 0:
			return True

		return False

	def AppendMasterAffectDescription(self, index, desc, color):
		self.AppendTextLine(desc, color)

	def AppendNextAffectDescription(self, index, desc):
		self.AppendTextLine(desc, self.DISABLE_COLOR)

	def AppendNeedHP(self, needSP, continuationSP, color):

		self.AppendTextLine(localeInfo.TOOLTIP_NEED_HP % (needSP), color)

		if continuationSP > 0:
			self.AppendTextLine(localeInfo.TOOLTIP_NEED_HP_PER_SEC % (continuationSP), color)

	def AppendNeedSP(self, needSP, continuationSP, color):

		if -1 == needSP:
			self.AppendTextLine(localeInfo.TOOLTIP_NEED_ALL_SP, color)

		else:
			self.AppendTextLine(localeInfo.TOOLTIP_NEED_SP % (needSP), color)

		if continuationSP > 0:
			self.AppendTextLine(localeInfo.TOOLTIP_NEED_SP_PER_SEC % (continuationSP), color)

	def AppendPartySkillData(self, skillGrade, skillLevel):
		def fix001(vl):
			return vl.replace("%,0f", "%.0f")

		if 1 == skillGrade:
			skillLevel += 19
		elif 2 == skillGrade:
			skillLevel += 29
		elif 3 == skillGrade:
			skillLevel =  40

		if skillLevel <= 0:
			return

		skillIndex = player.SKILL_INDEX_TONGSOL
		slotIndex = player.GetSkillSlotIndex(skillIndex)
		skillPower = player.GetSkillCurrentEfficientPercentage(slotIndex)
		if localeInfo.IsBRAZIL():
			k = skillPower
		else:
			k = player.GetSkillLevel(skillIndex) / 100.0
		self.AppendSpace(5)
		self.AutoAppendTextLine(localeInfo.TOOLTIP_PARTY_SKILL_LEVEL % skillLevel, self.NORMAL_COLOR)

		if skillLevel>=10:
			self.AutoAppendTextLine(fix001(localeInfo.PARTY_SKILL_ATTACKER) % chop( 10 + 60 * k ))

		if skillLevel>=20:
			self.AutoAppendTextLine(fix001(localeInfo.PARTY_SKILL_BERSERKER) 	% chop(1 + 5 * k))
			self.AutoAppendTextLine(fix001(localeInfo.PARTY_SKILL_TANKER) 	% chop(50 + 1450 * k))

		if skillLevel>=25:
			self.AutoAppendTextLine(fix001(localeInfo.PARTY_SKILL_BUFFER) % chop(5 + 45 * k ))

		if skillLevel>=35:
			self.AutoAppendTextLine(fix001(localeInfo.PARTY_SKILL_SKILL_MASTER) % chop(25 + 600 * k ))

		if skillLevel>=40:
			self.AutoAppendTextLine(fix001(localeInfo.PARTY_SKILL_DEFENDER) % chop( 5 + 30 * k ))

		self.AlignHorizonalCenter()

	def __AppendSummonDescription(self, skillLevel, color):
		if skillLevel > 1:
			self.AppendTextLine(localeInfo.SKILL_SUMMON_DESCRIPTION % (skillLevel * 10), color)
		elif 1 == skillLevel:
			self.AppendTextLine(localeInfo.SKILL_SUMMON_DESCRIPTION % (15), color)
		elif 0 == skillLevel:
			self.AppendTextLine(localeInfo.SKILL_SUMMON_DESCRIPTION % (10), color)


if __name__ == "__main__":
	import app
	import wndMgr
	import systemSetting
	import mouseModule
	import grp
	import ui

	#wndMgr.SetOutlineFlag(True)

	app.SetMouseHandler(mouseModule.mouseController)
	app.SetHairColorEnable(True)
	wndMgr.SetMouseHandler(mouseModule.mouseController)
	wndMgr.SetScreenSize(systemSetting.GetWidth(), systemSetting.GetHeight())
	app.Create("METIN2 CLOSED BETA", systemSetting.GetWidth(), systemSetting.GetHeight(), 1)
	mouseModule.mouseController.Create()

	toolTip = ItemToolTip()
	toolTip.ClearToolTip()
	#toolTip.AppendTextLine("Test")
	desc = "Item descriptions:|increase of width of display to 35 digits per row AND installation of function that the displayed words are not broken up in two parts, but instead if one word is too long to be displayed in this row, this word will start in the next row."
	summ = ""

	toolTip.AddItemData_Offline(10, desc, summ, 0, 0)
	toolTip.Show()

	app.Loop()
