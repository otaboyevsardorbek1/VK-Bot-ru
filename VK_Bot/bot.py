# -*- coding: utf-8 -*-

# VK_API
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

# PyQt5
from PyQt5.QtCore import QThread, pyqtSignal

# Другие
import global_variables as GlobalVariables
import server as Server
import requests

# Классы для работы бота
# ==================================================================
class Sender:
	def __init__(self, vk_session: vk_api.VkApi):
		self.vk_session = vk_session

	def send_message(self, peer_id: int, message: str):
		self.vk_session.method(
			'messages.send',
			{
				'peer_id': peer_id,
				'message': message,
				'random_id': 0
			}
		)

class MyBotLongPool(VkBotLongPoll):
	def __init__(self, vk: vk_api.VkApi, group_id: int):
		self.bot_theard_run = True
		super().__init__(vk, group_id)

	def _parse_event(self, raw_event):
		if self.bot_theard_run == True:
			event_class = self.CLASS_BY_EVENT_TYPE.get(
				raw_event['type'],
				self.DEFAULT_EVENT_CLASS
			)
			return event_class(raw_event)

	def update_longpoll_server(self, update_ts=True):
		if self.bot_theard_run == True:
			values = {
				'group_id': self.group_id
			}
			response = self.vk.method('groups.getLongPollServer', values)

			self.key = response['key']
			self.server = response['server']

			self.url = self.server

			if update_ts:
				self.ts = response['ts']

	def check(self):
		if self.bot_theard_run == True:
			values = {
				'act': 'a_check',
				'key': self.key,
				'ts': self.ts,
				'wait': self.wait,
			}
			response = self.session.get(self.url, params=values, timeout=self.wait + 10).json()

			if 'failed' not in response:
				self.ts = response['ts']
				return [self._parse_event(raw_event) for raw_event in response['updates']]
			elif response['failed'] == 1:
				self.ts = response['ts']
			elif response['failed'] == 2:
				self.update_longpoll_server(update_ts=False)
			elif response['failed'] == 3:
				self.update_longpoll_server()
			return []

	def listen(self):
		while self.bot_theard_run == True:
			try:
				for event in self.check():
					yield event
			except requests.exceptions.ReadTimeout:
				pass
# ==================================================================

