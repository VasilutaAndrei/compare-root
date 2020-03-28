import app
import uiScriptLocale

window = {
	"name" : "LoginWindow",
	"sytle" : ("movable",),

	"x" : 0, 
	"y" : 0,

	"width" : SCREEN_WIDTH,
	"height" : SCREEN_HEIGHT,

	"children" : 
	(
		# Background
		{
			"name" : "background", 
			"type" : "expanded_image",

			"x" : 0, 
			"y" : 0,

			"x_scale" : float(SCREEN_WIDTH) / 1920.0,
			"y_scale" : float(SCREEN_HEIGHT) / 1080.0,

			"image" : "twix_work/loginwindow/background.jpg",
		},

		# Board
		{
			"name" : "board_main",
			"type" : "window",
					
			"x" : 0, 
			"y" : 0,
					
			"width" : 352, 
			"height" : 290,
					
			"vertical_align" : "center",
			"horizontal_align" : "center",
					
			"children" :
			(
				{
					"name" : "board",
					"type" : "image",
							
					"x" : 0, 
					"y" : 0,
					
					"vertical_align" : "center",
					"horizontal_align" : "center",
							
					"image" : "twix_work/loginwindow/board.tga",
							
					"children" : 
					(
						{
							"name" : "id_slotbar",
							"type" : "image",
									
							"x" : 0, 
							"y" : -39,
									
							"horizontal_align" : "center",
							"vertical_align" : "center",
									
							"image" : "twix_work/loginwindow/slotbar.tga",
									
							"children" : 
							(
								{
									"name" : "id",
									"type" : "editline",
											
									"x" : 12, 
									"y" : 10,
											
									"width" : 200, 
									"height" : 16,
											
									"color" : 0xffccb3ad,
									"input_limit": 16,
								},
							),
						},
						{
							"name" : "pwd_slotbar",
							"type" : "image",
									
							"x" : 0, 
							"y" : 7,
							
							"horizontal_align" : "center",
							"vertical_align" : "center",
									
							"image" : "twix_work/loginwindow/slotbar.tga",
									
							"children" : 
							(
								{
									"name" : "pwd",
									"type" : "editline",
											
									"x" : 12, 
									"y" : 10,
											
									"width" : 200, 
									"height" : 16,
											
									"color" : 0xffccb3ad,
									"input_limit": 16,
									"secret_flag": 1,
								},
							),
						},
						{
							"name" : "login_button",
							"type" : "button",

							"x" : -2, 
							"y" : 83,

							"horizontal_align" : "center",
							"vertical_align" : "center",

							"default_image" : "twix_work/loginwindow/button_0.tga", 
							"over_image" : "twix_work/loginwindow/button_1.tga",
							"down_image" : "twix_work/loginwindow/button_2.tga",

							"children" : 
							(
								{
									"name" : "login_text",
									"type" : "text",
											
									"x" : 26, 
									"y" : 7,
											
									"text" : uiScriptLocale.LOGIN_CONNECT,
									"color" : 0xffe8b478,
								},
							),
						},
						{
							"name" : "buttonExpand",
							"type" : "button",

							"x" : 88,
							"y" : 244,

							"default_image": "twix_work/loginwindow/btn_belt_open_01_normal.tga",
							"over_image": "twix_work/loginwindow/btn_belt_open_02_hover.tga",
							"down_image": "twix_work/loginwindow/btn_belt_open_03_active.tga",
						},
					),
				},
			),
		},
		{
			"name" : "changechannel",
			"type" : "expanded_image",
			
			"x" : 0,
			"y" : 144,

			"image": "twix_work/loginwindow/channel/board.tga",
			
			"horizontal_align" : "center",
			"vertical_align" : "center",

			"children" :
			(
				{
					"name" : "ch1",
					"type" : "radio_button",
					
					"x" : -41, 
					"y" : -15,
					
					"horizontal_align" : "center",
					"vertical_align" : "center",
					
					"default_image" : "twix_work/loginwindow/channel/button_0.tga",
					"over_image" : "twix_work/loginwindow/channel/button_1.tga",
					"down_image" : "twix_work/loginwindow/channel/button_2.tga",
					
					"children" : 
					(
						{
							"name" : "ch1_text",
							"type" : "text",
									
							"x" : 18, 
							"y" : 6,
									
							"text" : "Canal 1",
							"color" : 0xffe8b478,
						},
					),
				},
				{
					"name" : "ch2",
					"type" : "radio_button",
					
					"x" : 41, 
					"y" : -15,
					
					"horizontal_align" : "center",
					"vertical_align" : "center",
					
					"default_image" : "twix_work/loginwindow/channel/button_0.tga",
					"over_image" : "twix_work/loginwindow/channel/button_1.tga",
					"down_image" : "twix_work/loginwindow/channel/button_2.tga",
					
					"children" : 
					(
						{
							"name" : "ch2_text",
							"type" : "text",
									
							"x" : 18, 
							"y" : 6,
									
							"text" : "Canal 2",
							"color" : 0xffe8b478,
						},
					),
				},
				{
					"name" : "ch3",
					"type" : "radio_button",
					
					"x" : -41, 
					"y" : 12,
					
					"horizontal_align" : "center",
					"vertical_align" : "center",
					
					"default_image" : "twix_work/loginwindow/channel/button_0.tga",
					"over_image" : "twix_work/loginwindow/channel/button_1.tga",
					"down_image" : "twix_work/loginwindow/channel/button_2.tga",

					"children" : 
					(
						{
							"name" : "ch3_text",
							"type" : "text",
									
							"x" : 18, 
							"y" : 6,
									
							"text" : "Canal 3",
							"color" : 0xffe8b478,
						},
					),
				},
				{
					"name" : "ch4",
					"type" : "radio_button",
					
					"x" : 41, 
					"y" : 12,
					
					"horizontal_align" : "center",
					"vertical_align" : "center",
					
					"default_image" : "twix_work/loginwindow/channel/button_0.tga",
					"over_image" : "twix_work/loginwindow/channel/button_1.tga",
					"down_image" : "twix_work/loginwindow/channel/button_2.tga",
					
					"children" : 
					(
						{
							"name" : "ch4_text",
							"type" : "text",
									
							"x" : 18, 
							"y" : 6,
									
							"text" : "Canal 4",
							"color" : 0xffe8b478,
						},
					),
				},
				{
					"name" : "buttonMinimize",
					"type" : "button",

					"x" : 0,
					"y" : 32,
					
					"horizontal_align" : "center",
					"vertical_align" : "center",

					"default_image": "twix_work/loginwindow/btn_belt_close_01_normal.tga",
					"over_image": "twix_work/loginwindow/btn_belt_close_02_hover.tga",
					"down_image": "twix_work/loginwindow/btn_belt_close_03_active.tga",
				},
			),
		},	
		{
			"name" : "dog",
			"type" : "button",
							
			"x" :0, 
			"y" : 300,
							
			"horizontal_align" : "center",
			"vertical_align" : "center",
							
			"default_image" : "twix_work/loginwindow/dog1.tga", 
			"over_image" : "twix_work/loginwindow/dog2.tga",
			"down_image" : "twix_work/loginwindow/dog2.tga",
		},
		{
			"name" : "account_board",
			"type" : "image",
			
			"x" : 290,
			"y" : 0,

			"horizontal_align" : "right",
			"vertical_align" : "center",

			"image" : "twix_work/loginwindow/account/board.tga",

			"children" :
			(
				{
					"name" : "account_0_image",
					"type" : "image",
					
					"x" : 28, 
					"y" : 24,
					
					"image" : "twix_work/loginwindow/slotbar.tga",
					
					"children" : 
					(
						{
							"name" : "account_0_text",
							"type" : "text",

							"x" : 0, 
							"y" : -1,

							"color" : 0xffccb3ad,
							"all_align" : True,
						},
					),
				},
				{
					"name" : "delete_button_0",
					"type" : "button",
					
					"x" : 260, 
					"y" : 27,
					
					"default_image" : "twix_work/loginwindow/account/delete_0.tga",
					"over_image" :  "twix_work/loginwindow/account/delete_1.tga",
					"down_image" : "twix_work/loginwindow/account/delete_2.tga",
				},
				{
					"name" : "save_button_0",
					"type" : "button",
					
					"x" : 260, 
					"y" : 27,
					
					"default_image" : "twix_work/loginwindow/account/save_0.tga",
					"over_image" :  "twix_work/loginwindow/account/save_1.tga",
					"down_image" : "twix_work/loginwindow/account/save_2.tga",
				},
				{
					"name" : "load_button_0",
					"type" : "button",
					
					"x" : 150, 
					"y" : 26,
					
					"default_image" : "twix_work/loginwindow/button_0.tga",
					"over_image" :  "twix_work/loginwindow/button_1.tga",
					"down_image" : "twix_work/loginwindow/button_2.tga",
					
					"children" : 
					(
						{
							"name" : "load_text",
							"type" : "text",

							"x" : 36, 
							"y" : 7,

							"text" : uiScriptLocale.LOGIN_ACCOUNT_LOAD,
							"color" : 0xffe8b478,
						},
					),
				},
				{
					"name" : "account_1_image",
					"type" : "image",
					"x" : 28, "y" : 74,
					"image" : "twix_work/loginwindow/slotbar.tga",
					"children" : 
					(
						{
							"name" : "account_1_text",
							"type" : "text",
							
							"x" : 0, 
							"y" : -1,
							
							"color" : 0xffccb3ad,
							"all_align" : True,
						},
					),
				},
				{
					"name" : "delete_button_1",
					"type" : "button",
					
					"x" : 260, 
					"y" : 77,
					
					"default_image" : "twix_work/loginwindow/account/delete_0.tga",
					"over_image" :  "twix_work/loginwindow/account/delete_1.tga",
					"down_image" : "twix_work/loginwindow/account/delete_2.tga",
				},
				{
					"name" : "save_button_1",
					"type" : "button",
					
					"x" : 260, 
					"y" : 77,
					
					"default_image" : "twix_work/loginwindow/account/save_0.tga",
					"over_image" :  "twix_work/loginwindow/account/save_1.tga",
					"down_image" : "twix_work/loginwindow/account/save_2.tga",
				},
				{
					"name" : "load_button_1",
					"type" : "button",
					
					"x" : 150, 
					"y" : 76,
					
					"default_image" : "twix_work/loginwindow/button_0.tga",
					"over_image" :  "twix_work/loginwindow/button_1.tga",
					"down_image" : "twix_work/loginwindow/button_2.tga",
					
					"children" : 
					(
						{
							"name" : "load_text",
							"type" : "text",

							"x" : 36, 
							"y" : 7,

							"text" : uiScriptLocale.LOGIN_ACCOUNT_LOAD,
							"color" : 0xffe8b478,
						},
					),
				},
				{
					"name" : "account_2_image",
					"type" : "image",
					"x" : 28, "y" : 124,
					"image" : "twix_work/loginwindow/slotbar.tga",
					"children" : 
					(
						{
							"name" : "account_2_text",
							"type" : "text",
							
							"x" : 0, 
							"y" : -1,
							
							"color" : 0xffccb3ad,
							"all_align" : True,
						},
					),
				},
				{
					"name" : "delete_button_2",
					"type" : "button",
					
					"x" : 260, 
					"y" : 126,
					
					"default_image" : "twix_work/loginwindow/account/delete_0.tga",
					"over_image" :  "twix_work/loginwindow/account/delete_1.tga",
					"down_image" : "twix_work/loginwindow/account/delete_2.tga",
				},
				{
					"name" : "save_button_2",
					"type" : "button",
					
					"x" : 260, 
					"y" : 126,
					
					"default_image" : "twix_work/loginwindow/account/save_0.tga",
					"over_image" :  "twix_work/loginwindow/account/save_1.tga",
					"down_image" : "twix_work/loginwindow/account/save_2.tga",
				},
				{
					"name" : "load_button_2",
					"type" : "button",
					
					"x" : 150, 
					"y" : 125,
					
					"default_image" : "twix_work/loginwindow/button_0.tga",
					"over_image" :  "twix_work/loginwindow/button_1.tga",
					"down_image" : "twix_work/loginwindow/button_2.tga",
					
					"children" : 
					(
						{
							"name" : "load_text",
							"type" : "text",

							"x" : 36, 
							"y" : 7,

							"text" : uiScriptLocale.LOGIN_ACCOUNT_LOAD,
							"color" : 0xffe8b478,
						},
					),
				},
				{
					"name" : "account_3_image",
					"type" : "image",
					"x" : 28, "y" : 174,
					"image" : "twix_work/loginwindow/slotbar.tga",
					"children" : 
					(
						{
							"name" : "account_3_text",
							"type" : "text",
							
							"x" : 0, 
							"y" : -1,
							
							"color" : 0xffccb3ad,
							"all_align" : True,
						},
					),
				},
				{
					"name" : "delete_button_3",
					"type" : "button",
					
					"x" : 260, 
					"y" : 177,
					
					"default_image" : "twix_work/loginwindow/account/delete_0.tga",
					"over_image" :  "twix_work/loginwindow/account/delete_1.tga",
					"down_image" : "twix_work/loginwindow/account/delete_2.tga",
				},
				{
					"name" : "save_button_3",
					"type" : "button",
					
					"x" : 260, 
					"y" : 177,
					
					"default_image" : "twix_work/loginwindow/account/save_0.tga",
					"over_image" :  "twix_work/loginwindow/account/save_1.tga",
					"down_image" : "twix_work/loginwindow/account/save_2.tga",
				},
				{
					"name" : "load_button_3",
					"type" : "button",
					
					"x" : 150, 
					"y" : 176,
					
					"default_image" : "twix_work/loginwindow/button_0.tga",
					"over_image" :  "twix_work/loginwindow/button_1.tga",
					"down_image" : "twix_work/loginwindow/button_2.tga",
					
					"children" : 
					(
						{
							"name" : "load_text",
							"type" : "text",

							"x" : 36, 
							"y" : 7,

							"text" : uiScriptLocale.LOGIN_ACCOUNT_LOAD,
							"color" : 0xffe8b478,
						},
					),
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