import os
import telebot
import data_base

bot = telebot.TeleBot(os.environ.get('token'))
invite_link = 'https://t.me/{}?start={}'

@bot.message_handler(commands=['start'])
def start(message):
    unique_code = extract_unique_code(message.text)
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    markup.row('Get invite link', 'Refresh')
    create_new_user(message.chat.id)
    if unique_code:
        status = add_new_user(message, unique_code)
        if status:
            bot.send_message(chat_id=message.chat.id, text=status, reply_markup=markup)
            return
    bot.send_message(chat_id=message.chat.id, text='Hello', reply_markup=markup)

def add_new_user(message, invite_id):
    data_base_object = data_base.DataBaseConnect()
    response = data_base_object.add_user(message.chat.id, invite_id)
    data_base_object.close_connection()
    if isinstance(response, dict):
        return response['message']
    return False

def create_new_user(user_id):
    data_base_object = data_base.DataBaseConnect()
    data_base_object.create_user(user_id)
    data_base_object.close_connection()

def extract_unique_code(text):
    # Extracts the unique_code from the sent /start command.
    return text.split()[1] if len(text.split()) > 1 else None

def refresh_status(message):
    data_base_object = data_base.DataBaseConnect()
    users_count = len(data_base_object.get_users(message.chat.id)) - 1
    data_base_object.close_connection()
    # заменить на желаемое кол-во требуемых приглашений
    if users_count >= 2:
        # text = заменить на желаемый текст при достаточном кол-ве приглашенных
        bot.send_message(chat_id=message.chat.id, text='Good')
    else:
        bot.send_message(chat_id=message.chat.id, text=f'*Invited by: {users_count}\nNeed more: {2-users_count}*', parse_mode='Markdown')

@bot.message_handler(content_types=['text'])
def markup_handler(message):
    data_base_object = data_base.DataBaseConnect()
    if message.text == 'Get invite link':
        bot.send_message(chat_id=message.chat.id, text=invite_link.format(bot.get_me().username, message.chat.id))
    elif message.text == 'Refresh':
        refresh_status(message)

if __name__ == '__main__':
    bot.polling(none_stop=True)