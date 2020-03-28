import uiScriptLocale

ROOT_PATH = "d:/ymir work/ui/public/"

BOARD_WIDTH = 250
BOARD_HEIGHT = 150

window = {
	"name" : "SoulStoneBoard",
	"style" : ("movable", "float",),

	"x" : SCREEN_WIDTH / 2 - BOARD_WIDTH / 2,
	"y" : SCREEN_HEIGHT / 2 - BOARD_HEIGHT / 2,

	"width" : BOARD_WIDTH,
	"height" : BOARD_HEIGHT,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board_with_titlebar",

			"x" : 0,
			"y" : 0,

			"width" : BOARD_WIDTH,
			"height" : BOARD_HEIGHT,

			"title" : "Abizu2 Seelenstein",

			"children" :
			(
				{
					"name" : "skill_slot",
					"type" : "slot",
					
					"x" : 0,
					"y" : 38,
					
					"width" : 32 * 6 + 5 * (6 - 1),
					"height" : 32,
					
					"image" : "d:/ymir work/ui/public/Slot_Base.sub",
					
					"horizontal_align" : "center",
					
					"slot" :
					(
						{"index":0, "x":37*0, "y":0, "width":32, "height":32},
						{"index":1, "x":37*1, "y":0, "width":32, "height":32},
						{"index":2, "x":37*2, "y":0, "width":32, "height":32},
						{"index":3, "x":37*3, "y":0, "width":32, "height":32},
						{"index":4, "x":37*4, "y":0, "width":32, "height":32},
						{"index":5, "x":37*5, "y":0, "width":32, "height":32},
					),
				},
				{
					"name" : "item_slot",
					"type" : "slot",
					
					"x" : 0,
					"y" : 38 + 32 + 10,
					
					"width" : 32 * 3 + 5 * (3 - 1),
					"height" : 32,
					
					"image" : "d:/ymir work/ui/public/Slot_Base.sub",
					
					"horizontal_align" : "center",
					
					"slot" :
					(
						{"index":0, "x":0, "y":0, "width":32, "height":32},
						{"index":1, "x":(32 * 3 + 5 * (3 - 1) - 32), "y":0, "width":32, "height":32},
					),
				},
				{
					"name" : "button",
					"type" : "button",
					
					"x" : 0,
					"y" : BOARD_HEIGHT - 21 - 15,
					
					"default_image" : "d:/ymir work/ui/public/XLarge_Button_01.sub",
					"over_image" : "d:/ymir work/ui/public/XLarge_Button_02.sub",
					"down_image" : "d:/ymir work/ui/public/XLarge_Button_03.sub",
					
					"horizontal_align" : "center",
					
					"text" : "Seelenstein lesen",
				},
			),
		},
	),
}
