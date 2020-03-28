import uiScriptLocale
#3 Regate by [Tupeu]
window = {
	"name" : "SelectCharacterWindow",

	"x" : 0,
	"y" : 0,

	"width" : SCREEN_WIDTH,
	"height" : SCREEN_HEIGHT,

	"children" :
	(
		{
			"name" : "Background",
			"type" : "expanded_image",

			"x" : 0,
			"y" : 0,

			"horizontal_align" : "center",
			"vertical_align" : "center",
			
			"image" : "twix_work/loginwindow/background.png",
			
			"x_scale" : float(SCREEN_WIDTH) / 1920.0,
			"y_scale" : float(SCREEN_HEIGHT) / 1080.0,

			"children" :
			(
				{
					"name" : "Ascalon",
					"type" : "expanded_image",
					
					"x" : -350,
					"y" : 0,
					
					"horizontal_align" : "center",
					"vertical_align" : "center",
					"width" : 308,
					"height" : 154,					
					"image" : "twix_work/selectempirewindow/mildos_0.tga",
				},
				{
					"name" : "Mildos",
					"type" : "expanded_image",
					
					"x" : 350,
					"y" : 0,
					"width" : 308,
					"height" : 154,						
					"horizontal_align" : "center",
					"vertical_align" : "center",
					
					"image" : "twix_work/selectempirewindow/ascalon_0.tga",
				},
				{
					"name" : "Blue",
					"type" : "expanded_image",
					"width" : 308,
					"height" : 154,							
					"x" : 0,
					"y" : 0,
					
					"horizontal_align" : "center",
					"vertical_align" : "center",
					
					"image" : "twix_work/selectempirewindow/blue_0.tga",
				},				
			),
		},
		{
			"name" : "exit_button",
			"type" : "button",
				
			"x" : SCREEN_WIDTH - 110, 
			"y" : 10,
					
			"default_image" : "twix_work/loginwindow/button_0.tga",
			"over_image" :  "twix_work/loginwindow/button_1.tga",
			"down_image" : "twix_work/loginwindow/button_2.tga",

			"children" : 
			(
				{
					"name" : "exit_text",
					"type" : "text",

					"x" : 36, 
					"y" : 7,

					"text" : uiScriptLocale.LOGIN_EXIT,
					"color" : 0xffe8b478,
				},
			),
		},
	),
}