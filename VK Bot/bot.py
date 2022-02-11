# -*- coding: utf-8 -*-

# VK_API
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

# PyQt5
from PyQt5 import QtCore

# Другие
import server as Server
import config as Config
import datetime
import json

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
		self.bot_run = True
		while self.bot_run:
			try:
				for event in self.check():
					if self.bot_run == True:
						yield event
			except:
				pass

class Bot(QtCore.QThread):
	signalMuteTime = QtCore.pyqtSignal()
	signalPrintUserMessage = QtCore.pyqtSignal(str, str)

	def __init__(self, token, group_id):
		QtCore.QThread.__init__(self)

		self.dict_for_warning_func = {}
		self.warning = 0

		self.vk_session = vk_api.VkApi(token = token)
		self.longpoll = MyBotLongPool(self.vk_session, int(group_id))

		self._sender = Sender(self.vk_session)

		Server.edit_database("""
			CREATE TABLE IF NOT EXISTS Users(
				id BIGINT,
				level BIGINT,
				cash BIGINT,
				exp BIGINT,
				rank TEXT,
				mute TEXT
			)
		""")

		self.signalMuteTime.emit()

	def send_command_list(self, peer_id):
		self._sender.send_message(peer_id,  """\
Команды для беседы:
•  !Cписок команд
•  !Статистика [ID пользователя (По умолчанию ваш ID)]
•  !Пожать руку пользователю [ID пользователя]

Команды для личных сообщений:
•  !Мут-чата

PS: Для того, чтобы использовать "Команды для личных сообщений", напишите боту в личные сообщения команду, которую вы хотите использовать.
""")

	def send_statistic(self, id, peer_id, message):
		user_data = self.vk_session.method('users.get',{'user_ids': id, 'fields': 'verified'})[0]
		if len(message.split()) > 1:
			other_id = int(message.split()[1].split('|')[0].replace('[', '').replace('id', '').strip())
			chat_members = self.vk_session.method('messages.getConversationMembers', {'peer_id': peer_id, 'fields': 'verified'})
			other_user_find_in_chat_members = False
			for chat_member in chat_members['items']:
				if other_id == chat_member['member_id']:
					other_user_find_in_chat_members = True
			other_user_data = self.vk_session.method('users.get',{'user_ids': other_id, 'fields': 'verified'})[0]
			other_user = Server.find_in_database(f"SELECT * FROM Users WHERE id = '{other_id}'")
			if other_user != None:
				if other_user_find_in_chat_members == True:
					self._sender.send_message(peer_id, f"""\
Имя пользователя: @id{id} ({other_user_data['first_name']} {other_user_data['last_name']})
Ранг пользователя: {other_user[4]}
Балланс пользователя: {other_user[2]}
Уровень пользователя: {other_user[1]}
Опыт пользователя: {other_user[3]}/{other_user[1] * 20}
""")
				else:
					self._sender.send_message(peer_id, f"@id{id} ({user_data['first_name']} {user_data['last_name']}), вы не можете получить статистику пользователя @id{other_id} ({other_user_data['first_name']} {other_user_data['last_name']}), потому-что он не является участником данной беседы!")
			else:
				self._sender.send_message(peer_id, f"@id{id} ({user_data['first_name']} {user_data['last_name']}), пользователя @id{other_id} ({other_user_data['first_name']} {other_user_data['last_name']}) нету в базе данных бота, попробуйте в другой раз!")
		else:
			user = Server.find_in_database(f"SELECT * FROM Users WHERE id = '{id}'")
			self._sender.send_message(peer_id, f"""\
Вас зовут: @id{id} ({user_data['first_name']} {user_data['last_name']})
Ваш ранг: {user[4]}
Ваш балланс: {user[2]}
Ваш уровень: {user[1]}
Ваш опыт: {user[3]}/{user[1] * 20}
""")

	def send_mute_chat_time(self, id):
		user_data = self.vk_session.method('users.get',{'user_ids': id, 'fields': 'verified'})[0]
		user = Server.find_in_database(f"SELECT * FROM Users WHERE id = '{id}'")
		mute = json.loads(user[5])
		if mute['Value'] == True:
			self._sender.send_message(id, f"@id{id} ({user_data['first_name']} {user_data['last_name']}), вам осталось подождать {mute['Time Left']} мин.")
		else:
			self._sender.send_message(id, f"@id{id} ({user_data['first_name']} {user_data['last_name']}), у вас нету чат-мута!")

	def shake_hands_with_the_user(self, id, peer_id, message):
		if len(message.split()) > 4:
			self._sender.send_message(peer_id, 'Вы неверно ввели команд "!Пожать руку пользователю [ID пользователя]"!\nВот пример: !Пожать руку пользователю 599251585')
		else:
			other_id = int(message.split()[3].split('|')[0].replace('[', '').replace('id', '').strip())
			other_user_data = self.vk_session.method('users.get',{'user_ids': other_id, 'fields': 'verified'})[0]
			user_data = self.vk_session.method('users.get',{'user_ids': id, 'fields': 'verified'})[0]
			chat_members = self.vk_session.method('messages.getConversationMembers', {'peer_id': peer_id, 'fields': 'verified'})
			other_user_find_in_chat_members = False
			for chat_member in chat_members['items']:
				if other_id == chat_member['member_id']:
					other_user_find_in_chat_members = True
			if other_user_find_in_chat_members == True:
				self._sender.send_message(peer_id, f"@id{id} ({user_data['first_name']} {user_data['last_name']}) пожал руку пользователю @id{other_id} ({other_user_data['first_name']} {other_user_data['last_name']})")
			else:
				self._sender.send_message(peer_id, f"@id{id} ({user_data['first_name']} {user_data['last_name']}), вы не можете пожать руку пользователю @id{other_id} ({other_user_data['first_name']} {other_user_data['last_name']}), потому-что он не является участником данной беседы!")

	def new_message(self, event):
		id, peer_id, message = event.obj.from_id, event.obj.peer_id, event.obj.text

		user_data = self.vk_session.method('users.get', {'user_ids': id, 'fields': 'verified'})[0]
		self.signalPrintUserMessage.emit(f"{user_data['first_name']} {user_data['last_name']}", message)

		user = Server.find_in_database(f"SELECT * FROM Users WHERE id = '{id}'")
		if user == None:
			self._sender.send_message(peer_id, f"""\
Добро пожаловать @id{id} ({user_data['first_name']} {user_data['last_name']})!
Так как я тебя раньше не видел, попрошу тебя ознакомится с списком команд через команду "!Список команд".
""")
			Server.edit_database("INSERT INTO Users VALUES (?, ?, ?, ?, ?, ?)", values = (id, 1, 0, 0, 'Посвящённый', json.dumps({'Value': False, 'Time': None, 'Time Left': None}, ensure_ascii = False)))
		user = Server.find_in_database(f"SELECT * FROM Users WHERE id = '{id}'")

		mute = json.loads(user[5])
		if mute['Value'] == True:
			self.vk_session.method('messages.delete', {'peer_id': peer_id, 'message_ids': event.obj.conversation_message_id, 'spam': 1,})
		elif mute['Value'] == False:
			if peer_id - 2000000000 > 0:
				Server.edit_database(f"UPDATE Users SET exp = '{user[3] + 1}' WHERE id = '{id}'")
				if user[3] + 1 >= user[1] * 20:
					Server.edit_database(f"UPDATE Users SET level = '{user[1] + 1}' WHERE id = '{id}'")
					self._sender.send_message(peer_id, f"Пользователь @id{id} ({user_data['first_name']} {user_data['last_name']}) получил новый уровень!")
					user = Server.find_in_database(f"SELECT * FROM Users WHERE id = '{id}'")
				if user[1] in Config.RANKS and Config.RANKS[user[1]] != user[4]:
					Server.edit_database(f"UPDATE Users SET rank = '{Config.RANKS[user[1]]}' WHERE id = '{id}'")
					self._sender.send_message(peer_id, f"Пользователь @id{id} ({user_data['first_name']} {user_data['last_name']}) получает новый ранг \"{Config.RANKS[user[1]]}\"!")

			if len(list(message.strip())) > 1:
				if list(message.strip())[0] == '!':
					try:
						message = ''.join(list(message)[1:len(list(message)) + 1])
						find_command = False
						if peer_id - 2000000000 > 0:
							if message.lower() == 'список команд':
								find_command = True
								self.send_command_list(peer_id)
							elif message.split()[0].lower() == 'статистика':
								find_command = True
								self.send_statistic(id, peer_id, message)
							elif ' '.join(message.split()[:3]).lower() == 'пожать руку пользователю':
								find_command = True
								self.shake_hands_with_the_user(id, peer_id, message)
						else:
							if message.lower() == 'мут-чата':
								find_command = True
								self.send_mute_chat_time(id)

						if find_command == False:
							bot_settings = Server.get_bot_settings()
							if bot_settings['User_Commands'] == True:
								user_commands = Server.get_user_commands()
								for user_command in user_commands:
									if message.lower() == user_command['Command'].lower():
										user = Server.find_in_database(f"SELECT * FROM Users WHERE id = '{id}'")

										if user_command['Command_Answer'].find('{user}') != -1:
											user_command['Command_Answer'] = f"@id{id} ({user_data['first_name']} {user_data['last_name']})".join(user_command['Command_Answer'].split('{user}'))
										if user_command['Command_Answer'].find('{db[1]}') != -1:
											user_command['Command_Answer'] = f'{user[1]}'.join(user_command['Command_Answer'].split('{db[1]}'))
										if user_command['Command_Answer'].find('{db[2]}') != -1:
											user_command['Command_Answer'] = f'{user[2]}'.join(user_command['Command_Answer'].split('{db[2]}'))
										if user_command['Command_Answer'].find('{db[3]}') != -1:
											user_command['Command_Answer'] = f'{user[3]}/{user[1] * 20}'.join(user_command['Command_Answer'].split('{db[3]}'))

										self._sender.send_message(peer_id, user_command['Command_Answer'])
							else:
								self._sender.send_message(peer_id, f"@id{id} ({user_data['first_name']} {user_data['last_name']}), команды \"{message}\" не существует!")
					except:
						self._sender.send_message(peer_id, f"@id{id} ({user_data['first_name']} {user_data['last_name']}), вы неправильно ввели команду!")

	def run(self):
		for event in self.longpoll.listen():
			if event.type == VkBotEventType.MESSAGE_NEW:
				id, peer_id, message = event.obj.from_id, event.obj.peer_id, event.obj.text
				if peer_id - 2000000000 > 0:
					if peer_id in self.dict_for_warning_func:
						if self.dict_for_warning_func[peer_id][0] == message:
							self.dict_for_warning_func.update({peer_id: [message, self.dict_for_warning_func[peer_id][1] + 1]})
							if self.dict_for_warning_func[peer_id][1] == 3:
								self.dict_for_warning_func.update({peer_id: [message, 1]})
								self.warning += 1
								user_data = self.vk_session.method('users.get',{'user_ids': id, 'fields': 'verified'})[0]
								self._sender.send_message(peer_id, f"""\
@id{id} ({user_data['first_name']} {user_data['last_name']}), хватит флудить!
Вам выдано предупреждение {self.warning}/3.
При достижении 3/3 предупреждений, вы получите мут-чата!
""")
								if self.warning == 3:
									self.warning = 0
									now_time = datetime.datetime.now()
									Server.edit_database(f"UPDATE Users SET mute = '{json.dumps({'Value': True, 'Time': f'{now_time.day}:{now_time.hour}:{now_time.minute}:{now_time.second}', 'Time Left': 120}, ensure_ascii = False)}' WHERE id = '{id}'")
									self._sender.send_message(peer_id, f"""\
@id{id} ({user_data['first_name']} {user_data['last_name']}), вы получаете мут-чата на 2 часа за флуд!
Время мута вы можете отслеживать в личных сообщениях у бота, через команду \"!Мут-чата\".
""")
						else:
							self.dict_for_warning_func.update({peer_id: [message, 1]})
					else:
						self.dict_for_warning_func.update({peer_id: [message, 1]})
				self.new_message(event)