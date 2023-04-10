import os
from dotenv import load_dotenv, find_dotenv

import telebot

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from db_driver import search_object, insert_primary_data_to_the_table, insert_file_to_the_table,\
    insert_photo_to_the_table, change_subscribe_of_object, change_status_problem_of_object,\
    change_priority_of_object, change_address_of_object
from extensions import TempData, get_image, ident_search_type, check_yn, check_date, make_cad_num_for_db, show_object


load_dotenv(find_dotenv())
TOKEN = os.environ.get("TOKEN")
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id,
                     f'Здравствуйте, {message.chat.username}.\n'
                     f'Я помогу вам отслеживать решения по объектам, требующим внимания!'
                     )


@bot.message_handler(commands=['dev'])
def send_devs(message):
    bot.send_message(message.chat.id,
                     f'Данный продукт был разработан командой INITA team!\n'
                     f'По всем вопросам, связанным с поддержкой и разработкой, обращайтесь в телеграм:\n'
                     f'https://t.me/uga_liant'
                     )


@bot.message_handler(commands=['start'])
def main_menu(message):
    markup = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton('Поиск объекта', callback_data='main_1')
    markup.row(btn1)
    btn2 = InlineKeyboardButton('Добавить новый объект', callback_data='main_2')
    markup.row(btn2)
    btn3 = InlineKeyboardButton('Отслеживаемые объекты', callback_data='main_3')
    markup.row(btn3)
    bot.send_photo(message.chat.id, photo=get_image('main.png'), reply_markup=markup)


# ветка поиска объекта
@bot.callback_query_handler(func=lambda call: call.data.startswith('main_1'))
def search_inline(call):
    msg = bot.send_message(call.message.chat.id, 'Введите адрес или кадастровый номер')
    bot.register_next_step_handler(msg, object_actions)


def object_actions(message):

    search_type = ident_search_type(message.text)
    if search_type == 'bad':
        msg = bot.send_message(message.chat.id, 'Вы ввели не кадастровый номер или адрес')
        bot.register_next_step_handler(msg, object_actions)
    else:
        if search_type == 'num':
            message.text = make_cad_num_for_db(message.text)
        object_info = search_object([message.text, search_type])
        if object_info == 'bad_request':
            msg = bot.send_message(message.chat.id, 'Данные по объекту не найдены, попробуйте найти другой объект')
            bot.register_next_step_handler(msg, object_actions)
        else:
            bot.send_message(message.chat.id, show_object(object_info))
            temp_data = TempData(object_info)
            temp_data.add_data_to_temp()

            markup = InlineKeyboardMarkup()
            btn1 = InlineKeyboardButton('Отслеживать / не отслеживать', callback_data='object_actions_1')
            markup.row(btn1)
            btn2 = InlineKeyboardButton('Внести правки в адрес', callback_data='object_actions_2')
            markup.row(btn2)
            btn3 = InlineKeyboardButton('Добавить фото', callback_data='object_actions_3')
            markup.row(btn3)
            btn4 = InlineKeyboardButton('Добавить документ', callback_data='object_actions_4')
            markup.row(btn4)
            btn5 = InlineKeyboardButton('Изменить статус', callback_data='object_actions_5')
            markup.row(btn5)
            btn6 = InlineKeyboardButton('Изменить приоритет', callback_data='object_actions_6')
            markup.row(btn6)
            bot.send_photo(message.chat.id, photo=get_image('object_actions.png'), reply_markup=markup)



# ветка действий с найденным объектом
@bot.callback_query_handler(func=lambda call: call.data.startswith('object_actions_1'))
def action_subscribe(call):
    temp_data = TempData()
    object_info = temp_data.get_data_from_temp()
    status = change_subscribe_of_object(object_info[0])
    bot.send_message(call.message.chat.id, f'{status}')


@bot.callback_query_handler(func=lambda call: call.data.startswith('object_actions_2'))
def action_redact(call):
    msg = bot.send_message(call.message.chat.id, f'Введите корректный адрес объекта')
    bot.register_next_step_handler(msg, redact_object_addr)


