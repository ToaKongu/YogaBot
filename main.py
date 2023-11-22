import config
import keyboards
import telebot
import replies
from telebot import types
import pymysql
from mysql.connector import connect, Error
from datetime import datetime
import time as time_for_sleep
from threading import Thread


bot = telebot.TeleBot(config.TOKEN)
SonyaID = token.owner_id

conn_and_cur = ['', '']
def connection_to_mysql():
	try:
		with pymysql.connect(
			host=config.host,
			user=config.user,
			password=config.password,
			database=config.database
		) as connection:
			print(connection)

		create_table = '''CREATE TABLE IF NOT EXISTS accounts
			(user_id INT(20), username CHAR(30), date_start CHAR(10), date_finish CHAR(10) NOT NULL, PRIMARY KEY(user_id))'''
		cursor = connection.cursor()
		connection.ping(reconnect=True)
		cursor.execute(create_table)
		connection.commit()
		conn_and_cur[0], conn_and_cur[1] = connection, cursor
	except Error as err:
		print(err)

def reconnect_to_mysql():
	while True:
		connection_to_mysql()
		time_for_sleep.sleep(60 * 60)

months = {'01': 'января', '02': 'февраля', '03': 'марта', '04': 'апреля',
			'05': 'мая', '06': 'июня', '07': 'июля', '08': 'августа',
			'09': 'сентября', '10': 'октября', '11': 'ноября', '12': 'декабря',}

@bot.message_handler(commands=['start'])
def start_message(message):
	bot.send_message(message.chat.id, replies.rep[0], reply_markup=keyboards.main_kb)
	bot.send_message(message.chat.id, replies.rep[1], reply_markup=keyboards.keyboard_start)


@bot.message_handler(commands=['show_info'])
def hiden_func(message):
	conn_and_cur[1].execute("SELECT username, date_start, date_finish FROM accounts ORDER BY username")
	data = conn_and_cur[1].fetchall()
	result = ''
	for i in range(len(data)):
		result = result + f'@{data[i][0]}:  {data[i][1]}  -  {data[i][2]}\n'
	if result:
		bot.send_message(SonyaID, result)
	else:
		bot.send_message(SonyaID, replies.rep[8])


