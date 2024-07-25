import os
import re
import time

from mcdreforged.api.types import Info, PluginServerInterface
from mcdreforged.api.rtext import RText, RColor

last = 0
data_path = ''
player_set = set()


def on_load(server: PluginServerInterface, _):
	global data_path, player_set
	data_path = server.get_data_folder() + '/player_set.set'
	if not os.path.exists(server.get_data_folder()):
		os.mkdir(server.get_data_folder())
	if os.path.exists(data_path):
		with open(data_path, 'r') as f:
			player_set = eval(f.read())


def on_info(server: PluginServerInterface, info: Info):
	global last
	now = time.time()
	if info.is_from_server and '[Server thread/INFO]' in info.raw_content:
		if check(info):
			if now-last > 60:
				server.say(RText(time.strftime('此消息的时间是%H:%M', time.localtime()), color=RColor.light_purple).set_hover_text(time.strftime('详细时间为%Y-%m-%d %H:%M:%S', time.localtime())))
			last = now


def check(info: Info) -> bool:
	if info.is_player or 'left the game' in info.content or 'joined the game' in info.content:
		return True
	else:
		raw = re.match(r'\w+ ', info.content)
		if raw:
			first_word = raw[0][:-1]
			if first_word in player_set and ' lost connection: ' not in info.content:
				return True
	return False


def on_unload(_):
	with open(data_path, 'w') as f:
		f.write(str(player_set))


def on_player_joined(__, player: str, _):
	player_set.add(player)
	with open(data_path, 'w') as f:
		f.write(str(player_set))