# Бот
# ==================================================================
class Bot(QThread):
	signalPrintUserMessage = pyqtSignal(str, str, str)

	def __init__(self, token: str, group_id: str, bot_name: str):
		QThread.__init__(self)

		self.bot_name = bot_name
		self.dict_for_warning_func = {}
		self.warning_dict = {}

		self.vk_session = vk_api.VkApi(token = token)
		self.longpoll = MyBotLongPool(self.vk_session, int(group_id))
		self.sender = Sender(self.vk_session)
	
	def get_commands_list(self):
		commands_list = ''
		user_commands = Server.get_user_commands(self.bot_name)
		for user_command in user_commands:
			if user_command['Flags']['Show_Command_In_Commands_List'] == True:
				command = user_command['Command']
				if command.find('{take_user_id}') != -1:
					command  = f'[ID другого пользователя]'.join(command.split('{take_user_id}'))
				commands_list += f"•  {command}\n"
		return commands_list

	def default_command(self, id: int, user_data: dict, user: list, user_command: dict):
		command_answer = user_command['Command_Answer']
		if command_answer.find('{user}') != -1:
			command_answer = f"@id{id} ({user_data['first_name']} {user_data['last_name']})".join(command_answer.split('{user}'))
		if command_answer.find('{db[1]}') != -1:
			command_answer = f'{user[1]}'.join(command_answer.split('{db[1]}'))
		if command_answer.find('{db[2]}') != -1:
			command_answer = f'{user[2]}'.join(command_answer.split('{db[2]}'))
		if command_answer.find('{db[3]}') != -1:
			command_answer = f'{user[3]}/{user[1] * 20}'.join(command_answer.split('{db[3]}'))
		if command_answer.find('{all_commands}') != -1:
			commands_list = self.get_commands_list()
			command_answer = commands_list.join(command_answer.split('{all_commands}'))
		return command_answer

	def not_default_command(self, peer_id: int, id: int, user_data: dict, user: list, message: str, message_value: int, user_command: dict):
		other_id = int(message.split()[message_value].split('|')[0].replace('[', '').replace('id', '').replace('!', '').strip())
		chat_members = self.vk_session.method('messages.getConversationMembers', {'peer_id': peer_id, 'fields': 'verified'})
		command_answer = user_command['Command_Answer']

		other_user_find_in_chat_members = False
		for chat_member in chat_members['items']:
			if other_id == chat_member['member_id']:
				other_user_find_in_chat_members = True
				break

		code_work = True
		other_user = Server.find_in_database(self.bot_name, f"SELECT * FROM Users WHERE id = '{other_id}'")
		other_user_data = self.vk_session.method('users.get',{'user_ids': other_id, 'fields': 'verified'})[0]
		if other_user != None:
			if other_user_find_in_chat_members == True:
				if command_answer.find('{other_user}') != -1:
					command_answer = f"@id{other_id} ({other_user_data['first_name']} {other_user_data['last_name']})".join(command_answer.split('{other_user}'))
				if command_answer.find('{other_db[1]}') != -1:
					command_answer = f'{other_user[1]}'.join(command_answer.split('{other_db[1]}'))
				if command_answer.find('{other_db[2]}') != -1:
					command_answer = f'{other_user[2]}'.join(command_answer.split('{other_db[2]}'))
				if command_answer.find('{other_db[3]}') != -1:
					command_answer = f'{other_user[3]}/{user[1] * 20}'.join(command_answer.split('{other_db[3]}'))
				if command_answer.find('{other_db[4]}') != -1:
					command_answer = f'{other_user[4]}'.join(command_answer.split('{other_db[4]}'))
			else:
				command_answer = f"@id{id} ({user_data['first_name']} {user_data['last_name']}), пользователь @id{other_id} ({other_user_data['first_name']} {other_user_data['last_name']}) не является участником данной беседы!"
				code_work = False
		else:
			command_answer =  f"@id{id} ({user_data['first_name']} {user_data['last_name']}), пользователя @id{other_id} ({other_user_data['first_name']} {other_user_data['last_name']}) нет в базе данных бота, попробуйте в другой раз!"
			code_work = False

		if code_work == True:
			if command_answer.find('{user}') != -1:
				command_answer = f"@id{id} ({user_data['first_name']} {user_data['last_name']})".join(command_answer.split('{user}'))
			if command_answer.find('{db[1]}') != -1:
				command_answer = f'{user[1]}'.join(command_answer.split('{db[1]}'))
			if command_answer.find('{db[2]}') != -1:
				command_answer = f'{user[2]}'.join(command_answer.split('{db[2]}'))
			if command_answer.find('{db[3]}') != -1:
				command_answer = f'{user[3]}/{user[1] * 20}'.join(command_answer.split('{db[3]}'))
			if command_answer.find('{db[4]}') != -1:
				command_answer = f'{user[4]}'.join(command_answer.split('{db[4]}'))
			if command_answer.find('{all_commands}') != -1:
				commands_list = self.get_commands_list()
				command_answer = commands_list.join(command_answer.split('{all_commands}'))
		return command_answer

	def user_command_answer(self, peer_id: int, id: int, user_data: dict, user: list, message: str, user_commands: dict):
		default_command = None
		for user_command in user_commands:
			command = user_command['Command'].lower()
			if message == command:
				default_command = True
				break
			elif message.find('[id') != -1:
				message_value = 0
				for word in message.split():
					if word.find('[id') != -1:
						break
					message_value += 1
				if len(command.split()) > message_value:
					remove_word = message.split()[message_value]
					if command.replace('{take_user_id}', '').strip() == message.replace(remove_word, '').strip():
						default_command = False
						break

		if default_command != None:
			if default_command == True:
				command_answer = user_command['Command_Answer']
				command_answer = self.default_command(id, user_data, user, user_command)
				self.sender.send_message(peer_id, command_answer)
			else:
				command_answer = self.not_default_command(peer_id, id, user_data, user, message, message_value, user_command)
				self.sender.send_message(peer_id, command_answer)

	def new_message(self, event):
		id, peer_id, message = event.obj.from_id, event.obj.peer_id, event.obj.text.lower().strip()
		user_commands = Server.get_user_commands(self.bot_name)

		user_data = self.vk_session.method('users.get', {'user_ids': id, 'fields': 'verified'})[0]
		self.signalPrintUserMessage.emit(self.bot_name, f"{user_data['first_name']} {user_data['last_name']}", event.obj.text.strip())

		user = Server.find_in_database(self.bot_name, f"SELECT * FROM Users WHERE id = '{id}'")
		if user == None:
			for user_command in user_commands:
				if user_command['Flags']['Message_For_New_User'] == True:
					command_answer = self.default_command(id, user_data, user, user_command)
					self.sender.send_message(peer_id, command_answer)
			Server.edit_database(self.bot_name, "INSERT INTO Users VALUES (?, ?, ?, ?)", values = (id, 1, 0, 0))
			user = Server.find_in_database(self.bot_name, f"SELECT * FROM Users WHERE id = '{id}'")

		if peer_id - 2000000000 > 0:
			Server.edit_database(self.bot_name, f"UPDATE Users SET exp = '{user[3] + 1}' WHERE id = '{id}'")
			if user[3] + 1 >= user[1] * 20:
				for user_command in user_commands:
					if user_command['Flags']['Message_For_Up_Level'] == True:
						command_answer = self.default_command(id, user_data, user, user_command)
						self.sender.send_message(peer_id, command_answer)
				Server.edit_database(self.bot_name, f"UPDATE Users SET level = '{user[1] + 1}' WHERE id = '{id}'")
				user = Server.find_in_database(self.bot_name, f"SELECT * FROM Users WHERE id = '{id}'")

		self.user_command_answer(peer_id, id, user_data, user, message, user_commands)

	def run(self):
		Server.edit_database(self.bot_name, """
			CREATE TABLE IF NOT EXISTS Users(
				id BIGINT,
				level BIGINT,
				cash BIGINT,
				exp BIGINT
			)
		""")

		for event in self.longpoll.listen():
			if self.longpoll.bot_theard_run and event.type == VkBotEventType.MESSAGE_NEW:
				while GlobalVariables.new_user_message:
					pass
				GlobalVariables.new_user_message = True
				self.new_message(event)
# ==================================================================