@bot.callback_query_handler(func=lambda callback: callback.data)
def callback_func(callback):
	if callback.data == 'ib_start_1' or callback.data == 'ib_back_1':
		bot.edit_message_text(chat_id=callback.message.chat.id,
			message_id=callback.message.id, text=replies.rep[2], reply_markup=keyboards.keyboard_1)
	elif callback.data == 'ib_start_2':
		msg = bot.edit_message_text(chat_id=callback.message.chat.id,
			message_id=callback.message.id, text=replies.rep[3])
		bot.register_next_step_handler(msg, review, callback.message.chat.username)

	elif callback.data == 'ib_start_3':
		bot.edit_message_text(chat_id=callback.message.chat.id,
			message_id=callback.message.id, text=replies.rep[4])

	elif callback.data == 'ib1_1':
		conn_and_cur[1].execute(f"SELECT date_finish FROM accounts WHERE user_id = {callback.message.chat.id}")
		data = conn_and_cur[1].fetchone()
		if not data:
			bot.edit_message_text(chat_id=callback.message.chat.id,
				message_id=callback.message.id, text=replies.rep[5], reply_markup=keyboards.tariffes)
		else:
			bot.edit_message_text(chat_id=callback.message.chat.id,
				message_id=callback.message.id, text=replies.rep[9], reply_markup=keyboards.back_1)

	elif callback.data == 'ib1_2':
		conn_and_cur[1].execute(f"SELECT date_finish FROM accounts WHERE user_id = {callback.message.chat.id}")
		data = conn_and_cur[1].fetchone()
		if data:
			bot.edit_message_text(chat_id=callback.message.chat.id,
				message_id=callback.message.id, text=replies.rep[6], reply_markup=keyboards.tariffes)
		else:
			bot.edit_message_text(chat_id=callback.message.chat.id,
				message_id=callback.message.id, text=replies.rep[10], reply_markup=keyboards.back_1)

	elif callback.data == 'ib1_3':
		conn_and_cur[1].execute(f"SELECT date_finish FROM accounts WHERE user_id = {callback.message.chat.id}")
		data = conn_and_cur[1].fetchone()
		if not data:
			bot.edit_message_text(chat_id=callback.message.chat.id,
							message_id=callback.message.id, text=replies.rep[7], reply_markup=keyboards.buy_access)
		else:
			new_date = data[0].split('.')
			day, month, year = new_date[0], new_date[1], new_date[2]
			else_day = '0' + day if len(day) == 1 else day
			else_month = '0' + month if len(month) == 1 else month
			bot.edit_message_text(chat_id=callback.message.chat.id,
							message_id=callback.message.id, text=f'Твоя подписка действует до {day} {months[month]} {year} года ({else_day}.{else_month}.{year}). Не забудь её продлить, чтобы оставаться на коврике')
	elif callback.data == 'ib1_4':
		bot.edit_message_text(chat_id=callback.message.chat.id,
			message_id=callback.message.id, text=replies.rep[1], reply_markup=keyboards.keyboard_start)

	elif callback.data == 'ib_access':
		bot.edit_message_text(chat_id=callback.message.chat.id,
			message_id=callback.message.id, text=replies.rep[5], reply_markup=keyboards.tariffes)

	elif callback.data == 'ib_tar_1':
		bot.edit_message_text(chat_id=callback.message.chat.id,
			message_id=callback.message.id, text='Можно оплачивать!')
		title = 'Подписка на месяц занятий Йогой с Сонечкой)))'
		price = 1190 * 100
		command_pay(callback.message.chat.id, title, price)
	elif callback.data == 'ib_tar_2':
		bot.edit_message_text(chat_id=callback.message.chat.id,
			message_id=callback.message.id, text='Можно оплачивать!')
		title = 'Подписка на три месяца занятий Йогой с Сонечкой)))'
		price = 3200 * 100
		command_pay(callback.message.chat.id, title, price)
	elif callback.data == 'ib_tar_3':
		bot.edit_message_text(chat_id=callback.message.chat.id,
			message_id=callback.message.id, text='Можно оплачивать!')
		title = 'Подписка на 6 месяцев занятий Йогой с Сонечкой)))'
		price = 5600 * 100
		command_pay(callback.message.chat.id, title, price)
	elif callback.data == 'ib_tar_4':
		bot.edit_message_text(chat_id=callback.message.chat.id,
			message_id=callback.message.id, text='Выбери опцию', reply_markup=keyboards.keyboard_1)


@bot.message_handler(content_types=['text'])
def tariffes_func(message):
	if message.text == 'Меню':
		bot.send_message(message.chat.id, replies.rep[1], reply_markup=keyboards.keyboard_start)
	else:
		bot.send_message(message.chat.id, replies.rep[11], reply_markup=keyboards.main_kb)


def review(message, username):
	bot.send_message(SonyaID, f'Чел с ником @{username} отправил тебе следующий отзыв:\n\n{message.text}')
	bot.send_message(message.chat.id, replies.rep[12])


def command_pay(message_chat_id, title, price):
	bot.send_invoice(chat_id=message_chat_id,
						title=title,
						description='Каждый день ты будешь получать всякие видео с йогой или как там это работает...',
						invoice_payload='',
						provider_token=config.PAYMENT_TOKEN,
						currency='RUB',
						prices=[types.LabeledPrice(title, price)])


@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
	bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
								error_message='Кажется, что-то пошло не так. Попробуйте оплатить позже.')