def redact_object_addr(message):
    temp_data = TempData()
    object_info = temp_data.get_data_from_temp()
    if ident_search_type(message.text) == 'addr':
        status = change_address_of_object([message.text, object_info[0]])
        bot.send_message(message.chat.id, f'{status}')
    else:
        msg = bot.send_message(message.chat.id, 'Вы ввели не адрес, попробуйте ещё раз')
        bot.register_next_step_handler(msg, redact_object_addr)


@bot.callback_query_handler(func=lambda call: call.data.startswith('object_actions_3'))
def action_add_photo(call):
    msg = bot.send_message(call.message.chat.id, f'Пришлите файл с фотографией боту')
    bot.register_next_step_handler(msg, bot_add_photo)


@bot.message_handler(content_types=['photo'])
def bot_add_photo(message):
    temp_data = TempData()
    object_info = temp_data.get_data_from_temp()

    file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    src = 'storage/data/' + file_info.file_path
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)

    status = insert_photo_to_the_table([src, object_info[0]])
    bot.send_message(message.chat.id, f'{status}')


@bot.callback_query_handler(func=lambda call: call.data.startswith('object_actions_4'))
def action_add_doc(call):
    msg = bot.send_message(call.message.chat.id, f'Пришлите файл боту')
    bot.register_next_step_handler(msg, bot_add_file)


@bot.message_handler(content_types=['document'])
def bot_add_file(message):
    temp_data = TempData()
    object_info = temp_data.get_data_from_temp()
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    src = 'storage/data/' + message.document.file_name
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)

    status = insert_file_to_the_table([src, object_info[0]])
    bot.send_message(message.chat.id, f'{status}')


@bot.callback_query_handler(func=lambda call: call.data.startswith('object_actions_5'))
def action_status(call):
    temp_data = TempData()
    object_info = temp_data.get_data_from_temp()
    status = change_status_problem_of_object(object_info[0])
    bot.send_message(call.message.chat.id, f'{status}')


@bot.callback_query_handler(func=lambda call: call.data.startswith('object_actions_6'))
def action_priority(call):
    temp_data = TempData()
    object_info = temp_data.get_data_from_temp()
    status = change_priority_of_object(object_info[0])
    bot.send_message(call.message.chat.id, f'{status}')


# ветка добавления объекта
@bot.callback_query_handler(func=lambda call: call.data.startswith('main_2'))
def creation_inline(call):
    msg = bot.send_message(call.message.chat.id, 'Введите кадастровый номер объекта')
    query = []
    bot.register_next_step_handler(msg, creation_num_add, query)


@bot.message_handler(content_types=['text'])
def creation_num_add(message, query):
    if ident_search_type(message.text) != 'num':
        msg = bot.send_message(message.chat.id, 'Вы ввели не кадастровый номер объекта')
        bot.register_next_step_handler(msg, creation_num_add, query)
    else:
        cad_num = make_cad_num_for_db(message.text)
        query.append(cad_num)
        msg = bot.send_message(message.chat.id, 'Введите адрес объекта')
        bot.register_next_step_handler(msg, creation_addr_add, query)


@bot.message_handler(content_types=['text'])
def creation_addr_add(message, query):
    if ident_search_type(message.text) != 'addr':
        msg = bot.send_message(message.chat.id, 'Вы ввели не адрес объекта')
        bot.register_next_step_handler(msg, creation_addr_add, query)
    else:
        query.append(message.text)
        msg = bot.send_message(message.chat.id, 'Является ли объект проблемным (да/нет)?')
        bot.register_next_step_handler(msg, creation_status_problem_add, query)


@bot.message_handler(content_types=['text'])
def creation_status_problem_add(message, query):
    answer = message.text.lower()
    if check_yn(answer) == 0:
        msg = bot.send_message(message.chat.id, 'Вы ввели некорректный ответ')
        bot.register_next_step_handler(msg, creation_status_problem_add, query)
    else:
        query.append({'да': 1, 'нет': 0}[answer])
        msg = bot.send_message(message.chat.id, 'Исполнено ли решение по объекту (да/нет)?')
        bot.register_next_step_handler(msg, creation_status_execution_add, query)


@bot.message_handler(content_types=['text'])
def creation_status_execution_add(message, query):
    answer = message.text.lower()
    if check_yn(answer) == 0:
        msg = bot.send_message(message.chat.id, 'Вы ввели некорректный ответ')
        bot.register_next_step_handler(msg, creation_status_execution_add, query)
    else:
        query.append({'да': 1, 'нет': 0}[answer])
        msg = bot.send_message(message.chat.id, 'Сделать объект отслеживаемым (да/нет)?')
        bot.register_next_step_handler(msg, creation_tracking_add, query)


