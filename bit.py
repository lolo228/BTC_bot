# Импорт библиотек
import os
from telebot import types
import telebot
import sqlite3
import time

# Токен бота
bot = telebot.TeleBot('1827342878:AAFu1H9bN0k-D-rNOnes8lqKFGniu6QXVQI')

# Команда start и запись данных в бд
@bot.message_handler(commands=['start'])
def command_start(message):
    if message.from_user.username is None:
        bot.send_message(message.from_user.id, 'Добавьте Имя пользвателя(тег), чтобы пользоваться ботом')
    else:
        connect = sqlite3.connect('user.bd')
        cursor = connect.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS users_info(
            user_id INTEGER,
            user_teg TEXT
        )""")
        connect.commit()

        # Проверка на повтор данных
        people_id = message.from_user.id
        cursor.execute(f"SELECT user_id FROM users_info WHERE user_id = {people_id}")
        data = cursor.fetchone()
        if data is None:
            user_id = message.from_user.id
            user_teg = message.from_user.username

            user_inf = [user_id, user_teg]

            cursor.execute("INSERT INTO users_info VALUES(?,?);", user_inf)
            connect.commit()
        else:
            var = None

        connect = sqlite3.connect('ban_user.bd')
        cursor = connect.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS ban_users_info(
            ban_users_id INT PRIMARY KEY
        )""")

        cursor.execute(f"SELECT ban_users_id FROM ban_users_info WHERE ban_users_id = {people_id}")
        information = cursor.fetchone()
        connect.commit()

        if information is None:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            box = types.KeyboardButton('🗃Коробка')
            info = types.KeyboardButton('📋Информация')
            Cooperation = types.KeyboardButton('🛠Сотрудничество')

            markup.add(box, info, Cooperation)
            send_mess = f"Привет <b> {message.from_user.username} </b>!\nЭто бот с халявой\nАдминистратор - @SPICERMr\nЧтобы узнать подробности пропиши\n/help"
            bot.send_message(message.chat.id, send_mess, parse_mode='html', reply_markup=markup)
        else:
            bot.send_message(message.from_user.id, 'Вы были забанены администрацией в данном боте, для получения ответов обратитесь к администратору - @SPICERMr')

            connect = sqlite3.connect('user.bd')
            cursor = connect.cursor()

            cursor.execute(f"DELETE FROM users_info WHERE user_id = {people_id}")
            connect.commit()

# Команда ban
@bot.message_handler(commands=['ban'])
def command_ban(message):
    people_id = message.from_user.id
    if int(people_id) == 1672521583:
        bot.send_message(message.chat.id, 'Напишите тег юзера которого вы хотите забанить(без @)')

        bot.register_next_step_handler(message, ban_hendler)
    else:
        bot.send_message(message.from_user.id, '⛔️Вы не администратор⛔️')


# Обработка команды бана
def ban_hendler(message):
    teg_for_ban = message.text

    connect = sqlite3.connect('user.bd')
    cursor = connect.cursor()

    cursor.execute('SELECT user_id FROM users_info WHERE user_teg = ?', (teg_for_ban,))
    id_for_ban = cursor.fetchone()
    connect.commit()

    connect = sqlite3.connect('ban_user.bd')
    cursor = connect.cursor()

    cursor.execute(f"SELECT ban_users_id FROM ban_users_info WHERE ban_users_id = {id_for_ban[0]}")
    check = cursor.fetchone()

    if check is None:
        cursor.execute(f'INSERT INTO ban_users_info VALUES(?);', id_for_ban)
        connect.commit()
        bot.send_message(message.from_user.id, '✅Юзер был добавлен в список забаненых✅')

        connect = sqlite3.connect('user.bd')
        cursor = connect.cursor()

        cursor.execute(f"DELETE FROM users_info WHERE user_id = {id_for_ban[0]}")
        connect.commit()

    else:
        bot.send_message(message.from_user.id, '⛔️Данный юзер уже забанен!⛔️')


