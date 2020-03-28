import uiScriptLocale

ROOT_PATH = "d:/ymir work/ui/public/battle/"
BACK_IMG_PATH = "d:/ymir work/ui/pattern/"

window = {
	"name" : "BattleWindow",

	"x" : (SCREEN_WIDTH -518) / 2,
	"y" : (SCREEN_HEIGHT - 400) / 2,

	"style" : ("movable","float",),

	"width" : 325,
	"height" : 200,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board",

			"x" : 0,
			"y" : 0,

			"width" : 325,
			"height" : 200,

			"children" :
			(
				## Title
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 8,
					"y" : 7,

					"width" : 310,
					"color" : "yellow",

					"children" :
					(
						{ "name":"title_name", "type":"text", "x":0, "y":-1, "text": "Zona de Lupta", "all_align":"center" },
					),
				},
				
				###########
				
				{
					"name" : "text_board",
					"type" : "window",
					"x" : 14,
					"y" : 36,
					"width" : 0,
					"height" : 0,
				},



				## RankingList bg
				{
					"name" : "ranking_list",
					"type" : "window",

					"x" : 51,
					"y" : 66,

					"width" : 0,
					"height" : 0,
					
					"children" :
					(
						## LeftTop
						
					),	
				},

				## Tab Area
				{
					"name" : "tab_control",
					"type" : "window",

					"x" : 7,
					"y" : 36,

					"width" : 0,
					"height" : 0,

					"children" :
					(
						## Tab
						{
							"name" : "tab_01",
							"type" : "image",

							"x" : 0,
							"y" : 0,

							"width" : 0,
							"height" : 0,

							"image" : ROOT_PATH+"tab_current_rank.sub",
						},
						{
							"name" : "tab_02",
							"type" : "image",

							"x" : 0,
							"y" : 0,

							"width" : 0,
							"height" : 0,
							
							"image" : ROOT_PATH+"tab_accum_rank.sub",
						},
						## RadioButton ##
						{
							"name" : "tab_button_01",
							"type" : "radio_button",

							"x" : 0,
							"y" : 0,

							"width" : 0,
							"height" : 0,
						},
						{
							"name" : "tab_button_02",
							"type" : "radio_button",

							"x" : 124,
							"y" : 0,

							"width" : 0,
							"height" : 0,
						},
					),
				},
				## List Column Titlebar
				{
					"name" : "list",
					"type" : "window",

					"x" : 7,
					"y" : 76,

					"width" : 0,
					"height" : 0,

					"children" :
					(
						{
							"name" : "sub_titlebar",
							"type" : "image",

							"x" : 0,
							"y" : 0,

							"image" : ROOT_PATH+"column_titlebar.sub",

							"children" :
							(
								{ "name":"column_rank", "type":"text", "x":227-170, "y":73-69, "text":"Scurte Informatii", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
								{ "name":"title_name", "type":"text", "x":227-100, "y":90-69, "text":"Esti pregatit pentru lupta finala ? Omorand oponentii", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
								{ "name":"title_name", "type":"text", "x":227-100, "y":107-69, "text":"vei obtine puncte de lupta pe care le vei folosi pentru", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
								{ "name":"title_name", "type":"text", "x":250-100, "y":122-69, "text":"a cumpara iteme valoroase.", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
								{ "name":"title_name", "type":"text", "x":237-100, "y":133-69, "text":"Concursul se tine aproape zilnic si va fi anuntat de un GM.", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
							),
						},
					),
				},
				## Battle info
				{
					"name" : "battle_info",
					"type" : "window",

					"x" : -2,
					"y" : 160,

					"width" : 0,
					"height" : 0,

					"children" :
					(
						{
							"name" : "point_icon",
							"type" : "image",

							"x" : 17,
							"y" : 10,

							"image" : ROOT_PATH+"icon_my_point.sub",
						},
						{ "name":"my_point", "type":"text", "x":41, "y":18, "text": "Zona de Lupta", "text_vertical_align":"center" },
						{
							"name" : "notice_icon",
							"type" : "image",

							"x" : 133,
							"y" : 10,

							"image" : ROOT_PATH+"icon_notice.sub",
						},
						{ "name":"notice", "type":"text", "x":160, "y":18, "text": "Intrare Administratorul Luptelor.", "text_vertical_align":"center" },
						#{
							#"name" : "enter_button",
							#"type" : "button",

							#"x" : 215,
							#"y" : 30,

							#"text" : "Intra",

							#"default_image" : "d:/ymir work/ui/public/large_button_01.sub",
							#"over_image" : "d:/ymir work/ui/public/large_button_02.sub",
							#"down_image" : "d:/ymir work/ui/public/large_button_03.sub",
						#},
					),
				},
				#############
				
			),
		},
	),
}
