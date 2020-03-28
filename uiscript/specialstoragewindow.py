import uiScriptLocale
import app

window = {
	"name" : "SpecialStorageWindow",

	"x" : SCREEN_WIDTH - 400,
	"y" : 10,

	"style" : ("movable", "float",),

	"width" : 184,
	"height" : 328+32+35,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : 184,
			"height" : 328+32+35,

			"children" :
			(
				## Title
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 46,
					"y" : 8,

					"width" : 130,
					"color" : "gray",

					"children" :
					(
						{ "name":"TitleName", "type":"text", "x":66, "y":4, "text":"Magazie", "text_horizontal_align":"center" },
					),
				},

				{
					"name":"SetItemsStorage",
					"type":"button",
					"x":7,
					"y":8,
					"tooltip_text" : "Aranjare Iteme",
					"horizontal_align":"left",
					"default_image" : "d:/ymir work/ui/public/button_refresh_02.sub",
					"over_image" : "d:/ymir work/ui/public/button_refresh_01.sub",
					"down_image" : "d:/ymir work/ui/public/button_refresh_03.sub",
				},
				
				## Item Slot
				{
					"name" : "ItemSlot",
					"type" : "grid_table",

					"x" : 12,
					"y" : 34,

					"start_index" : 0,
					"x_count" : 5,
					"y_count" : 9,
					"x_step" : 32,
					"y_step" : 32,

					"image" : "d:/ymir work/ui/public/Slot_Base.sub",
				},
				
				{
					"name" : "Inventory_Tab_01",
					"type" : "radio_button",

					"x" : 14,
					"y" : 295+32,

					"default_image" : "d:/ymir work/ui/game/special_storage/tab_button_large_01.sub",
					"over_image" : "d:/ymir work/ui/game/special_storage/tab_button_large_02.sub",
					"down_image" : "d:/ymir work/ui/game/special_storage/tab_button_large_03.sub",
					"children" :
					(
						{
							"name" : "Inventory_Tab_01_Print_2",
							"type" : "text",

							"x" : 0,
							"y" : 0,

							"all_align" : "center",
							"text" : "I",
						},
					),
				},
				
				{
					"name" : "Inventory_Tab_02",
					"type" : "radio_button",

					"x" : 14 + 40,
					"y" : 295+32,

					"default_image" : "d:/ymir work/ui/game/special_storage/tab_button_large_01.sub",
					"over_image" : "d:/ymir work/ui/game/special_storage/tab_button_large_02.sub",
					"down_image" : "d:/ymir work/ui/game/special_storage/tab_button_large_03.sub",

					"children" :
					(
						{
							"name" : "Inventory_Tab_02_Print_2",
							"type" : "text",

							"x" : 0,
							"y" : 0,

							"all_align" : "center",
							"text" : "II",
						},
					),
				},
				{
					"name" : "Inventory_Tab_03",
					"type" : "radio_button",

					"x" : 14 + 80,
					"y" : 295+32,

					"default_image" : "d:/ymir work/ui/game/special_storage/tab_button_large_01.sub",
					"over_image" : "d:/ymir work/ui/game/special_storage/tab_button_large_02.sub",
					"down_image" : "d:/ymir work/ui/game/special_storage/tab_button_large_03.sub",

					"children" :
					(
						{
							"name" : "Inventory_Tab_03_Print",
							"type" : "text",

							"x" : 0,
							"y" : 0,

							"all_align" : "center",
							"text" : "III",
						},
					),
				},
				{
					"name" : "Inventory_Tab_04",
					"type" : "radio_button",

					"x" : 14 + 120,
					"y" : 295+32,

					"default_image" : "d:/ymir work/ui/game/special_storage/tab_button_large_01.sub",
					"over_image" : "d:/ymir work/ui/game/special_storage/tab_button_large_02.sub",
					"down_image" : "d:/ymir work/ui/game/special_storage/tab_button_large_03.sub",

					"children" :
					(
						{
							"name" : "Inventory_Tab_04_Print",
							"type" : "text",

							"x" : 0,
							"y" : 0,

							"all_align" : "center",
							"text" : "IV",
						},
					),
				},
				
				{
					"name" : "Category_Tab_01",
					"type" : "radio_button",

					"x" : 30,
					"y" : 295+32+30,

					"default_image" : "d:/ymir work/ui/game/special_storage/tab_upgrade_button_middle_01.sub",
					"over_image" : "d:/ymir work/ui/game/special_storage/tab_upgrade_button_middle_02.sub",
					"down_image" : "d:/ymir work/ui/game/special_storage/tab_upgrade_button_middle_03.sub",
				},
					
				{
					"name" : "Category_Tab_02",
					"type" : "radio_button",

					"x" : 30+41,
					"y" : 295+32+30,
					"default_image" : "d:/ymir work/ui/game/special_storage/tab_book_button_middle_01.sub",
					"over_image" : "d:/ymir work/ui/game/special_storage/tab_book_button_middle_02.sub",
					"down_image" : "d:/ymir work/ui/game/special_storage/tab_book_button_middle_03.sub",
				},
				
				{
					"name" : "Category_Tab_03",
					"type" : "radio_button",

					"x" : 30+41+41,
					"y" : 295+32+30,

					"default_image" : "d:/ymir work/ui/game/special_storage/tab_stone_button_middle_01.sub",
					"over_image" : "d:/ymir work/ui/game/special_storage/tab_stone_button_middle_02.sub",
					"down_image" : "d:/ymir work/ui/game/special_storage/tab_stone_button_middle_03.sub",
				},
			),
		},
	),
}