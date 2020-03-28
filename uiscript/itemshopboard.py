import localeInfo

BOARD_WIDTH = 700
BOARD_HEIGHT = 532

LR_BORDER_WIDTH = 15*2
TB_BORDER_HEIGHT = 10*2
DIF_HEIGHT = 20
DIF_WIDTH = 20

TITLE_HEIGHT = 30
TITLE_WIDTH = BOARD_WIDTH - 8*2
TOP_BOARD_HEIGHT = 70
TOP_BOARD_WIDTH = BOARD_WIDTH - LR_BORDER_WIDTH
LEFT_BOARD_HEIGHT = BOARD_HEIGHT - TB_BORDER_HEIGHT - TITLE_HEIGHT - TOP_BOARD_HEIGHT - DIF_HEIGHT - 10
LEFT_BOARD_WIDTH = (BOARD_WIDTH - LR_BORDER_WIDTH - DIF_WIDTH) * 0.35
RIGHT_BOARD_HEIGHT = LEFT_BOARD_HEIGHT
RIGHT_BOARD_WIDTH = (BOARD_WIDTH - LR_BORDER_WIDTH - DIF_WIDTH) * 0.65

DRAGON_COINS_IMAGE_HEIGHT = 26
DRAGON_MARKS_IMAGE_HEIGHT = 25

ITEMSHOP_PATH = "locale/ro/ui/itemshop/"

ITEMLIST_DIF_HEIGHT = 15

