# -*- coding: utf-8 -*-

# VK_API
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

# PyQt5
from PyQt5 import QtCore

# Другие
import server as Server

# Классы для потоков ниже
# ==================================================================
class Sender:
	def __init__(self, vk_session):
		self.vk_session = vk_session

	def send_message(self, peer_id, message, keyboard = None):
		if keyboard != None:
			self.vk_session.method(
				'messages.send',
				{
					'peer_id': peer_id,
					'message': message,
					'keyboard': keyboard.encode('UTF-8'),
					'random_id': 0
				}
			)
		else:
			self.vk_session.method(
				'messages.send',
				{
					'peer_id': peer_id,
					'message': message,
					'random_id': 0
				}
			)

class MyBotLongPool(VkBotLongPoll):
	def listen(self):
		self.bot_theard_run = True
		while self.bot_theard_run:
			try:
				for event in self.check():
					if self.bot_theard_run == True:
						yield event
			except:
				pass
# ==================================================================

# Потоки
# ==================================================================
class Bot(QtCore.QThread):
	signalPrintUserMessage = QtCore.pyqtSignal(str, str)

	def __init__(self, token, group_id):
		QtCore.QThread.__init__(self)

		self.dict_for_warning_func = {}
		self.warning_dict = {}

		self.vk_session = vk_api.VkApi(token = token)
		self.longpoll = MyBotLongPool(self.vk_session, int(group_id))

		self._sender = Sender(self.vk_session)

		Server.edit_database("""
			CREATE TABLE IF NOT EXISTS Users(
				id BIGINT,
				level BIGINT,
				cash BIGINT,
				exp BIGINT,
				rank TEXT
			)
		""")

	def new_message(self, event):
		id, peer_id, message = event.obj.from_id, event.obj.peer_id, event.obj.text.lower().strip()

		user_data = self.vk_session.method('users.get', {'user_ids': id, 'fields': 'verified'})[0]
		self.signalPrintUserMessage.emit(f"{user_data['first_name']} {user_data['last_name']}", event.obj.text.strip())

		user = Server.find_in_database(f"SELECT * FROM Users WHERE id = '{id}'")
		if user == None:
			self._sender.send_message(peer_id, f"""\
Добро пожаловать @id{id} ({user_data['first_name']} {user_data['last_name']})!
Так как я тебя раньше не видел, попрошу тебя ознакомится с списком команд через команду "!Список команд".
""")
			Server.edit_database("INSERT INTO Users VALUES (?, ?, ?, ?, ?)", values = (id, 1, 0, 0, 'Недоступно пока что... 😅'))
		user = Server.find_in_database(f"SELECT * FROM Users WHERE id = '{id}'")

		if peer_id - 2000000000 > 0:
			Server.edit_database(f"UPDATE Users SET exp = '{user[3] + 1}' WHERE id = '{id}'")
			if user[3] + 1 >= user[1] * 20:
				Server.edit_database(f"UPDATE Users SET level = '{user[1] + 1}' WHERE id = '{id}'")
				self._sender.send_message(peer_id, f"Пользователь @id{id} ({user_data['first_name']} {user_data['last_name']}) получил новый уровень!")
				user = Server.find_in_database(f"SELECT * FROM Users WHERE id = '{id}'")

			user_commands = Server.get_user_commands()
			for user_command in user_commands:
				command = user_command['Command'].lower()
				command_answer = user_command['Command_Answer']

				if message == command:
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
						user_commands, message = Server.get_user_commands(), ''
						for user_command in user_commands:
							command = user_command['Command']
							if command.find('{take_user_id}') != -1:
								command  = f'[ID другого пользователя]'.join(command.split('{take_user_id}'))
							message += f"•  {command}\n"
						command_answer = message.join(command_answer.split('{all_commands}'))
					self._sender.send_message(peer_id, command_answer)
				else:
					if message.find('[id') != -1:
						message_value = 0
						for word in message.split():
							if word.find('[id') != -1:
								break
							message_value += 1

						try:
							if message.replace(message.split()[message_value], '').strip() == command.replace(command.split()[message_value], '').strip():
								other_id = int(message.split()[message_value].split('|')[0].replace('[', '').replace('id', '').strip())
								chat_members = self.vk_session.method('messages.getConversationMembers', {'peer_id': peer_id, 'fields': 'verified'})

								other_user_find_in_chat_members = False
								for chat_member in chat_members['items']:
									if other_id == chat_member['member_id']:
										other_user_find_in_chat_members = True
										break

								code_work = True
								other_user = Server.find_in_database(f"SELECT * FROM Users WHERE id = '{other_id}'")
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
										self._sender.send_message(peer_id, f"@id{id} ({user_data['first_name']} {user_data['last_name']}), пользователь @id{other_id} ({other_user_data['first_name']} {other_user_data['last_name']}) не является участником данной беседы!")
										code_work = False
								else:
									self._sender.send_message(peer_id, f"@id{id} ({user_data['first_name']} {user_data['last_name']}), пользователя @id{other_id} ({other_user_data['first_name']} {other_user_data['last_name']}) нету в базе данных бота, попробуйте в другой раз!")
									code_work = False

								if code_work:
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
										message = ''
										user_commands = Server.get_user_commands()
										for user_command in user_commands:
											message += f"• {user_command['Command']}\n"
										command_answer = message.join(command_answer.split('{all_commands}'))

									self._sender.send_message(peer_id, command_answer)
						except:
							continue

	def run(self):
		for event in self.longpoll.listen():
			if event.type == VkBotEventType.MESSAGE_NEW:
				self.new_message(event)
# ==================================================================