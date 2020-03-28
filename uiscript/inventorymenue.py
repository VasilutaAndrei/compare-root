import uiScriptLocale
import app

ROOT = "d:/ymir work/ui/game/"

window = {
	"name" : "InventoryMenue",
	
	"style" : ("movable", "float",),
	
	"x" : SCREEN_WIDTH / 2,
	"y" : SCREEN_HEIGHT /2,

	"width" : 180,
	"height" : 134 + 30,

	"children" :
	(
	
		{
			"name" : "board",
			"type" : "board_with_titlebar",

			"x" : 0,
			"y" : 0,

			"width" : 180,
			"height" : 134 + 30,
			"title" : uiScriptLocale.INVENTORY_MENUE_TITLE,

			"children" :
			(
			
				{
					"name" : "menue_board",
					"type" : "thinboard_circle",

					"x" : 10,
					"y" : 37,

					"width" : 160,
					"height" : 87 + 30,
				
					"children" :
					(
				
						{
							"name" : "normal_storage",
							"type" : "button",

							"x" : 6,
							"y" : 4,

							"text" : uiScriptLocale.INVENTORY_MENUE_NORMAL,

							"default_image" : "d:/ymir work/ui/game/myshop_deco/select_btn_01.sub",
							"over_image" : "d:/ymir work/ui/game/myshop_deco/select_btn_02.sub",
							"down_image" : "d:/ymir work/ui/game/myshop_deco/select_btn_03.sub",
						},
						
						{
							"name" : "itemshop_storage",
							"type" : "button",

							"x" : 6,
							"y" : 4 + 28,

							"text" : uiScriptLocale.INVENTORY_MENUE_ITEMSHOP,

							"default_image" : "d:/ymir work/ui/game/myshop_deco/select_btn_01.sub",
							"over_image" : "d:/ymir work/ui/game/myshop_deco/select_btn_02.sub",
							"down_image" : "d:/ymir work/ui/game/myshop_deco/select_btn_03.sub",
						},
						
						{
							"name" : "guild_storage",
							"type" : "button",

							"x" : 6,
							"y" : 4 + 28 + 28,

							"text" : uiScriptLocale.INVENTORY_MENUE_GUILD,

							"default_image" : "d:/ymir work/ui/game/myshop_deco/select_btn_01.sub",
							"over_image" : "d:/ymir work/ui/game/myshop_deco/select_btn_02.sub",
							"down_image" : "d:/ymir work/ui/game/myshop_deco/select_btn_03.sub",
						},
						
						{
							"name" : "special_storage",
							"type" : "button",

							"x" : 6,
							"y" : 4 + 28 + 28 + 28,

							"text" : "Switchbot",

							"default_image" : "d:/ymir work/ui/game/myshop_deco/select_btn_01.sub",
							"over_image" : "d:/ymir work/ui/game/myshop_deco/select_btn_02.sub",
							"down_image" : "d:/ymir work/ui/game/myshop_deco/select_btn_03.sub",
						},
						
					)
				},
			),
		},
	)
}