window = {
	"name" : "itemshop",
	"style" : ("movable", "float",),

	"x" : (SCREEN_WIDTH - BOARD_WIDTH) / 2,
	"y" : (SCREEN_HEIGHT - BOARD_HEIGHT) / 2,

	"width" : BOARD_WIDTH,
	"height" : BOARD_HEIGHT,
	
	"children" :
	(
		{
			"name" : "board",
			"type" : "board",
			
			"x" : 0,
			"y" : 0,
			
			"width" : BOARD_WIDTH,
			"height" : BOARD_HEIGHT,
			
			"children" :
			(
				
				##############################################
				#### TITLE
				##############################################
				
				{
					"name" : "titlebar",
					"type" : "titlebar",
					"style" : ("attach",),
					
					"x" : 8,
					"y" : 7,
					
					"width" : TITLE_WIDTH,
					
					"children" :
					(
						{
							"name" : "title",
							"type" : "text",
							"style" : ("attach",),
							
							"x" : 0,
							"y" : 3,
							
							"horizontal_align" : "center",
							"text_horizontal_align" : "center",
							"color" : 0xffF8BF24,
							
							"text" : "Latino - Itemshop",
						},
					),
				},
				
				##############################################
				#### TOP BOARD
				##############################################
				
				{
					"name" : "top_board",
					"type" : "board",

					"x" : LR_BORDER_WIDTH/2,
					"y" : TB_BORDER_HEIGHT/2+TITLE_HEIGHT,

					"width" : TOP_BOARD_WIDTH,
					"height" : TOP_BOARD_HEIGHT,

					"decoration" : "FALSE",

					"children" :
					(
						{
							"name" : "tb_dragoncoins",

							"x" : 20,
							"y" : 10,

							"width" : 190,
							"height" : 70 - 10 * 2,

							"children" :
							(
								{
									"name" : "tb_dc_image",
									"type" : "image",

									"x" : 0,
									"y" : 0,
									"vertical_align" : "center",

									"image" : ITEMSHOP_PATH+"dragoncoins.tga",
								},
								{
									"name" : "tb_dc_title",
									"type" : "image",

									"x" : 40,
									"y" : 0-DRAGON_COINS_IMAGE_HEIGHT/2,
									"vertical_align" : "center",

									"image" : ITEMSHOP_PATH+"dragoncoins_title.tga",
								},
								{
									"name" : "tb_dc_account_text",
									"type" : "text",

									"r" : 0.86,
									"g" : 0.553,
									"b" : 0.03,

									"x" : 40,
									"y" : DRAGON_COINS_IMAGE_HEIGHT/2-12,
									"vertical_align" : "center",

									"text" : localeInfo.DRAGON_COINS_ACCOUNT_TEXT,
								},
							),
						},
						{
							"name" : "tb_donate",
							"type" : "button",

							"x" : TOP_BOARD_WIDTH - 180 - 20-235,
							"y" : 0,

							"vertical_align" : "center",

							"default_image" : "d:/ymir work/age_of_zaria/public/xlarge_button_01.sub",
							"over_image" : "d:/ymir work/age_of_zaria/public/xlarge_button_02.sub",
							"down_image" : "d:/ymir work/age_of_zaria/public/xlarge_button_03.sub",

							"text" : "Donaciones",
						},
						{
							"name" : "tb_dragonmarks",

							"x" : 450,
							"y" : 10,

							"width" : 190,
							"height" : 70 - 10 * 2,

							"children" :
							(
								{
									"name" : "tb_dc_image2",
									"type" : "image",

									"x" : 0,
									"y" : 0,
									"vertical_align" : "center",

									"image" : ITEMSHOP_PATH+"dragoncoins.tga",
								},
								{
									"name" : "tb_dc_title2",
									"type" : "image",

									"x" : 40,
									"y" : 0-DRAGON_COINS_IMAGE_HEIGHT/2,
									"vertical_align" : "center",

									"image" : ITEMSHOP_PATH+"dragonmarks_title.tga",
								},
								{
									"name" : "tb_dc_account_text2",
									"type" : "text",

									"r" : 0.86,
									"g" : 0.553,
									"b" : 0.03,

									"x" : 40,
									"y" : DRAGON_COINS_IMAGE_HEIGHT/2-12,
									"vertical_align" : "center",

									"text" : localeInfo.DRAGON_MARKS_ACCOUNT_TEXT,
								},
							),
						},
					),
				},
	
				##############################################
				#### LEFT BOARD
				##############################################
				
				{
					"name" : "left_board",
					"type" : "transthinboard_with_titlebar",

					"x" : LR_BORDER_WIDTH/2,
					"y" : TB_BORDER_HEIGHT/2+TITLE_HEIGHT+TOP_BOARD_HEIGHT+DIF_HEIGHT,

					"width" : LEFT_BOARD_WIDTH,
					"height" : LEFT_BOARD_HEIGHT,

					"title" : "Categorias",
					"no_exit" : "TRUE",
					"decoration" : "FALSE",
					"size_type" : "middle",

					"children" : (
						{
							"name" : "CategoryList",
							"type" : "buttonlistbox",

							"dif_size" : 5,

							"x" : 5,
							"y" : TITLE_HEIGHT + 15,

							"width" : LEFT_BOARD_WIDTH - 5*2,
							"height" : LEFT_BOARD_HEIGHT - TITLE_HEIGHT - 10*2,
						},
						{
							"name" : "CategoryLoading",
							"type" : "ani_image",

							"x" : -15,
							"y" : 0,
							"horizontal_align" : "center",
							"vertical_align" : "center",

							"delay" : 5,

							"images" : (
								"waiting_animation/waiting_animation_frame_0001.tga",
								"waiting_animation/waiting_animation_frame_0002.tga",
								"waiting_animation/waiting_animation_frame_0003.tga",
								"waiting_animation/waiting_animation_frame_0004.tga",
								"waiting_animation/waiting_animation_frame_0005.tga",
								"waiting_animation/waiting_animation_frame_0006.tga",
								"waiting_animation/waiting_animation_frame_0007.tga",
								"waiting_animation/waiting_animation_frame_0008.tga",
								"waiting_animation/waiting_animation_frame_0009.tga",
								"waiting_animation/waiting_animation_frame_0010.tga",
								"waiting_animation/waiting_animation_frame_0011.tga",
								"waiting_animation/waiting_animation_frame_0012.tga",
							),
						},
					),
				},
				
				##############################################
				#### RIGHT BOARD
				##############################################
				
				{
					"name" : "right_board",
					"type" : "transthinboard_with_titlebar",

					"x" : LR_BORDER_WIDTH/2+LEFT_BOARD_WIDTH+DIF_WIDTH,
					"y" : TB_BORDER_HEIGHT/2+TITLE_HEIGHT+TOP_BOARD_HEIGHT+DIF_HEIGHT,

					"width" : RIGHT_BOARD_WIDTH,
					"height" : RIGHT_BOARD_HEIGHT,

					"title" : "Items",
					"no_exit" : "TRUE",
					"decoration" : "FALSE",
					"size_type" : "middle",

					"children" : (
						{
							"name" : "ItemList",
							"type" : "itemshoplistbox",

							"dif_size" : ITEMLIST_DIF_HEIGHT,

							"x" : 15,
							"y" : TITLE_HEIGHT + 15,

							"width" : RIGHT_BOARD_WIDTH - 15*2,
							"height" : RIGHT_BOARD_HEIGHT - TITLE_HEIGHT - 10*2,
						},
						{
							"name" : "ItemLoading",
							"type" : "ani_image",

							"x" : -15,
							"y" : 0,
							"horizontal_align" : "center",
							"vertical_align" : "center",

							"delay" : 5,

							"images" : (
								"waiting_animation/waiting_animation_frame_0001.tga",
								"waiting_animation/waiting_animation_frame_0002.tga",
								"waiting_animation/waiting_animation_frame_0003.tga",
								"waiting_animation/waiting_animation_frame_0004.tga",
								"waiting_animation/waiting_animation_frame_0005.tga",
								"waiting_animation/waiting_animation_frame_0006.tga",
								"waiting_animation/waiting_animation_frame_0007.tga",
								"waiting_animation/waiting_animation_frame_0008.tga",
								"waiting_animation/waiting_animation_frame_0009.tga",
								"waiting_animation/waiting_animation_frame_0010.tga",
								"waiting_animation/waiting_animation_frame_0011.tga",
								"waiting_animation/waiting_animation_frame_0012.tga",
							),
						},
						{
							"name" : "ItemFail",

							"x" : 0,
							"y" : 0,
							"horizontal_align" : "center",
							"vertical_align" : "center",

							"width" : 180,
							"height" : 15 + 25,

							"children" : (
								{
									"name" : "ItemFailText",
									"type" : "text",

									"x" : 0,
									"y" : 0,
									"text_horizontal_align" : "center",
									"horizontal_align" : "center",

									"text" : "Error al cargar la Itemshop.",
								},
								{
									"name" : "ItemFailButton",
									"type" : "button",

									"x" : 0,
									"y" : 15,

									"default_image" : "d:/ymir work/age_of_zaria/public/XLarge_Button_01.sub",
									"over_image" : "d:/ymir work/age_of_zaria/public/XLarge_Button_02.sub",
									"down_image" : "d:/ymir work/age_of_zaria/public/XLarge_Button_03.sub",

									"text" : "Reconectar",
								},
							),
						},
					),
				},
			),
		},
	),
}