@bot.message_handler(content_types=['text'])
def creation_tracking_add(message, query):
    answer = message.text.lower()
    if check_yn(answer) == 0:
        msg = bot.send_message(message.chat.id, 'Вы ввели некорректный ответ')
        bot.register_next_step_handler(msg, creation_tracking_add, query)
    else:
        query.append({'да': 1, 'нет': 0}[answer])
        msg = bot.send_message(message.chat.id, 'Сделать объект приоритетным (да/нет)?')
        bot.register_next_step_handler(msg, creation_priority_add, query)


@bot.message_handler(content_types=['text'])
def creation_priority_add(message, query):
    answer = message.text.lower()
    if check_yn(answer) == 0:
        msg = bot.send_message(message.chat.id, 'Вы ввели некорректный ответ')
        bot.register_next_step_handler(msg, creation_priority_add, query)
    else:
        query.append({'да': 1, 'нет': 0}[answer])
        msg = bot.send_message(message.chat.id, 'Назовите дату дедлайна (в формате день.месяц.год)')
        bot.register_next_step_handler(msg, creation_object_add_to_db, query)


@bot.message_handler(content_types=['text'])
def creation_object_add_to_db(message, query):
    if check_date(message.text) == 0:
        msg = bot.send_message(message.chat.id, 'Вы ввели не дату или дату в неправильном формате')
        bot.register_next_step_handler(msg, creation_object_add_to_db, query)
    else:
        query.append(message.text)
        status = insert_primary_data_to_the_table(query)
        bot.send_message(message.chat.id, f'{status}')


# ветка отслеживаемых объектов
@bot.callback_query_handler(func=lambda call: call.data.startswith('main_3'))
def vip_inline(call):

    bot.send_message(call.message.chat.id, 'Выберите тип фильтрации или сортировки объектов')

    markup_filter = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton('Приоритетные объекты', callback_data='filter_1')
    markup_filter.row(btn1)
    btn2 = InlineKeyboardButton('Добавленные объекты', callback_data='filter_2')
    markup_filter.row(btn2)
    bot.send_photo(call.message.chat.id, photo=get_image('filter.png'), reply_markup=markup_filter)

    markup_sorting = InlineKeyboardMarkup()
    btn3 = InlineKeyboardButton('По решению', callback_data='sorting_1')
    markup_sorting.row(btn3)
    btn4 = InlineKeyboardButton('По дедлайну', callback_data='sorting_2')
    markup_sorting.row(btn4)
    btn5 = InlineKeyboardButton('По кадастровому номеру', callback_data='sorting_3')
    markup_sorting.row(btn5)
    btn6 = InlineKeyboardButton('По адресу', callback_data='sorting_4')
    markup_sorting.row(btn6)
    bot.send_photo(call.message.chat.id, photo=get_image('sorting.png'), reply_markup=markup_sorting)


@bot.callback_query_handler(func=lambda call: call.data.startswith('filter_1'))
def filter_priority(call):
    bot.send_message(call.message.chat.id, 'фильтр по приоритету')


@bot.callback_query_handler(func=lambda call: call.data.startswith('filter_2'))
def filter_added(call):
    bot.send_message(call.message.chat.id, 'фильтр по дате добавления')


@bot.callback_query_handler(func=lambda call: call.data.startswith('sorting_1'))
def sorting_solution(call):
    bot.send_message(call.message.chat.id, 'сортировка по решению')


@bot.callback_query_handler(func=lambda call: call.data.startswith('sorting_2'))
def sorting_deadline(call):
    bot.send_message(call.message.chat.id, 'сортировка по дедлайну')


@bot.callback_query_handler(func=lambda call: call.data.startswith('sorting_3'))
def sorting_number(call):
    bot.send_message(call.message.chat.id, 'сортировка по кадастровому номеру')


@bot.callback_query_handler(func=lambda call: call.data.startswith('sorting_4'))
def sorting_address(call):
    bot.send_message(call.message.chat.id, 'сортировка по адресу')


if __name__ == '__main__':

    bot.polling(none_stop=True, interval=0)
