from telebot import types


keyboard_start = types.InlineKeyboardMarkup()
ib_start_1 = types.InlineKeyboardButton(text='Оплатить доступ', callback_data='ib_start_1')
ib_start_2 = types.InlineKeyboardButton(text='Поделиться ощущениями', callback_data='ib_start_2')
ib_start_3 = types.InlineKeyboardButton(text='Задать вопрос', callback_data='ib_start_3')
keyboard_start.add(ib_start_1)
keyboard_start.add(ib_start_2)
keyboard_start.add(ib_start_3)

keyboard_1 = types.InlineKeyboardMarkup()
ib1_1 = types.InlineKeyboardButton(text='Попасть на канал', callback_data='ib1_1')
ib1_2 = types.InlineKeyboardButton(text='Продлить подписку', callback_data='ib1_2')
ib1_3 = types.InlineKeyboardButton(text='Моя подписка', callback_data='ib1_3')
ib1_4 = types.InlineKeyboardButton(text='Назад', callback_data='ib1_4')
keyboard_1.add(ib1_1)
keyboard_1.add(ib1_2)
keyboard_1.add(ib1_3)
keyboard_1.add(ib1_4)

tariffes = types.InlineKeyboardMarkup()
ib_tar_1 = types.InlineKeyboardButton(text='1 месяц', callback_data='ib_tar_1')
ib_tar_2 = types.InlineKeyboardButton(text='3 месяца', callback_data='ib_tar_2')
ib_tar_3 = types.InlineKeyboardButton(text='6 месяцев', callback_data='ib_tar_3')
ib_tar_4 = types.InlineKeyboardButton(text='Назад', callback_data='ib_tar_4')
tariffes.add(ib_tar_1)
tariffes.add(ib_tar_2)
tariffes.add(ib_tar_3)
tariffes.add(ib_tar_4)

pay_options = types.InlineKeyboardMarkup()
ib_pay_1 = types.InlineKeyboardButton(text='Перевод по российской карте', callback_data='ib_pay_1')
ib_pay_2 = types.InlineKeyboardButton(text='PayPal', callback_data='ib_pay_2')
ib_pay_3 = types.InlineKeyboardButton(text='Назад', callback_data='ib_pay_3')
pay_options.add(ib_pay_1)
pay_options.add(ib_pay_2)
pay_options.add(ib_pay_3)

buy_access = types.InlineKeyboardMarkup()
ib_access = types.InlineKeyboardButton(text='Попасть на канал', callback_data='ib_access')
buy_access.add(ib_access)

back_1 = types.InlineKeyboardMarkup()
ib_back_1 = types.InlineKeyboardButton(text='Назад', callback_data='ib_back_1')
back_1.add(ib_back_1)

main_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
b = types.KeyboardButton('Меню')
main_kb.add(b)