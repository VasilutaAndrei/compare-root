SERVER_1	= "Live Server"
SERVER_IP	= "35.240.49.101"
CH_1_NAME	= "Canal 1"
CH_2_NAME	= "Canal 2"
CH_3_NAME	= "Canal 3"
CH_4_NAME	= "Canal 4"
CH_1		= 13001
CH_2 		= 13101
CH_3 		= 13201
CH_4 		= 13301

AUTH 		= 11003
MARKADDR	= 13001


SERVER_2	= "Beta Server"
SERVER2_IP	= "35.240.49.101"

STATE_NONE = "..."

STATE_DICT = {
	0 : "...",
	1 : "NORM",
	2 : "FULL",
	3 : "Busy"
}

SERVER01_CHANNEL_DICT = {
	1:{"key":11,"name":CH_1_NAME,"ip":SERVER_IP,"tcp_port":CH_1,"udp_port":CH_1,"state":STATE_NONE,},
	2:{"key":12,"name":CH_2_NAME,"ip":SERVER_IP,"tcp_port":CH_2,"udp_port":CH_2,"state":STATE_NONE,},
	3:{"key":13,"name":CH_3_NAME,"ip":SERVER_IP,"tcp_port":CH_3,"udp_port":CH_3,"state":STATE_NONE,},
	4:{"key":14,"name":CH_4_NAME,"ip":SERVER_IP,"tcp_port":CH_4,"udp_port":CH_4,"state":STATE_NONE,},
	# 5:{"key":15,"name":CH_5_NAME,"ip":SERVER_IP,"tcp_port":CH_5,"udp_port":CH_5,"state":STATE_NONE,},
}

SERVER02_CHANNEL_DICT = {
	1:{"key":21,"name":CH_1_NAME,"ip":SERVER2_IP,"tcp_port":CH_1,"udp_port":CH_1,"state":STATE_NONE,},
	2:{"key":22,"name":CH_2_NAME,"ip":SERVER2_IP,"tcp_port":CH_2,"udp_port":CH_2,"state":STATE_NONE,},
	3:{"key":23,"name":CH_3_NAME,"ip":SERVER2_IP,"tcp_port":CH_3,"udp_port":CH_3,"state":STATE_NONE,},
	4:{"key":24,"name":CH_4_NAME,"ip":SERVER2_IP,"tcp_port":CH_4,"udp_port":CH_4,"state":STATE_NONE,},
}

REGION_NAME_DICT = {
	0 : "",		
}

REGION_AUTH_SERVER_DICT = {
	0 : {
		1 : { "ip":SERVER_IP, "port":AUTH, },
		2 : { "ip":SERVER2_IP, "port":AUTH, },

	}		
}

REGION_DICT = {
	0 : {
		1 : { "name" :SERVER_1, "channel" : SERVER01_CHANNEL_DICT, },
		2 : { "name" :SERVER_2, "channel" : SERVER02_CHANNEL_DICT, },
	},
}

MARKADDR_DICT = {
	10 : { "ip" : SERVER_IP, "tcp_port" : MARKADDR, "mark" : "10.tga", "symbol_path" : "10", },
	20 : { "ip" : SERVER2_IP, "tcp_port" : MARKADDR, "mark" : "10.tga", "symbol_path" : "10", },
}