@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
	bot.send_message(message.chat.id, f'Поздравляю! Твои `{message.successful_payment.total_amount / 100}` рублей потрачены не зря!', parse_mode='Markdown')
	conn_and_cur[1].execute(f"SELECT date_finish FROM accounts WHERE user_id = {message.chat.id}")
	data = conn_and_cur[1].fetchone()
	if message.successful_payment.total_amount == 119000:
		plus_months = 1
	elif message.successful_payment.total_amount == 320000:
		plus_months = 3
	elif message.successful_payment.total_amount == 560000:
		plus_months = 6
	if not data:
		cur_date = datetime.now()
		cur_year, cur_month, cur_day = cur_date.year, cur_date.month, cur_date.day
		finish_month = cur_month + plus_months
		finish_year = cur_year
		if finish_month > 12:
			finish_month = finish_month % 12
			finish_month = 12 if finish_month == 0 else finish_month
			finish_year = finish_year + 1
		start_date = '.'.join(['0' + str(cur_day) if len(str(cur_day)) == 1 else str(cur_day), '0' + str(cur_month) if len(str(cur_month)) == 1 else str(cur_month), str(cur_year)])
		finish_date = '.'.join(['0' + str(cur_day) if len(str(cur_day)) == 1 else str(cur_day), '0' + str(finish_month) if len(str(finish_month)) == 1 else str(finish_month), str(finish_year)])
		conn_and_cur[1].execute(f"""INSERT INTO accounts (user_id, username, date_start, date_finish)
						VALUES ({message.chat.id}, '{message.chat.username}', '{start_date}', '{finish_date}');""")
		conn_and_cur[0].commit()
		bot.send_message(SonyaID, f'Чел с ником @{message.chat.username} приобрел подписку на {plus_months} месяцев (до {finish_date})!\n\nНажми /show_info, чтобы увидеть информацию и своих клиентах')
	else:
		new_date = data[0].split('.')
		day, month, year = int(new_date[0]), int(new_date[1]), int(new_date[2])
		month = month + plus_months
		if month > 12:
			month = month % 12
			month = 12 if month == 0 else month
			year = year + 1
		finish_date = '.'.join(['0' + str(day) if len(str(day)) == 1 else str(day), '0' + str(month) if len(str(month)) == 1 else str(month), str(year)])
		conn_and_cur[1].execute(f"UPDATE accounts SET date_finish = '{finish_date}' WHERE user_id = {message.chat.id}")
		conn_and_cur[0].commit()
		bot.send_message(SonyaID, f'Чел с ником @{message.chat.username} продлил подписку на {plus_months} месяцев (до {finish_date})!\n\nНажми /show_info, чтобы увидеть информацию и своих клиентах')


def editing_users():
	while True:
		datetime_now = datetime.now()
		hours_now = datetime_now.hour
		minutes_now = datetime_now.minute
		if hours_now == 10 and minutes_now == 0:
			conn_and_cur[1].execute("SELECT user_id, username, date_finish FROM accounts")
			data = conn_and_cur[1].fetchall()
			if not data:
				continue
			for info in data:
				day, month, year = map(int, info[2].split('.'))
				delta = datetime(year, month, day) - datetime_now
				if delta.days <= 0:
					conn_and_cur[1].execute(f"DELETE FROM accounts WHERE user_id = {info[0]};")
					conn_and_cur[0].commit()
					bot.send_message(int(info[0]), replies.rep[13])
					bot.send_message(SonyaID, f'Чел с ником @{info[1]} НЕ УСПЕЛ продлить подписку...\nПришлось вышвырнуть его из таблицы\n\nНажми /show_info, чтобы увидеть информацию и своих клиентах')
				elif delta.days <= 3:
					bot.send_message(info[0], f'Твоя подписка завершится через {delta.days} дней! Не забудь продлить ее, чтобы оставаться на коврике!')

				time_for_sleep.sleep(60 * 23)
		time_for_sleep.sleep(60)

def polling():
	bot.polling(none_stop=True)

polling_thread = Thread(target=polling)
editing_users_thread = Thread(target=editing_users)
reconn_to_mysql = Thread(target=reconnect_to_mysql)

polling_thread.start()
editing_users_thread.start()
reconn_to_mysql.start()