# Команда help
@bot.message_handler(commands=['help'])
def command_help(message):
    if message.from_user.username is None:
        bot.send_message(message.from_user.id, 'Добавьте Имя пользвателя(тег), чтобы пользоваться ботом')
    else:
        connect = sqlite3.connect('ban_user.bd')
        cursor = connect.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS ban_users_info(
            ban_users_id INT PRIMARY KEY
        )""")

        people_id = message.from_user.id

        cursor.execute(f"SELECT ban_users_id FROM ban_users_info WHERE ban_users_id = {people_id}")
        information = cursor.fetchone()
        connect.commit()

        if information is None:
            bot.send_message(message.chat.id, 'Привет, чтобы найти BTC чек с деньгами нажми на кнопку 🗃<b>Коробка</b> в коробке не всегда есть чеки, переодически администратор кладёт чеки туда', parse_mode='html')
        else:
            bot.send_message(message.from_user.id, 'Вы были забанены администрацией в данном боте, для получения ответов обратитесь к администратору - @SPICERMr')

# Команда admin
@bot.message_handler(commands=['admin'])
def command_admin(message):
    user_id = message.from_user.id
    if int(user_id) == 1672521583:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        check = types.KeyboardButton('➕Добавить BTC чек')
        mailing = types.KeyboardButton('📣Запусить рассылку')
        exit = types.KeyboardButton('Выход')
        markup.add(check, mailing, exit)
        send_mess = "✅ Привет администратор!"
        bot.send_message(message.chat.id, send_mess, reply_markup=markup)
    else:
        bot.send_message(message.chat.id, '⛔ Ты не администратор!')


# Обработка кнопок
@bot.message_handler(content_types=['text'])
def get_text_message(message, reply_to_user=None):
    if message.from_user.username is None:
        bot.send_message(message.from_user.id, 'Добавьте Имя пользвателя(тег), чтобы пользоваться ботом')
    else:
        connect = sqlite3.connect('ban_user.bd')
        cursor = connect.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS ban_users_info(
            ban_users_id INT PRIMARY KEY
        )""")

        people_id = message.from_user.id

        cursor.execute(f"SELECT ban_users_id FROM ban_users_info WHERE ban_users_id = {people_id}")
        information = cursor.fetchone()
        connect.commit()

        if information is None:
            if message.text == 'Выход':
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
                box = types.KeyboardButton('🗃Коробка')
                info = types.KeyboardButton('📋Информация')
                Cooperation = types.KeyboardButton('🛠Сотрудничество')

                markup.add(box, info, Cooperation)
                send_mess = 'Вы вернулись в главное меню!'
                bot.send_message(message.chat.id, send_mess, parse_mode='html', reply_markup=markup)

            elif message.text == '📋Информация':
                connect = sqlite3.connect('user.bd')
                cursor = connect.cursor()

                cursor.execute("SELECT COUNT(user_id) FROM users_info")
                lines = cursor.fetchone()

                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
                exit = types.KeyboardButton('Выход')
                markup.add(exit)
                send_mess = f'В боте {lines[0]} пользователей 👥'
                bot.send_message(message.chat.id, send_mess, parse_mode='html', reply_markup=markup)

            elif message.text == '🛠Сотрудничество':
                bot.send_message(message.chat.id, 'Для сотрудничесвта пишите ему @SPICERMr')

            elif message.text == '💸Получить чек':
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
                exit = types.KeyboardButton('Выход')
                markup.add(exit)
                connect = sqlite3.connect('BTC_check.bd')
                cursor = connect.cursor()

                cursor.execute("SELECT * FROM btc_check")
                if cursor.fetchone() is None:
                    connect.commit()
                    bot.send_message(message.from_user.id, '😔 Упс похоже в данный момент чеков нет', reply_markup=markup)
                else:
                    connect = sqlite3.connect('BTC_check.bd')
                    cursor = connect.cursor()

                    cursor.execute("SELECT check_url FROM btc_check")
                    rows = cursor.fetchone()
                    connect.commit()
                    BTC = rows[0]
                    bot.send_message(message.from_user.id, BTC, reply_markup=markup)

                connect = sqlite3.connect('BTC_check.bd')
                cursor = connect.cursor()

                cursor.execute("""DELETE from btc_check""")
                connect.commit()

            elif message.text == '🗃Коробка':
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
                BTC_check_button = types.KeyboardButton('💸Получить чек')
                exit = types.KeyboardButton('Выход')
                markup.add(BTC_check_button, exit)

                bot.send_message(message.chat.id, "Нажми на кнопку чтобы получить чек", parse_mode='html', reply_markup=markup)

            check_for_admin_id = message.from_user.id

            if int(check_for_admin_id) == 1672521583:
                if message.text == '➕Добавить BTC чек':
                    message = bot.send_message(message.from_user.id, 'Отправьте BTC чек, для отмены действия напиши -')
                    bot.register_next_step_handler(message, message1)

                elif message.text == '📣Запусить рассылку':
                    message = bot.send_message(message.from_user.id, 'Отправь мне фото, для отмены рассылки напиши -')
                    bot.register_next_step_handler(message, photo)
            else:
                pass
        else:
            bot.send_message(message.from_user.id, 'Вы были забанены администрацией в данном боте, для получения ответов обратитесь к администратору - @SPICERMr')


def photo(message):
    sent_message = message.text
    if sent_message == '-':
        bot.send_message(message.chat.id, 'Рассылка отменена!')
    else:
        global photo_id, photo_extension

        photo_id = message.photo[-1].file_id
        file_photo = bot.get_file(photo_id)
        photo_name, photo_extension = os.path.splitext(file_photo.file_path)

        downloaded_photo = bot.download_file(file_photo.file_path)

        src = 'Photo/' + photo_id + photo_extension
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_photo)
        msg = bot.send_message(message.chat.id, 'Отправьте текст для рассылки')
        bot.register_next_step_handler(msg, mailig)


def mailig(message):
    mailing_text = message.text
    connect = sqlite3.connect('user.bd')
    cursor = connect.cursor()

    cursor.execute("SELECT user_id FROM users_info")
    all_users_id = cursor.fetchall()
    connect.commit()

    bot.send_message(message.from_user.id, '✅ Рассылка начата!')

    for i in range(len(all_users_id)):
        try:
            time.sleep(1)
            photo_path = 'Photo/' + photo_id + photo_extension
            photo = open(photo_path, 'rb')
            bot.send_photo(all_users_id[i][0], photo, caption=mailing_text)
        except:
            pass
    bot.send_message(message.from_user.id, '✅ Рассылка завершена!')


def message1(message):
    btc_url = message.text
    if btc_url == '-':
        bot.send_message(message.chat.id, 'Действие отменено!')
    else:
        bot.send_message(message.chat.id, '✅ BTC чек успешно сохранён!')

        connect = sqlite3.connect('BTC_check.bd')
        cursor = connect.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS btc_check(
            check_url TEXT
        )""")
        connect.commit()

        cursor.execute("INSERT INTO btc_check VALUES(?);", (btc_url,))
        connect.commit()

bot.polling()