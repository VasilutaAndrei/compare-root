import uiScriptLocale
import item

window = {
	"name" : "SupportInformationWindow",
	"x" : SCREEN_WIDTH - 175 - 90,
	"y" : SCREEN_HEIGHT - 37 - 175,
	"style" : ("movable", "float",),
	"width" : 90,
	"height" : 175,
	"children" :
	(
		{
			"name" : "board",
			"type" : "board",
			"style" : ("attach",),
			"x" : 0,
			"y" : 0,
			"width" : 90,
			"height" : 175,
			"children" :
			(
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),
					"x" : 6,
					"y" : 6,
					"width" : 80,
					"color" : "yellow",
					"children" :
					(
						{ "name":"TitleName", "type":"text", "x":30, "y":3, "text":"Buff", "text_horizontal_align":"center"},
					),
				},
				
				{ 
					"name" : "CloseButton", 
					"type" : "button", 
					"x" : 68, 
					"y" : 10, 
					"tooltip_text" : "Inchide", 
					"default_image" : "d:/ymir work/ui/public/close_button_01.sub",	
					"over_image" : "d:/ymir work/ui/public/close_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/close_button_03.sub",
				},				
				
				{
					"name" : "CombSlot",
					"type" : "image",
					"x" : 13,
					"y" : 38,
					"image" : "supp_bg.tga",
					"children" :
					(
						{
							"name" : "CombSlot",
							"type" : "slot",
							"x" : 3,
							"y" : 3,
							"width" : 90,
							"height" : 175,
							"slot" : (
										{"index":1, "x":18, "y":35, "width":32, "height":64},
										{"index":2, "x":18, "y": 3, "width":32, "height":32},
							),
						},
					),
				},
			),
		},
	),
}

