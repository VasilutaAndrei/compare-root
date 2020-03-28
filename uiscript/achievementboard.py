import uiScriptLocale
Abstand = 30
Board_width = 220

window = {
	"name" : "achievementboard",
	"style" : ("movable", "float",),

	"x" : SCREEN_WIDTH - Board_width - 15,
	"y" : SCREEN_HEIGHT - 90 - 55,

	"width" : Board_width,
	"height" : 90,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board",

			"x" : 0,
			"y" : 0,

			"width" : Board_width,
			"height" : 90,

			"children" :
			(
				{
					"name" : "Achievement_Image",
					"type" : "image",

					"x" : 19,
					"y" : 14 + 10,

					"image" : "d:/ymir work/ui/public/achievement_small.sub",
				},
				{
					"name" : "Achievement_Filler",
					"type" : "text",

					"x" : 80,
					"y" : 14 + 5,

					"text" : "Logro alcanzado:",
				},
				{
					"name" : "Achievement_Text",
					"type" : "text",

					"x" : 80,
					"y" : 14 + 25,

					"text" : "Achievement",
				},
				{
					"name" : "Achievement_Points_Text",
					"type" : "text",

					"x" : 100,
					"y" : 14 + 25,

					"text" : "",
				},
				{
					"name" : "Count_Filler",
					"type" : "text",

					"x" : 80,
					"y" : 14 + 45,

					"text" : "Cantidad:",
				},
				{
					"name" : "Count_Achievement_Text",
					"type" : "text",

					"x" : 125,
					"y" : 14 + 45,

					"text" : "Cantidad",
				},
				{
					"name" : "Achievement_Info_1",
					"type" : "text",

					"x" : 80,
					"y" : 14 + 5,

					"text" : "",
				},
				{
					"name" : "Achievement_Info_2",
					"type" : "text",

					"x" : 80,
					"y" : 14 + 25,

					"text" : "",
				},
				{
					"name" : "Achievement_Info_3",
					"type" : "text",

					"x" : 80,
					"y" : 14 + 45,

					"text" : "",
				},
			),
		},
	),
}
