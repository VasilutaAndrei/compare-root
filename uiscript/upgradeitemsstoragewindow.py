import uiScriptLocale

window = {
	"name" : "UpgradeStorageWindow",

	"x" : 100,
	"y" : 20,

	"style" : ("movable", "float",),

	"width" : 176,
	"height" : 250,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board",

			"x" : 0,
			"y" : 0,

			"width" : 176,
			"height" : 250,

			"children" :
			(
				## Title
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 8,
					"y" : 7,

					"width" : 161,
					"color" : "yellow",

					"children" :
					(
						# { "name":"TitleName", "type":"text", "x":77, "y":3, "text": "Depozit Materiale", "text_horizontal_align":"center" },
						{ "name":"TitleName", "type":"text", "x":77, "y":3, "text":"Depozit Materiale", "text_horizontal_align":"center" },
					),
				},
				{
					"name" : "board_miljoc_stil_rama",
					"type" : "new_board",
					
					"x" : 11,
					"y" : 330,
					
					"width": 152,###
					"height": 75,###
				},
				## Button
				{
					"name" : "ExitButton",
					"type" : "button",

					"x" : 0,
					"y" : 37,

					"text" : uiScriptLocale.CLOSE,
					"horizontal_align" : "center",
					"vertical_align" : "bottom",

					"default_image" : "d:/ymir work/ui/public/large_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/large_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/large_button_03.sub",
				},

			),
		},
	),
}
