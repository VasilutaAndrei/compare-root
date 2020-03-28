import localeInfo

SIZE_BOARD_X = 288
SIZE_BOARD_Y = 150

window = {
	"name" : "AdminTool",
	"x" : 0,
	"y" : 0,
	"style" : ("movable", "float",),
	"width" : SIZE_BOARD_X,
	"height" : SIZE_BOARD_Y,
	"children" :
	(
		{
			"name" : "board",
			"type" : "board",
			"x" : 0,
			"y" : 0,
			"width" : SIZE_BOARD_X,
			"height" : SIZE_BOARD_Y,
			"children" :
			(
				{
					"name" : "titlebar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 8,
					"y" : 8,
 
					"width" : SIZE_BOARD_X - 15,
					"color" : "gray",

					"children" :
					(
						{
							"name" : "TitleName",
							"type" : "text",
							"x" : 0,
							"y" : 3,
							"horizontal_align" : "center",
							"text" : localeInfo.ADMIN_MANAGER_TITLE_NAME,
							"text_horizontal_align":"center"
						},
					),
				},
				
				{
					"name" : "ban_result_reason_slot",
					"type" : "slotbar",
					"x" : 60,
					"y" : 33,
					"width" : 200,
					"height" : 18,
					"children" :
					(
						{
							"name" : "ban_result_reason_text",
							"type" : "text",
							"x" : - 50,
							"y" : 3,
							"text" : localeInfo.ADMIN_MANAGER_REASON,
						},					
						{
							"name" : "ban_result_reason",
							"type" : "editline",
							"x" : 3,
							"y" : 3,
							"width" : 200,
							"height" : 200,
							"input_limit" : 32,
							"text" : localeInfo.ADMIN_MANAGER_REASON_TYPE,
						},
					),
				},
				
				{
					"name" : "ban_result_day_slot",
					"type" : "slotbar",
					"x" : 45,
					"y" : 85,
					"width" : 22,
					"height" : 18,
					"children" :
					(
						{
							"name" : "ban_result_day_text",
							"type" : "text",
							"x" : - 35,
							"y" : 3,
							"text" : localeInfo.ADMIN_MANAGER_DAY,
						},					
						{
							"name" : "ban_result_day",
							"type" : "editline",
							"x" : 3,
							"y" : 3,
							"width" : 200,
							"height" : 200,
							"input_limit" : 3,
							"only_number" : 1,
							"text" : "0",
						},
					),
				},
				
				{
					"name" : "ban_result_hour_slot",
					"type" : "slotbar",
					"x" : 110,
					"y" : 85,
					"width" : 22,
					"height" : 18,
					"children" :
					(
						{
							"name" : "ban_result_hour_text",
							"type" : "text",
							"x" : - 37,
							"y" : 3,
							"text" : localeInfo.ADMIN_MANAGER_HOUR,
						},					
						{
							"name" : "ban_result_hour",
							"type" : "editline",
							"x" : 3,
							"y" : 3,
							"width" : 200,
							"height" : 200,
							"input_limit" : 2,
							"only_number" : 1,
							"text" : "0",
						},
					),
				},
				
				{
					"name" : "ban_result_minute_slot",
					"type" : "slotbar",
					"x" : 175,
					"y" : 85,
					"width" : 22,
					"height" : 18,
					"children" :
					(
						{
							"name" : "ban_result_minute_text",
							"type" : "text",
							"x" : - 35,
							"y" : 3,
							"text" : localeInfo.ADMIN_MANAGER_MINUTE,
						},					
						{
							"name" : "ban_result_minute",
							"type" : "editline",
							"x" : 3,
							"y" : 3,
							"width" : 200,
							"height" : 200,
							"input_limit" : 2,
							"only_number" : 1,
							"text" : "0",
						},
					),
				},
				
				{
					"name" : "block_button",
					"type" : "button",
					"x" : 220,
					"y" : 70,
					"text" : localeInfo.ADMIN_MANAGER_BAN,
					"default_image" : "d:/ymir work/ui/public/xlarge_thin_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/xlarge_thin_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/xlarge_thin_button_03.sub",
				},

				
				{
					"name" : "ban_result_user_name_slot",
					"type" : "slotbar",
					"x" : 60,
					"y" : 60,
					"width" : 100,
					"height" : 18,
					"children" :
					(
						{
							"name" : "ban_result_user_name_text",
							"type" : "text",
							"x" : - 50,
							"y" : 3,
							"text" : localeInfo.ADMIN_MANAGER_USERNAME,
						},					
						{
							"name" : "ban_result_user_name",
							"type" : "editline",
							"x" : 3,
							"y" : 3,
							"width" : 100,
							"height" : 18,
							"input_limit" : 12,
						},
					),
				},
			),
		},
	),
}